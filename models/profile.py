"""
Profile 模型模块
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ProfileResponse(BaseModel):
    """
    个人资料响应模型
    """
    id: int = Field(..., description="主键ID")
    name: str = Field(..., description="姓名")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    title: Optional[str] = Field(None, description="头衔")
    bio: Optional[str] = Field(None, description="个人简介")
    tech_tags: Optional[List[str]] = Field(None, description="技术标签数组")
    github: Optional[str] = Field(None, description="GitHub 链接")
    gitee: Optional[str] = Field(None, description="Gitee 链接")
    wechat: Optional[str] = Field(None, description="微信号")
    qq: Optional[str] = Field(None, description="QQ号")
    email: Optional[List[str]] = Field(None, description="邮箱列表")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "xiny",
                "avatar_url": "/api/avatar/D:/File/photos/%E8%90%BD%E6%97%A5.jpg",
                "title": "全栈开发工程师 · AI Agent 探索者",
                "bio": "持续追踪 Vue3 与 AI Agent 前沿技术，通过实践快速掌握。具备跨专业协作能力，坚持每周技术复盘。",
                "tech_tags": ["Vue3", "FastAPI", "MySQL", "OpenClaw", "HarmonyOS", "ECharts"],
                "github": "https://github.com/xin-07",
                "gitee": "https://gitee.com/xin-keep-going",
                "wechat": "Yyk-293342",
                "qq": "2074835619",
                "email": ["2074835619@qq.com", "xin_y0607@outlook.com", "xiny0607.23@gmail.com"],
                "created_at": "2026-06-09 18:50:32",
                "updated_at": "2026-06-09 18:54:38"
            }
        }