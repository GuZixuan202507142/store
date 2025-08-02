import stripe
import logging
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from . import email_service
from .inventory_service import inventory_service

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Stripe with API key
if settings.STRIPE_API_KEY:
    stripe.api_key = settings.STRIPE_API_KEY
    logger.info(f"Stripe API key initialized with key ending in: {settings.STRIPE_API_KEY[-4:]}")
else:
    logger.error("STRIPE_API_KEY not found in environment variables")
    raise ValueError("STRIPE_API_KEY not configured")

async def handle_stripe_webhook(payload: bytes, sig_header: str, db: AsyncSession):
    """
    Handles Stripe webhook events, specifically for completed checkouts.
    """
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        logger.info(f"Received webhook event: {event['type']}")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Webhook signature verification failed: {str(e)}")
        raise ValueError("Invalid signature") from e

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email')
        
        if not customer_email:
            logger.error(f"Customer email not found in webhook event for session {session.id}")
            raise ValueError("Customer email not found in webhook event.")

        try:
            # 🔥 核心业务逻辑：分配GitHub Copilot账号
            account_type = "education"  # 根据产品类型确定账号类型
            
            # 从库存中获取可用账号
            available_account = await inventory_service.get_available_account(account_type, db)
            
            if available_account:
                # 分配账号给客户
                success = await inventory_service.assign_account(
                    available_account, customer_email, 0, db
                )
                
                if success:
                    logger.info(f"成功分配账号 {available_account.email} 给客户 {customer_email}")
                    
                    # 发送账号密码邮件
                    try:
                        await email_service.send_account_credentials(
                            to_email=customer_email,
                            account_email=available_account.email,
                            account_password=available_account.password,
                            order_id=0
                        )
                        logger.info(f"已发送账号密码到 {customer_email}")
                    except Exception as email_error:
                        logger.error(f"发送账号密码邮件失败: {str(email_error)}")
                        # 账号已分配，但邮件发送失败，需要手动处理
                else:
                    logger.error(f"分配账号失败，客户: {customer_email}")
            else:
                logger.error(f"没有可用的 {account_type} 账号！客户: {customer_email}")
                # 应该发送缺货通知或退款
                
        except Exception as db_error:
            logger.error(f"Database error processing webhook: {str(db_error)}")
            await db.rollback()
            raise

    else:
        logger.info(f"Unhandled event type {event['type']}")
        print(f"Unhandled event type {event['type']}")

async def get_inventory_count(db: AsyncSession):
    """
    Returns the number of items in the inventory.
    """
    return await inventory_service.get_inventory_count(db)

async def add_inventory_item(username: str, password: str, db: AsyncSession):
    """
    Adds a new item to the inventory.
    """
    await inventory_service.add_inventory_item(username=username, password=password, db=db)
