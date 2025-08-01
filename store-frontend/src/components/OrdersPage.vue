<template>
  <div class="orders-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">我的订单</h1>
      
      <!-- 邮箱输入 -->
      <div class="mb-6">
        <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
          请输入您的邮箱查看订单
        </label>
        <div class="flex gap-2">
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="example@email.com"
            class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            @keyup.enter="fetchOrders"
          />
          <button
            @click="fetchOrders"
            :disabled="!email || loading"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '查询中...' : '查询订单' }}
          </button>
        </div>
      </div>

      <!-- 错误消息 -->
      <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
        <p class="text-red-800">{{ error }}</p>
      </div>

      <!-- 订单列表 -->
      <div v-if="orders.length > 0" class="space-y-4">
        <div
          v-for="order in orders"
          :key="order.id"
          class="bg-white p-6 rounded-lg shadow-md border"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">
                订单 #{{ order.id }}
              </h3>
              <p class="text-sm text-gray-600">
                {{ formatDate(order.created_at) }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-lg font-bold text-gray-900">
                {{ formatAmount(order.amount, order.currency) }}
              </p>
              <span
                :class="getStatusClass(order.status)"
                class="inline-block px-2 py-1 rounded-full text-xs font-medium"
              >
                {{ getStatusText(order.status) }}
              </span>
            </div>
          </div>
          
          <div class="text-sm text-gray-600">
            <p><strong>客户邮箱:</strong> {{ order.customer_email }}</p>
            <p v-if="order.payment_intent_id">
              <strong>支付ID:</strong> {{ order.payment_intent_id }}
            </p>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div
        v-else-if="!loading && email && searchPerformed"
        class="text-center py-12"
      >
        <div class="text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2 2v-5m16 0h-2M4 13h2m13-8l-4 4-4-4m0 0l-4 4" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">暂无订单</h3>
          <p class="mt-1 text-sm text-gray-500">
            该邮箱下暂无订单记录
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAppStore } from '../stores/appStore'
import api from '../services/api'

const appStore = useAppStore()
const email = ref(appStore.email || '')
const orders = ref([])
const loading = ref(false)
const error = ref('')
const searchPerformed = ref(false)

// 获取订单列表
const fetchOrders = async () => {
  if (!email.value) {
    error.value = '请输入邮箱地址'
    return
  }

  loading.value = true
  error.value = ''
  searchPerformed.value = false

  try {
    const response = await api.get(`/orders/email/${email.value}`)
    orders.value = response.data
    searchPerformed.value = true
    
    // 保存邮箱到store
    appStore.setEmail(email.value)
  } catch (err) {
    error.value = err.response?.data?.detail || '获取订单失败，请稍后重试'
    orders.value = []
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知时间'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return '时间格式错误'
  }
}

// 格式化金额
const formatAmount = (amount, currency = 'usd') => {
  const currencyMap = {
    usd: '$',
    cny: '¥',
    eur: '€'
  }
  
  const symbol = currencyMap[currency?.toLowerCase()] || '$'
  const value = (amount / 100).toFixed(2) // 假设金额以分为单位存储
  
  return `${symbol}${value}`
}

// 获取状态样式
const getStatusClass = (status) => {
  const statusClasses = {
    pending: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    cancelled: 'bg-gray-100 text-gray-800'
  }
  
  return statusClasses[status] || 'bg-gray-100 text-gray-800'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusTexts = {
    pending: '待处理',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消'
  }
  
  return statusTexts[status] || '未知状态'
}

// 页面加载时如果store中有邮箱，自动查询
onMounted(() => {
  if (email.value) {
    fetchOrders()
  }
})
</script>

<style scoped>
.orders-page {
  min-height: calc(100vh - 200px);
}
</style>
