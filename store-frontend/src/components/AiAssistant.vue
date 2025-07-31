<template>
  <div class="ai-assistant">
    <button 
      @click="toggleChat" 
      class="ai-button"
      :class="{ 'active': isOpen }"
    >
      <span v-if="!isOpen">💬</span>
      <span v-else">✕</span>
    </button>
    
    <div v-if="isOpen" class="ai-chat-window">
      <div class="ai-header">
        <h3>AI Assistant</h3>
        <p>How can I help you today?</p>
      </div>
      
      <div class="ai-messages" ref="messagesContainer">
        <div 
          v-for="message in messages" 
          :key="message.id"
          class="ai-message"
          :class="message.type"
        >
          <p>{{ message.text }}</p>
        </div>
      </div>
      
      <div class="ai-input">
        <input 
          v-model="currentMessage"
          @keyup.enter="sendMessage"
          placeholder="Type your message..."
          class="ai-input-field"
        />
        <button @click="sendMessage" class="ai-send-btn">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AiAssistant',
  data() {
    return {
      isOpen: false,
      currentMessage: '',
      messages: [
        {
          id: 1,
          text: 'Hello! I\'m here to help you with your shopping experience.',
          type: 'assistant'
        }
      ]
    }
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen
    },
    sendMessage() {
      if (!this.currentMessage.trim()) return
      
      // Add user message
      this.messages.push({
        id: Date.now(),
        text: this.currentMessage,
        type: 'user'
      })
      
      const userMessage = this.currentMessage
      this.currentMessage = ''
      
      // Simulate AI response
      setTimeout(() => {
        this.messages.push({
          id: Date.now(),
          text: this.generateResponse(userMessage),
          type: 'assistant'
        })
        this.scrollToBottom()
      }, 1000)
      
      this.scrollToBottom()
    },
    generateResponse(message) {
      // Simple response logic - in production, this would call the Gemini API
      const responses = [
        'That\'s a great question! Let me help you with that.',
        'I understand what you\'re looking for. Here\'s what I recommend...',
        'Based on your query, I can suggest the following options.',
        'Let me provide you with more information about that.'
      ]
      return responses[Math.floor(Math.random() * responses.length)]
    },
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.messagesContainer) {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight
        }
      })
    }
  }
}
</script>

<style scoped>
.ai-assistant {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
}

.ai-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.ai-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.ai-chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  text-align: center;
}

.ai-header h3 {
  margin-bottom: 0.25rem;
  font-size: 1.1rem;
}

.ai-header p {
  font-size: 0.9rem;
  opacity: 0.9;
}

.ai-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background: #f8fafc;
}

.ai-message {
  margin-bottom: 1rem;
  max-width: 80%;
}

.ai-message.user {
  margin-left: auto;
}

.ai-message.user p {
  background: #667eea;
  color: white;
  padding: 0.75rem;
  border-radius: 12px 12px 4px 12px;
}

.ai-message.assistant p {
  background: white;
  color: #374151;
  padding: 0.75rem;
  border-radius: 12px 12px 12px 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ai-input {
  display: flex;
  padding: 1rem;
  background: white;
  border-top: 1px solid #e5e7eb;
}

.ai-input-field {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  margin-right: 0.5rem;
  outline: none;
}

.ai-input-field:focus {
  border-color: #667eea;
}

.ai-send-btn {
  padding: 0.75rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.ai-send-btn:hover {
  background: #5a67d8;
}
</style>
