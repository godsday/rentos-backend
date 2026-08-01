# Rentos Architecture

**Project:** Rentos
**Version:** 0.1.0
**Status:** Active Development

---

# 1. Introduction

## Purpose

This document describes the overall architecture of the Rentos platform.

It explains:

* Overall system design
* Application architecture
* Folder organization
* Data flow
* Multi-tenant strategy
* Backend layers
* Future scalability
* Integration strategy

This document should be updated whenever the application's architecture changes.

---

# 2. Project Overview

Rentos is a cloud-based Rental Management SaaS platform that enables multiple rental businesses to operate independently using a shared application.

Each rental business (Vendor) has complete ownership of its own:

* Inventory
* Customers
* Rental Orders
* Employees
* Reports
* Settings
* Financial Data

Although all vendors use the same platform, their data remains isolated.

---

# 3. High-Level Architecture

```text
                    Customer

                       │

               Flutter / Web App

                       │

                 HTTPS / REST API

                       │

                  FastAPI Backend

                       │

      ┌─────────────────────────────────┐
      │        Business Services        │
      └─────────────────────────────────┘
                       │
      ┌─────────────────────────────────┐
      │        Repository Layer         │
      └─────────────────────────────────┘
                       │
      ┌─────────────────────────────────┐
      │        SQLAlchemy ORM           │
      └─────────────────────────────────┘
                       │
                 PostgreSQL Database
```

---

# 4. Technology Stack

| Layer             | Technology              |
| ----------------- | ----------------------- |
| Frontend          | Flutter, Web (Future)   |
| Backend           | FastAPI                 |
| Language          | Python                  |
| ORM               | SQLAlchemy              |
| Database          | PostgreSQL              |
| Migration         | Alembic                 |
| Authentication    | JWT                     |
| Validation        | Pydantic                |
| API Documentation | Swagger/OpenAPI         |
| Containerization  | Docker                  |
| Reverse Proxy     | Nginx (Future)          |
| Background Jobs   | Celery / RQ (Future)    |
| Cache             | Redis (Future)          |
| Storage           | AWS S3 / MinIO (Future) |

---

# 5. Backend Architecture

The backend follows a layered architecture.

```text
Client
   │
API Layer
   │
Service Layer
   │
Repository Layer
   │
Database Layer
```

Each layer has a single responsibility.

---

## API Layer

Responsibilities

* Receive HTTP requests
* Validate input
* Authenticate users
* Call business services
* Return JSON responses

Contains:

* Routers
* Request models
* Response models

---

## Service Layer

Contains business logic.

Examples

* Create Rental
* Return Product
* Calculate Fine
* Generate Invoice

Services never communicate directly with HTTP.

---

## Repository Layer

Responsible for database access.

Responsibilities

* CRUD operations
* Database queries
* Transactions

Business logic should never be written inside repositories.

---

## Database Layer

Responsible only for:

* Database connection
* ORM
* Sessions
* Models

---

# 6. Request Lifecycle

```text
Flutter App

      │

HTTP Request

      │

FastAPI Router

      │

Validation

      │

Authentication

      │

Service

      │

Repository

      │

Database

      │

Repository

      │

Service

      │

JSON Response

      │

Flutter
```

Every request follows this lifecycle.

---

# 7. Folder Structure

```text
backend/

│

├── app/
│
├── api/
│
├── config/
│
├── core/
│
├── database/
│
├── middleware/
│
├── auth/
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── utils/
│
└── main.py

├── tests/

├── alembic/

├── .env

├── requirements.txt

└── README.md
```

Each folder has a clearly defined responsibility.

Detailed folder documentation is available in `folder-structure.md`.

---

# 8. Module Architecture

The platform will be divided into independent business modules.

```text
Authentication

Vendor

Employees

Inventory

Customers

Rental Orders

Bookings

Invoices

Payments

Reports

Notifications

Settings
```

Each module will contain:

* Models
* Schemas
* Services
* Repositories
* API Endpoints

Modules should remain independent whenever possible.

---

# 9. Multi-Tenant Architecture

Rentos follows a Shared Database, Shared Schema architecture.

```text
Database

│

├── Vendor A
│      Inventory
│      Customers
│      Rentals

├── Vendor B
│      Inventory
│      Customers
│      Rentals

└── Vendor C
       Inventory
       Customers
       Rentals
```

Every business record belongs to exactly one vendor.

Each table will include a Vendor ID.

Example

```text
Inventory

id

vendor_id

product_name

quantity
```

Every database query must filter by the authenticated vendor.

Example

```sql
SELECT *
FROM inventory
WHERE vendor_id = current_vendor;
```

This prevents data leakage between businesses.

---

# 10. Authentication Flow

Future authentication process.

```text
Login

↓

Verify Credentials

↓

Generate JWT

↓

Return Access Token

↓

Flutter Stores Token

↓

Every API Request

↓

Authorization Header

↓

JWT Validation

↓

Identify Vendor

↓

Execute Request
```

---

# 11. Configuration Management

Application configuration is stored in `.env`.

Examples

* Database URL
* Secret Keys
* API Keys
* Environment Variables
* Debug Mode

Configuration is loaded through Pydantic Settings.

Secrets must never be hardcoded.

---

# 12. API Design Principles

The API follows REST principles.

Examples

```text
GET /vendors

GET /inventory

POST /rentals

PUT /customers/{id}

DELETE /inventory/{id}
```

JSON is used for all communication.

---

# 13. Error Handling

Every API response should follow a consistent structure.

Success

```json
{
    "success": true,
    "message": "Rental created successfully",
    "data": {}
}
```

Error

```json
{
    "success": false,
    "message": "Customer not found",
    "errors": []
}
```

This format should remain consistent across the application.

---

# 14. Security Principles

The application follows these security rules:

* JWT Authentication
* Password Hashing
* HTTPS in Production
* SQL Injection Protection
* ORM Queries Only
* Input Validation
* Role-Based Authorization
* Vendor Isolation
* Environment Variables for Secrets

---

# 15. Scalability Goals

The architecture is designed to support:

* Thousands of vendors
* Hundreds of thousands of customers
* Millions of rental records

Future enhancements include:

* Redis Caching
* Background Workers
* Horizontal Scaling
* Object Storage
* CDN
* Microservices (if required)

The initial architecture remains modular so these additions require minimal changes.

---

# 16. Future Integrations

Planned integrations:

* Payment Gateway
* SMS Provider
* Email Service
* WhatsApp Notifications
* Barcode Scanner
* QR Code Support
* Accounting Software
* AI-Based Insights
* Mobile Push Notifications

These integrations should be implemented through dedicated service classes.

---

# 17. Architecture Principles

The following principles guide development.

1. Single Responsibility Principle
2. Separation of Concerns
3. Modular Design
4. Reusable Components
5. Loose Coupling
6. High Cohesion
7. Dependency Injection
8. Clean Code
9. Security by Design
10. Documentation First

Every new feature should follow these principles.

---

# 18. Current Status

## Completed

* Python Environment
* Virtual Environment
* FastAPI Setup
* Uvicorn Configuration
* Configuration Management (.env)
* Pydantic Settings
* Swagger Documentation

## In Progress

* PostgreSQL Integration

## Planned

* SQLAlchemy
* Alembic
* Authentication
* Vendor Management
* Inventory
* Customers
* Rentals
* Payments
* Reports

---

# 19. Revision History

| Version | Date      | Description                            |
| ------- | --------- | -------------------------------------- |
| 0.1.0   | July 2026 | Initial architecture document created. |

---

# 20. Notes

This document is intended to evolve throughout the lifetime of the project.

Every architectural decision that changes the overall system design should be reflected here before implementation.

Architecture documentation should always remain synchronized with the actual implementation.
