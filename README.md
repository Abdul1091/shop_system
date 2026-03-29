# 🛒 Shop Management System API

A scalable, secure, and production-ready backend for managing shop operations including users, inventory, sales, and authentication. Built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**.

---

## 🚀 Features

### 🔐 Authentication & Authorization

* JWT-based authentication
* Secure password hashing (bcrypt)
* Role-Based Access Control (RBAC)

  * **Owner** – full access
  * **Cashier** – sales operations
  * **Staff** – restricted access

---

### 👥 User Management

* Register new users
* Login with JWT token
* Role and status management

---

### 📦 Product & Inventory Management

* Create and manage products
* Track stock levels
* Automatic inventory creation
* Low-stock threshold support
* Inventory transaction history:

  * Sales
  * Purchases (future)
  * Adjustments

---

### 💰 Sales System (Core Feature)

* Create sales invoices
* Multiple products per sale
* Automatic inventory deduction
* Prevents overselling (stock validation)
* Tracks payment methods
* Maintains historical sale records

---

### 🧾 Inventory Tracking

* Real-time stock updates
* Full audit trail via transactions
* Data consistency with transactional safety

---

## 🏗️ Project Structure

```
app/
├── core/              # Security & dependencies
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── services/          # Business logic layer
├── routes/            # API endpoints
├── database.py        # DB setup
├── main.py            # App entry point
```

---

## ⚙️ Tech Stack

* **FastAPI** – API framework
* **SQLAlchemy** – ORM
* **SQLite** – Database (dev)
* **Pydantic** – Data validation
* **JWT (python-jose)** – Authentication
* **Passlib (bcrypt)** – Password hashing
* **Uvicorn** – ASGI server
* **uv** – Package manager

---

## 🛠️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Abdul1091/shop_system
```

---

### 2. Install Dependencies (using uv)

```bash
uv sync
```

---

### 3. Run the Server

```bash
uv run uvicorn app.main:app --reload
```

---

### 4. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

### 1. Register

```
POST /auth/register
```

```json
{
  "name": "Admin",
  "email": "admin@example.com",
  "password": "password",
  "role": "owner"
}
```

---

### 2. Login

```
POST /auth/login
```

```json
{
  "email": "admin@example.com",
  "password": "password"
}
```

Response:

```json
{
  "access_token": "your_token_here",
  "token_type": "bearer"
}
```

---

### 3. Authorize Requests

In Swagger UI:

* Click **Authorize 🔒**
* Enter:

```
Bearer <your_token>
```

---

## 📦 Product API

### Create Product (Owner only)

```
POST /products/
```

```json
{
  "name": "Rice",
  "sku": "RICE001",
  "category": "Food",
  "purchase_price": 10000,
  "selling_price": 12000,
  "supplier": "Local Supplier",
  "initial_quantity": 50
}
```

---

### List Products

```
GET /products/
```

---

## 💰 Sales API

### Create Sale (Owner / Cashier)

```
POST /sales/
```

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 }
  ],
  "payment_method": "cash"
}
```

---

## 🔒 Security Features

* JWT authentication required for protected routes
* Role-based access enforcement
* Secure password hashing
* Input validation via Pydantic

---

## ⚠️ Error Handling

| Status Code | Meaning                                        |
| ----------- | ---------------------------------------------- |
| 400         | Business logic error (e.g. insufficient stock) |
| 401         | Not authenticated                              |
| 403         | Forbidden (wrong role)                         |
| 422         | Validation error                               |

---

## 📊 Current System Capabilities

* ✔ Authentication (JWT)
* ✔ Role-based authorization
* ✔ Product management
* ✔ Inventory tracking
* ✔ Sales processing
* ✔ Transaction safety (atomic operations)

---

## 🚧 Future Improvements

* 📈 Reports (daily, monthly, profit/loss)
* 🏪 Multi-store support
* 🔔 Low stock notifications
* 🧾 Purchase & supplier management
* 🧪 Automated tests
* 🗄️ PostgreSQL for production
* 🔄 Alembic migrations
* 📊 Dashboard (frontend)

---

## 🧠 Design Principles

* Clean architecture (separation of concerns)
* Transaction-safe operations
* Scalable service layer
* Production-oriented structure

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

Abdullahi Tukur Bakiyawa
Developed as a scalable backend system for real-world shop management use cases.

---

## ⭐ Final Note

This project goes beyond a simple CRUD app. It implements:

* **Business rules enforcement**
* **Data consistency guarantees**
* **Secure access control**

It is designed to serve as a **foundation for a production-grade commerce system**.