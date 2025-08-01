#!/usr/bin/env python3
"""
脚本用于设置库存系统和添加测试账号
"""
import asyncio
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.append('/usr/src/app')

from app.db.session import get_session
from app.models.inventory import CopilotAccount
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text

async def setup_inventory_system():
    """设置库存系统"""
    
    try:
        async for session in get_session():
            print("🔄 正在设置库存系统...")
            
            # 创建库存表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS copilot_account (
                id SERIAL PRIMARY KEY,
                email VARCHAR NOT NULL,
                password VARCHAR NOT NULL,
                account_type VARCHAR DEFAULT 'education',
                status VARCHAR DEFAULT 'available',
                assigned_to_email VARCHAR DEFAULT NULL,
                assigned_at TIMESTAMP DEFAULT NULL,
                order_id INTEGER DEFAULT NULL,
                expires_at TIMESTAMP DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT DEFAULT NULL
            );
            """
            
            await session.exec(text(create_table_sql))
            await session.commit()
            print("✅ 库存表创建成功")
            
            # 添加测试账号
            test_accounts = [
                {
                    "email": "copilot.edu.001@github.com",
                    "password": "TempPass123!",
                    "account_type": "education",
                    "notes": "测试账号 - Education Edition"
                },
                {
                    "email": "copilot.edu.002@github.com", 
                    "password": "TempPass456!",
                    "account_type": "education",
                    "notes": "测试账号 - Education Edition"
                },
                {
                    "email": "copilot.pro.001@github.com",
                    "password": "ProPass789!",
                    "account_type": "pro",
                    "notes": "测试账号 - Pro Edition"
                },
                {
                    "email": "copilot.biz.001@github.com",
                    "password": "BizPass101!",
                    "account_type": "business", 
                    "notes": "测试账号 - Business Edition"
                }
            ]
            
            print("🔄 正在添加测试账号到库存...")
            for i, account_data in enumerate(test_accounts, 1):
                new_account = CopilotAccount(**account_data)
                session.add(new_account)
                print(f"✅ 添加账号 {i}: {account_data['email']} ({account_data['account_type']})")
            
            await session.commit()
            print(f"\n🎉 成功添加 {len(test_accounts)} 个测试账号到库存！")
            
            # 验证库存状态
            from sqlmodel import select
            statement = select(CopilotAccount)
            result = await session.exec(statement)
            all_accounts = result.all()
            
            print(f"\n📊 库存状态 (总共 {len(all_accounts)} 个账号):")
            
            for account_type in ["education", "pro", "business"]:
                available = len([a for a in all_accounts if a.account_type == account_type and a.status == "available"])
                assigned = len([a for a in all_accounts if a.account_type == account_type and a.status == "assigned"])
                print(f"  📋 {account_type.title()}: {available} 可用, {assigned} 已分配")
            
            print("\n📝 账号详情:")
            for account in all_accounts:
                status_icon = "🟢" if account.status == "available" else "🔴"
                print(f"  {status_icon} {account.email} ({account.account_type}) - {account.status}")
            
            break
            
    except Exception as e:
        print(f"❌ 设置库存系统时出错: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(setup_inventory_system())
