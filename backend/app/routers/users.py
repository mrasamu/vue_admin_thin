from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("", response_model=schemas.PaginatedResponse)
def get_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, alias="limit", ge=1, le=100),
    mobile: Optional[str] = None,
    gender: Optional[int] = None,
    isMember: Optional[int] = None,
    minTradeCount: Optional[int] = None,
    maxTradeCount: Optional[int] = None,
    wechatName: Optional[str] = None,
    wechatRemark: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    tags: Optional[str] = None
):
    query = db.query(models.User)
    
    # 应用过滤条件
    if mobile:
        query = query.filter(models.User.mobile.like(f"%{mobile}%"))
    if gender is not None:
        query = query.filter(models.User.yz_gender == gender)
    if isMember is not None:
        query = query.filter(models.User.yz_is_member == isMember)
    if minTradeCount is not None:
        query = query.filter(models.User.yz_trade_count >= minTradeCount)
    if maxTradeCount is not None:
        query = query.filter(models.User.yz_trade_count <= maxTradeCount)
    if wechatName:
        query = query.filter(models.User.wechat_name.like(f"%{wechatName}%"))
    if wechatRemark:
        query = query.filter(models.User.wechat_remark.like(f"%{wechatRemark}%"))
    if startDate:
        query = query.filter(models.User.yz_created_at >= datetime.strptime(startDate, "%Y-%m-%d"))
    if endDate:
        query = query.filter(models.User.yz_created_at <= datetime.strptime(f"{endDate} 23:59:59", "%Y-%m-%d %H:%M:%S"))
    
    # 标签过滤（较为复杂，需要JSON查询）
    if tags:
        tags_list = json.loads(tags)
        for tag in tags_list:
            query = query.filter(models.User.wechat_labels.like(f"%{tag}%"))
    
    # 计算总数
    total = query.count()
    
    # 分页
    users = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "total": total,
        "data": users
    }

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户数据
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/export", response_model=List[schemas.User])
def export_users(
    db: Session = Depends(get_db),
    mobile: Optional[str] = None,
    gender: Optional[int] = None,
    isMember: Optional[int] = None,
    minTradeCount: Optional[int] = None,
    maxTradeCount: Optional[int] = None,
    wechatName: Optional[str] = None,
    wechatRemark: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    tags: Optional[str] = None
):
    query = db.query(models.User)
    
    # 应用与get_users相同的过滤条件
    if mobile:
        query = query.filter(models.User.mobile.like(f"%{mobile}%"))
    if gender is not None:
        query = query.filter(models.User.yz_gender == gender)
    if isMember is not None:
        query = query.filter(models.User.yz_is_member == isMember)
    if minTradeCount is not None:
        query = query.filter(models.User.yz_trade_count >= minTradeCount)
    if maxTradeCount is not None:
        query = query.filter(models.User.yz_trade_count <= maxTradeCount)
    if wechatName:
        query = query.filter(models.User.wechat_name.like(f"%{wechatName}%"))
    if wechatRemark:
        query = query.filter(models.User.wechat_remark.like(f"%{wechatRemark}%"))
    if startDate:
        query = query.filter(models.User.yz_created_at >= datetime.strptime(startDate, "%Y-%m-%d"))
    if endDate:
        query = query.filter(models.User.yz_created_at <= datetime.strptime(f"{endDate} 23:59:59", "%Y-%m-%d %H:%M:%S"))
    
    # 标签过滤
    if tags:
        tags_list = json.loads(tags)
        for tag in tags_list:
            query = query.filter(models.User.wechat_labels.like(f"%{tag}%"))
    
    # 获取所有匹配的用户
    users = query.all()
    
    return users