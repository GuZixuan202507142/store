import logging
from typing import Optional
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.inventory import CopilotAccount

logger = logging.getLogger(__name__)

class InventoryService:
    """库存管理服务"""
    
    @staticmethod
    async def get_available_account(account_type: str, db: AsyncSession) -> Optional[CopilotAccount]:
        """获取可用的账号"""
        try:
            statement = select(CopilotAccount).where(
                CopilotAccount.account_type == account_type,
                CopilotAccount.status == "available"
            ).limit(1)
            
            result = await db.exec(statement)
            account = result.first()
            
            if account:
                logger.info(f"找到可用账号: {account.email} (类型: {account_type})")
            else:
                logger.warning(f"没有可用的 {account_type} 账号")
                
            return account
            
        except Exception as e:
            logger.error(f"查询可用账号时出错: {str(e)}")
            return None
    
    @staticmethod
    async def assign_account(
        account: CopilotAccount, 
        customer_email: str, 
        order_id: int,
        db: AsyncSession
    ) -> bool:
        """分配账号给客户"""
        try:
            account.status = "assigned"
            account.assigned_to_email = customer_email
            account.assigned_at = datetime.utcnow()
            account.order_id = order_id
            # 设置账号1年后过期
            account.expires_at = datetime.utcnow() + timedelta(days=365)
            
            db.add(account)
            await db.commit()
            await db.refresh(account)
            
            logger.info(f"成功分配账号 {account.email} 给客户 {customer_email}")
            return True
            
        except Exception as e:
            logger.error(f"分配账号时出错: {str(e)}")
            await db.rollback()
            return False
    
    @staticmethod
    async def add_account_to_inventory(
        email: str,
        password: str, 
        account_type: str,
        db: AsyncSession,
        notes: Optional[str] = None
    ) -> Optional[CopilotAccount]:
        """添加账号到库存"""
        try:
            new_account = CopilotAccount(
                email=email,
                password=password,
                account_type=account_type,
                status="available",
                notes=notes
            )
            
            db.add(new_account)
            await db.commit()
            await db.refresh(new_account)
            
            logger.info(f"成功添加账号到库存: {email} (类型: {account_type})")
            return new_account
            
        except Exception as e:
            logger.error(f"添加账号到库存时出错: {str(e)}")
            await db.rollback()
            return None
    
    @staticmethod
    async def get_inventory_status(db: AsyncSession) -> dict:
        """获取库存状态"""
        try:
            # 查询各类型账号数量
            result = {}
            
            for account_type in ["education", "pro", "business"]:
                for status in ["available", "assigned", "expired"]:
                    statement = select(CopilotAccount).where(
                        CopilotAccount.account_type == account_type,
                        CopilotAccount.status == status
                    )
                    count_result = await db.exec(statement)
                    count = len(count_result.all())
                    
                    if account_type not in result:
                        result[account_type] = {}
                    result[account_type][status] = count
            
            logger.info(f"库存状态: {result}")
            return result
            
        except Exception as e:
            logger.error(f"查询库存状态时出错: {str(e)}")
            return {}

# 创建全局实例
inventory_service = InventoryService()
