const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Request timeout configuration
const REQUEST_TIMEOUT = 30000; // 30 seconds

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add timeout to request
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

  try {
    const response = await fetch(url, { 
      ...options, 
      headers,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { detail: `HTTP ${response.status}: ${response.statusText}` };
      }
      throw new Error(errorData.detail || 'An API error occurred');
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }
    throw error;
  }
}

export async function createCheckoutSession(email) {
  const priceId = import.meta.env.VITE_STRIPE_PRICE_ID;
  
  if (!priceId) {
    throw new Error('Stripe Price ID not configured');
  }
  
  if (!email || !email.includes('@')) {
    throw new Error('Valid email address is required');
  }
  
  return request('/payments/create-checkout-session', {
    method: 'POST',
    body: JSON.stringify({ email, price_id: priceId }),
  });
}

// Placeholder for Gemini API call if proxied through backend
export async function askGemini(prompt, history) {
  // This would be implemented if the backend proxies Gemini calls
  // For now, the AI Logic SDK will handle this on the client
  console.log("Sending to Gemini:", prompt, history);
  // Example:
  // return request('/ai/chat', {
  //   method: 'POST',
  //   body: JSON.stringify({ prompt, history }),
  // });
}
