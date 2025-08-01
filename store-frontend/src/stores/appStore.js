import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAppStore = defineStore('app', () => {
  // State
  const email = ref('');
  const isChatOpen = ref(false);
  const chatMessages = ref([
    {
      id: 1,
      role: 'ai',
      text: '您好！我是您的专属助手，有什么可以帮助您的吗？'
    }
  ]);

  // Actions
  function setEmail(newEmail) {
    email.value = newEmail;
  }

  function toggleChat() {
    isChatOpen.value = !isChatOpen.value;
  }

  function addMessage(message) {
    chatMessages.value.push(message);
  }

  return {
    email,
    isChatOpen,
    chatMessages,
    setEmail,
    toggleChat,
    addMessage,
  };
});
