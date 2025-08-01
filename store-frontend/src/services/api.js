const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'An API error occurred');
  }

  return response.json();
}

export async function createCheckoutSession(email) {
  const priceId = "price_1RpqYvDq9KoUFEhjZVIMM90q"; // Using the provided Stripe Price ID
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
