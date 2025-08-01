<template>
  <div class="product-card">
    <div class="price-section">
      <div class="price">¥50</div>
      <div class="price-description">一次性付费，长期使用</div>
    </div>

    <div class="verification-links">
      <a href="https://github.com/features/copilot" target="_blank" rel="noopener noreferrer" class="verification-link">GitHub Copilot 官网</a>
      <a href="https://education.github.com/pack" target="_blank" rel="noopener noreferrer" class="verification-link">学生包权益详情</a>
    </div>

    <div class="form-section">
      <input 
        type="email" 
        class="email-input" 
        placeholder="请输入您的邮箱地址"
        :value="appStore.email"
        @input="appStore.setEmail($event.target.value)"
      >
      <button 
        class="buy-button"
        @click="handlePurchase"
        :disabled="isProcessing"
      >
        {{ isProcessing ? '处理中...' : '立即购买' }}
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAppStore } from '@/stores/appStore';
import { createCheckoutSession } from '@/services/api';

const appStore = useAppStore();
const isProcessing = ref(false);
const errorMessage = ref('');

const handlePurchase = async () => {
  errorMessage.value = '';
  if (!appStore.email) {
    errorMessage.value = '请输入您的邮箱地址';
    return;
  }
  if (!/^\S+@\S+\.\S+$/.test(appStore.email)) {
    errorMessage.value = '请输入有效的邮箱地址';
    return;
  }

  isProcessing.value = true;
  try {
    const response = await createCheckoutSession(appStore.email);
    window.location.href = response.url;
  } catch (error) {
    console.error('Failed to create checkout session:', error);
    errorMessage.value = '创建支付链接失败，请稍后重试。';
  } finally {
    isProcessing.value = false;
  }
};
</script>

<style scoped>
.product-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 48px;
  margin: 48px auto 0;
  max-width: 500px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
}

.price-section {
  text-align: center;
  margin-bottom: 32px;
}

.price {
  font-size: 48px;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 8px;
}

.price-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
}

.verification-links {
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  gap: 16px;
}

.verification-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
  padding: 8px 16px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  transition: all 0.3s ease;
  flex: 1;
  text-align: center;
}

.verification-link:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.5);
}

.form-section {
  display: flex;
  flex-direction: column;
}

.email-input {
  width: 100%;
  padding: 16px 20px;
  font-size: 17px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #f5f5f7;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.email-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(255, 255, 255, 0.12);
}

.email-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.buy-button {
  width: 100%;
  padding: 18px;
  font-size: 17px;
  font-weight: 600;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.buy-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
}

.buy-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  color: #ff4d4f;
  text-align: center;
  margin-top: 12px;
  font-size: 14px;
}
</style>