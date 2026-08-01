# Database Overview

## Database Engine

PostgreSQL 18

## ORM

SQLAlchemy 2.x

## Migration Tool

Alembic

## Architecture

Shared Database
Shared Schema
Multi-Tenant

Each business (Vendor) owns its own data.

Every business table contains:

- vendor_id

This ensures complete tenant isolation.

---

## Database Layers

FastAPI

↓

SQLAlchemy

↓

Alembic

↓

PostgreSQL

---

## Naming Conventions

Tables

snake_case

Examples

vendors
customers
inventory_items

Columns

snake_case

Examples

created_at
updated_at
vendor_id

Primary Key

id

Foreign Key

vendor_id

Soft Delete

planned

Timezone

UTC