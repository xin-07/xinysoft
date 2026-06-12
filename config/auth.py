"""
认证模块：JWT、密码哈希、登录频率限制
"""
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict

import bcrypt
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("环境变量 JWT_SECRET_KEY 未配置，请使用 openssl rand -hex 32 生成一个随机密钥")

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 7

# 登录失败记录：{ip: [timestamp1, timestamp2, ...]}
_failure_records: dict[str, list[datetime]] = defaultdict(list)
MAX_FAILURES = 5          # 最大失败次数
FAILURE_WINDOW = 15       # 时间窗口（分钟）


def create_access_token(username: str) -> str:
    """
    生成 JWT Token

    Args:
        username: 用户名

    Returns:
        JWT Token 字符串
    """
    expire = datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRE_DAYS)
    payload = {
        "sub": username,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict | None:
    """
    验证并解析 JWT Token

    Args:
        token: JWT Token 字符串

    Returns:
        解析后的 payload 字典；无效或过期时返回 None
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def hash_password(password: str) -> str:
    """
    使用 bcrypt 对密码进行哈希

    Args:
        password: 明文密码

    Returns:
        哈希后的密码字符串
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    使用 bcrypt 验证密码

    Args:
        plain: 明文密码
        hashed: 哈希密码

    Returns:
        密码匹配返回 True，否则返回 False
    """
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def _clean_expired(ip: str) -> None:
    """清除指定 IP 的过期失败记录"""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=FAILURE_WINDOW)
    _failure_records[ip] = [t for t in _failure_records[ip] if t > cutoff]
    if not _failure_records[ip]:
        del _failure_records[ip]


def check_rate_limit(ip: str) -> bool:
    """
    检查 IP 登录频率

    Args:
        ip: 客户端 IP 地址

    Returns:
        True 表示允许登录，False 表示被限制
    """
    _clean_expired(ip)
    return len(_failure_records.get(ip, [])) < MAX_FAILURES


def record_login_failure(ip: str) -> None:
    """
    记录登录失败

    Args:
        ip: 客户端 IP 地址
    """
    _failure_records[ip].append(datetime.now(timezone.utc))


def reset_rate_limit(ip: str) -> None:
    """
    登录成功后清除指定 IP 的失败记录

    Args:
        ip: 客户端 IP 地址
    """
    _failure_records.pop(ip, None)