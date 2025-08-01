<template>
  <div id="app">
    <Navbar @navigate="handleNavigation" />
    <main>
      <HeroSection v-if="currentPage === 'home'" />
      <OrdersPage v-if="currentPage === 'orders'" />
    </main>
    <AppFooter />
    <AiAssistant />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import HeroSection from './components/HeroSection.vue'
import OrdersPage from './components/OrdersPage.vue'
import AppFooter from './components/AppFooter.vue'
import AiAssistant from './components/AiAssistant.vue'

const currentPage = ref('home')

const handleNavigation = (page) => {
  currentPage.value = page
}
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
