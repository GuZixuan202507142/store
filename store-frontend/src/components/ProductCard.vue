<template>
  <div class="product-card">
    <div class="product-image">
      <img :src="product.image" :alt="product.name" loading="lazy" />
      <div class="product-overlay">
        <button class="quick-view-btn" @click="$emit('quick-view', product)">
          👁️ Quick View
        </button>
      </div>
    </div>
    
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-description">{{ product.description }}</p>
      
      <div class="product-rating" v-if="product.rating">
        <div class="stars">
          <span v-for="star in 5" :key="star" class="star" :class="{ 'filled': star <= product.rating }">
            ⭐
          </span>
        </div>
        <span class="rating-text">({{ product.reviewCount || 0 }} reviews)</span>
      </div>
      
      <div class="product-price">
        <span v-if="product.originalPrice" class="original-price">${{ product.originalPrice }}</span>
        <span class="current-price">${{ product.price }}</span>
        <span v-if="product.discount" class="discount">-{{ product.discount }}%</span>
      </div>
      
      <div class="product-actions">
        <button 
          class="btn btn-primary add-to-cart-btn"
          @click="handleAddToCart"
          :disabled="!product.inStock"
        >
          <span v-if="product.inStock">🛒 Add to Cart</span>
          <span v-else">Out of Stock</span>
        </button>
        
        <button 
          class="btn btn-secondary wishlist-btn"
          @click="handleWishlist"
          :class="{ 'in-wishlist': isInWishlist }"
        >
          {{ isInWishlist ? '❤️' : '🤍' }}
        </button>
      </div>
      
      <div class="product-badges">
        <span v-if="product.isNew" class="badge new-badge">New</span>
        <span v-if="product.isBestseller" class="badge bestseller-badge">Bestseller</span>
        <span v-if="product.discount" class="badge sale-badge">Sale</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true,
      default: () => ({
        id: '',
        name: '',
        description: '',
        price: 0,
        originalPrice: null,
        image: '',
        rating: 0,
        reviewCount: 0,
        inStock: true,
        isNew: false,
        isBestseller: false,
        discount: null
      })
    }
  },
  data() {
    return {
      isInWishlist: false
    }
  },
  methods: {
    handleAddToCart() {
      if (this.product.inStock) {
        this.$emit('add-to-cart', this.product)
      }
    },
    handleWishlist() {
      this.isInWishlist = !this.isInWishlist
      this.$emit('toggle-wishlist', {
        product: this.product,
        isInWishlist: this.isInWishlist
      })
    }
  }
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.product-image {
  position: relative;
  overflow: hidden;
  aspect-ratio: 4/3;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .product-overlay {
  opacity: 1;
}

.quick-view-btn {
  background: white;
  color: #374151;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-view-btn:hover {
  background: #f3f4f6;
  transform: scale(1.05);
}

.product-info {
  padding: 1.5rem;
}

.product-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.product-description {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stars {
  display: flex;
  gap: 0.1rem;
}

.star {
  font-size: 0.9rem;
  opacity: 0.3;
  transition: opacity 0.2s ease;
}

.star.filled {
  opacity: 1;
}

.rating-text {
  font-size: 0.8rem;
  color: #6b7280;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.original-price {
  color: #9ca3af;
  text-decoration: line-through;
  font-size: 0.9rem;
}

.current-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.discount {
  background: #ef4444;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.product-actions {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.add-to-cart-btn {
  flex: 1;
  padding: 0.75rem;
  font-weight: 600;
}

.add-to-cart-btn:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

.wishlist-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  padding: 0;
}

.wishlist-btn.in-wishlist {
  background: #fee2e2;
  color: #dc2626;
}

.product-badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.new-badge {
  background: #10b981;
  color: white;
}

.bestseller-badge {
  background: #f59e0b;
  color: white;
}

.sale-badge {
  background: #ef4444;
  color: white;
}

@media (max-width: 480px) {
  .product-info {
    padding: 1rem;
  }
  
  .product-name {
    font-size: 1.1rem;
  }
  
  .current-price {
    font-size: 1.25rem;
  }
  
  .product-actions {
    flex-direction: column;
  }
  
  .wishlist-btn {
    width: 100%;
    height: auto;
    padding: 0.75rem;
  }
}
</style>
