<template>
  <section class="hero-section">
    <div class="hero-background">
      <div class="hero-overlay"></div>
    </div>
    
    <div class="container">
      <div class="hero-content">
        <h1 class="hero-title">
          Welcome to the Future of Shopping
        </h1>
        <p class="hero-subtitle">
          Discover amazing products with AI-powered recommendations and seamless checkout experience
        </p>
        <div class="hero-actions">
          <button @click="handleShopNow" class="btn btn-primary hero-btn">
            Shop Now
          </button>
          <button @click="handleLearnMore" class="btn btn-secondary hero-btn">
            Learn More
          </button>
        </div>
      </div>
      
      <div class="hero-features">
        <div class="feature">
          <div class="feature-icon">🤖</div>
          <h3>AI Assistant</h3>
          <p>Get personalized recommendations with our smart AI</p>
        </div>
        <div class="feature">
          <div class="feature-icon">💳</div>
          <h3>Secure Payment</h3>
          <p>Safe and secure transactions with Stripe</p>
        </div>
        <div class="feature">
          <div class="feature-icon">⚡</div>
          <h3>Fast Delivery</h3>
          <p>Quick and reliable shipping worldwide</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroSection',
  methods: {
    handleShopNow() {
      // Scroll to products section or handle shop action
      this.$emit('shop-now')
    },
    handleLearnMore() {
      // Show more information or scroll to about section
      this.$emit('learn-more')
    }
  }
}
</script>

<style scoped>
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: -2;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.1);
  z-index: -1;
}

.hero-content {
  text-align: center;
  color: white;
  margin-bottom: 4rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  background: linear-gradient(45deg, #ffffff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}

.hero-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.hero-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  color: white;
  transition: all 0.3s ease;
}

.feature:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.feature p {
  opacity: 0.9;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-btn {
    width: 100%;
    max-width: 280px;
  }
  
  .hero-features {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .feature {
    padding: 1.5rem;
  }
}
</style>
