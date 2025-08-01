# GitHub Copilot 学生包销售平台

一个基于 FastAPI 和 Vue 3 构建的现代化电商平台，专门用于销售 GitHub Copilot 学生包账号权益。

## 项目简介

本项目是一个全栈电商应用，提供 GitHub Copilot 教育版账号的在线购买服务。平台集成了 Stripe 支付系统、AI 客服助手、邮件通知等现代化功能，为用户提供便捷、安全的购买体验。

## 核心功能

### 🛒 前端功能
- **响应式购买页面** - 移动端友好的用户界面
- **Stripe 安全支付** - 支持信用卡在线支付
- **AI 智能客服** - 基于 Google Gemini 的聊天助手
- **实时状态反馈** - 购买流程可视化
- **邮箱验证** - 自动验证用户邮箱格式

### ⚡ 后端功能
- **异步 API 接口** - 基于 FastAPI 的高性能后端
- **支付处理** - Stripe 支付集成和 Webhook 处理
- **订单管理** - 完整的订单创建、查询、状态管理
- **邮件通知** - Gmail API 自动发送购买确认邮件
- **数据库存储** - PostgreSQL 持久化存储
- **API 文档** - 自动生成的 OpenAPI/Swagger 文档

### 🤖 AI 集成
- **智能客服助手** - 回答用户关于 GitHub Copilot 的问题
- **聊天记录存储** - Firebase 云存储聊天历史
- **会话管理** - 支持多轮对话和上下文理解

## 技术栈

### 后端技术
- **FastAPI** - 现代 Python Web 框架
- **SQLModel** - 类型安全的数据库 ORM
- **PostgreSQL** - 关系型数据库
- **Stripe** - 支付处理平台
- **Gmail API** - 邮件发送服务
- **Google Gemini** - AI 对话模型

### 前端技术
- **Vue 3** - 渐进式 JavaScript 框架
- **Pinia** - 状态管理库
- **Vite** - 快速构建工具
- **Firebase** - 聊天数据存储
- **CSS3** - 现代样式设计

### 运维技术
- **Docker** - 容器化部署
- **Docker Compose** - 本地开发编排
- **Alembic** - 数据库迁移工具

## 安装与运行

### 环境要求
- Docker 和 Docker Compose
- Git

### 快速启动

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd store
   ```

2. **配置环境变量**
   
   在 `store-backend` 目录下创建 `.env` 文件：
   ```bash
   # 数据库配置
   DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/store_db
   
   # Stripe 配置
   STRIPE_API_KEY=sk_test_your_stripe_secret_key
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
   STRIPE_PRICE_ID=price_your_product_price_id
   FRONTEND_URL=http://localhost:5173
   
   # Gmail API 配置
   GMAIL_CLIENT_ID=your_gmail_client_id
   GMAIL_CLIENT_SECRET=your_gmail_client_secret
   GMAIL_REFRESH_TOKEN=your_gmail_refresh_token
   EMAIL_SENDER=your_email@gmail.com
   
   # Gemini AI 配置
   GEMINI_API_KEY=your_gemini_api_key
   ```

   在 `store-frontend` 目录下创建 `.env` 文件：
   ```bash
   # API 配置
   VITE_API_BASE_URL=http://localhost:8000
   
   # Firebase 配置
   VITE_FIREBASE_API_KEY=your_firebase_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   VITE_FIREBASE_APP_ID=your_app_id
   
   # Gemini AI 配置（用于前端 AI 助手）
   VITE_GEMINI_API_KEY=your_gemini_api_key
   ```

   在根目录创建 `.env` 文件（用于 Docker Compose）：
   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   POSTGRES_DB=store_db
   ```

3. **启动应用**
   ```bash
   docker-compose up --build
   ```

4. **访问应用**
   - 前端界面：http://localhost:5173
   - 后端 API：http://localhost:8000
   - API 文档：http://localhost:8000/docs

### 本地开发

**后端开发**
```bash
cd store-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**前端开发**
```bash
cd store-frontend
npm install
npm run dev
```

## API 密钥配置

### 1. Stripe 配置
- 访问 [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
- 获取 API 密钥和创建产品价格 ID
- 配置 Webhook 端点：`your_domain/api/v1/payments/webhook`

### 2. Gmail API 配置
- 在 [Google Cloud Console](https://console.cloud.google.com/) 创建项目
- 启用 Gmail API
- 创建 OAuth 2.0 凭据
- 获取刷新令牌

### 3. Google Gemini AI 配置
- 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
- 创建 API 密钥

### 4. Firebase 配置
- 在 [Firebase Console](https://console.firebase.google.com/) 创建项目
- 启用 Firestore 数据库
- 获取项目配置信息

## 项目结构

```
store/
├── store-backend/              # FastAPI 后端应用
│   ├── app/
│   │   ├── api/v1/            # API 路由
│   │   │   ├── payments.py    # 支付相关接口
│   │   │   └── orders.py      # 订单管理接口
│   │   ├── core/              # 核心配置
│   │   │   └── config.py      # 应用配置
│   │   ├── db/                # 数据库配置
│   │   │   └── session.py     # 数据库会话
│   │   ├── models/            # 数据模型
│   │   │   └── order.py       # 订单模型
│   │   ├── schemas/           # 数据验证模式
│   │   │   ├── order.py       # 订单模式
│   │   │   └── payment.py     # 支付模式
│   │   ├── services/          # 业务逻辑服务
│   │   │   ├── payment_service.py  # 支付服务
│   │   │   └── email_service.py    # 邮件服务
│   │   └── main.py            # 应用入口
│   ├── alembic/               # 数据库迁移
│   ├── tests/                 # 测试文件
│   ├── requirements.txt       # Python 依赖
│   └── Dockerfile            # Docker 配置
├── store-frontend/            # Vue 3 前端应用
│   ├── src/
│   │   ├── components/        # Vue 组件
│   │   │   ├── Navbar.vue     # 导航栏
│   │   │   ├── HeroSection.vue # 主页横幅
│   │   │   ├── ProductCard.vue # 产品卡片
│   │   │   ├── AiAssistant.vue # AI 助手
│   │   │   └── AppFooter.vue  # 页脚
│   │   ├── services/          # 服务层
│   │   │   ├── api.js         # API 客户端
│   │   │   └── firebase.js    # Firebase 配置
│   │   ├── stores/            # 状态管理
│   │   │   └── appStore.js    # 应用状态
│   │   ├── App.vue            # 应用根组件
│   │   └── main.ts            # 应用入口
│   ├── package.json           # Node.js 依赖
│   └── Dockerfile            # Docker 配置
├── docker-compose.yml         # 开发环境编排
└── README.md                 # 项目文档
```

## 常见问题

### Q: 支付失败怎么办？
A: 请检查网络连接，确保使用有效的信用卡信息。如问题持续，请联系客服。

### Q: 没有收到确认邮件？
A: 请检查垃圾邮件文件夹，或联系客服获取订单状态。

### Q: AI 助手无法正常工作？
A: 请确保 Gemini API 密钥配置正确，网络连接正常。

### Q: 如何查看我的订单？
A: 目前可以通过 API 接口查询：`GET /api/v1/orders/email/{your_email}`

## 注意事项

1. **安全配置**：请妥善保管所有 API 密钥，不要提交到版本控制系统
2. **测试环境**：开发阶段请使用 Stripe 测试密钥
3. **数据备份**：生产环境请定期备份数据库
4. **监控日志**：建议配置日志监控以及时发现问题

## 许可证

本项目基于 MIT 许可证开源。