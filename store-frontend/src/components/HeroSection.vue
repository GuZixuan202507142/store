<template>
  <div class="w-full max-w-2xl mx-auto bg-gray-800/50 backdrop-blur-xl border border-gray-700/50 rounded-2xl shadow-2xl overflow-hidden">
    <div class="p-6 sm:p-8 min-h-[450px]">
      <div class="text-center">
        <h3 class="text-xl font-bold text-white">🤖 AI智能客服助手</h3>
        <p class="mt-2 text-sm text-gray-400">我是您的专属AI助手，随时为您解答关于GitHub Copilot学生包的任何疑问。</p>
      </div>
      <div v-if="aiMessage || aiError" class="mt-6 p-4 rounded-lg text-sm" :class="aiError ? 'bg-red-500/10 text-red-300 border border-red-500/20' : 'bg-blue-500/10 text-gray-300 border border-blue-500/20'">
        <p v-if="aiMessage" class="whitespace-pre-wrap leading-relaxed">{{ aiMessage }}</p>
        <p v-if="aiError">{{ aiError }}</p>
      </div>
      <div class="mt-6">
        <input v-model="userInput" @keyup.enter="askAi" class="flex-grow w-full px-4 py-3 bg-gray-900/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors" placeholder="请输入您的问题...">
        <button @click="askAi" :disabled="aiLoading" class="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800/50 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-blue-500 mt-4">
          <svg v-if="aiLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ aiLoading ? '思考中...' : '发送' }}</span>
        </button>
      </div>
      <div class="mt-6">
        <a href="https://buy.stripe.com/test_eVq5kD9E71Fo010bGC0Ba00" target="_blank" class="w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-green-500">
          立即购买
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../services/api';

const aiLoading = ref(false);
const aiMessage = ref('');
const aiError = ref('');
const userInput = ref('');

const askAi = async () => {
  if (!userInput.value) return;

  aiLoading.value = true;
  aiError.value = '';
  aiMessage.value = '';

  try {
    const response = await api.post('/ai/chat', { prompt: userInput.value });
    aiMessage.value = response.message;
  } catch (err) {
    aiError.value = err.message || '与AI助手通信时发生错误。';
  } finally {
    aiLoading.value = false;
    userInput.value = '';
  }
};
</script>
