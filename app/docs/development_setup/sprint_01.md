# Rentos Backend Development Guide

## Sprint 1 - Development Environment & Project Foundation

### Overview

This sprint focuses on preparing a professional backend development environment. At this stage, no business logic has been implemented. The goal is to establish a reliable foundation that will support all future development.

The backend is built using **FastAPI**, with **PostgreSQL** as the database. The project is designed to follow a modular and scalable architecture suitable for a multi-tenant SaaS application.

---

# Project Goal

Rentos is a cloud-based Rental Management SaaS platform where multiple rental shop owners (vendors) can independently manage their rental businesses using a single shared platform.

Each vendor will have:

* Their own inventory
* Their own customers
* Their own rental orders
* Their own staff
* Their own reports
* Their own settings

Although all vendors use the same application, their data remains completely isolated.

---

# Technology Stack

| Component          | Technology                                         |
| ------------------ | -------------------------------------------------- |
| Language           | Python 3.14                                        |
| Backend Framework  | FastAPI                                            |
| ASGI Server        | Uvicorn                                            |
| ORM                | SQLAlchemy *(to be configured in the next sprint)* |
| Database           | PostgreSQL *(next sprint)*                         |
| Database Migration | Alembic *(next sprint)*                            |
| Configuration      | Pydantic Settings                                  |
| API Documentation  | Swagger / OpenAPI                                  |
| IDE                | Cursor                                             |
| Version Control    | Git                                                |
| Containerization   | Docker *(planned)*                                 |

---

# Why FastAPI?

Several backend frameworks were considered.

FastAPI was selected because it provides:

* Excellent performance
* Native asynchronous programming support
* Automatic OpenAPI documentation
* Strong type checking
* Excellent developer experience
* Easy integration with Flutter applications
* Large ecosystem

Since Rentos will expose REST APIs for Flutter, Web, and future integrations, FastAPI is an excellent fit.

---

# Why a Virtual Environment?

Python projects should never rely on globally installed packages.

Instead, every project owns its own isolated Python environment.

Without a virtual environment:

Project A and Project B share the same package versions, causing dependency conflicts.

With a virtual environment:

Each project manages its own packages independently.

Benefits:

* No package conflicts
* Easy dependency management
* Reproducible development environment
* Safer upgrades

The virtual environment for Rentos is located inside:

```
backend/.venv
```

---

# Installing Dependencies

The following core libraries were installed.

## FastAPI

Provides the REST API framework.

Responsibilities:

* Route handling
* Request validation
* Response serialization
* OpenAPI documentation
* Dependency Injection

---

## Uvicorn

ASGI server responsible for serving the FastAPI application.

Responsibilities:

* Receive HTTP requests
* Execute FastAPI application
* Return HTTP responses

---

## SQLAlchemy *(Installed but configured later)*

Will be responsible for:

* Database communication
* ORM mapping
* Query building
* Relationship management

---

## Alembic *(Installed but configured later)*

Will manage database schema migrations.

Responsibilities:

* Create tables
* Upgrade schema
* Rollback schema
* Maintain migration history

---

## Pydantic Settings

Used for configuration management.

Instead of hardcoding secrets into Python files, configuration values are loaded from environment variables.

---

# Starting the Application

The application is started using:

```bash
python -m uvicorn app.main:app --reload
```

Explanation:

**python**

Runs the Python interpreter from the active virtual environment.

**-m**

Executes a Python module.

Instead of running a file directly, Python runs the installed Uvicorn module.

**uvicorn**

Starts the ASGI web server.

**app.main**

Imports:

```
backend/app/main.py
```

**:app**

Uses the FastAPI application instance named:

```python
app = FastAPI(...)
```

**--reload**

Automatically restarts the server whenever source files change.

This significantly improves development productivity.

---

# FastAPI Request Lifecycle

```
Browser

      │

HTTP Request

      │

Uvicorn

      │

FastAPI Router

      │

Python Function

      │

JSON Response

      │

Browser
```

Every API request follows this flow.

---

# Automatic API Documentation

FastAPI automatically generates Swagger documentation.

Available at:

```
http://127.0.0.1:8000/docs
```

Advantages:

* Interactive testing
* Request examples
* Response schemas
* API discovery
* Client integration support

No additional code is required.

---

# Configuration Management

The project uses a `.env` file to separate configuration from source code.

Example:

```
APP_NAME=Rentos API
APP_VERSION=1.0.0
DEBUG=True

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=rentos
DATABASE_USER=postgres
DATABASE_PASSWORD=********

SECRET_KEY=********
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Configuration values are loaded using Pydantic Settings.

Advantages:

* Environment-specific configuration
* Better security
* Cleaner source code
* Easier deployment

---

# Application Settings

The configuration object is centralized in:

```
app/config/settings.py
```

Every module can access configuration through:

```python
from app.config.settings import settings
```

Example:

```python
settings.app_name
settings.debug
settings.database_host
```

This avoids hardcoded values throughout the project.

---

# Current Folder Structure

```
backend/

│

├── app/
│
├── config/
│
├── api/
│
├── auth/
│
├── common/
│
├── core/
│
├── database/
│
├── middleware/
│
├── models/
│
├── repositories/
│
├── schemas/
│
├── services/
│
├── utils/
│
└── main.py

├── .venv/

├── .env

└── requirements.txt
```

This structure will continue evolving as new modules are introduced.

---

# What Has Been Completed

Environment Setup

* Python installed
* Virtual environment created
* Required packages installed
* Cursor configured
* FastAPI running
* Swagger available

Backend Foundation

* Application startup
* Configuration system
* Environment variables
* Settings management

Documentation

* Initial project documentation
* Development guide

---

# What Has NOT Been Built Yet

The following modules are intentionally postponed.

Authentication

Vendor Management

Customer Management

Inventory

Rental Orders

Invoices

Payments

Reports

Notifications

Role-Based Access Control

Multi-Tenant Data Isolation

Database Schema

Caching

Background Jobs

Deployment Pipeline

---

# Lessons Learned

1. Always activate the virtual environment before development.

2. Never install packages globally.

3. Store secrets inside `.env`, never in source code.

4. Use `python -m pip` instead of `pip` when possible to ensure packages are installed into the active interpreter.

5. Verify the selected Python interpreter inside the IDE if import errors appear.

6. FastAPI automatically generates API documentation through Swagger.

7. Uvicorn is the web server responsible for executing the FastAPI application.

---

# Next Sprint

Sprint 2 will establish the database layer.

Goals:

* Create PostgreSQL database
* Configure SQLAlchemy
* Configure Alembic
* Create the database session
* Create the Base model
* Verify database connectivity

After the database layer is complete, authentication and business modules can be built safely on top of it.

---

Version: 0.0.1

Status: Completed

Last Updated: July 2026
