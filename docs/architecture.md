
## Step 3 — add architecture document

Create `docs/architecture.md`

```md
# Architecture

## System Overview

The Insurance Underwriting Platform is a lightweight API-driven application that simulates a digital insurance intake and decision workflow.

## Components

### Frontend
A basic HTML form allows users to submit insurance application data.

### Backend API
FastAPI handles incoming requests, validates data, applies business rules, and returns responses.

### Database
SQLite stores application records for retrieval and tracking.

### Rules Engine
A simple underwriting rules module calculates risk based on:
- age
- smoker status
- annual income
- coverage amount

## Request Flow

1. User submits application from frontend or Swagger UI
2. API validates request schema
3. Rules engine calculates risk and decision
4. Database stores application
5. API returns structured response

## Design Goals

- Simple and understandable for demonstration
- Easy to test locally
- Organized like a real backend project
- Extendable to production-style features later

## Future Architecture Enhancements

- PostgreSQL instead of SQLite
- authentication and authorization
- audit log service
- containerization with Docker
- CI/CD with GitHub Actions
- event-based processing for underwriting workflows
