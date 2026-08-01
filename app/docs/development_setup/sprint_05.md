# Sprint 5 - User Registration

## Goal

Implement complete user registration.

The objective is to create the first production-ready API endpoint.

---

## Registration Flow

```
Client

↓

POST /auth/register

↓

User Router

↓

User Service

↓

User Repository

↓

Base Repository

↓

PostgreSQL
```

---

## Request Schema

Implemented CreateUserRequest.

Fields:

- full_name
- email
- phone
- password

Validation performed automatically by Pydantic.

---

## Response Schema

Implemented UserResponse.

Returned:

- id
- full_name
- email
- phone
- profile_image
- is_email_verified
- is_phone_verified
- is_active

Password hash is never returned.

---

## Password Hashing

Implemented using Passlib + bcrypt.

Functions:

```python
hash_password()

verify_password()
```

Passwords are stored using bcrypt.

Verified hash format:

```
$2b$
```

No plain text passwords are stored.

---

## Duplicate Validation

Business rules implemented inside UserService.

Checks:

Email already exists

Phone already exists

Responses:

400 Bad Request

Example:

```json
{
    "detail": "Email already exists."
}
```

---

## Exception Handling

Replaced:

```python
raise ValueError(...)
```

With:

```python
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="..."
)
```

API now returns proper HTTP responses.

---

## Swagger

Verified:

Swagger UI

OpenAPI Documentation

Request Validation

Response Validation

Automatic Documentation

---

## Database Verification

Successfully inserted user.

Verified:

- UUID Generated
- Password Hashed
- created_at populated
- updated_at populated

---

## Architecture

Final registration flow:

```
Request

↓

Router

↓

Service

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL

↓

Response
```

Business logic exists only inside the Service layer.

Repository contains database operations only.

Router contains HTTP logic only.

---

## Lessons Learned

Resolved:

- Python virtual environment configuration
- PostgreSQL connection
- Alembic migrations
- bcrypt compatibility issue
- email-validator dependency
- Repository architecture
- FastAPI routing
- Swagger configuration

---

## Completed

✅ User Registration API

✅ Password Hashing

✅ Duplicate Email Validation

✅ Duplicate Phone Validation

✅ Generic Repository Working

✅ PostgreSQL Persistence

✅ Swagger Documentation

✅ Proper HTTP Exceptions

Sprint Status

COMPLETE