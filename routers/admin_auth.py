"""
认证中间件：管理员身份验证依赖
"""
from fastapi import Request, HTTPException

from config.auth import verify_token


async def get_current_admin(request: Request) -> str:
    """
    从请求头解析 JWT Token 并验证管理员身份

    Args:
        request: FastAPI Request 对象

    Returns:
        验证通过后返回 username（字符串）

    Raises:
        HTTPException: Token 缺失、无效或过期时返回 401
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未认证或Token已过期")

    token = auth_header[len("Bearer "):]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="未认证或Token已过期")

    return payload.get("sub", "")