# CASE Tool - Enterprise Software Cost Estimation Platform

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-org/casetool)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-blue.svg)](https://fastapi.tiangolo.com/)
[![WCAG](https://img.shields.io/badge/WCAG-2.1%20AA-green.svg)](https://www.w3.org/WAI/WCAG21/quickref/)

A comprehensive, production-ready enterprise-grade Software Cost Estimation CASE Tool built with Python FastAPI and modern web technologies.

## 🚀 Features

### Core Functionality
- ✅ **Multiple Estimation Methods**: COCOMO, Function Points, Hybrid approaches
- ✅ **Project Management**: Create, track, and manage software projects
- ✅ **Cost Estimation**: Accurate effort, duration, and cost calculations
- ✅ **Cost Drivers**: Industry-standard cost factors and multipliers
- ✅ **What-If Scenarios**: Sensitivity analysis with multiple scenarios
- ✅ **Risk Management**: Identify, track, and manage project risks
- ✅ **Historical Analysis**: Calibrate estimates with actual project data
- ✅ **Advanced Reporting**: Comprehensive reports with charts and analysis
- ✅ **ML-Ready**: Architecture supports machine learning model integration

### Enterprise Features
- 🔐 **Role-Based Access Control**: Admin, Project Manager, Estimator, Analyst, Viewer
- 🔐 **JWT Authentication**: Secure token-based authentication
- 📊 **Audit Logging**: Complete audit trail for compliance
- 🌐 **Multi-Tenant Ready**: Scalable architecture for multiple organizations
- 🔄 **Data Export**: Export estimates and reports in multiple formats
- 📈 **Performance Metrics**: Track estimation accuracy over time
- 🔔 **Notifications**: Alert on project milestones and updates

### Accessibility & Compliance
- ♿ **WCAG 2.1 Level AA**: Full accessibility compliance
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🌐 **Internationalization Ready**: Support for multiple languages
- 📋 **SOC 2 Compliant**: Enterprise security standards

## 📋 Requirements

### System Requirements
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (for containerized deployment)
- 4GB RAM minimum (8GB recommended)
- 20GB storage minimum

### Software Requirements
- FastAPI 0.104+
- SQLAlchemy 2.0+
- Pydantic 2.5+
- PostgreSQL client

## 🚀 Quick Start

### With Docker Compose (Recommended)
```bash
# Clone repository
git clone https://github.com/your-org/casetool.git
cd CaseTool

# Configure environment
cp backend/.env.example backend/.env

# Build and start
cd deployment/docker
docker-compose up -d

# Initialize database
bash ../../deployment/scripts/init_db.sh

# Access application
# Frontend: http://localhost
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Manual Installation
See [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) for detailed setup instructions.

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION_GUIDE.md) - Setup and deployment instructions
- [User Manual](docs/user/USER_MANUAL.md) - Complete user guide
- [API Documentation](docs/api/API_DOCUMENTATION.md) - REST API reference
- [Technical Documentation](docs/technical/TECHNICAL_DOCUMENTATION.md) - Architecture and design

## 🏗️ Project Structure

```
CaseTool/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── core/              # Configuration & security
│   │   ├── db/                # Database setup
│   │   ├── utils/             # Utility functions
│   │   └── main.py            # Application entry
│   ├── tests/                 # Unit & integration tests
│   ├── requirements.txt        # Python dependencies
│   └── run.py                 # Development server
├── frontend/                   # Web frontend
│   ├── templates/             # HTML templates
│   ├── assets/
│   │   ├── css/               # Stylesheets
│   │   ├── js/                # JavaScript files
│   │   └── images/            # Assets
├── database/                   # Database resources
│   ├── schemas/               # SQL schemas
│   └── seeds/                 # Seed data (CSV)
├── deployment/                # Deployment configuration
│   ├── docker/                # Dockerfiles & compose
│   ├── kubernetes/            # K8s manifests
│   └── scripts/               # Deployment scripts
├── docs/                      # Documentation
│   ├── api/                   # API reference
│   ├── technical/             # Technical docs
│   └── user/                  # User guide
└── README.md                  # This file
```

## 🔑 Key Features

### Estimation Engines

**COCOMO (Constructive Cost Model)**
- Intermediate model with cost drivers
- Supports reliability, complexity, time constraints, team experience
- Automatic calculation of effort, duration, and cost

**Function Point Analysis (FPA)**
- Data function analysis (ILF, EIF)
- Transaction function analysis (EI, EO, EQ)
- Value Adjustment Factor (VAF) support
- Productivity metrics

**Hybrid Approach**
- Combines multiple estimation methods
- Weighted scoring
- Calibration with historical data

### Project Management
- Create and track projects
- Version control for estimates
- Team resource allocation
- Stakeholder management

### Analysis & Reporting
- What-if scenario analysis
- Risk assessment and tracking
- Historical project calibration
- Comprehensive report generation
- Export to multiple formats

## 🔐 Security

- **Authentication**: JWT-based with refresh tokens
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: AES-256 for sensitive data
- **Audit Logging**: Complete activity tracking
- **Input Validation**: Comprehensive validation on all inputs
- **HTTPS/TLS**: Required in production
- **CORS**: Configurable cross-origin policies
- **Rate Limiting**: Built-in rate limiting

## 📊 Database Schema

16 core tables with full referential integrity:
- users, roles - Authentication
- projects, project_versions - Project management
- estimates, function_points - Estimation data
- cost_drivers, scale_factors - Calibration factors
- scenarios, risks, resources - Project planning
- reports, audit_logs - Reporting and compliance
- calibration_models, ml_models - Advanced analysis

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/unit/test_security.py -v
```

Test Coverage:
- Unit Tests: Security, calculations, utilities
- Integration Tests: API endpoints, database operations
- End-to-End Tests: Complete workflows

## 🚀 Deployment

### Docker Compose (Development/Testing)
```bash
docker-compose -f deployment/docker/docker-compose.yml up -d
```

### Kubernetes (Production)
```bash
kubectl apply -f deployment/kubernetes/deployment.yaml
```

### Manual (Advanced)
See deployment scripts in `deployment/scripts/`

## 📈 Performance

- Response time: < 500ms (p95)
- API throughput: 100+ requests/second
- Database queries: Optimized with indexes
- Caching: Redis support for frequently accessed data
- Horizontal scaling: Stateless design

## 🔄 API Endpoints

### Core Endpoints
- `POST /auth/login` - User authentication
- `POST /projects` - Create project
- `POST /estimates` - Create estimate
- `GET /reports` - Generate reports
- `POST /scenarios` - Create scenarios

See [API Documentation](docs/api/API_DOCUMENTATION.md) for complete endpoint reference.

## 📱 Frontend

- **Framework**: Vanilla HTML5/CSS3/JavaScript
- **Accessibility**: WCAG 2.1 AA compliant
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Works without JavaScript
- **Performance**: Optimized asset delivery

## 🛠️ Technology Stack

**Backend**
- Python 3.11
- FastAPI 0.104
- SQLAlchemy 2.0
- PostgreSQL 15
- Pydantic 2.5

**Frontend**
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)
- Fetch API

**DevOps**
- Docker & Docker Compose
- Kubernetes
- nginx
- gunicorn

**Testing**
- pytest
- pytest-asyncio
- pytest-cov

## 📝 License

Proprietary - All rights reserved

## 👥 Contributing

For contribution guidelines, please see [CONTRIBUTING.md](CONTRIBUTING.md)

## 📞 Support

- **Documentation**: See docs/ directory
- **Issues**: [GitHub Issues](https://github.com/your-org/casetool/issues)
- **Email**: support@casetool.example.com
- **Training**: Available upon request

## 🎯 Roadmap

- [ ] Machine learning model integration
- [ ] Advanced Monte Carlo simulation
- [ ] Real-time collaboration
- [ ] Mobile native apps
- [ ] Advanced analytics dashboard
- [ ] Integration with project management tools
- [ ] CI/CD pipeline integration

## 📜 Acknowledgments

Built with modern Python technologies and best practices from enterprise software development.

---

**Version**: 1.0.0  
**Last Updated**: April 30, 2026  
**Status**: Production Ready
