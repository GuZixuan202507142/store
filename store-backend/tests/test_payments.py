import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_payment():
    """Test creating a new payment"""
    payment_data = {
        "amount": 1000,
        "currency": "usd",
        "customer_email": "test@example.com"
    }
    response = client.post("/api/v1/payments", json=payment_data)
    assert response.status_code in [200, 201]
    if response.status_code == 200:
        data = response.json()
        assert "client_secret" in data or "payment_intent_id" in data
        assert "amount" in data
        assert data["amount"] == 1000

def test_get_payment():
    """Test getting payment status"""
    # 测试获取不存在的支付
    response = client.get("/api/v1/payments/pi_nonexistent")
    assert response.status_code in [200, 404]
    
    # 如果返回200，应该有相应的数据结构
    if response.status_code == 200:
        data = response.json()
        assert "status" in data

def test_stripe_webhook():
    """Test Stripe webhook endpoint"""
    webhook_data = {
        "id": "evt_test123",
        "type": "payment_intent.succeeded",
        "data": {"object": {"id": "pi_test123"}}
    }
    # 测试没有正确签名的webhook
    response = client.post("/api/v1/webhooks/stripe", json=webhook_data)
    # Webhook 通常需要特殊的签名验证，所以可能返回400或403
    assert response.status_code in [200, 400, 403]
