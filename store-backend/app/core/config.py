from pydantic_settings import BaseSettings
from pydantic import validator
import os
import re

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Stripe
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PRICE_ID: str
    FRONTEND_URL: str

    # Gmail API OAuth2
    GMAIL_CLIENT_ID: str
    GMAIL_CLIENT_SECRET: str
    GMAIL_REFRESH_TOKEN: str
    EMAIL_SENDER: str

    # Gemini API
    GEMINI_API_KEY: str

    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        if not v:
            raise ValueError('DATABASE_URL is required')
        if not v.startswith(('postgresql://', 'postgresql+asyncpg://')):
            raise ValueError('DATABASE_URL must be a valid PostgreSQL connection string')
        return v

    @validator('STRIPE_API_KEY')
    def validate_stripe_key(cls, v):
        if not v.startswith(('sk_test_', 'sk_live_')):
            raise ValueError('STRIPE_API_KEY must be a valid Stripe secret key (starts with sk_test_ or sk_live_)')
        return v

    @validator('STRIPE_WEBHOOK_SECRET')
    def validate_webhook_secret(cls, v):
        if not v.startswith('whsec_'):
            raise ValueError('STRIPE_WEBHOOK_SECRET must start with whsec_')
        return v

    @validator('STRIPE_PRICE_ID')
    def validate_price_id(cls, v):
        if not v.startswith('price_'):
            raise ValueError('STRIPE_PRICE_ID must start with price_')
        return v

    @validator('FRONTEND_URL')
    def validate_frontend_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('FRONTEND_URL must be a valid URL starting with http:// or https://')
        return v

    @validator('GMAIL_CLIENT_ID')
    def validate_gmail_client_id(cls, v):
        if not v.endswith('.apps.googleusercontent.com') and v != 'your_gmail_client_id_here':
            raise ValueError('GMAIL_CLIENT_ID must end with .apps.googleusercontent.com')
        return v

    @validator('EMAIL_SENDER')
    def validate_email_sender(cls, v):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v) and v != 'your-email@gmail.com':
            raise ValueError('EMAIL_SENDER must be a valid email address')
        return v

    @validator('GEMINI_API_KEY')
    def validate_gemini_key(cls, v):
        if not v.startswith('AIzaSy') and v != 'AIzaSy_your_gemini_api_key_here':
            raise ValueError('GEMINI_API_KEY must start with AIzaSy')
        return v

    def validate_all_required(self):
        """验证所有必需的配置是否正确设置"""
        errors = []
        
        # 检查是否使用了示例值
        example_values = {
            'DATABASE_URL': 'postgresql+asyncpg://user:password@localhost:5432/store',
            'STRIPE_API_KEY': 'sk_test_your_stripe_secret_key_here',
            'STRIPE_WEBHOOK_SECRET': 'whsec_your_webhook_secret_here',
            'STRIPE_PRICE_ID': 'price_your_price_id_here',
            'GMAIL_CLIENT_ID': 'your_gmail_client_id_here',
            'GMAIL_CLIENT_SECRET': 'your_gmail_client_secret_here',
            'GMAIL_REFRESH_TOKEN': 'your_gmail_refresh_token_here',
            'EMAIL_SENDER': 'your-email@gmail.com',
            'GEMINI_API_KEY': 'AIzaSy_your_gemini_api_key_here'
        }
        
        for field, example_value in example_values.items():
            current_value = getattr(self, field, '')
            if current_value == example_value:
                errors.append(f'{field} is still using the example value. Please set a real value.')
        
        if errors:
            error_message = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(error_message)
        
        return True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 创建设置实例并验证
settings = Settings()

# 在开发环境中验证配置
if os.getenv('ENVIRONMENT', 'development') == 'development':
    try:
        settings.validate_all_required()
        print("✅ 配置验证通过")
    except ValueError as e:
        print(f"⚠️  配置验证警告: {e}")
        print("请检查 .env 文件并设置正确的配置值")
