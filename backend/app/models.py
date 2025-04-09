'''
Author: Mrasamu
Date: 2025-04-09 21:05:43
LastEditors: Mrasamu
LastEditTime: 2025-04-09 21:05:47
description: file content
FilePath: /pure-admin-thin/backend/app/models.py
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    mobile = Column(String(15), unique=True, nullable=False)
    yz_gender = Column(Integer, nullable=True)
    yz_is_member = Column(Integer, nullable=True)
    yz_trade_count = Column(Integer, nullable=True)
    yz_show_name = Column(String(100), nullable=True)
    yz_is_mobile_auth = Column(Boolean, nullable=True)
    yz_open_id = Column(String(100), nullable=True)
    yz_created_at = Column(DateTime, nullable=True)
    yz_points = Column(Integer, nullable=True)
    wechat_name = Column(String(100), nullable=True)
    wechat_friend_record_id = Column(String(100), nullable=True)
    wechat_remark = Column(String(255), nullable=True)
    wechat_gender = Column(Integer, nullable=True)
    wechat_province = Column(String(50), nullable=True)
    wechat_city = Column(String(50), nullable=True)
    wechat_account_id = Column(String(50), nullable=True)
    wechat_labels = Column(Text, nullable=True)  # 存储JSON字符串
    wechat_extend_fileds = Column(Text, nullable=True)  # 存储JSON字符串
    wechat_system_tags = Column(Text, nullable=True)  # 存储JSON字符串