# Sprint 2 - Database Foundation

## Objective

The objective of Sprint 2 was to establish a reliable and scalable database foundation for the Rentos backend. This included installing PostgreSQL, configuring SQLAlchemy, and creating the database connection layer that will be used by every feature in the application.

---

## Completed Tasks

### PostgreSQL Installation

Installed PostgreSQL 18 using the official PostgreSQL installer.

Verified installation by connecting through the PostgreSQL command line interface.

```bash
psql -U postgres
```

Successfully connected to PostgreSQL.

---

### Created Project Database

Created the primary application database.

```sql
CREATE DATABASE rentos;
```

Verified database creation.

```sql
\l
```

Connected to the newly created database.

```sql
\c rentos
```

Verified that the database initially contained no tables.

```sql
\dt
```

---

### Database Configuration

Configured application settings using Pydantic Settings.

Database configuration values are loaded from the `.env` file.

Example configuration:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=rentos
DATABASE_USER=postgres
DATABASE_PASSWORD=********
```

---

### SQLAlchemy Setup

Created the database layer inside:

```
app/db/
```

Files created:

```
app/db/
│
├── __init__.py
├── base.py
├── session.py
└── models.py
```

Responsibilities:

- Base Model
- SQLAlchemy Engine
- Session Factory
- Database Dependency

---

### Database Engine

Configured SQLAlchemy Engine.

Responsibilities:

- Establish connection to PostgreSQL
- Manage connection pool
- Execute SQL through ORM

---

### Session Management

Implemented SessionLocal.

Added FastAPI Dependency Injection.

```python
def get_db():
    ...
```

Each request now automatically:

- Opens a database session
- Executes database operations
- Closes the session

This prevents connection leaks.

---

### Health APIs

Created basic application endpoints.

```
GET /
GET /health
GET /db-test
```

Purpose:

- Verify API availability
- Verify database connectivity
- Test dependency injection

---

### Router Architecture

Introduced centralized API routing.

```
app/
└── api/
    └── v1/
        ├── router.py
        ├── health.py
        └── test_db.py
```

The application now follows modular routing instead of placing all endpoints inside `main.py`.

---

## Sprint 2 Outcome

Successfully established the complete database communication layer.

Architecture after Sprint 2:

Flutter/Web
↓

FastAPI

↓

Router Layer

↓

Database Dependency

↓

SQLAlchemy

↓

PostgreSQL

---