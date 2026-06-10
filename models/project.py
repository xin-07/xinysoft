"""
Project 模型模块
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    """
    项目响应模型
    """
    id: int = Field(..., description="主键ID")
    title: str = Field(..., description="项目标题")
    subtitle: Optional[str] = Field(None, description="项目副标题")
    description: Optional[str] = Field(None, description="项目描述")
    tech_stack: Optional[List[str]] = Field(None, description="技术栈数组")
    cover_url: Optional[str] = Field(None, description="封面图URL")
    screenshots: Optional[List[str]] = Field(None, description="截图URL数组")
    live_url: Optional[str] = Field(None, description="在线演示地址")
    repo_url: Optional[str] = Field(None, description="仓库地址")
    is_featured: bool = Field(False, description="是否为精选项目")
    sort_order: int = Field(0, description="排序顺序")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "个人作品集网站",
                "subtitle": "FastAPI + Vue3 全栈项目",
                "description": "基于 FastAPI 和 Vue3 构建的个人作品集网站，展示个人资料、技术栈、项目经历等信息。",
                "tech_stack": ["FastAPI", "Vue3", "MySQL", "Pydantic", "SQLAlchemy"],
                "cover_url": "/static/images/projects/portfolio-cover.png",
                "screenshots": [
                    "/static/images/projects/portfolio-1.png",
                    "/static/images/projects/portfolio-2.png"
                ],
                "live_url": "https://example.com",
                "repo_url": "https://github.com/xin-07/portfolio",
                "is_featured": True,
                "sort_order": 1,
                "created_at": "2026-06-09 18:50:32",
                "updated_at": "2026-06-09 18:54:38"
            }
        }


class ProjectListResponse(BaseModel):
    """
    项目列表响应模型
    """
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    items: List[ProjectResponse] = Field(..., description="项目列表")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 10,
                "page": 1,
                "page_size": 10,
                "items": [
                    {
                        "id": 1,
                        "title": "个人作品集网站",
                        "subtitle": "FastAPI + Vue3 全栈项目",
                        "description": "基于 FastAPI 和 Vue3 构建的个人作品集网站。",
                        "tech_stack": ["FastAPI", "Vue3", "MySQL"],
                        "cover_url": "/static/images/projects/portfolio-cover.png",
                        "screenshots": ["/static/images/projects/portfolio-1.png"],
                        "live_url": "https://example.com",
                        "repo_url": "https://github.com/xin-07/portfolio",
                        "is_featured": True,
                        "sort_order": 1,
                        "created_at": "2026-06-09 18:50:32",
                        "updated_at": "2026-06-09 18:54:38"
                    }
                ]
            }
        }