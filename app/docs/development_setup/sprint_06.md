# Sprint 06 - Authentication System

## Sprint Goal

Build a production-ready authentication module that can be reused across every future SaaS product.

---

# Features Completed

## User Registration

Endpoint

POST /api/v1/auth/register

Request

{
  "full_name": "Muhammed Rafi",
  "email": "rafi@gmail.com",
  "phone": "9876543210",
  "password": "password123"
}

Validation

✔ Email uniqueness

✔ Phone uniqueness

✔ Password hashing

✔ Soft delete support

---

## User Login

Endpoint

POST /api/v1/auth/login

Request

{
  "email": "rafi@gmail.com",
  "password": "password123"
}

Process

Find user

↓

Verify password

↓

Generate JWT

↓

Return Access Token

Response

{
  "access_token": "...",
  "token_type": "bearer"
}

---

## Password Security

Using

Passlib

bcrypt

Functions

hash_password()

verify_password()

Passwords are never stored in plain text.

---

## JWT Authentication

Implemented

create_access_token()

decode_access_token()

JWT Payload

{
  "sub": "<user_id>",
  "exp": "<expiry>"
}

---

## Protected Routes

Created

GET /api/v1/auth/me

Flow

Bearer Token

↓

Decode JWT

↓

Find User

↓

Return Current User

---

## Dependency Injection

Created

get_current_user()

Responsibilities

Read Authorization Header

↓

Extract JWT

↓

Decode

↓

Find User

↓

Return User

---

## Repository Layer

Implemented

UserRepository

Functions

create()

get_by_email()

get_by_phone()

get_by_id()

---

## Service Layer

Implemented

UserService

Responsibilities

Business Validation

Password Hashing

Authentication

JWT Creation

User Registration

---

## Swagger Authentication

Verified

Login API

↓

Copy Token

↓

Authorize

↓

Access Protected Endpoints

---

# Folder Structure

app/modules/auth

models.py

schema.py

repository.py

service.py

router.py

---

# Security

Password Hashing

JWT Authentication

Bearer Token

Protected APIs

Soft Delete Support

---

# Architecture

Router

↓

Service

↓

Repository

↓

Database

Business Logic exists ONLY inside Services.

Repositories only access database.

---

# Sprint Result

Completed

Authentication Module

JWT

Password Hashing

Protected APIs

Swagger Authentication

Production Ready Authentication Layer
