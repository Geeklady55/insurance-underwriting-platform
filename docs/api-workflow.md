# API Workflow

## Purpose

This document explains how the API processes an insurance application from intake to decision.

## Endpoint Used

`POST /applications`

## Workflow Steps

### 1. Request Submitted
A user submits:
- full name
- age
- smoker status
- annual income
- coverage amount

### 2. Validation
FastAPI and Pydantic validate:
- required fields
- numeric values
- age range
- smoker input format

### 3. Risk Calculation
The rules engine evaluates risk based on:
- applicant age
- smoker status
- requested coverage amount
- annual income

### 4. Decision
The API returns one of three decisions:
- Approved
- Manual Review
- Declined

### 5. Persistence
The completed application is saved to the database.

### 6. Response
The API sends a JSON response containing:
- application ID
- status
- risk score
- decision

## Example Outcome

A low-risk applicant may receive:
- risk score: 0
- decision: Approved

A higher-risk applicant may receive:
- risk score: 70+
- decision: Declined
