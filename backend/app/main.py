'''
Author: Mrasamu
Date: 2025-04-09 21:06:42
LastEditors: Mrasamu
LastEditTime: 2025-04-09 21:06:47
description: file content
FilePath: /pure-admin-thin/backend/app/main.py
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users
from . import models
from .database import engine

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(title="用户管理系统API")

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该指定前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "欢迎使用用户管理系统API"}