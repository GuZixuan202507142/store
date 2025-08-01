import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAppStore = defineStore('app', () => {
  // State
  const email = ref('');
  const isChatOpen = ref(false);

  // Actions
  function setEmail(newEmail) {
    email.value = newEmail;
  }

  function toggleChat() {
    isChatOpen.value = !isChatOpen.value;
  }

  return {
    email,
    isChatOpen,
    setEmail,
    toggleChat,
  };
});
