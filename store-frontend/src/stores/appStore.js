import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    // Cart state
    cart: [],
    cartTotal: 0,
    
    // User state
    user: null,
    isAuthenticated: false,
    
    // UI state
    loading: false,
    notification: null,
    
    // AI Assistant state
    aiMessages: [
      {
        id: 1,
        text: 'Hello! I\'m here to help you with your shopping experience.',
        type: 'assistant',
        timestamp: new Date()
      }
    ],
    
    // Products state
    products: [],
    featuredProducts: [],
    
    // Order state
    currentOrder: null,
    orderHistory: []
  }),

  getters: {
    cartItemsCount: (state) => {
      return state.cart.reduce((total, item) => total + item.quantity, 0)
    },
    
    cartSubtotal: (state) => {
      return state.cart.reduce((total, item) => total + (item.price * item.quantity), 0)
    },
    
    isCartEmpty: (state) => {
      return state.cart.length === 0
    }
  },

  actions: {
    // Cart actions
    addToCart(product) {
      const existingItem = this.cart.find(item => item.id === product.id)
      
      if (existingItem) {
        existingItem.quantity += 1
      } else {
        this.cart.push({
          ...product,
          quantity: 1
        })
      }
      
      this.updateCartTotal()
      this.showNotification('Product added to cart!', 'success')
    },

    removeFromCart(productId) {
      const index = this.cart.findIndex(item => item.id === productId)
      if (index > -1) {
        this.cart.splice(index, 1)
        this.updateCartTotal()
        this.showNotification('Product removed from cart!', 'info')
      }
    },

    updateCartItemQuantity(productId, quantity) {
      const item = this.cart.find(item => item.id === productId)
      if (item) {
        if (quantity <= 0) {
          this.removeFromCart(productId)
        } else {
          item.quantity = quantity
          this.updateCartTotal()
        }
      }
    },

    clearCart() {
      this.cart = []
      this.updateCartTotal()
    },

    updateCartTotal() {
      this.cartTotal = this.cartSubtotal
    },

    // User actions
    setUser(user) {
      this.user = user
      this.isAuthenticated = true
    },

    logout() {
      this.user = null
      this.isAuthenticated = false
      this.clearCart()
    },

    // UI actions
    setLoading(loading) {
      this.loading = loading
    },

    showNotification(message, type = 'info', duration = 3000) {
      this.notification = {
        message,
        type,
        id: Date.now()
      }
      
      setTimeout(() => {
        this.notification = null
      }, duration)
    },

    // AI Assistant actions
    addAiMessage(message, type = 'user') {
      this.aiMessages.push({
        id: Date.now(),
        text: message,
        type,
        timestamp: new Date()
      })
    },

    // Products actions
    setProducts(products) {
      this.products = products
    },

    setFeaturedProducts(products) {
      this.featuredProducts = products
    },

    // Order actions
    setCurrentOrder(order) {
      this.currentOrder = order
    },

    addToOrderHistory(order) {
      this.orderHistory.unshift(order)
    },

    // Initialize store with mock data
    initializeStore() {
      // Mock featured products
      this.featuredProducts = [
        {
          id: '1',
          name: 'Premium Wireless Headphones',
          description: 'High-quality wireless headphones with noise cancellation',
          price: 299.99,
          originalPrice: 399.99,
          image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
          rating: 4.5,
          reviewCount: 128,
          inStock: true,
          isNew: false,
          isBestseller: true,
          discount: 25
        },
        {
          id: '2',
          name: 'Smart Watch Series X',
          description: 'Advanced fitness tracking and health monitoring',
          price: 399.99,
          image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
          rating: 4.8,
          reviewCount: 89,
          inStock: true,
          isNew: true,
          isBestseller: false,
          discount: null
        },
        {
          id: '3',
          name: 'Laptop Pro 15"',
          description: 'Professional laptop for creators and developers',
          price: 1299.99,
          originalPrice: 1499.99,
          image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400',
          rating: 4.7,
          reviewCount: 203,
          inStock: true,
          isNew: false,
          isBestseller: true,
          discount: 13
        }
      ]
    }
  }
})
