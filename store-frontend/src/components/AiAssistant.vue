<template>
  <div class="ai-assistant">
    <h2 class="ai-title">🤖 AI智能客服助手</h2>
    <p class="ai-description">有疑问？我是您的专属AI助手，可以帮您了解GitHub Copilot学生包服务。</p>
    
    <button 
      class="ai-button"
      @click="getAiWelcome"
      :disabled="aiLoading"
    >
      {{ aiLoading ? '正在为您准备服务...' : '开始咨询服务' }}
    </button>
    
    <div v-if="aiMessage" class="ai-message">
      <p>{{ aiMessage }}</p>
    </div>
    
    <div v-if="aiError" class="ai-error">
      <p>{{ aiError }}</p>
    </div>

    <!-- 订单查询功能 -->
    <div class="order-query-section">
      <h3 class="order-title">📋 查询我的订单</h3>
      <p class="order-description">输入您的邮箱地址查看订单状态</p>
      <div class="order-form">
        <input 
          v-model="queryEmail"
          type="email" 
          class="query-input" 
          placeholder="请输入购买时使用的邮箱"
        >
        <button 
          class="query-button"
          @click="queryOrders"
          :disabled="queryLoading || !queryEmail"
        >
          {{ queryLoading ? '查询中...' : '查询订单' }}
        </button>
      </div>
      <div v-if="orderResult" class="order-result">
        <p v-if="orderResult.length === 0" class="no-orders">暂无订单记录</p>
        <div v-else class="orders-list">
          <div v-for="order in orderResult" :key="order.id" class="order-item">
            <p><strong>订单号:</strong> #{{ order.id }}</p>
            <p><strong>状态:</strong> <span :class="getStatusClass(order.status)">{{ getStatusText(order.status) }}</span></p>
            <p><strong>金额:</strong> ¥{{ (order.amount_total / 100).toFixed(2) }}</p>
            <p><strong>时间:</strong> {{ formatDate(order.created_at) }}</p>
          </div>
        </div>
      </div>
      <div v-if="queryError" class="ai-error">
        <p>{{ queryError }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// AI客服相关状态
const aiLoading = ref(false);
const aiMessage = ref('');
const aiError = ref('');

// 订单查询相关状态
const queryEmail = ref('');
const queryLoading = ref(false);
const orderResult = ref(null);
const queryError = ref('');

// Gemini API配置
const API_KEY = "AIzaSyA2-M7sWX18X8unq1Hn1QKHOevUSiw9QRU";

// AI客服功能
const getAiWelcome = async () => {
  if (API_KEY === "YOUR_GEMINI_API_KEY") {
    aiError.value = '请配置Gemini API密钥。';
    return;
  }

  aiLoading.value = true;
  aiError.value = '';
  aiMessage.value = '';

  const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`;
  
  // 定制化前置prompt - 针对GitHub Copilot学生包销售平台
  const systemPrompt = `你是一个专业的AI客服助手，为GitHub Copilot学生包销售平台提供服务。

【平台信息】
- 平台名称：GitHub Copilot学生包销售平台
- 主要产品：GitHub Copilot学生包权益
- 价格：¥50 一次性付费，长期使用
- 技术栈：基于FastAPI后端 + Vue 3前端的现代化电商平台

【核心功能与服务】
1. 🛒 购买服务
   - 响应式购买页面，移动端友好
   - Stripe安全支付系统，支持信用卡在线支付
   - 实时购买状态反馈和流程可视化
   - 自动邮箱验证和确认邮件发送

2. 🤖 AI智能客服（就是你）
   - 基于Google Gemini 2.0 Flash的聊天助手
   - 提供GitHub Copilot相关技术支持
   - 购买流程指导和问题解答

【GitHub Copilot学生包详细信息】
- 什么是GitHub Copilot：AI编程助手，基于OpenAI Codex
- 主要功能：
  * 实时代码建议和自动完成
  * 支持多种编程语言（Python、JavaScript、TypeScript、Go、Ruby等）
  * 智能注释转代码
  * 代码解释和优化建议
  * 单元测试生成

- 学生包权益：
  * 免费使用GitHub Copilot（原价$10/月）
  * 访问GitHub Student Developer Pack其他工具
  * 无限制的AI代码建议
  * 集成主流IDE（VS Code、Neovim、JetBrains等）

【购买流程】
1. 在左侧输入有效邮箱地址
2. 点击"立即购买"按钮
3. 跳转到Stripe安全支付页面
4. 完成¥50支付
5. 系统自动发送确认邮件和权益信息

【常见问题解答】
Q: 支付安全吗？
A: 我们使用Stripe国际支付平台，银行级安全加密，您的支付信息完全安全。

Q: 支付后多久能收到账号？
A: 支付成功后立即自动发送确认邮件，包含详细的权益激活指导。

请始终保持友善、专业和耐心的态度，用简洁明了的语言回答问题。你代表的是一个值得信赖的GitHub Copilot学生包服务提供商，致力于帮助学生和教育工作者提升编程效率。`;

  const prompt = `${systemPrompt}\n\n请生成一条简短、友好且专业的欢迎信息，介绍我们的GitHub Copilot学生包服务，让访问用户感受到我们的专业性和热情，并简要说明您能提供的服务内容。`;

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-goog-api-key': API_KEY,
      },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: prompt
          }]
        }]
      })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error.message || '请求失败');
    }

    const data = await response.json();
    aiMessage.value = data.candidates[0].content.parts[0].text;

  } catch (err) {
    console.error('调用 Gemini API 时出错:', err);
    aiError.value = `生成消息时出错: ${err.message}`;
  } finally {
    aiLoading.value = false;
  }
};

// 订单查询功能
const queryOrders = async () => {
  if (!queryEmail.value) {
    queryError.value = '请输入邮箱地址';
    return;
  }

  queryLoading.value = true;
  queryError.value = '';
  orderResult.value = null;

  try {
    const response = await fetch(`http://localhost:8000/api/v1/orders/email/${queryEmail.value}`);
    
    if (!response.ok) {
      throw new Error('查询失败，请检查邮箱地址');
    }

    const orders = await response.json();
    orderResult.value = orders;

  } catch (err) {
    console.error('查询订单时出错:', err);
    queryError.value = `查询失败: ${err.message}`;
  } finally {
    queryLoading.value = false;
  }
};

// 辅助函数
const getStatusClass = (status) => {
  switch (status) {
    case 'completed': return 'status-completed';
    case 'pending': return 'status-pending';
    case 'failed': return 'status-failed';
    default: return 'status-unknown';
  }
};

const getStatusText = (status) => {
  switch (status) {
    case 'completed': return '已完成';
    case 'pending': return '处理中';
    case 'failed': return '失败';
    default: return '未知';
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN');
};
</script>

<style scoped>
.ai-assistant {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  margin: 0 auto;
}

.ai-title {
  color: #f5f5f7;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
  text-align: center;
}

.ai-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  text-align: center;
  margin-bottom: 24px;
  line-height: 1.6;
}

.ai-button {
  width: 100%;
  padding: 16px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.ai-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.ai-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.ai-message {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.ai-message p {
  color: #f5f5f7;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

.ai-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.ai-error p {
  color: #fca5a5;
  font-size: 14px;
  margin: 0;
}

/* 订单查询样式 */
.order-query-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.order-title {
  color: #f5f5f7;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  text-align: center;
}

.order-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  text-align: center;
  margin-bottom: 20px;
  line-height: 1.5;
}

.order-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.query-input {
  width: 100%;
  padding: 16px 20px;
  font-size: 15px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #f5f5f7;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.query-input:focus {
  outline: none;
  border-color: #8b5cf6;
  background: rgba(255, 255, 255, 0.12);
}

.query-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.query-button {
  width: 100%;
  padding: 16px;
  font-size: 15px;
  font-weight: 500;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.query-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
}

.query-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.order-result {
  margin-top: 16px;
}

.no-orders {
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  font-size: 14px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
}

.order-item p {
  color: #f5f5f7;
  font-size: 14px;
  margin: 4px 0;
}

.order-item strong {
  color: rgba(255, 255, 255, 0.9);
}

.status-completed {
  color: #10b981;
  font-weight: 600;
}

.status-pending {
  color: #f59e0b;
  font-weight: 600;
}

.status-failed {
  color: #ef4444;
  font-weight: 600;
}

.status-unknown {
  color: #6b7280;
  font-weight: 600;
}
</style>
