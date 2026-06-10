"""
Cloudflare Workers 入口文件
用于将 FastAPI 应用适配到 Workers 环境
"""
from workers import WorkerEntrypoint
import asgi
from main import app


class Default(WorkerEntrypoint):
    """
    Workers 入口点类
    将 FastAPI 应用适配到 Workers 的 fetch handler
    """
    
    async def fetch(self, request):
        """
        处理 HTTP 请求
        
        Args:
            request: Workers 请求对象
            
        Returns:
            Workers Response 对象
        """
        return await asgi.fetch(app, request, self.env)