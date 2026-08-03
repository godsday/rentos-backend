# Sprint 09 - Item Management

## Sprint Goal

Build the inventory module used by the rental business.

Every rentable product is represented as an Item.

Examples

- Camera
- Bike
- Speaker
- Generator
- Tent
- Drone

---

# Features Completed

- Item Model
- Repository
- Service
- Router
- Schemas
- CRUD APIs
- Tenant Isolation
- Category Validation
- SKU Validation
- Inventory Fields
- Soft Delete

---

# Database Structure

Table

items

Columns

- id
- tenant_id
- category_id
- name
- sku
- description
- rental_price
- security_deposit
- quantity
- available_quantity
- barcode
- image
- is_active
- created_at
- updated_at
- is_deleted
- deleted_at

Relationships

Tenant

↓

Categories

↓

Items

Each item belongs to

- one Tenant
- one Category

---

# Folder Structure

app/modules/items/

├── models.py
├── repository.py
├── service.py
├── router.py
├── schema.py

---

# APIs

POST

/api/v1/items

GET

/api/v1/items

GET

/api/v1/items/{id}

PUT

/api/v1/items/{id}

DELETE

/api/v1/items/{id}

---

# Business Rules

## Tenant Isolation

Tenant A

Camera

Tenant B

Camera

Allowed

---

## Category Validation

Before creating an item

Verify

Category exists.

Category belongs to current tenant.

Otherwise

403 Access Denied

---

## Duplicate SKU

SKU must be unique

inside one tenant.

Example

Tenant A

CAM001

CAM001

Not Allowed

Tenant B

CAM001

Allowed

---

# Composite Unique Constraint

Database Constraint

UNIQUE

(
tenant_id,
sku
)

Reason

Every business manages its own inventory.

Different businesses can reuse the same SKU.

---

# SKU

SKU

Stock Keeping Unit

Examples

CAM001

MIC001

LIGHT015

TENT008

Used for

Inventory

Barcode

Rental Tracking

Reports

Searching

---

# Inventory Fields

quantity

Total inventory

Example

10

available_quantity

Currently available inventory

Example

7

Meaning

3 items are currently rented.

---

# Current Logic

On creation

quantity

equals

available_quantity

Example

Quantity = 10

Available = 10

---

# Future Improvement

When Rental module is implemented

available_quantity

will decrease automatically.

Example

Total

10

Rented

3

Available

7

Updating quantity

10

to

15

will become

Available

12

instead of

15

This logic will be implemented in Sprint 11.

---

# Repository Methods

Implemented

create()

get_by_id()

get_all_by_tenant()

get_by_name()

get_by_sku()

update()

soft_delete()

---

# Service Responsibilities

Validate Category

Validate Tenant

Validate SKU

Validate Item Ownership

Perform CRUD

Raise HTTP Exceptions

---

# Authentication

JWT Protected

Current User

↓

Tenant

↓

Item Access

Users can only access

their own tenant's inventory.

---

# Soft Delete

Deleting an item

does not remove the record.

Instead

is_deleted

becomes

true

---

# Swagger Testing

Verified

Create

Read

Update

Delete

Duplicate SKU

Category Validation

Authorization

Tenant Isolation

---

# Challenges Faced

Repository transaction handling

Composite unique constraint

SKU design decisions

Duplicate validation

Tenant ownership verification

Category validation

---

# Lessons Learned

Inventory modelling

Repository pattern

Business validation

Foreign key relationships

Composite unique constraints

Tenant-aware architecture

Inventory design

---

# Sprint Outcome

The Rentos Inventory Module is now complete.

The backend now supports

Users

Tenants

Roles

Tenant Members

Categories

Items

The platform is now ready to implement Customer Management and Rental Management.

Status

Completed