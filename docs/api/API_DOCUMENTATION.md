# API Documentation

## CASE Tool API v1.0

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
All endpoints (except `/auth/login` and `/auth/refresh`) require Bearer token authentication.

```bash
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### Login
**POST** `/auth/login`

Login with email and password to get access and refresh tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Status Codes:**
- `200` - Login successful
- `401` - Invalid credentials
- `403` - User account inactive

---

### Refresh Token
**POST** `/auth/refresh`

Get a new access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** Same as Login endpoint

---

### Get Current User
**GET** `/auth/me`

Get information about the currently authenticated user.

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "role_id": 2
}
```

---

## User Management

### Register User
**POST** `/users/register`

Create a new user account.

**Request:**
```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "full_name": "New User",
  "password": "securepassword123",
  "role_id": 3,
  "phone": "+1234567890",
  "organization": "ACME Corp",
  "department": "Engineering"
}
```

**Response:**
```json
{
  "id": 2,
  "email": "newuser@example.com",
  "username": "newuser",
  "full_name": "New User",
  "role_id": 3,
  "is_active": true,
  "is_verified": false,
  "created_at": "2026-04-30T10:00:00",
  "updated_at": "2026-04-30T10:00:00"
}
```

---

### Get User
**GET** `/users/{user_id}`

Get user information by ID.

---

### Update User
**PUT** `/users/{user_id}`

Update user information.

**Request:**
```json
{
  "full_name": "Updated Name",
  "phone": "+0987654321"
}
```

---

### List Users
**GET** `/users?skip=0&limit=50`

Get paginated list of users.

**Response:**
```json
{
  "total": 10,
  "skip": 0,
  "limit": 50,
  "data": [...]
}
```

---

## Project Management

### Create Project
**POST** `/projects`

Create a new project.

**Request:**
```json
{
  "name": "Mobile App Development",
  "description": "iOS and Android app",
  "status": "planning",
  "budget": 100000.00,
  "team_size": 5,
  "client_name": "Acme Inc",
  "project_manager": "John Manager",
  "department": "Development"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Mobile App Development",
  "description": "iOS and Android app",
  "created_by": 1,
  "status": "planning",
  "budget": 100000.00,
  "team_size": 5,
  "created_at": "2026-04-30T10:00:00",
  "updated_at": "2026-04-30T10:00:00",
  "is_active": true,
  "versions": []
}
```

---

### Get Project
**GET** `/projects/{project_id}`

Get project details with all related data.

---

### List Projects
**GET** `/projects?skip=0&limit=50&status_filter=planning`

Get paginated list of projects.

**Query Parameters:**
- `skip` - Number of records to skip (default: 0)
- `limit` - Number of records to return (default: 50)
- `status_filter` - Filter by status (planning, in_progress, completed, archived, on_hold)

---

### Update Project
**PUT** `/projects/{project_id}`

Update project information.

---

### Delete Project
**DELETE** `/projects/{project_id}`

Delete a project and all related data.

---

## Estimates

### Create Estimate
**POST** `/estimates`

Create a new software cost estimate.

**Request:**
```json
{
  "project_id": 1,
  "version_id": 1,
  "estimation_method": "COCOMO",
  "estimated_effort_hours": 800,
  "estimated_duration_months": 4,
  "estimated_cost": 40000.00,
  "estimated_team_size": 4,
  "confidence_level": 80,
  "confidence_interval_low": 35000,
  "confidence_interval_high": 45000,
  "notes": "Based on COCOMO intermediate model",
  "assumptions": "Team experience: 3+ years, Modern tech stack"
}
```

---

### Get Estimate
**GET** `/estimates/{estimate_id}`

Get estimate details.

---

### List Estimates for Project
**GET** `/estimates/project/{project_id}?skip=0&limit=50`

Get all estimates for a specific project.

---

### Update Estimate
**PUT** `/estimates/{estimate_id}`

Update estimate information.

---

## Cost Drivers

### Create Cost Driver
**POST** `/estimates/cost-drivers`

Create a new cost driver.

**Request:**
```json
{
  "name": "High Complexity",
  "description": "Very complex algorithms and data structures",
  "category": "complexity",
  "impact_factor": 1.65,
  "effort_multiplier": 1.65,
  "cost_multiplier": 1.65,
  "duration_multiplier": 1.40,
  "is_active": true
}
```

---

### List Cost Drivers
**GET** `/estimates/cost-drivers?skip=0&limit=50`

Get all active cost drivers.

---

## Function Points

### Create Function Points
**POST** `/estimates/{estimate_id}/function-points`

Add function point analysis to an estimate.

**Request:**
```json
{
  "ilf_count": 5,
  "ilf_complexity": "average",
  "eif_count": 2,
  "eif_complexity": "average",
  "ei_count": 8,
  "ei_complexity": "average",
  "eo_count": 6,
  "eo_complexity": "average",
  "eq_count": 4,
  "eq_complexity": "average",
  "unadjusted_fp": 300,
  "vaf": 1.0,
  "adjusted_fp": 300
}
```

---

## Scenarios

### Create Scenario
**POST** `/scenarios`

Create a what-if scenario for sensitivity analysis.

**Request:**
```json
{
  "project_id": 1,
  "name": "Optimistic Scenario",
  "description": "Best case with experienced team",
  "scenario_type": "optimistic",
  "effort_adjustment": 0.8,
  "duration_adjustment": 0.85,
  "cost_adjustment": 0.8,
  "team_size_adjustment": 0.9
}
```

---

### Get Scenarios
**GET** `/projects/{project_id}/scenarios`

Get all scenarios for a project.

---

## Risks

### Create Risk
**POST** `/risks`

Identify and track project risks.

**Request:**
```json
{
  "project_id": 1,
  "description": "Key developer unavailability",
  "category": "resource",
  "probability": 0.3,
  "impact": 0.8,
  "mitigation_strategy": "Cross-train team members",
  "owner": "John Manager",
  "status": "active",
  "effort_contingency": 160,
  "cost_contingency": 8000
}
```

---

## Reports

### Generate Report
**POST** `/reports`

Generate an estimation report.

**Request:**
```json
{
  "project_id": 1,
  "title": "Q2 2026 Estimate",
  "report_type": "estimate",
  "format": "html",
  "include_confidence_intervals": true,
  "include_risks": true,
  "include_scenarios": true
}
```

---

### Get Project Reports
**GET** `/reports/projects/{project_id}/reports`

Get all reports for a project.

---

## Status Codes

- `200` - Successful GET, PUT, DELETE
- `201` - Successful POST (resource created)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (duplicate resource)
- `500` - Internal Server Error

---

## Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently no rate limiting is applied. Production environments should implement:
- 100 requests per minute per user
- 1000 requests per minute per IP
- 10MB maximum request size

---

## Pagination

All list endpoints support pagination with:
- `skip` - Offset (default: 0)
- `limit` - Number of records (default: 50, max: 1000)

Response includes:
```json
{
  "total": 100,
  "skip": 0,
  "limit": 50,
  "data": [...]
}
```
