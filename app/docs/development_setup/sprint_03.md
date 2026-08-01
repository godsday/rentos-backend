# Sprint 3 - Database Versioning (Alembic)

## Objective

The objective of Sprint 3 was to introduce version-controlled database schema management using Alembic.

All future database changes will now be performed through migrations instead of manually writing SQL.

---

## Completed Tasks

### Alembic Initialization

Initialized Alembic inside the backend project.

```
backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
└── alembic.ini
```

---

### Alembic Configuration

Configured Alembic to use application settings instead of hardcoded database URLs.

Database configuration is now shared between:

- FastAPI
- SQLAlchemy
- Alembic

This eliminates duplicate configuration.

---

### Base Entity

Created the application's reusable base entity.

Common fields include:

- id
- created_at
- updated_at

Every future database table will inherit from this class.

Benefits:

- Eliminates duplicate code
- Consistent timestamps
- Standard primary key

---

### Vendor Model

Created the first business entity.

```
vendors
```

Initially includes:

- id
- name

This table serves as the first migration and validates the complete migration workflow.

---

### Model Registration

Registered SQLAlchemy models inside:

```
app/db/models.py
```

This allows Alembic to automatically detect models during migration generation.

---

### First Migration

Generated the first migration.

```bash
alembic revision --autogenerate -m "create vendors table"
```

Alembic created a migration inside:

```
alembic/versions/
```

---

### Database Migration

Applied migration.

```bash
alembic upgrade head
```

Alembic created:

```
vendors
```

and

```
alembic_version
```

tables inside PostgreSQL.

---

### Database Verification

Verified successful migration.

```sql
\dt
```

Output:

```
alembic_version

vendors
```

---

## Why Alembic?

Without Alembic:

- Developers manually execute SQL.
- Production databases become inconsistent.
- Rollbacks are difficult.

With Alembic:

- Database schema is version controlled.
- Team members share identical database structure.
- Deployments become repeatable.
- Rollbacks become possible.

Alembic serves the same role for database schema that Git serves for source code.

---

## Current Architecture

Current backend architecture:

Client

↓

FastAPI

↓

API Router

↓

Service Layer

↓

Repository Layer

↓

SQLAlchemy ORM

↓

Alembic Migration Layer

↓

PostgreSQL

---

## Sprint 3 Outcome

The backend now supports:

- Version-controlled database schema
- Automatic migration generation
- Migration history
- Consistent database deployment
- Production-ready database workflow

Future tables such as:

- Customers
- Inventory
- Rentals
- Employees
- Payments

will all be managed through Alembic migrations.

---

## Project Status After Sprint 3

Completed:

- Python Environment
- Virtual Environment
- FastAPI
- PostgreSQL
- SQLAlchemy
- Database Sessions
- Dependency Injection
- API Routing
- Health APIs
- Database Connectivity
- Alembic
- First Migration
- Vendor Table

Next Sprint:

Vendor Management Module

This sprint will introduce:

- Vendor CRUD APIs
- Request Validation
- Response Schemas
- Repository Layer
- Service Layer
- Unit Testing