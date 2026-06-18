"""
GitHub Webhook 路由模块
"""
import hashlib
import hmac
import json
import logging
import os

from fastapi import APIRouter, Request, Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api", tags=["webhook"])

# Webhook 密钥（应与 GitHub Webhook 配置中的 Secret 一致）
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


def verify_signature(payload: bytes, signature: str) -> bool:
    """
    验证 GitHub Webhook 签名，确保请求来自 GitHub

    Args:
        payload: 请求体原始字节
        signature: 请求头中的签名（sha256=xxx 格式）

    Returns:
        bool: 签名是否有效
    """
    if not signature or not signature.startswith("sha256="):
        return False

    expected = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected}", signature)


@router.post("/webhook/github", summary="接收 GitHub Webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(default=None, alias="X-Hub-Signature-256"),
    x_github_event: str = Header(default=None, alias="X-GitHub-Event"),
):
    """
    接收 GitHub Webhook 回调

    用于接收 GitHub 仓库事件通知（如 push、PR 等）。

    Args:
        request: FastAPI 请求对象
        x_hub_signature_256: GitHub 签名，用于验证请求来源
        x_github_event: 触发的事件类型（push、pull_request 等）

    Returns:
        dict: 处理结果
    """
    # 读取原始请求体（签名验证需要原始字节）
    body_bytes = await request.body()
    payload = json.loads(body_bytes)

    # 验证签名（未配置 WEBHOOK_SECRET 时跳过验证）
    if WEBHOOK_SECRET:
        if not verify_signature(body_bytes, x_hub_signature_256):
            logger.warning("GitHub Webhook 签名验证失败")
            raise HTTPException(status_code=401, detail="签名验证失败")
    else:
        logger.debug("WEBHOOK_SECRET 未配置，跳过签名验证")

    # 记录事件
    event_type = x_github_event or "unknown"
    logger.info(
        f"收到 GitHub Webhook 事件: {event_type}, "
        f"仓库: {payload.get('repository', {}).get('full_name')}"
    )

    # 根据事件类型处理业务逻辑
    try:
        if event_type == "push":
            ref = payload.get("ref", "")
            pusher = payload.get("pusher", {}).get("name", "unknown")
            commits = payload.get("commits", [])
            logger.info(
                f"Push 事件 - 分支: {ref}, 推送者: {pusher}, 提交数: {len(commits)}"
            )
            # TODO: 在此处添加 push 事件的具体处理逻辑

        elif event_type == "ping":
            logger.info("收到 GitHub Webhook ping 测试")

        else:
            logger.info(f"未处理的事件类型: {event_type}")

        return {
            "code": 200,
            "message": "Webhook 已接收",
            "data": {"event": event_type},
        }

    except Exception as e:
        logger.error(f"处理 Webhook 异常: {str(e)}")
        raise HTTPException(status_code=500, detail="服务器内部错误")
