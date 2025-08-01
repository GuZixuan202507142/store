from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class CopilotAccount(SQLModel, table=True):
    """GitHub Copilot账号库存表"""
    __tablename__ = "copilot_account"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, description="GitHub Copilot账号邮箱")
    password: str = Field(description="GitHub Copilot账号密码")
    account_type: str = Field(default="education", description="账号类型：education, pro, business")
    status: str = Field(default="available", description="状态：available, assigned, expired")
    assigned_to_email: Optional[str] = Field(default=None, description="分配给的客户邮箱")
    assigned_at: Optional[datetime] = Field(default=None, description="分配时间")
    order_id: Optional[int] = Field(default=None, description="关联订单ID")
    expires_at: Optional[datetime] = Field(default=None, description="账号过期时间")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    notes: Optional[str] = Field(default=None, description="备注信息")
