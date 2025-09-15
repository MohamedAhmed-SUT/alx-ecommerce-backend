# E-Commerce Backend

**Version:** v1
**Base URL (local):** http://127.0.0.1:8000/api/
**Swagger UI:** http://127.0.0.1:8000/api/docs/

Backend for an e-commerce project using the Django REST Framework and JWT Authentication.

---

## Features

- New User Registration (Signup)
- Login with JWT (Login)
- CRUD on Products and Categories (Categories & Products)
- Security: Read for all, edit only for administrators (Admin)
- Order Management (Orders & OrderItems)
- Checkout from Cart to Order
- Swagger / Redoc API documentation
- Filter, Sort, and Browse Products (Filter, Sort, Pagination)

---

## Requirements

- Python 3.10+
- Django 4+
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- drf-yasg (Swagger)

> All libraries are located in `requirements.txt`

---

## Installation & Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd <project-folder>