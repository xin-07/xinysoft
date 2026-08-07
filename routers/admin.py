"""
Admin 管理后台 API 路由模块
"""
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request, UploadFile, File, Query

from config.database import execute_query, execute_query_all, get_db
from config.auth import (
    create_access_token,
    verify_password,
    check_rate_limit,
    record_login_failure,
    reset_rate_limit,
)
from models.admin import (
    LoginRequest,
    ProjectCreateRequest,
    ProjectUpdateRequest,
    StatusUpdateRequest,
    ProfileUpdateRequest,
)
from routers.admin_auth import get_current_admin

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api/admin", tags=["admin"])


# ==================== 工具函数 ====================

def execute_modify(sql, params=None) -> int:
    """执行 INSERT/UPDATE/DELETE，返回受影响行数"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, params)
            conn.commit()
            return rows


def execute_insert(sql, params=None) -> int:
    """执行 INSERT，返回新插入的 ID（PostgreSQL 使用 RETURNING 子句）"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            sql_returning = sql.rstrip(';') + ' RETURNING id'
            cursor.execute(sql_returning, params)
            conn.commit()
            return cursor.fetchone()['id']


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
    # 无需再次 json.loads，直接返回即可
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


def convert_file_url(file_path: str) -> str:
    """
    将本地文件路径转换为可访问的 /api/files/ URL

    Args:
        file_path: 本地文件路径（如 D:\\Project\\web\\xinysoft_Vite\\public\\鲜途智送.png）
                   或已转换的 API 路径（如 /api/files/D%3A/.../xxx.png）

    Returns:
        str: 可访问的 URL（如 /api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送.png）
    """
    if not file_path:
        return None

    # 已经是 /api/files/ 格式，直接返回避免二次编码
    if file_path.startswith('/api/files/'):
        return file_path

    # 将 Windows 路径分隔符转换为 URL 格式
    url_path = file_path.replace('\\', '/')
    encoded_path = quote(url_path, safe='/')
    return f"/api/files/{encoded_path}"


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


def _format_project(project: dict) -> dict:
    """格式化项目数据：解析 JSON 字段，转换文件 URL"""
    if project:
        project['tech_stack'] = parse_json_field(project.get('tech_stack'))
        project['screenshots'] = parse_json_field(project.get('screenshots'))
        project['cover_url'] = convert_file_url(project.get('cover_url'))
        project['screenshots'] = convert_file_urls(project.get('screenshots'))
    return project


def _format_profile(profile: dict) -> dict:
    """格式化个人资料数据：解析 JSON 字段，转换头像 URL"""
    if profile:
        profile['tech_tags'] = parse_json_field(profile.get('tech_tags'))
        profile['email'] = parse_json_field(profile.get('email'))
        profile['avatar_url'] = convert_file_url(profile.get('avatar_url'))
    return profile


# ==================== 认证接口 ====================

@router.post("/login", summary="管理员登录")
async def login(request: Request, req: LoginRequest):
    """
    管理员登录

    Args:
        request: FastAPI Request 对象
        req: 登录请求体

    Returns:
        JSON 响应
    """
    ip = request.client.host

    # 频率限制检查
    if not check_rate_limit(ip):
        return {
            "code": 429,
            "message": "操作过于频繁，请稍后再试",
            "data": None
        }

    try:
        # 查询管理员用户
        user = execute_query(
            "SELECT id, username, password_hash FROM admin_users WHERE username = %s",
            (req.username,)
        )

        if not user or not verify_password(req.password, user['password_hash']):
            record_login_failure(ip)
            return {
                "code": 401,
                "message": "用户名或密码错误",
                "data": None
            }

        # 登录成功
        reset_rate_limit(ip)
        token = create_access_token(req.username)

        return {
            "code": 200,
            "message": "success",
            "data": {
                "token": token,
                "token_type": "bearer"
            }
        }

    except Exception as e:
        logger.error(f"登录异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


@router.post("/verify", summary="验证 Token")
async def verify(username: str = Depends(get_current_admin)):
    """
    验证管理员 Token 有效性

    Args:
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    return {
        "code": 200,
        "message": "success",
        "data": {
            "username": username
        }
    }


# ==================== 项目管理接口 ====================

@router.get("/projects", summary="获取所有项目（管理端）")
async def get_all_projects(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=1000, description="每页数量"),
    username: str = Depends(get_current_admin)
):
    """
    查询所有项目（不限状态），支持分页

    Args:
        page: 页码，从 1 开始
        page_size: 每页数量
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        # 查询总数
        count_result = execute_query("SELECT COUNT(*) as total FROM projects")
        total = count_result['total'] if count_result else 0

        # 查询列表
        offset = (page - 1) * page_size
        projects = execute_query_all(
            "SELECT * FROM projects ORDER BY sort_order DESC LIMIT %s OFFSET %s",
            (page_size, offset)
        )

        # 格式化数据
        items = [_format_project(p) for p in projects]

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
        logger.error(f"查询项目列表异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


@router.get("/projects/{project_id}", summary="获取单个项目（管理端）")
async def get_project_by_id(
    project_id: int,
    username: str = Depends(get_current_admin)
):
    """
    根据 ID 查询项目（不限状态）

    Args:
        project_id: 项目 ID
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        project = execute_query(
            "SELECT * FROM projects WHERE id = %s",
            (project_id,)
        )

        if not project:
            return {
                "code": 404,
                "message": "项目不存在",
                "data": None
            }

        return {
            "code": 200,
            "message": "success",
            "data": _format_project(project)
        }

    except Exception as e:
        logger.error(f"查询项目详情异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


@router.post("/projects", summary="创建项目")
async def create_project(
    req: ProjectCreateRequest,
    username: str = Depends(get_current_admin)
):
    """
    创建新项目

    Args:
        req: 项目创建请求体
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        tech_stack_json = json.dumps(req.tech_stack) if req.tech_stack else None
        screenshots_json = json.dumps(req.screenshots) if req.screenshots else None

        sql = """
            INSERT INTO projects
                (title, subtitle, description, tech_stack, cover_url, screenshots,
                 live_url, repo_url, is_featured, sort_order, status)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        new_id = execute_insert(sql, (
            req.title,
            req.subtitle,
            req.description,
            tech_stack_json,
            req.cover_url,
            screenshots_json,
            req.live_url,
            req.repo_url,
            req.is_featured,
            req.sort_order,
            'published'
        ))

        # 查询新创建的项目
        project = execute_query("SELECT * FROM projects WHERE id = %s", (new_id,))

        return {
            "code": 200,
            "message": "success",
            "data": _format_project(project)
        }

    except Exception as e:
        logger.error(f"创建项目异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


@router.put("/projects/{project_id}", summary="编辑项目")
async def update_project(
    project_id: int,
    req: ProjectUpdateRequest,
    username: str = Depends(get_current_admin)
):
    """
    编辑项目（仅更新非 None 字段）

    Args:
        project_id: 项目 ID
        req: 项目更新请求体
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        # 检查项目是否存在
        existing = execute_query("SELECT id FROM projects WHERE id = %s", (project_id,))
        if not existing:
            return {
                "code": 404,
                "message": "项目不存在",
                "data": None
            }

        # 获取变更字段
        update_data = req.model_dump(exclude_unset=True)

        if not update_data:
            # 无变更，直接返回当前项目
            project = execute_query("SELECT * FROM projects WHERE id = %s", (project_id,))
            return {
                "code": 200,
                "message": "success",
                "data": _format_project(project)
            }

        # 处理 JSON 字段
        if 'tech_stack' in update_data:
            update_data['tech_stack'] = json.dumps(update_data['tech_stack']) if update_data['tech_stack'] else None
        if 'screenshots' in update_data:
            update_data['screenshots'] = json.dumps(update_data['screenshots']) if update_data['screenshots'] else None

        # 动态构建 UPDATE SQL
        set_parts = []
        values = []
        for key, value in update_data.items():
            set_parts.append(f"{key} = %s")
            values.append(value)

        values.append(project_id)
        sql = f"UPDATE projects SET {', '.join(set_parts)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        execute_modify(sql, tuple(values))

        # 查询更新后的项目
        project = execute_query("SELECT * FROM projects WHERE id = %s", (project_id,))

        return {
            "code": 200,
            "message": "success",
            "data": _format_project(project)
        }

    except Exception as e:
        logger.error(f"更新项目异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


@router.delete("/projects/{project_id}", summary="删除项目")
async def delete_project(
    project_id: int,
    username: str = Depends(get_current_admin)
):
    """
    删除项目

    Args:
        project_id: 项目 ID
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        existing = execute_query("SELECT id FROM projects WHERE id = %s", (project_id,))
        if not existing:
            return {
                "code": 404,
                "message": "项目不存在",
                "data": None
            }

        execute_modify("DELETE FROM projects WHERE id = %s", (project_id,))

        return {
            "code": 200,
            "message": "删除成功",
            "data": None
        }

    except Exception as e:
        logger.error(f"删除项目异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


@router.patch("/projects/{project_id}/status", summary="切换项目状态")
async def update_project_status(
    project_id: int,
    req: StatusUpdateRequest,
    username: str = Depends(get_current_admin)
):
    """
    切换项目发布状态（published / draft）

    Args:
        project_id: 项目 ID
        req: 状态更新请求体
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        existing = execute_query("SELECT id FROM projects WHERE id = %s", (project_id,))
        if not existing:
            return {
                "code": 404,
                "message": "项目不存在",
                "data": None
            }

        execute_modify(
            "UPDATE projects SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (req.status, project_id)
        )

        project = execute_query("SELECT * FROM projects WHERE id = %s", (project_id,))

        return {
            "code": 200,
            "message": "success",
            "data": _format_project(project)
        }

    except Exception as e:
        logger.error(f"更新项目状态异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


# ==================== 个人资料管理接口 ====================

@router.get("/profile", summary="获取个人资料（管理端）")
async def get_admin_profile(username: str = Depends(get_current_admin)):
    """
    获取个人资料信息（管理端，复用 /api/profile 逻辑）

    Args:
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        result = execute_query("SELECT * FROM profile WHERE id = 1")

        if not result:
            return {
                "code": 404,
                "message": "个人资料不存在",
                "data": None
            }

        return {
            "code": 200,
            "message": "success",
            "data": _format_profile(result)
        }

    except Exception as e:
        logger.error(f"查询个人资料异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


@router.put("/profile", summary="更新个人资料")
async def update_admin_profile(
    req: ProfileUpdateRequest,
    username: str = Depends(get_current_admin)
):
    """
    更新个人资料（profile 表 id=1 记录）

    Args:
        req: 个人资料更新请求体
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        # 检查 profile 是否存在
        existing = execute_query("SELECT id FROM profile WHERE id = 1")
        if not existing:
            return {
                "code": 404,
                "message": "个人资料不存在",
                "data": None
            }

        update_data = req.model_dump(exclude_unset=True)

        if not update_data:
            result = execute_query("SELECT * FROM profile WHERE id = 1")
            return {
                "code": 200,
                "message": "success",
                "data": _format_profile(result)
            }

        # 处理 JSON 字段
        if 'tech_tags' in update_data:
            update_data['tech_tags'] = json.dumps(update_data['tech_tags']) if update_data['tech_tags'] else None
        if 'email' in update_data:
            update_data['email'] = json.dumps(update_data['email']) if update_data['email'] else None

        # 动态构建 UPDATE SQL
        set_parts = []
        values = []
        for key, value in update_data.items():
            set_parts.append(f"{key} = %s")
            values.append(value)

        values.append(1)
        sql = f"UPDATE profile SET {', '.join(set_parts)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        execute_modify(sql, tuple(values))

        # 查询更新后的 profile
        result = execute_query("SELECT * FROM profile WHERE id = 1")

        return {
            "code": 200,
            "message": "success",
            "data": _format_profile(result)
        }

    except Exception as e:
        logger.error(f"更新个人资料异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }


# ==================== 文件上传接口 ====================

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/upload", summary="上传文件")
async def upload_file(
    file: UploadFile = File(...),
    username: str = Depends(get_current_admin)
):
    """
    上传图片文件

    Args:
        file: 上传的文件
        username: 当前管理员用户名

    Returns:
        JSON 响应
    """
    try:
        # 校验文件后缀
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return {
                "code": 400,
                "message": f"不支持的文件格式，仅允许 {', '.join(ALLOWED_EXTENSIONS)}",
                "data": None
            }

        # 读取文件内容并校验大小
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            return {
                "code": 400,
                "message": "文件大小不能超过 5MB",
                "data": None
            }

        # 构建上传路径
        upload_dir = os.getenv("UPLOAD_DIR", r"D:\File\photos")
        date_subdir = datetime.now().strftime("%Y-%m-%d")
        target_dir = os.path.join(upload_dir, "uploads", date_subdir)

        # 创建目录
        os.makedirs(target_dir, exist_ok=True)

        # 生成唯一文件名
        unique_name = f"{uuid.uuid4().hex}{file_ext}"
        target_path = os.path.join(target_dir, unique_name)

        # 写入文件
        with open(target_path, "wb") as f:
            f.write(contents)

        # 返回文件 URL
        return {
            "code": 200,
            "message": "上传成功",
            "data": {
                "url": convert_file_url(target_path)
            }
        }

    except Exception as e:
        logger.error(f"文件上传异常: {str(e)}")
        return {
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }