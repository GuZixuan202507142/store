<template>
  <div class="ai-assistant">
    <button class="ai-toggle" @click="appStore.toggleChat">
      <span v-if="!appStore.isChatOpen">AI 助手</span>
      <span v-else>✕</span>
    </button>
    
    <div class="ai-chat" :class="{ active: appStore.isChatOpen }">
      <div class="chat-header">AI 助手</div>
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="msg in messages" :key="msg.id" class="message" :class="msg.role === 'user' ? 'user-message' : 'ai-message'">
          {{ msg.text }}
        </div>
        <div v-if="isTyping" class="message ai-message typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
      <div class="chat-input-container">
        <input 
          type="text" 
          class="chat-input" 
          placeholder="输入您的问题..." 
          v-model="userInput"
          @keypress.enter="sendMessage"
          :disabled="isTyping"
        >
        <button class="send-button" @click="sendMessage" :disabled="isTyping">发送</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { useAppStore } from '@/stores/appStore';
import { geminiModel, saveMessage, getChatHistory } from '@/services/firebase';
import { v4 as uuidv4 } from 'uuid';

const appStore = useAppStore();
const userInput = ref('');
const messages = ref([]);
const isTyping = ref(false);
const messagesContainer = ref(null);
const sessionId = ref(null);

onMounted(() => {
  let storedSessionId = localStorage.getItem('chatSessionId');
  if (!storedSessionId) {
    storedSessionId = uuidv4();
    localStorage.setItem('chatSessionId', storedSessionId);
  }
  sessionId.value = storedSessionId;

  getChatHistory(sessionId.value, (history) => {
    messages.value = history;
    scrollToBottom();
  });
});

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

watch(messages, scrollToBottom, { deep: true });

const sendMessage = async () => {
  const text = userInput.value.trim();
  if (!text || isTyping.value) return;

  const userMessage = { role: 'user', text, timestamp: new Date() };
  await saveMessage(sessionId.value, userMessage);
  userInput.value = '';
  isTyping.value = true;

  try {
    const chat = geminiModel.startChat({
        history: messages.value.map(m => ({
            role: m.role,
            parts: [{ text: m.text }]
        })),
    });
    const result = await chat.sendMessage(text);
    const response = await result.response;
    const aiText = response.text();

    const aiMessage = { role: 'model', text: aiText, timestamp: new Date() };
    await saveMessage(sessionId.value, aiMessage);

  } catch (error) {
    console.error("Gemini API error:", error);
    const errorMessage = { role: 'model', text: '抱歉，我暂时无法回答。请稍后再试。', timestamp: new Date() };
    await saveMessage(sessionId.value, errorMessage);
  } finally {
    isTyping.value = false;
  }
};
</script>

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

.ai-toggle {
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

.ai-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(59, 130, 246, 0.6);
}

.ai-chat {
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
  display: none;
  flex-direction: column;
  overflow: hidden;
}

.ai-chat.active {
  display: flex;
}

.chat-header {
  padding: 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.4;
}

.user-message {
  align-self: flex-end;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.ai-message {
  align-self: flex-start;
  background: #f1f5f9;
  color: #334155;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #9e9ea3;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.3s infinite ease-in-out;
}

.typing-indicator span:nth-of-type(2) { 
  animation-delay: -1.1s; 
}

.typing-indicator span:nth-of-type(3) { 
  animation-delay: -0.9s; 
}

@keyframes bounce {
  0%, 80%, 100% { 
    transform: scale(0); 
  }
  40% { 
    transform: scale(1.0); 
  }
}

.chat-input-container {
  display: flex;
  padding: 20px;
  gap: 10px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.chat-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}

.chat-input:focus {
  border-color: #3b82f6;
}

.send-button {
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

.send-button:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-1px);
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .ai-chat {
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
