<template>
  <div id="app">
    <Navbar />
    <main>
      <HomeView />
    </main>
    <AppFooter />
    <AiAssistant />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import AppFooter from './components/AppFooter.vue'
import AiAssistant from './components/AiAssistant.vue'
import HomeView from './views/HomeView.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    AppFooter,
    AiAssistant,
    HomeView
  }
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
