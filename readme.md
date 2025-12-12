#  Mini ERP System

> A modern, feature-rich ERP system built with Django REST Framework for managing products, customers, sales orders, and inventory operations.

[![Django](https://img.shields.io/badge/Django-5.2.9-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)


##  Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Business Logic](#-business-logic)

##  Features

### Core Functionality
-  **Product Management** - Complete CRUD with image upload support
-  **Customer Management** - Auto-generated customer codes (CUST-00001)
-  **Sales Order System** - Full order lifecycle management
-  **Inventory Control** - Real-time stock tracking and updates
-  **Stock Movement Logs** - Complete audit trail of all stock changes
-  **Role-Based Access Control** - Admin and Sales User roles

### Advanced Features
-  **JWT Authentication** - Secure token-based auth with refresh tokens
-  **Dashboard Analytics** - Real-time business metrics
-  **Excel Export** - Comprehensive reports in XLSX format
-  **Search & Filters** - Advanced product search and filtering
-  **Pagination** - Efficient data loading for large datasets
-  **Swagger API Docs** - Interactive API documentation
-  **Role-Based Menus** - Dynamic menu generation based on user role

### Business Rules
-  Automatic stock reduction on order confirmation
-  Automatic stock restoration on order cancellation
-  Price validation (selling price ≥ cost price)
-  Stock availability validation before order confirmation
-  Transaction atomicity for data consistency
-  Comprehensive audit logging

## 🛠 Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Django 5.2.9, Django REST Framework 3.14 |
| **Authentication** | SimpleJWT (JWT tokens with blacklisting) |
| **Database** | SQLite (dev), PostgreSQL ready |
| **API Docs** | drf-yasg (Swagger/OpenAPI) |
| **File Processing** | Pillow (images), openpyxl (Excel) |
| **Configuration** | python-decouple |

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
virtualenv (recommended)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mini-erp.git
cd mini-erp
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your configurations
# Required variables:
# - SECRET_KEY
# - DEBUG
# - ALLOWED_HOSTS
```

5. **Database setup**
```bash
# Run migrations
python manage.py migrate

# Create superuser (Admin)
python manage.py createsuperuser

# (Optional) Load sample data
python manage.py loaddata sample_data.json
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
-  **Swagger UI**: http://localhost:8000/swagger/
-  **Admin Panel**: http://localhost:8000/admin/
-  **ReDoc**: http://localhost:8000/redoc/

##  API Documentation

### Authentication Endpoints

#### Register New User
```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "salesuser",
  "password": "securepass123"
}
```

#### Login (Get Tokens)
```http
POST /api/accounts/login/
Content-Type: application/json

{
  "username": "salesuser",
  "password": "securepass123"
}

Response:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Access Token
```http
POST /api/accounts/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout
```http
POST /api/accounts/logout/
Authorization: Bearer <access_token>

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Product Endpoints

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/products/` | Authenticated | List all products |
| POST | `/api/products/` | Admin only | Create new product |
| GET | `/api/products/{id}/` | Authenticated | Get product details |
| PUT/PATCH | `/api/products/{id}/` | Admin only | Update product |
| DELETE | `/api/products/{id}/` | Admin only | Delete product |

**Query Parameters:**
- `?search=laptop` - Search by SKU, name, or category
- `?category=Electronics` - Filter by category
- `?page=2&page_size=20` - Pagination

**Example: Create Product**
```http
POST /api/products/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "sku": "PROD-001",
  "name": "Laptop Dell XPS",
  "category": "Electronics",
  "cost_price": 15000.00,
  "selling_price": 18000.00,
  "stock": 50,
  "image": <file>
}
```

### Customer Endpoints

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/customers/` | Authenticated | List all customers |
| POST | `/api/customers/` | Authenticated | Create new customer |
| GET | `/api/customers/{id}/` | Admin only | Get customer details |
| PUT/PATCH | `/api/customers/{id}/` | Admin only | Update customer |
| DELETE | `/api/customers/{id}/` | Admin only | Delete customer |

**Example: Create Customer**
```http
POST /api/customers/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Ahmed Hassan",
  "phone": "+201234567890",
  "email": "ahmed@example.com",
  "address": "123 Cairo Street, Egypt",
  "opening_balance": 5000.00
}

Response:
{
  "id": 1,
  "customer_code": "CUST-00001",
  "name": "Ahmed Hassan",
  ...
}
```

### Sales Order Endpoints

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/sales-orders/` | Authenticated | List orders |
| POST | `/api/sales-orders/` | Authenticated | Create new order |
| GET | `/api/sales-orders/{id}/` | Owner/Admin | Get order details |
| PUT/PATCH | `/api/sales-orders/{id}/` | Admin only | Update order |
| POST | `/api/sales-orders/{id}/confirm/` | Admin only | Confirm order |
| POST | `/api/sales-orders/{id}/cancel/` | Admin only | Cancel order |

**Example: Create Sales Order**
```http
POST /api/sales-orders/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "customer": 1,
  "lines": [
    {
      "product": 1,
      "qty": 2
    },
    {
      "product": 3,
      "qty": 5
    }
  ]
}

Response:
{
  "order_number": 1,
  "customer": 1,
  "customer_name": "Ahmed Hassan",
  "status": "pending",
  "total_amount": 36000.00,
  "lines": [
    {
      "product": 1,
      "product_name": "Laptop Dell XPS",
      "qty": 2,
      "price": 18000.00,
      "line_total": 36000.00,
      "available_stock": 48
    }
  ]
}
```

**Example: Confirm Order**
```http
POST /api/sales-orders/1/confirm/
Authorization: Bearer <admin_token>

Response:
{
  "status": "Order confirmed successfully"
}
```

### Report Endpoints

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/dashboard/` | Authenticated | Dashboard statistics |
| GET | `/api/menu/` | Authenticated | Role-based menu items |
| GET | `/api/export_full_report/` | Admin only | Download Excel report |

**Example: Dashboard Response**
```json
{
  "total_customers": 150,
  "total_sales_today": 23,
  "stock_running_low": [
    {
      "name": "Laptop Dell XPS",
      "stock": 3
    },
    {
      "name": "iPhone 15 Pro",
      "stock": 2
    }
  ]
}
```

### Stock Movement Endpoints

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/stock-movements/` | Authenticated | View stock logs |
| GET | `/api/stock-movements/{id}/` | Authenticated | View specific log |

##  Project Structure

```
MiniERP/
├── MiniERP/                    # Project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL routing
│   └── wsgi.py                # WSGI application
│
├── accounts/                   # Authentication module
│   ├── serializers.py         # User serializers
│   ├── views.py               # Auth views
│   └── urls.py                # Auth endpoints
│
├── products/                   # Product management
│   ├── models.py              # Product model
│   ├── serializers.py         # Product serializers
│   ├── views.py               # Product viewsets
│   ├── permissions.py         # Custom permissions
│   └── urls.py                # Product endpoints
│
├── customer/                   # Customer management
│   ├── models.py              # Customer model
│   ├── serializers.py         # Customer serializers
│   ├── views.py               # Customer viewsets
│   └── urls.py                # Customer endpoints
│
├── sales_order/                # Sales order system
│   ├── models.py              # Order & Line models
│   ├── serializers.py         # Order serializers
│   ├── views.py               # Order viewsets
│   ├── permissions.py         # Order permissions
│   └── urls.py                # Order endpoints
│
├── reports/                    # Reporting module
│   ├── views.py               # Dashboard & exports
│   └── urls.py                # Report endpoints
│
├── media/                      # Uploaded files
│   └── products/              # Product images
│
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

##  Business Logic

### Order Status Workflow

```
┌──────────┐
│ PENDING  │  (Initial state - order created)
└──────────┘
     │
     │ confirm() 
     ↓
┌───────────┐
│ CONFIRMED │  (Stock reduced, order active)
└───────────┘
     ↕
     │ cancel()  / confirm() 
     │ (Bidirectional)
     ↕
┌───────────┐
│ CANCELLED │  (Stock restored, order closed)
└───────────┘
```

**Status Transitions:**
- `PENDING` → `CONFIRMED` (one-way, via confirm)
- `CONFIRMED` ⟷ `CANCELLED` (bidirectional, can go back and forth)
  - Cancel: Restores stock
  - Re-confirm: Reduces stock again

### Stock Management Rules

1. **Order Creation (Pending)**
   -  Order is created
   - ❌ Stock is NOT reduced
   -  Stock availability is validated

2. **Order Confirmation**
   -  Stock is reduced for all items
   -  Stock movement logs are created
   -  Transaction is atomic (all or nothing)
   - ❌ Cannot confirm if insufficient stock

3. **Order Cancellation**
   -  Stock is restored for all items
   -  Reverse stock movement logs are created
   -  Can only cancel confirmed orders

### Permission Matrix

| Action | Admin | Sales User |
|--------|-------|------------|
| View Products |  |  |
| Create Product |  | ❌ |
| Edit Product |  | ❌ |
| Delete Product |  | ❌ |
| View Customers |  |  |
| Create Customer |  |  |
| Edit Customer |  | ❌ |
| Delete Customer |  | ❌ |
| Create Order |  |  |
| View Own Orders |  |  |
| View All Orders |  | ❌ |
| Confirm Order |  | ❌ |
| Cancel Order |  | ❌ |
| View Reports |  | ❌ |
| Export Excel |  | ❌ |

##  License & Usage

This project is **free and open-source** 
