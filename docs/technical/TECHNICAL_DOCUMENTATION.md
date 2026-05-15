# Technical Documentation

## CASE Tool - Architecture and Technical Details

### Table of Contents
1. Architecture Overview
2. Technology Stack
3. Database Design
4. API Architecture
5. Security Architecture
6. Performance Considerations
7. Scalability
8. Development Guide
9. Deployment Architecture
10. Monitoring and Logging

---

## 1. Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Frontend   │  │   Mobile     │  │   Third-     │     │
│  │   (HTML/JS)  │  │   Apps       │  │   party      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS/REST
┌──────────────────────▼──────────────────────────────────────┐
│                  API Gateway                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentication | Authorization | Rate Limiting       │  │
│  │  Request Validation | Response Formatting            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Application Server (FastAPI)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  REST API    │  │  Business    │  │  Data        │    │
│  │  Endpoints   │  │  Logic       │  │  Validation  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Estimation Engines (COCOMO, FPA, ML)                │  │
│  │  Report Generator | Cache Management                 │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ SQL
┌──────────────────────▼──────────────────────────────────────┐
│                 Data Layer                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database                                 │  │
│  │  - User Management | Projects | Estimates            │  │
│  │  - Cost Drivers | Historical Data | ML Models        │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Redis Cache (Optional)                              │  │
│  │  - Session Management | Query Results                │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.11
- **ORM**: SQLAlchemy 2.0.23
- **Database**: PostgreSQL 15+
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt + passlib
- **Validation**: Pydantic 2.5.0
- **Testing**: pytest 7.4.3
- **API Documentation**: Swagger/OpenAPI

### Frontend
- **Markup**: HTML5 (WCAG 2.1 AA)
- **Styling**: CSS3 with custom properties
- **Scripting**: Vanilla JavaScript (ES6+)
- **HTTP Client**: Fetch API
- **Architecture**: MVC (Model-View-Controller)
- **State Management**: LocalStorage + SessionStorage

### DevOps
- **Containerization**: Docker 20.10+
- **Orchestration**: Docker Compose / Kubernetes
- **Reverse Proxy**: nginx 1.20+
- **Process Manager**: gunicorn
- **Package Manager**: pip, npm

### Monitoring & Logging
- **Application Logging**: Python logging module
- **Metrics**: Prometheus (optional)
- **APM**: Application Performance Monitoring ready
- **Log Aggregation**: ELK Stack compatible

---

## 3. Database Design

### Database Schema Overview

```sql
-- Core Tables
├── users (Authentication & Authorization)
├── roles (Role-Based Access Control)
├── projects (Software Projects)
├── project_versions (Version Control)
├── estimates (Cost Estimates)
├── function_points (FPA Data)
├── cost_drivers (Cost Factors)
├── scale_factors (Scaling Multipliers)
├── historical_projects (Calibration Data)
├── scenarios (What-If Analysis)
├── risks (Risk Management)
├── resources (Team Allocation)
├── reports (Generated Reports)
├── audit_logs (Compliance Trail)
├── calibration_models (Model Calibration)
└── ml_models (Machine Learning Models)
```

### Table Relationships

```
users (1:N) projects
users (1:N) estimates
users (1:N) resources
projects (1:N) project_versions
project_versions (1:N) estimates
estimates (N:M) cost_drivers (via estimate_cost_drivers)
estimates (N:M) scale_factors (via estimate_scale_factors)
estimates (1:N) function_points
projects (1:N) scenarios
projects (1:N) risks
projects (1:N) resources
projects (1:N) reports
users (1:N) audit_logs
```

### Key Indexes
```sql
-- Performance critical indexes
INDEX idx_users_email ON users(email)
INDEX idx_projects_created_by ON projects(created_by)
INDEX idx_estimates_project_id ON estimates(project_id)
INDEX idx_estimates_status ON estimates(status)
INDEX idx_audit_logs_user_id ON audit_logs(user_id)
```

---

## 4. API Architecture

### API Versioning
- Current Version: v1
- Base Path: `/api/v1`
- Format: REST
- Versioning Strategy: URL-based

### Endpoint Organization
```
/api/v1/
├── /auth/ (Authentication)
│   ├── POST   /login
│   ├── POST   /refresh
│   ├── GET    /me
│   └── POST   /change-password
├── /users/ (User Management)
│   ├── POST   / (Register)
│   ├── GET    / (List)
│   ├── GET    /{id}
│   ├── PUT    /{id}
│   └── DELETE /{id}
├── /projects/ (Project Management)
│   ├── POST   /
│   ├── GET    /
│   ├── GET    /{id}
│   ├── PUT    /{id}
│   ├── DELETE /{id}
│   └── /versions (Project versions)
├── /estimates/ (Cost Estimation)
│   ├── POST   /
│   ├── GET    /
│   ├── GET    /{id}
│   ├── PUT    /{id}
│   └── /cost-drivers (Cost drivers)
├── /scenarios/ (What-If Analysis)
├── /risks/ (Risk Management)
├── /resources/ (Team Allocation)
├── /reports/ (Report Generation)
└── /ml-models/ (ML Predictions)
```

### Request/Response Cycle

1. **Request Validation**
   - Pydantic schema validation
   - Input sanitization
   - Type checking

2. **Authentication**
   - JWT token verification
   - User identity confirmation
   - Session validation

3. **Authorization**
   - Role-based access control
   - Resource ownership check
   - Permission validation

4. **Business Logic**
   - Database operations
   - Calculations
   - Rule application

5. **Response Formatting**
   - Serialization
   - Status code assignment
   - Error handling

---

## 5. Security Architecture

### Authentication
- **Method**: JWT (JSON Web Token)
- **Algorithm**: HS256
- **Token Types**:
  - Access Token: 30-minute expiration
  - Refresh Token: 7-day expiration

### Authorization
- **Model**: RBAC (Role-Based Access Control)
- **Roles**:
  - Admin: Full system access
  - Project Manager: Project and team management
  - Estimator: Estimation creation
  - Analyst: View and report generation
  - Viewer: Read-only access

### Password Security
- **Algorithm**: bcrypt with salt
- **Rounds**: 12
- **Minimum Length**: 8 characters
- **Requirements**: Mixed case, numbers, special chars (enforced)

### API Security
- **HTTPS**: Required in production
- **CORS**: Configurable origins
- **Rate Limiting**: 100 req/min per user
- **Request Signing**: Optional for critical endpoints
- **XSS Protection**: Content-Security-Policy headers
- **CSRF Protection**: SameSite cookie policy

### Data Protection
- **Encryption at Rest**: Database encryption (TDE)
- **Encryption in Transit**: TLS 1.3+
- **PII Handling**: Data minimization, retention policies
- **Backup**: Encrypted backups stored securely

---

## 6. Performance Considerations

### Query Optimization
- **N+1 Prevention**: Eager loading with SQLAlchemy
- **Index Strategy**: Composite indexes on foreign keys
- **Query Pagination**: Default limit 50, max 1000
- **Query Caching**: Redis for frequently accessed data

### Database Tuning
```sql
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
random_page_cost = 1.1
```

### Application Optimization
- **Response Compression**: gzip compression
- **Async Operations**: Long-running tasks in background
- **Connection Pooling**: PQPool with 20 connections
- **Static Asset Caching**: 1-year cache headers

### Monitoring Performance
```python
# Response time tracking
@app.middleware("http")
async def timing_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.url.path}: {duration:.3f}s")
    return response
```

### Typical Response Times
- Login: < 100ms
- Project List: < 200ms
- Estimate Creation: < 500ms
- Report Generation: 1-5s

---

## 7. Scalability

### Horizontal Scaling
- **Stateless Application**: No session affinity required
- **Load Balancing**: Round-robin or least-connection
- **Container Orchestration**: Kubernetes-ready
- **Auto-scaling**: Based on CPU/Memory metrics

### Vertical Scaling
- **Database**: PostgreSQL with replication
- **Cache**: Redis cluster for distributed caching
- **CDN**: CloudFront or similar for static assets

### Database Scalability
- **Read Replicas**: For read-heavy workloads
- **Partitioning**: Historical data sharding
- **Connection Pooling**: PgBouncer for connection management
- **Archive Strategy**: Move old data to archive

---

## 8. Development Guide

### Setup Development Environment
```bash
# Clone and setup
git clone <repo>
cd CaseTool/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env for local development

# Run tests
pytest -v

# Start development server
python run.py
```

### Code Structure
```
app/
├── api/v1/
│   ├── endpoints/     # Route handlers
│   └── router.py      # Route aggregation
├── core/
│   ├── config/        # Configuration
│   └── security/      # Auth & security
├── db/
│   └── base.py        # Database setup
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── services/          # Business logic
├── utils/             # Utilities
├── middleware/        # Middleware
└── main.py            # Application entry
```

### Coding Standards
- **Style**: PEP 8 with Black formatter
- **Linting**: Flake8 and Pylint
- **Type Hints**: Required for all functions
- **Documentation**: Docstrings on all modules/classes
- **Testing**: Minimum 80% coverage

### Git Workflow
```bash
# Feature branch
git checkout -b feature/my-feature

# Commit messages: type(scope): description
git commit -m "feat(auth): add two-factor authentication"

# Push and create PR
git push origin feature/my-feature
```

---

## 9. Deployment Architecture

### Development Deployment
```
Single Machine
├── Python (FastAPI)
├── PostgreSQL
└── nginx
```

### Production Deployment
```
Load Balancer (nginx)
├── App Server 1 (FastAPI + gunicorn)
├── App Server 2 (FastAPI + gunicorn)
└── App Server 3 (FastAPI + gunicorn)
    │
    └─→ PostgreSQL (Primary)
        ├── Replica 1 (Read)
        └── Replica 2 (Read)
        │
        └─→ Redis Cache
            └── Cluster Nodes
```

### Container Orchestration (Kubernetes)
```
Ingress (nginx)
    ↓
Load Balancer Service
    ↓
Backend Pod (×3)
├── Liveness Probe: /health
├── Readiness Probe: /health
└── Startup Probe: /health
    ↓
Database StatefulSet (PostgreSQL)
└── Persistent Volume
```

---

## 10. Monitoring and Logging

### Application Metrics
```python
# Key metrics tracked
- Request count (by endpoint, status code)
- Response time (min, max, avg, p95, p99)
- Error rate
- Cache hit ratio
- Database query performance
- User activity
```

### Logging Strategy
```python
import logging

# Structured logging
logger = logging.getLogger(__name__)
logger.info("user_login", extra={
    "user_id": user.id,
    "ip": request.client.host,
    "timestamp": datetime.utcnow().isoformat()
})
```

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": db_status(),
        "version": app_version
    }
```

### Alert Thresholds
- Error rate > 1%: Warning
- Response time > 2s (p95): Alert
- Database connections > 80%: Alert
- Disk usage > 85%: Warning

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [COCOMO Model](https://en.wikipedia.org/wiki/COCOMO)
- [Function Points Analysis](https://en.wikipedia.org/wiki/Function_point)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

---

**Version**: 1.0.0  
**Last Updated**: April 30, 2026
