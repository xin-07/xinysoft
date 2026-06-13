"""
Profile API 路由模块
"""
import json
import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pathlib import Path
from config.database import execute_query
from models.profile import ProfileResponse

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api", tags=["profile"])


def get_default_profile() -> Dict[str, Any]:
    """
    获取默认个人资料数据（数据库异常时使用）

    Returns:
        包含默认个人资料的字典
    """
    return {
        "id": 1,
        "name": "xiny",
        "avatar_url": None,
        "title": "全栈开发工程师 · AI Agent 探索者",
        "bio": "持续追踪 Vue3 与 AI Agent 前沿技术，通过实践快速掌握。具备跨专业协作能力，坚持每周技术复盘。",
        "tech_tags": ["Vue3", "FastAPI", "MySQL", "OpenClaw", "HarmonyOS", "ECharts"],
        "github": "https://github.com/xin-07",
        "gitee": "https://gitee.com/xin-keep-going",
        "wechat": "Yyk-293342",
        "qq": "2074835619",
        "email": ["2074835619@qq.com", "xin_y0607@outlook.com", "xiny0607.23@gmail.com"],
        "created_at": None,
        "updated_at": None
    }


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


def convert_avatar_url(avatar_path: str) -> str:
    """
    将本地头像路径转换为前端可访问的静态资源相对路径

    头像存储在 Vite public/ 目录下，构建后由 Cloudflare Pages 直接托管为静态资源

    Args:
        avatar_path: 本地文件路径（如 D:\\File\\photos\\落日.jpg）

    Returns:
        str: 静态资源相对路径（如 /落日.jpg）
    """
    if not avatar_path:
        return None

    return f"/{Path(avatar_path).name}"


@router.get("/profile", response_model=ProfileResponse, summary="获取个人资料")
async def get_profile():
    """
    获取个人资料信息

    用于前端 Hero 区域展示个人信息

    Returns:
        ProfileResponse: 个人资料数据

    Raises:
        HTTPException: 数据库异常时返回默认数据
    """
    try:
        # 查询数据库
        result = execute_query("SELECT * FROM profile WHERE id = 1")

        if result:
            # 解析 JSON 字段
            result['tech_tags'] = parse_json_field(result.get('tech_tags'))
            result['email'] = parse_json_field(result.get('email'))
            # 转换头像 URL
            result['avatar_url'] = convert_avatar_url(result.get('avatar_url'))
            return result
        else:
            # 数据库中没有数据，返回默认数据
            logger.warning("数据库中没有找到个人资料数据，返回默认数据")
            return get_default_profile()

    except Exception as e:
        # 数据库异常时返回默认数据，保证前端可用
        logger.error(f"数据库查询异常: {str(e)}")
        return get_default_profile()