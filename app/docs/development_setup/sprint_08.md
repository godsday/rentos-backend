# Sprint 08 - Category Management

## Sprint Goal

Implement a complete Category Management module with proper multi-tenant isolation.

Each business (Tenant) should be able to manage its own rental categories independently.

---

# Features Completed

- Category Model
- Category Repository
- Category Service
- Category Router
- Category Schemas
- CRUD APIs
- JWT Authentication
- Tenant Isolation
- Soft Delete
- Duplicate Name Validation

---

# Database Structure

Table

categories

Columns

- id
- tenant_id
- name
- description
- created_at
- updated_at
- is_deleted
- deleted_at

Relationships

Tenant (1)
    │
    ├───────────────► Categories (Many)

Every category belongs to exactly one tenant.

---

# Folder Structure

app/modules/categories/

├── models.py
├── repository.py
├── service.py
├── router.py
├── schema.py

---

# APIs

## Create Category

POST

/api/v1/categories

Request

{
    "name": "Camera",
    "description": "Photography Equipment"
}

Response

{
    "id": "...",
    "name": "Camera",
    "description": "Photography Equipment"
}

---

## Get Categories

GET

/api/v1/categories

Returns

[
    ...
]

Only categories belonging to the logged-in tenant are returned.

---

## Get Category

GET

/api/v1/categories/{id}

Returns a single category.

Tenant ownership is validated.

---

## Update Category

PUT

/api/v1/categories/{id}

Updates

- Name
- Description

---

## Delete Category

DELETE

/api/v1/categories/{id}

Soft delete only.

No data is permanently removed.

---

# Business Rules

## Tenant Isolation

Tenant A

Camera

Tenant B

Camera

Allowed

Because categories are tenant specific.

---

## Duplicate Validation

Inside same tenant

Camera

Camera

Not Allowed

---

## Soft Delete

Deleting a category only sets

is_deleted = true

instead of removing the record.

Benefits

- Data recovery
- Audit history
- Rental history remains valid

---

# Authentication

Every endpoint requires

Authorization

Bearer Token

The JWT contains

- User ID
- Tenant ID
- Role

The tenant_id is extracted inside

get_current_user()

and injected into every service.

---

# Architecture

Client

↓

Router

↓

Service

↓

Repository

↓

Database

Business logic never exists inside Router.

Repository contains only database operations.

Service contains business rules.

---

# Repository Methods

Implemented

create()

get_by_id()

get_all_by_tenant()

get_by_name()

update()

soft_delete()

---

# Service Responsibilities

Validate duplicate category names.

Validate tenant ownership.

Call repository.

Raise HTTP exceptions.

---

# Security

Users cannot

Read another tenant's category.

Update another tenant's category.

Delete another tenant's category.

Create duplicate category names.

---

# Swagger Tested

Verified

Create

Read

Update

Delete

Authorization

Tenant Isolation

---

# Challenges Faced

## Transactions

Initially data disappeared after POST.

Reason

Repository switched from

commit()

to

flush()

Solution

Commit is now handled by

get_db()

using transaction management.

---

# Lessons Learned

Difference between

flush()

refresh()

commit()

Transaction lifecycle

Service vs Repository responsibilities

Tenant isolation

Soft delete implementation

JWT based authorization

---

# Sprint Outcome

Category Management is production-ready.

Future modules such as Items and Rentals can safely reference Categories.

Status

Completed