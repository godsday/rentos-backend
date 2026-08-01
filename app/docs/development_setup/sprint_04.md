# Sprint 4 - User Module Foundation

## Goal

Build the foundation of the User module using a modular architecture.

This sprint focuses on creating a reusable structure that every future module (Vendor, Customer, Inventory, Rentals, etc.) will follow.

---

## Folder Structure

```
app/
│
├── api/
│   └── v1/
│       └── router.py
│
├── core/
│
├── db/
│   ├── base.py
│   ├── base_entity.py
│   ├── base_repository.py
│   └── session.py
│
├── modules/
│   └── users/
│       ├── models.py
│       ├── schema.py
│       ├── repository.py
│       ├── service.py
│       └── router.py
│
└── main.py
```

---

## Base Entity

A reusable abstract model was created to eliminate duplicate code across all database tables.

Every entity inherits:

- UUID Primary Key
- Created Timestamp
- Updated Timestamp
- Soft Delete Flag
- Deleted Timestamp

Example:

```python
class User(BaseEntity):
    ...
```

---

## Generic Repository

A reusable BaseRepository was implemented.

Common database operations are centralized:

- create()
- get_by_id()
- get_all()
- update()
- soft_delete()
- hard_delete()

Future repositories inherit these methods.

Example:

```python
class UserRepository(BaseRepository[User]):
    ...
```

---

## User Repository

Custom database queries specific to the User module were implemented.

Current methods:

- get_by_email()
- get_by_phone()

Future custom queries will also be added here.

---

## Database

Alembic migration created.

Generated table:

users

Verified:

- UUID Primary Key
- Unique Email
- Soft Delete Fields
- Audit Fields

Migration executed successfully.

---

## Routing

User router registered.

Application routing:

```
main.py
        ↓
api/v1/router.py
        ↓
users/router.py
```

Endpoint exposed:

POST /api/v1/auth/register

---

## Architecture

Current architecture:

```
Client

↓

Router

↓

Service

↓

Repository

↓

Database
```

Each layer has a single responsibility.

Router
- HTTP only

Service
- Business Logic

Repository
- Database Operations

Database
- Persistence

---

## Completed

✅ Base Entity

✅ Base Repository

✅ User Repository

✅ User Module Structure

✅ Alembic Migration

✅ Users Table

✅ API Routing

Sprint Status

COMPLETE