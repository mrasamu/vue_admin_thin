'''
Author: Mrasamu
Date: 2025-04-09 21:06:09
LastEditors: Mrasamu
LastEditTime: 2025-04-09 21:06:12
description: file content
FilePath: /pure-admin-thin/backend/app/schemas.py
'''
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    mobile: str

class UserCreate(UserBase):
    yz_gender: Optional[int] = None
    yz_is_member: Optional[int] = None
    yz_trade_count: Optional[int] = None
    yz_show_name: Optional[str] = None
    yz_is_mobile_auth: Optional[bool] = None
    yz_open_id: Optional[str] = None
    yz_created_at: Optional[datetime] = None
    yz_points: Optional[int] = None
    wechat_name: Optional[str] = None
    wechat_friend_record_id: Optional[str] = None
    wechat_remark: Optional[str] = None
    wechat_gender: Optional[int] = None
    wechat_province: Optional[str] = None
    wechat_city: Optional[str] = None
    wechat_account_id: Optional[str] = None
    wechat_labels: Optional[str] = None
    wechat_extend_fileds: Optional[str] = None
    wechat_system_tags: Optional[str] = None

class User(UserBase):
    user_id: int
    yz_gender: Optional[int] = None
    yz_is_member: Optional[int] = None
    yz_trade_count: Optional[int] = None
    yz_show_name: Optional[str] = None
    yz_is_mobile_auth: Optional[bool] = None
    yz_open_id: Optional[str] = None
    yz_created_at: Optional[datetime] = None
    yz_points: Optional[int] = None
    wechat_name: Optional[str] = None
    wechat_friend_record_id: Optional[str] = None
    wechat_remark: Optional[str] = None
    wechat_gender: Optional[int] = None
    wechat_province: Optional[str] = None
    wechat_city: Optional[str] = None
    wechat_account_id: Optional[str] = None
    wechat_labels: Optional[str] = None
    wechat_extend_fileds: Optional[str] = None
    wechat_system_tags: Optional[str] = None

    class Config:
        orm_mode = True

class PaginatedResponse(BaseModel):
    success: bool = True
    total: int
    data: List[User]