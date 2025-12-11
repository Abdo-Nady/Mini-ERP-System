# Mini ERP System - Django Developer Task

## Introduction
This project is a simplified ERP system built with Django and Django REST Framework. 
It manages core business operations including products, customers, sales orders, and stock movements. 
Swagger is integrated for easy API exploration and testing.

## Objective
Simplified ERP module managing:
- Products
- Customers
- Sales Orders
- Stock movements

## Features Implemented

### 1. Authentication & Permissions
- Users must log in.
- Roles:
  - Admin → full access
  - Sales User → can create sales orders, cannot edit stock/products
- JWT authentication (DRF).

### 2. Product Module
- Fields: SKU, Name, Category, Cost Price, Selling Price, Stock
- Admin: CRUD
- Sales User: read-only
- Stock decreases automatically on confirmed sales orders

### 3. Customer Module
- Fields: Customer code, Name, Phone, Address, Email, Opening balance
- Admin: CRUD
- Sales User: can add customers, cannot delete

### 4. Sales Orders
- Fields: Order Number, Customer, Order Date, Created By, Status, Total Amount
- Details: Product, Qty, Price, Total
- Business Logic:
  - Confirmed → reduce stock
  - Cancelled → restore stock

### 5. Stock Movement Log
- Tracks all stock changes
- Fields: Product, Qty, User, Timestamp

### 6. API
- Django REST Framework
- JWT authentication
- Swagger API docs for easy testing

### 7. Optional Bonus Features
- Export reports as Excel
- Role-based menu display
- Product images upload
- Pagination, search, filters
