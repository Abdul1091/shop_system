import pytest

def test_create_product_success(client, auth_headers):
    # 1. Register Owner
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin@test.com", "password": "password", "role": "owner"
    })
    headers = auth_headers(user_id=1, role="owner")

    # 2. Create Product
    product_data = {
        "name": "Indomie",
        "sku": "IND-001",
        "category": "Noodles",
        "purchase_price": 100,
        "selling_price": 150,
        "supplier": "Indofood",
        "initial_quantity": 100
    }
    response = client.post("/products/", json=product_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Indomie"
    assert data["sku"] == "IND-001"

def test_duplicate_sku_fails(client, auth_headers):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin@test.com", "password": "password", "role": "owner"
    })
    headers = auth_headers(user_id=1, role="owner")

    product_data = {
        "name": "Item 1", "sku": "SAME", "purchase_price": 10, 
        "selling_price": 20, "initial_quantity": 5
    }
    
    # First creation
    client.post("/products/", json=product_data, headers=headers)
    
    # Second creation with same SKU
    response = client.post("/products/", json=product_data, headers=headers)
    
    assert response.status_code == 400
    assert "SKU already exists" in response.json()["detail"]

def test_stock_report_initial_state(client, auth_headers):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin@test.com", "password": "password", "role": "owner"
    })
    headers = auth_headers(user_id=1, role="owner")

    # Create Product
    client.post("/products/", headers=headers, json={
        "name": "Milk", "sku": "MILK-01", "purchase_price": 500, 
        "selling_price": 700, "initial_quantity": 25
    })

    # Check Report
    response = client.get("/products/report", headers=headers)
    assert response.status_code == 200
    report = response.json()[0]
    
    assert report["product_name"] == "Milk"
    assert report["initial_stock"] == 25
    assert report["current_stock"] == 25
    assert report["quantity_sold"] == 0

def test_product_creation_requires_owner(client, auth_headers):
    # Register a cashier instead of an owner
    client.post("/auth/register", json={
        "name": "Cashier", "email": "cashier@test.com", "password": "password", "role": "cashier"
    })
    headers = auth_headers(user_id=1, role="cashier")

    product_data = {
        "name": "Illegal Item", "sku": "BAD", "purchase_price": 1, 
        "selling_price": 2, "initial_quantity": 1
    }
    
    response = client.post("/products/", json=product_data, headers=headers)
    
    # Should be Forbidden (403) based on your require_roles logic
    assert response.status_code == 403