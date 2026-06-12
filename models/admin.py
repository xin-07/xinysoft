"""
Admin 管理后台模型模块
"""
from typing import Optional, List, Literal, Generic, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T")


class LoginRequest(BaseModel):
    """
    登录请求模型
    """
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "123456"
            }
        }


class TokenResponse(BaseModel):
    """
    Token 响应模型
    """
    token: str = Field(..., description="JWT Token")
    token_type: str = Field("bearer", description="Token 类型")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer"
            }
        }


class VerifyResponse(BaseModel):
    """
    Token 验证响应模型
    """
    username: str = Field(..., description="用户名")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin"
            }
        }


class ProjectCreateRequest(BaseModel):
    """
    创建项目请求模型
    """
    title: str = Field(..., min_length=1, max_length=100, description="项目标题")
    subtitle: Optional[str] = Field(None, max_length=200, description="项目副标题")
    description: Optional[str] = Field(None, max_length=5000, description="项目描述")
    tech_stack: Optional[List[str]] = Field(None, description="技术栈数组")
    cover_url: Optional[str] = Field(None, description="封面图URL")
    screenshots: Optional[List[str]] = Field(None, description="截图URL数组")
    live_url: Optional[str] = Field(None, description="在线演示地址")
    repo_url: Optional[str] = Field(None, description="仓库地址")
    is_featured: bool = Field(False, description="是否为精选项目")
    sort_order: int = Field(0, description="排序顺序")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "个人作品集网站",
                "subtitle": "FastAPI + Vue3 全栈项目",
                "description": "基于 FastAPI 和 Vue3 构建的个人作品集网站。",
                "tech_stack": ["FastAPI", "Vue3", "MySQL"],
                "cover_url": "/static/images/projects/portfolio-cover.png",
                "screenshots": ["/static/images/projects/portfolio-1.png"],
                "live_url": "https://example.com",
                "repo_url": "https://github.com/xin-07/portfolio",
                "is_featured": True,
                "sort_order": 1
            }
        }


class ProjectUpdateRequest(BaseModel):
    """
    编辑项目请求模型（所有字段可选）
    """
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="项目标题")
    subtitle: Optional[str] = Field(None, max_length=200, description="项目副标题")
    description: Optional[str] = Field(None, max_length=5000, description="项目描述")
    tech_stack: Optional[List[str]] = Field(None, description="技术栈数组")
    cover_url: Optional[str] = Field(None, description="封面图URL")
    screenshots: Optional[List[str]] = Field(None, description="截图URL数组")
    live_url: Optional[str] = Field(None, description="在线演示地址")
    repo_url: Optional[str] = Field(None, description="仓库地址")
    is_featured: Optional[bool] = Field(None, description="是否为精选项目")
    sort_order: Optional[int] = Field(None, description="排序顺序")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "个人作品集网站（更新）",
                "is_featured": False,
                "sort_order": 2
            }
        }


class StatusUpdateRequest(BaseModel):
    """
    状态切换请求模型
    """
    status: Literal["published", "draft"] = Field(..., description="项目状态")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "published"
            }
        }


class ProfileUpdateRequest(BaseModel):
    """
    个人资料更新请求模型
    """
    name: Optional[str] = Field(None, description="姓名")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    title: Optional[str] = Field(None, description="头衔")
    bio: Optional[str] = Field(None, description="个人简介")
    tech_tags: Optional[List[str]] = Field(None, description="技术标签数组")
    github: Optional[str] = Field(None, description="GitHub 链接")
    gitee: Optional[str] = Field(None, description="Gitee 链接")
    wechat: Optional[str] = Field(None, description="微信号")
    qq: Optional[str] = Field(None, description="QQ号")
    email: Optional[List[str]] = Field(None, description="邮箱列表")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "xiny",
                "title": "全栈开发工程师 · AI Agent 探索者",
                "bio": "持续追踪 Vue3 与 AI Agent 前沿技术，通过实践快速掌握。",
                "tech_tags": ["Vue3", "FastAPI", "MySQL"],
                "github": "https://github.com/xin-07",
                "email": ["2074835619@qq.com"]
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    分页响应模型（泛型）
    """
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    items: List[T] = Field(..., description="数据列表")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 10,
                "page": 1,
                "page_size": 10,
                "items": []
            }
        }