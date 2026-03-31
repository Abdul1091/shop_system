import pytest

def test_create_sale_and_verify_report(client, auth_headers):
    # 1. Setup: Register Owner and Create Product
    client.post("/auth/register", json={
        "name": "Abdullahi", "email": "owner@test.com", "password": "password", "role": "owner"
    })
    headers = auth_headers(user_id=1, role="owner")
    
    client.post("/products/", headers=headers, json={
        "name": "Bread", "sku": "BRD-01", "purchase_price": 400, 
        "selling_price": 500, "initial_quantity": 20
    })

    # 2. Action: Create a Sale
    sale_data = {
        "items": [{"product_id": 1, "quantity": 5}],
        "payment_method": "POS"
    }
    response = client.post("/sales/", json=sale_data, headers=headers)
    
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["total_amount"] == 2500  # 5 * 500
    assert len(res_data["items"]) == 1

    # 3. Verification: Check Inventory Deduction
    report_res = client.get("/products/report", headers=headers)
    report_data = report_res.json()[0]
    assert report_data["current_stock"] == 15 # 20 - 5
    assert report_data["quantity_sold"] == 5

    # 4. Verification: Detailed Sales Report (The "Who sold what")
    detailed_res = client.get("/sales/detailed-report", headers=headers)
    assert detailed_res.status_code == 200
    detail = detailed_res.json()[0]
    assert detail["cashier_name"] == "Abdullahi"
    assert detail["product_name"] == "Bread"
    assert detail["total_price"] == 2500

def test_sale_rollback_on_insufficient_stock(client, auth_headers):
    # Setup
    client.post("/auth/register", json={
        "name": "Cashier", "email": "c@test.com", "password": "pw", "role": "owner"
    })
    headers = auth_headers(user_id=1, role="owner")
    client.post("/products/", headers=headers, json={
        "name": "Soda", "sku": "SD-01", "purchase_price": 50, 
        "selling_price": 100, "initial_quantity": 2
    })

    # Try to sell 10 units when only 2 exist
    sale_data = {
        "items": [{"product_id": 1, "quantity": 10}],
        "payment_method": "Cash"
    }
    response = client.post("/sales/", json=sale_data, headers=headers)
    
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]

    # CRITICAL: Verify that NO sale was actually created in the DB due to rollback
    # We check the detailed report; it should be empty
    detailed_res = client.get("/sales/detailed-report", headers=headers)
    assert len(detailed_res.json()) == 0

def test_sale_invalid_product_id(client, auth_headers):
    client.post("/auth/register", json={
        "name": "Owner", "email": "o@test.com", "password": "pw", "role": "owner"
    })
    headers = auth_headers(user_id=1, role="owner")

    response = client.post("/sales/", headers=headers, json={
        "items": [{"product_id": 999, "quantity": 1}],
        "payment_method": "Cash"
    })
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()