<template>
  <div class="ai-assistant">
    <button 
      @click="appStore.toggleChat" 
      class="ai-button"
      :class="{ 'active': appStore.isChatOpen }"
    >
      <span v-if="!appStore.isChatOpen">💬</span>
      <span v-else>✕</span>
    </button>
    
    <div v-if="appStore.isChatOpen" class="ai-chat-window">
      <div class="ai-header">
        <h3>AI Assistant</h3>
        <p>有什么可以帮助您的吗？</p>
      </div>
      
      <div class="ai-messages" ref="messagesContainer">
        <div 
          v-for="message in appStore.chatMessages" 
          :key="message.id"
          class="ai-message"
          :class="message.role"
        >
          <p>{{ message.text }}</p>
        </div>
      </div>
      
      <div class="ai-input">
        <input 
          v-model="currentMessage"
          @keyup.enter="sendMessage"
          placeholder="请输入您的问题..."
          class="ai-input-field"
        />
        <button @click="sendMessage" class="ai-send-btn">发送</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useAppStore } from '@/stores/appStore';

const appStore = useAppStore();
const currentMessage = ref('');
const messagesContainer = ref(null);

const sendMessage = async () => {
  if (!currentMessage.value.trim()) return;

  // Add user message
  const userMessage = {
    id: Date.now(),
    role: 'user',
    text: currentMessage.value
  };
  appStore.addMessage(userMessage);

  const messageText = currentMessage.value;
  currentMessage.value = '';

  // Scroll to bottom
  await nextTick();
  scrollToBottom();

  // Simulate AI response (replace with actual AI integration)
  setTimeout(() => {
    const aiResponse = {
      id: Date.now() + 1,
      role: 'ai',
      text: generateAIResponse(messageText)
    };
    appStore.addMessage(aiResponse);
    
    nextTick(() => {
      scrollToBottom();
    });
  }, 1000);
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const generateAIResponse = (userMessage) => {
  // Simple response logic - replace with actual AI integration
  const responses = [
    '感谢您的问题！GitHub Copilot 学生包提供免费的 AI 编程助手服务。',
    '您可以通过学生邮箱申请 GitHub 学生包，其中包含 Copilot 的免费使用权限。',
    '如果您需要更多帮助，请访问 GitHub Education 官网了解详细信息。',
    '我很乐意为您解答关于 GitHub Copilot 的任何问题！'
  ];
  
  return responses[Math.floor(Math.random() * responses.length)];
};
</script>

<style scoped>
.ai-assistant {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.ai-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(59, 130, 246, 0.6);
}

.ai-button.active {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.ai-chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 450px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-header {
  padding: 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  text-align: center;
}

.ai-header h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
  font-weight: 600;
}

.ai-header p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.ai-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ai-message {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.4;
}

.ai-message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.ai-message.ai {
  align-self: flex-start;
  background: #f1f5f9;
  color: #334155;
}

.ai-message p {
  margin: 0;
}

.ai-input {
  display: flex;
  padding: 20px;
  gap: 10px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.ai-input-field {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}

.ai-input-field:focus {
  border-color: #3b82f6;
}

.ai-send-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.ai-send-btn:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .ai-chat-window {
    width: 300px;
    height: 400px;
    right: -10px;
  }
  
  .ai-assistant {
    bottom: 15px;
    right: 15px;
  }
}
</style>
