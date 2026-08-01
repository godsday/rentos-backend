# Sprint 07 - Multi Tenant Foundation

## Sprint Goal

Transform Rentos into a true SaaS platform where multiple businesses can operate independently inside a single application.

---

# SaaS Vision

Platform

↓

Tenant (Business)

↓

Users

↓

Permissions

↓

Business Data

Each business owns its own isolated data.

---

# Modules Added

Tenants

Roles

Tenant Members

Slug Generator

Role Seeder

---

# Database Tables

tenants

roles

tenant_members

---

# Tenants Table

Stores business information.

Columns

id

name

slug

logo

is_active

created_at

updated_at

is_deleted

---

Example

Rentos Rentals

Galaxy Rentals

ABC Constructions

XYZ Restaurant

Each one is a Tenant.

---

# Roles Table

Seeded Roles

SUPER_ADMIN

TENANT_OWNER

MANAGER

STAFF

Purpose

Role Based Access Control (RBAC)

---

# Tenant Members

Acts as bridge table.

tenant_id

↓

user_id

↓

role_id

One User

can belong to

many businesses.

---

Relationship

User

↓

TenantMember

↓

Tenant

↓

Role

---

# Registration Flow Updated

Before

Register User

↓

Done

After

Register Request

↓

Validate Email

↓

Validate Phone

↓

Generate Business Slug

↓

Create Tenant

↓

Create User

↓

Find TENANT_OWNER Role

↓

Create Tenant Member

↓

Commit Transaction

↓

Return User

---

Registration Request

POST

/api/v1/auth/register

Body

{
  "business_name": "Rentos Demo",
  "full_name": "Muhammed Rafi",
  "email": "demo@example.com",
  "phone": "9876543288",
  "password": "password123"
}

---

Generated Automatically

Tenant

User

Tenant Membership

Role Assignment

---

Current Database Structure

Users

↓

Tenant Members

↓

Roles

↓

Tenants

---

Repositories Added

TenantRepository

RoleRepository

TenantMemberRepository

---

Seeder

Role Seeder

Runs during startup.

Creates

SUPER_ADMIN

TENANT_OWNER

MANAGER

STAFF

Only inserts if missing.

Safe to execute repeatedly.

---

Slug Utility

Example

"Galaxy Rentals"

↓

galaxy-rentals

Ensures unique business URLs.

---

Architecture

Router

↓

Service

↓

Repository

↓

Database

Business logic remains inside Service Layer.

---

Important Lesson Learned

Repository should NOT own business logic.

Repository

Database Operations Only

Service

Validation

Workflow

Transactions

Business Rules

---

Current SaaS Capabilities

✔ Multiple Businesses

✔ Business Registration

✔ Owner Assignment

✔ Roles

✔ JWT Authentication

✔ Protected APIs

✔ Multi-Tenant Ready

---

Remaining Improvements

Database Transactions

Permission System

Subscription Module

Audit Logs

Tenant Middleware

Feature Flags

Redis Cache

Background Jobs

Storage

Billing

---

Sprint Outcome

Rentos is no longer a normal CRUD application.

It is now the foundation of a reusable Multi-Tenant SaaS Platform capable of powering

Rentos

Restaurant POS

School ERP

Hospital ERP

CRM

without changing the core architecture.
