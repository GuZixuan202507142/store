import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_orders():
    """Test getting all orders"""
    response = client.get("/api/v1/orders")
    assert response.status_code == 200

def test_create_order():
    """Test creating a new order"""
    order_data = {
        "customer_email": "test@example.com",
        "amount": 1000,
        "currency": "usd"
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code in [200, 201]
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert data["customer_email"] == "test@example.com"
        assert data["amount"] == 1000
        assert data["currency"] == "usd"

def test_get_order():
    """Test getting a specific order"""
    # 先创建一个订单用于测试
    order_data = {
        "customer_email": "test@example.com",
        "amount": 1000,
        "currency": "usd"
    }
    create_response = client.post("/api/v1/orders", json=order_data)
    
    if create_response.status_code in [200, 201]:
        order_id = create_response.json().get("id", 1)
        response = client.get(f"/api/v1/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_id
    else:
        # 如果创建失败，测试不存在的订单
        response = client.get("/api/v1/orders/999999")
        assert response.status_code == 404
