"""
Project Files API 路由模块
提供项目图片文件的 HTTP 访问服务
"""
import os
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api/files", tags=["files"])

# 允许访问的图片目录（后续可迁移到 .env）
ALLOWED_DIRS = [
    r"D:\Project\web\xinysoft_Vite\public",
    r"D:\File\photos",
]


def is_path_allowed(file_path: str) -> bool:
    """
    检查文件路径是否在允许的目录内

    Args:
        file_path: 文件路径

    Returns:
        bool: 是否允许访问
    """
    try:
        abs_path = Path(file_path).resolve()
        for allowed_dir in ALLOWED_DIRS:
            allowed_path = Path(allowed_dir).resolve()
            if str(abs_path).startswith(str(allowed_path)):
                return True
        return False
    except Exception:
        return False


def get_content_type(file_path: str) -> str:
    """
    根据文件扩展名获取 Content-Type

    Args:
        file_path: 文件路径

    Returns:
        str: Content-Type
    """
    ext = Path(file_path).suffix.lower()
    content_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.svg': 'image/svg+xml',
    }
    return content_types.get(ext, 'application/octet-stream')


@router.get("/{file_path:path}", summary="获取项目图片文件")
async def serve_file(file_path: str):
    """
    获取项目图片文件

    将本地文件路径转换为可访问的 HTTP URL
    例如：/api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送.png

    Args:
        file_path: 文件路径（URL 编码后的）

    Returns:
        FileResponse: 图片文件响应

    Raises:
        HTTPException: 文件不存在或无权访问
    """
    # 处理 Windows 路径（URL 中的 / 会被转换为 \）
    file_path = file_path.replace('/', '\\') if ':' in file_path else file_path

    logger.info(f"请求访问文件: {file_path}")

    # 安全检查：路径是否在允许的目录内
    if not is_path_allowed(file_path):
        logger.warning(f"拒绝访问路径（不在允许目录内）: {file_path}")
        raise HTTPException(status_code=403, detail="无权访问此文件")

    # 检查文件是否存在
    if not os.path.isfile(file_path):
        logger.warning(f"文件不存在: {file_path}")
        raise HTTPException(status_code=404, detail="文件不存在")

    # 获取 Content-Type 并返回文件
    return FileResponse(
        path=file_path,
        media_type=get_content_type(file_path),
        filename=Path(file_path).name
    )