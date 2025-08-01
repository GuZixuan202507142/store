#!/usr/bin/env python3
"""
脚本用于插入测试订单数据
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4

# 添加项目路径
sys.path.append('/usr/src/app')

from app.db.session import get_session
from app.models.order import Order
from sqlmodel.ext.asyncio.session import AsyncSession

async def insert_test_data():
    """插入测试订单数据"""
    
    test_orders = [
        {
            "customer_email": "fu908521560@gmail.com",
            "stripe_checkout_session_id": f"cs_test_{uuid4().hex[:24]}",
            "status": "completed",
            "product_name": "GitHub Copilot Education Edition",
            "amount_total": 2999,  # $29.99 in cents
            "created_at": datetime.utcnow() - timedelta(days=1)
        },
        {
            "customer_email": "fu908521560@gmail.com", 
            "stripe_checkout_session_id": f"cs_test_{uuid4().hex[:24]}",
            "status": "completed",
            "product_name": "GitHub Copilot Pro Monthly",
            "amount_total": 1999,  # $19.99 in cents
            "created_at": datetime.utcnow() - timedelta(hours=12)
        },
        {
            "customer_email": "fu908521560@gmail.com",
            "stripe_checkout_session_id": f"cs_test_{uuid4().hex[:24]}",
            "status": "pending",
            "product_name": "GitHub Copilot Business",
            "amount_total": 3999,  # $39.99 in cents
            "created_at": datetime.utcnow() - timedelta(hours=2)
        },
        {
            "customer_email": "test@example.com",
            "stripe_checkout_session_id": f"cs_test_{uuid4().hex[:24]}",
            "status": "completed",
            "product_name": "GitHub Copilot Education Edition",
            "amount_total": 2999,  # $29.99 in cents
            "created_at": datetime.utcnow() - timedelta(days=3)
        }
    ]
    
    try:
        async for session in get_session():
            print("🔄 开始插入测试数据...")
            
            for i, order_data in enumerate(test_orders, 1):
                new_order = Order(**order_data)
                session.add(new_order)
                print(f"✅ 插入订单 {i}: {order_data['customer_email']} - {order_data['product_name']}")
            
            await session.commit()
            print(f"\n🎉 成功插入 {len(test_orders)} 条测试订单数据！")
            
            # 验证插入的数据
            from sqlmodel import select
            statement = select(Order)
            result = await session.exec(statement)
            all_orders = result.all()
            
            print(f"\n📊 数据库中总共有 {len(all_orders)} 条订单:")
            for order in all_orders:
                print(f"  - ID: {order.id}, Email: {order.customer_email}, Status: {order.status}")
                print(f"    Product: {order.product_name}, Amount: ${order.amount_total/100:.2f}")
                print(f"    Created: {order.created_at}")
                print()
            
            break
            
    except Exception as e:
        print(f"❌ 插入数据时出错: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(insert_test_data())
