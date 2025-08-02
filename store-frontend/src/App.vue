<template>
  <div id="app">
    <main>
      <HeroSection />
    </main>
  </div>
</template>

<script setup>
import HeroSection from './components/HeroSection.vue'
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
