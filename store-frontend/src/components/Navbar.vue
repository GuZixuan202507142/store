<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-content">
        <!-- Logo -->
        <div class="nav-brand">
          <a href="/" class="brand-link">
            <span class="brand-icon">🛍️</span>
            <span class="brand-text">Store</span>
          </a>
        </div>
        
        <!-- Navigation Links -->
        <div class="nav-links" :class="{ 'nav-open': isMenuOpen }">
          <a href="#" class="nav-link" @click="navigate('home')">Home</a>
          <a href="#" class="nav-link" @click="navigate('orders')">我的订单</a>
          <a href="#products" class="nav-link" @click="closeMenu">Products</a>
          <a href="#about" class="nav-link" @click="closeMenu">About</a>
          <a href="#contact" class="nav-link" @click="closeMenu">Contact</a>
        </div>
        
        <!-- Action Buttons -->
        <div class="nav-actions">
          <button class="nav-action-btn search-btn" aria-label="Search">
            🔍
          </button>
          <button class="nav-action-btn cart-btn" aria-label="Shopping Cart">
            🛒
            <span v-if="cartItems > 0" class="cart-badge">{{ cartItems }}</span>
          </button>
          <button class="nav-action-btn user-btn" aria-label="User Account">
            👤
          </button>
        </div>
        
        <!-- Mobile Menu Toggle -->
        <button 
          class="mobile-menu-btn"
          @click="toggleMenu"
          aria-label="Toggle menu"
        >
          <span class="hamburger-line" :class="{ 'active': isMenuOpen }"></span>
          <span class="hamburger-line" :class="{ 'active': isMenuOpen }"></span>
          <span class="hamburger-line" :class="{ 'active': isMenuOpen }"></span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  emits: ['navigate'],
  data() {
    return {
      isMenuOpen: false,
      cartItems: 0 // This would come from store
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
    },
    closeMenu() {
      this.isMenuOpen = false
    },
    navigate(page) {
      this.$emit('navigate', page)
      this.closeMenu()
    }
  },
  mounted() {
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!this.$el.contains(e.target)) {
        this.isMenuOpen = false
      }
    })
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #1f2937;
  font-weight: 700;
  font-size: 1.5rem;
}

.brand-icon {
  margin-right: 0.5rem;
  font-size: 1.75rem;
}

.brand-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #374151;
  font-weight: 500;
  transition: color 0.2s ease;
  position: relative;
}

.nav-link:hover {
  color: #667eea;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-action-btn {
  position: relative;
  width: 44px;
  height: 44px;
  border: none;
  background: #f3f4f6;
  border-radius: 12px;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-action-btn:hover {
  background: #e5e7eb;
  transform: scale(1.05);
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ef4444;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.hamburger-line {
  width: 24px;
  height: 2px;
  background: #374151;
  margin: 2px 0;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.hamburger-line.active:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger-line.active:nth-child(2) {
  opacity: 0;
}

.hamburger-line.active:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

@media (max-width: 768px) {
  .nav-links {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-10px);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }
  
  .nav-links.nav-open {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }
  
  .nav-link {
    padding: 0.75rem 0;
    border-bottom: 1px solid #f3f4f6;
  }
  
  .nav-link:last-child {
    border-bottom: none;
  }
  
  .mobile-menu-btn {
    display: flex;
  }
  
  .nav-actions {
    gap: 0.5rem;
  }
  
  .nav-action-btn {
    width: 40px;
    height: 40px;
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .brand-text {
    display: none;
  }
  
  .nav-actions {
    gap: 0.25rem;
  }
  
  .nav-action-btn {
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }
}
</style>
