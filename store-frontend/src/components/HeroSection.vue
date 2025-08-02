<template>
  <!-- 主容器，采用现代化的玻璃拟态和阴影效果 -->
  <div class="w-full max-w-2xl mx-auto bg-gray-800/50 backdrop-blur-xl border border-gray-700/50 rounded-2xl shadow-2xl overflow-hidden">
    <!-- 标签页导航 -->
    <div class="flex border-b border-gray-700/50">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="[
          'flex-1 py-4 px-2 text-center text-sm font-medium transition-colors duration-300 focus:outline-none',
          activeTab === tab.id
            ? 'text-white bg-gray-700/60 border-b-2 border-blue-500'
            : 'text-gray-400 hover:bg-gray-700/30 hover:text-gray-200'
        ]"
      >
        <span class="flex items-center justify-center gap-2">
          <component :is="tab.icon" class="w-5 h-5" />
          {{ tab.name }}
        </span>
      </button>
    </div>

    <!-- 标签页内容区域 -->
    <div class="p-6 sm:p-8 min-h-[450px]">
      <!-- AI智能客服 面板 -->
      <div v-if="activeTab === 'ai-assistant'">
        <div class="text-center">
          <h3 class="text-xl font-bold text-white">🤖 AI智能客服助手</h3>
          <p class="mt-2 text-sm text-gray-400">我是您的专属AI助手，随时为您解答关于GitHub Copilot学生包的任何疑问。</p>
        </div>
        
        <!-- AI消息展示区域 -->
        <div v-if="aiMessage || aiError" class="mt-6 p-4 rounded-lg text-sm" :class="aiError ? 'bg-red-500/10 text-red-300 border border-red-500/20' : 'bg-blue-500/10 text-gray-300 border border-blue-500/20'">
          <p v-if="aiMessage" class="whitespace-pre-wrap leading-relaxed">{{ aiMessage }}</p>
          <p v-if="aiError">{{ aiError }}</p>
        </div>

        <!-- 触发按钮 -->
        <div class="mt-6">
          <button
            @click="getAiWelcome"
            :disabled="aiLoading"
            class="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800/50 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-blue-500"
          >
            <svg v-if="aiLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ aiLoading ? '思考中...' : '开始咨询' }}</span>
          </button>
        </div>
      </div>

      <!-- 订单查询 面板 -->
      <div v-if="activeTab === 'order-query'">
        <div class="text-center">
          <h3 class="text-xl font-bold text-white">📋 查询我的订单</h3>
          <p class="mt-2 text-sm text-gray-400">输入您购买时使用的邮箱地址，即可查看订单状态。</p>
        </div>
        
        <!-- 查询表单 -->
        <div class="mt-6 flex flex-col sm:flex-row gap-3">
          <input 
            v-model="queryEmail"
            type="email" 
            class="flex-grow w-full px-4 py-3 bg-gray-900/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors" 
            placeholder="请输入购买时使用的邮箱"
            @keyup.enter="queryOrders"
          >
          <button 
            @click="queryOrders"
            :disabled="queryLoading || !queryEmail"
            class="flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-800/50 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-purple-500"
          >
            <svg v-if="queryLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ queryLoading ? '查询中...' : '查询订单' }}</span>
          </button>
        </div>

        <!-- 查询结果 -->
        <div class="mt-6">
          <div v-if="queryError" class="p-4 rounded-lg text-sm bg-red-500/10 text-red-300 border border-red-500/20">
            <p>{{ queryError }}</p>
          </div>
          <div v-if="orderResult">
            <p v-if="orderResult.length === 0" class="text-center text-gray-400 py-4">暂无与此邮箱关联的订单记录。</p>
            <div v-else class="space-y-3">
              <div v-for="order in orderResult" :key="order.id" class="bg-gray-900/60 p-4 rounded-lg border border-gray-700/50">
                <div class="flex justify-between items-start">
                  <div>
                    <p class="text-xs text-gray-400">订单号</p>
                    <p class="font-mono text-white">#{{ order.id }}</p>
                  </div>
                  <span :class="getStatusClass(order.status)" class="text-xs font-bold px-2.5 py-1 rounded-full">
                    {{ getStatusText(order.status) }}
                  </span>
                </div>
                <div class="mt-4 grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p class="text-gray-400">金额</p>
                    <p class="text-white font-semibold">¥{{ (order.amount_total / 100).toFixed(2) }}</p>
                  </div>
                  <div>
                    <p class="text-gray-400">时间</p>
                    <p class="text-white">{{ formatDate(order.created_at) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, defineAsyncComponent } from 'vue';

// --- 图标定义 ---
// 使用 shallowRef 和 defineAsyncComponent 优化图标加载
const SparklesIcon = shallowRef(defineAsyncComponent(() => import('@heroicons/vue/24/outline/SparklesIcon.js')));
const MagnifyingGlassIcon = shallowRef(defineAsyncComponent(() => import('@heroicons/vue/24/outline/MagnifyingGlassIcon.js')));


// --- 核心逻辑：组合式函数 (Composable) ---
// 在真实项目中，下面的函数应该被拆分到独立的 'composables/useAiService.js' 和 'composables/useOrderService.js' 文件中
// 这使得逻辑可以被复用、测试和轻松维护

/**
 * @description AI客服相关逻辑的组合式函数
 */
function useAiService() {
  const aiLoading = ref(false);
  const aiMessage = ref('');
  const aiError = ref('');

  // 🔴 安全警告: API密钥绝不应该暴露在前端代码中。
  // 正确的做法是:
  // 1. 在后端服务器上创建一个API端点 (例如: /api/ai-welcome)。
  // 2. 从前端调用您自己的后端端点。
  // 3. 在后端服务器上，安全地存储和使用API密钥来调用Google Gemini API。
  // 4. 将结果返回给前端。
  // const API_KEY = "已移除，请通过后端代理调用";

  const getAiWelcome = async () => {
    // 模拟后端调用，因为前端不应包含API密钥
    aiLoading.value = true;
    aiError.value = '';
    aiMessage.value = '';

    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 1500));

    // 模拟成功响应
    aiMessage.value = `您好！欢迎来到GitHub Copilot学生包销售平台。我是您的AI助手，可以为您解答关于产品功能、购买流程、学生包权益等任何问题。今天有什么可以帮您？`;
    
    // 模拟失败情况 (可以取消下面一行的注释来测试错误状态)
    // aiError.value = "抱歉，AI助手当前无法连接，请稍后再试。";
    
    aiLoading.value = false;
  };

  return { aiLoading, aiMessage, aiError, getAiWelcome };
}


/**
 * @description 订单查询相关逻辑的组合式函数
 */
function useOrderService() {
  const queryEmail = ref('');
  const queryLoading = ref(false);
  const orderResult = ref(null);
  const queryError = ref('');

  const queryOrders = async () => {
    if (!queryEmail.value) {
      queryError.value = '请输入邮箱地址';
      return;
    }
    if (!/^\S+@\S+\.\S+$/.test(queryEmail.value)) {
      queryError.value = '请输入有效的邮箱地址';
      return;
    }

    queryLoading.value = true;
    queryError.value = '';
    orderResult.value = null;
    
    try {
      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 1000));

      // 🔴 注意: 这里的API地址是本地开发地址。在生产环境中，您需要替换为您的线上API地址。
      // const response = await fetch(`https://your-api.com/api/v1/orders/email/${queryEmail.value}`);
      // if (!response.ok) throw new Error('查询失败，请检查邮箱地址或稍后再试');
      // const orders = await response.json();
      // orderResult.value = orders;

      // 使用模拟数据进行演示
      if (queryEmail.value === 'test@example.com') {
        orderResult.value = [
          { id: 'cs_12345', status: 'completed', amount_total: 5000, created_at: new Date().toISOString() },
          { id: 'cs_67890', status: 'pending', amount_total: 5000, created_at: new Date(Date.now() - 86400000).toISOString() }
        ];
      } else {
        orderResult.value = [];
      }

    } catch (err) {
      console.error('查询订单时出错:', err);
      queryError.value = err.message || '查询时发生未知错误。';
    } finally {
      queryLoading.value = false;
    }
  };

  return { queryEmail, queryLoading, orderResult, queryError, queryOrders };
}


// --- 组件设置 ---
const activeTab = ref('ai-assistant');
const tabs = [
  { id: 'ai-assistant', name: 'AI 智能客服', icon: SparklesIcon },
  { id: 'order-query', name: '查询我的订单', icon: MagnifyingGlassIcon },
];

// 实例化组合式函数
const { aiLoading, aiMessage, aiError, getAiWelcome } = useAiService();
const { queryEmail, queryLoading, orderResult, queryError, queryOrders } = useOrderService();


// --- 辅助函数 ---
const getStatusClass = (status) => {
  const classes = {
    completed: 'bg-green-500/20 text-green-400',
    pending: 'bg-yellow-500/20 text-yellow-400',
    failed: 'bg-red-500/20 text-red-400',
  };
  return classes[status] || 'bg-gray-500/20 text-gray-400';
};

const getStatusText = (status) => {
  const texts = {
    completed: '已完成',
    pending: '处理中',
    failed: '失败',
  };
  return texts[status] || '未知';
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>

<style scoped>
/* 此组件的所有样式均由Tailwind CSS类提供。
  为了使用此组件，请确保您的项目已正确配置Tailwind CSS。
  同时，您需要安装 @heroicons/vue 库来显示图标：
  npm install @heroicons/vue
*/
</style>
