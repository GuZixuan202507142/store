<template>
  <div class="home-view">
    <!-- Hero Section -->
    <HeroSection 
      @shop-now="scrollToProducts"
      @learn-more="scrollToAbout"
    />
    
    <!-- Featured Products Section -->
    <section id="products" class="products-section">
      <div class="container">
        <div class="section-header">
          <h2>Featured Products</h2>
          <p>Discover our handpicked selection of premium products</p>
        </div>
        
        <div class="products-grid">
          <ProductCard
            v-for="product in featuredProducts"
            :key="product.id"
            :product="product"
            @add-to-cart="handleAddToCart"
            @quick-view="handleQuickView"
            @toggle-wishlist="handleToggleWishlist"
          />
        </div>
        
        <div class="section-actions">
          <button class="btn btn-primary">View All Products</button>
        </div>
      </div>
    </section>
    
    <!-- About Section -->
    <section id="about" class="about-section">
      <div class="container">
        <div class="about-content">
          <div class="about-text">
            <h2>Why Choose Our Store?</h2>
            <p>
              We're committed to providing you with the best shopping experience possible. 
              Our AI-powered platform helps you find exactly what you're looking for, 
              while our secure payment system ensures your transactions are safe and fast.
            </p>
            <ul class="about-features">
              <li>🤖 AI-powered product recommendations</li>
              <li>🔒 Secure and fast checkout with Stripe</li>
              <li>📧 Real-time order notifications</li>
              <li>🚀 Fast worldwide shipping</li>
              <li>💬 24/7 AI customer support</li>
            </ul>
          </div>
          <div class="about-image">
            <img 
              src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600" 
              alt="Shopping experience"
            />
          </div>
        </div>
      </div>
    </section>
    
    <!-- Stats Section -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">10K+</div>
            <div class="stat-label">Happy Customers</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">50K+</div>
            <div class="stat-label">Products Sold</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">99.9%</div>
            <div class="stat-label">Uptime</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Support</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useAppStore } from '../stores/appStore'
import HeroSection from '../components/HeroSection.vue'
import ProductCard from '../components/ProductCard.vue'

export default {
  name: 'HomeView',
  components: {
    HeroSection,
    ProductCard
  },
  computed: {
    ...mapState(useAppStore, ['featuredProducts'])
  },
  methods: {
    ...mapActions(useAppStore, ['addToCart', 'showNotification', 'initializeStore']),
    
    scrollToProducts() {
      document.getElementById('products')?.scrollIntoView({ 
        behavior: 'smooth' 
      })
    },
    
    scrollToAbout() {
      document.getElementById('about')?.scrollIntoView({ 
        behavior: 'smooth' 
      })
    },
    
    handleAddToCart(product) {
      this.addToCart(product)
    },
    
    handleQuickView(product) {
      // Handle quick view modal
      console.log('Quick view:', product)
    },
    
    handleToggleWishlist({ product, isInWishlist }) {
      const message = isInWishlist 
        ? `${product.name} added to wishlist!`
        : `${product.name} removed from wishlist!`
      this.showNotification(message, 'info')
    }
  },
  
  mounted() {
    this.initializeStore()
  }
}
</script>

<style scoped>
.home-view {
  padding-top: 80px; /* Account for fixed navbar */
}

.products-section {
  padding: 4rem 0;
  background: #f8fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-header p {
  font-size: 1.1rem;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.section-actions {
  text-align: center;
}

.about-section {
  padding: 4rem 0;
  background: white;
}

.about-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.about-text h2 {
  font-size: 2.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.about-text p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #4b5563;
  margin-bottom: 2rem;
}

.about-features {
  list-style: none;
}

.about-features li {
  font-size: 1rem;
  color: #374151;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.about-image img {
  width: 100%;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.stats-section {
  padding: 3rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .section-header h2 {
    font-size: 2rem;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .about-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }
  
  .about-text h2 {
    font-size: 1.75rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stat-number {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .products-section,
  .about-section {
    padding: 2rem 0;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
