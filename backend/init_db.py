'''
Author: Mrasamu
Date: 2025-04-09 21:08:33
LastEditors: Mrasamu
LastEditTime: 2025-04-09 21:09:45
description: file content
FilePath: /pure-admin-thin/backend/init_db.py
'''
# init_db.py
import random
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, Base

# 删除所有现有表并重新创建
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# 标签选项
tags = ["新客户", "老客户", "VIP", "高消费", "流失客户"]

# 创建会话
db = SessionLocal()

# 生成100个用户
for i in range(1, 101):
    # 生成随机标签
    user_tags = random.sample(tags, random.randint(1, 3))
    
    # 创建用户
    user = User(
        mobile=f"1{random.randint(3, 9)}{random.randint(100000000, 999999999)}",
        yz_gender=random.randint(0, 2),
        yz_is_member=random.randint(0, 1),
        yz_trade_count=random.randint(0, 50),
        yz_show_name=f"用户{i}",
        yz_is_mobile_auth=random.choice([True, False]),
        yz_open_id=f"open_id_{i}",
        yz_created_at=datetime.now() - timedelta(days=random.randint(0, 365)),
        yz_points=random.randint(0, 5000),
        wechat_name=f"微信用户{i}",
        wechat_friend_record_id=f"friend_{i}",
        wechat_remark=f"备注{i}" if random.random() > 0.5 else "",
        wechat_gender=random.randint(0, 2),
        wechat_province=random.choice(["北京", "上海", "广东", "四川"]),
        wechat_city=random.choice(["北京", "上海", "广州", "成都"]),
        wechat_account_id=f"account_{i}",
        wechat_labels=json.dumps(user_tags),
        wechat_extend_fileds="{}",
        wechat_system_tags="{}"
    )
    db.add(user)

# 提交事务
db.commit()
db.close()

print("数据初始化完成")