"""
Project API 路由模块
"""
import json
import logging
from urllib.parse import unquote
from fastapi import APIRouter, Query
from typing import Any, Optional
from pathlib import Path
from config.database import execute_query, execute_query_all
from models.project import ProjectResponse, ProjectListResponse
from models.common import ApiResponse

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api", tags=["projects"])


def parse_json_field(value: Any) -> Any:
    """
    解析 JSON 字段

    Args:
        value: JSON 字符串或已解析的对象（psycopg2 对 jsonb 会自动反序列化）

    Returns:
        解析后的 Python 对象
    """
    if value is None:
        return None
    # psycopg2 + RealDictCursor 对 jsonb/json 字段会自动返回 Python 原生类型
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


def convert_file_url(file_path: str) -> str:
    """
    将本地文件路径转换为前端可访问的静态资源相对路径

    图片存储在 Vite public/ 目录下，构建后由 Cloudflare Pages 直接托管为静态资源，
    无需经过后端 /api/files/ 代理（后端运行在 Cloudflare Linux 环境，无法访问本地磁盘）

    Args:
        file_path: 本地文件路径（如 D:\\Project\\web\\xinysoft_Vite\\public\\鲜途智送.png）
                   或已转换的 API 路径（如 /api/files/D%3A/.../uploads/2026-08-07/xxx.png）

    Returns:
        str: 静态资源相对路径（如 /鲜途智送.png 或 /uploads/2026-08-07/xxx.png）
    """
    if not file_path:
        return None

    # 处理已转换为 /api/files/ 格式的路径（向后兼容旧数据）
    if file_path.startswith('/api/files/'):
        # 从 URL 编码的绝对路径中提取 public/ 之后的相对路径
        # 如 /api/files/D%3A/.../public/uploads/2026-08-07/xxx.png → /uploads/2026-08-07/xxx.png
        try:
            decoded = file_path[len('/api/files/'):]
            decoded = unquote(decoded)
            public_marker = 'public'
            idx = decoded.lower().find(public_marker)
            if idx != -1:
                relative = decoded[idx + len(public_marker):]
                return relative.replace('\\', '/') if relative.startswith(('/', '\\')) else f'/{relative}'
        except Exception:
            pass
        # 解析失败则提取文件名作为降级
        filename = Path(file_path).name
        try:
            filename = unquote(filename)
        except Exception:
            pass
        return f"/{filename}"

    # 已经是相对路径（如 /uploads/2026-08-07/xxx.png），直接返回
    if file_path.startswith('/'):
        return file_path

    # Windows 绝对路径（如 D:\...\public\鲜途智送.png），提取文件名
    filename = Path(file_path).name
    return f"/{filename}"


def convert_file_urls(paths: list) -> list:
    """
    批量转换本地文件路径为 /api/files/ URL

    Args:
        paths: 本地文件路径列表

    Returns:
        list: URL 列表
    """
    if not paths:
        return None
    return [convert_file_url(p) for p in paths]


@router.get("/projects", response_model=ApiResponse[ProjectListResponse], summary="获取项目列表")
async def get_projects(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    featured: Optional[bool] = Query(None, description="是否只获取精选项目")
):
    """
    获取项目列表

    支持分页查询和精选项目筛选

    Args:
        page: 页码，从 1 开始
        page_size: 每页数量，默认 10，最大 100
        featured: 是否只获取精选项目，为 None 时获取所有项目

    Returns:
        ApiResponse[ProjectListResponse]: 项目列表数据
    """
    try:
        # 构建基础查询条件
        where_conditions = ["status = %s"]
        params = ['published']

        # 如果指定了 featured 参数
        if featured is not None:
            where_conditions.append("is_featured = %s")
            params.append(featured)

        where_clause = " AND ".join(where_conditions)

        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM projects WHERE {where_clause}"
        count_result = execute_query(count_sql, tuple(params))
        total = count_result['total'] if count_result else 0

        # 计算偏移量
        offset = (page - 1) * page_size

        # 查询项目列表
        list_sql = f"""
            SELECT id, title, subtitle, description, tech_stack, cover_url,
                   screenshots, live_url, repo_url, is_featured, sort_order,
                   created_at, updated_at
            FROM projects
            WHERE {where_clause}
            ORDER BY sort_order DESC
            LIMIT %s OFFSET %s
        """
        params_with_pagination = params + [page_size, offset]
        projects = execute_query_all(list_sql, tuple(params_with_pagination))

        # 解析 JSON 字段
        items = []
        for project in projects:
            project['tech_stack'] = parse_json_field(project.get('tech_stack'))
            project['screenshots'] = parse_json_field(project.get('screenshots'))
            project['cover_url'] = convert_file_url(project.get('cover_url'))
            project['screenshots'] = convert_file_urls(project.get('screenshots'))
            items.append(project)

        return {
            "code": 200,
            "message": "success",
            "data": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "items": items
            }
        }

    except Exception as e:
        # 数据库异常时返回空列表，保证前端可用
        logger.error(f"查询项目列表异常: {str(e)}")
        return {
            "code": 200,
            "message": "success",
            "data": {
                "total": 0,
                "page": page,
                "page_size": page_size,
                "items": []
            }
        }


@router.get("/projects/{project_id}", response_model=ApiResponse[ProjectResponse], summary="获取项目详情")
async def get_project(project_id: int):
    """
    获取项目详情

    根据项目 ID 获取单个项目的详细信息

    Args:
        project_id: 项目 ID

    Returns:
        ApiResponse[ProjectResponse]: 项目详情数据
    """
    try:
        # 查询项目
        sql = """
            SELECT id, title, subtitle, description, tech_stack, cover_url,
                   screenshots, live_url, repo_url, is_featured, sort_order,
                   created_at, updated_at
            FROM projects
            WHERE id = %s AND status = %s
        """
        project = execute_query(sql, (project_id, 'published'))

        if not project:
            return {
                "code": 404,
                "message": "项目不存在",
                "data": None
            }

        # 解析 JSON 字段
        project['tech_stack'] = parse_json_field(project.get('tech_stack'))
        project['screenshots'] = parse_json_field(project.get('screenshots'))
        project['cover_url'] = convert_file_url(project.get('cover_url'))
        project['screenshots'] = convert_file_urls(project.get('screenshots'))

        return {
            "code": 200,
            "message": "success",
            "data": project
        }

    except Exception as e:
        # 数据库异常时记录日志并返回错误
        logger.error(f"查询项目详情异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }