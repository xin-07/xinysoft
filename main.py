"""
xinysoft_FastAPI 应用入口
"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import profile, avatar, projects, files, admin, webhook

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="xinysoft API",
    description="个人作品集网站后端 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    全局异常处理器

    Args:
        request: 请求对象
        exc: 异常对象

    Returns:
        JSONResponse: 统一的错误响应
    """
    logger.error(f"全局异常: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )


# 注册路由
app.include_router(profile.router)
app.include_router(avatar.router)
app.include_router(projects.router)
app.include_router(files.router)
app.include_router(admin.router)
app.include_router(webhook.router)


@app.get("/", summary="根路径测试")
async def root():
    """
    根路径测试接口

    Returns:
        dict: 欢迎消息
    """
    return {
        "code": 200,
        "message": "Welcome to xinysoft API",
        "data": None
    }


@app.get("/hello/{name}", summary="Hello 测试接口")
async def say_hello(name: str):
    """
    Hello 测试接口

    Args:
        name: 用户名

    Returns:
        dict: 问候消息
    """
    return {
        "code": 200,
        "message": f"Hello {name}",
        "data": None
    }
