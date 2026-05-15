# Installation Guide

## CASE Tool - Enterprise Software Cost Estimation Platform

### System Requirements

#### Minimum Requirements
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB SSD
- Operating System: Linux, macOS, or Windows with Docker

#### Recommended Requirements
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+ SSD
- Operating System: Linux (Ubuntu 20.04 LTS or later)

### Prerequisites

1. **Docker** (v20.10+)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install docker.io docker-compose
   
   # macOS
   brew install docker docker-compose
   ```

2. **Git**
   ```bash
   sudo apt-get install git  # Ubuntu/Debian
   brew install git          # macOS
   ```

3. **PostgreSQL Client** (optional, for direct database access)
   ```bash
   sudo apt-get install postgresql-client
   ```

---

## Quick Start with Docker Compose

### 1. Clone Repository
```bash
git clone https://github.com/your-org/casetool.git
cd CaseTool
```

### 2. Configure Environment
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and change SECRET_KEY and other settings
```

### 3. Build and Start Services
```bash
cd deployment/docker
docker-compose up -d
```

### 4. Initialize Database
```bash
bash ../../deployment/scripts/init_db.sh
```

### 5. Access Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

### 6. Create Admin User
```bash
docker-compose exec backend python -c "
from app.models.user_models import Role, User
from app.db.base import SessionLocal, engine, Base
from app.core.security.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Create admin role
admin_role = Role(name='admin', description='Admin', permissions='*')
db.add(admin_role)
db.commit()

# Create admin user
admin = User(
    email='admin@example.com',
    username='admin',
    full_name='Administrator',
    hashed_password=get_password_hash('admin123'),
    role_id=admin_role.id,
    is_active=True,
    is_verified=True
)
db.add(admin)
db.commit()
print('Admin user created: admin@example.com / admin123')
"
```

---

## Manual Installation

### 1. Install Backend Dependencies

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure PostgreSQL

```bash
# Start PostgreSQL server
sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql <<EOF
CREATE USER casetool WITH PASSWORD 'casetool';
CREATE DATABASE casetool_db OWNER casetool;
ALTER ROLE casetool SET client_encoding TO 'utf8';
ALTER ROLE casetool SET default_transaction_isolation TO 'read committed';
ALTER ROLE casetool SET default_transaction_deferrable TO on;
ALTER ROLE casetool SET default_transaction_read_committed TO on;
EOF
```

### 3. Initialize Database Schema

```bash
cd database
psql -h localhost -U casetool -d casetool_db -f schemas/casetool_schema.sql
```

### 4. Seed Initial Data

```bash
# Create CSV import script
python3 <<'EOF'
import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine('postgresql://casetool:casetool@localhost:5432/casetool_db')

# Load and insert CSV data
seeds_dir = 'seeds/'

# Roles
roles_df = pd.read_csv(os.path.join(seeds_dir, 'roles.csv'))
roles_df.to_sql('roles', engine, if_exists='append', index=False)

# Cost drivers
drivers_df = pd.read_csv(os.path.join(seeds_dir, 'cost_drivers.csv'))
drivers_df.to_sql('cost_drivers', engine, if_exists='append', index=False)

# Scale factors
factors_df = pd.read_csv(os.path.join(seeds_dir, 'scale_factors.csv'))
factors_df.to_sql('scale_factors', engine, if_exists='append', index=False)

# Historical projects
history_df = pd.read_csv(os.path.join(seeds_dir, 'historical_projects.csv'))
history_df.to_sql('historical_projects', engine, if_exists='append', index=False)

print("Data seeding completed!")
EOF
```

### 5. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

Key settings:
```
DATABASE_URL=postgresql://casetool:casetool@localhost:5432/casetool_db
SECRET_KEY=your-very-secure-secret-key-here
ENVIRONMENT=production
DEBUG=False
```

### 6. Run Backend

```bash
cd backend
python run.py
```

Backend will start at `http://localhost:8000`

### 7. Setup Frontend

```bash
cd frontend

# For development
python -m http.server 5500

# For production
# Use your preferred web server (nginx, Apache, etc.)
```

Frontend accessible at `http://localhost:5500`

---

## Production Deployment

### 1. Using Kubernetes

```bash
# Create namespace
kubectl create namespace casetool

# Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# Verify deployment
kubectl get pods -n casetool
```

### 2. Using Docker Compose (Production)

```bash
# Set production environment
export ENVIRONMENT=production
export DEBUG=False

# Deploy with production settings
docker-compose -f deployment/docker/docker-compose.yml up -d
```

### 3. Setup Reverse Proxy (nginx)

```bash
# Install nginx
sudo apt-get install nginx

# Copy nginx config
sudo cp deployment/docker/nginx.conf /etc/nginx/sites-available/casetool

# Enable site
sudo ln -s /etc/nginx/sites-available/casetool /etc/nginx/sites-enabled/

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Enable HTTPS

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

## Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U casetool -d casetool_db
```

### Backend Not Starting
```bash
# Check logs
docker-compose logs backend

# Verify environment variables
docker-compose exec backend env
```

### Frontend Not Loading
```bash
# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Check API connectivity
curl -I http://localhost:8000/health
```

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :8000
sudo lsof -i :5432
sudo lsof -i :80

# Kill process
kill -9 <PID>
```

---

## Backup and Recovery

### Automated Backup
```bash
# Setup daily backup
0 2 * * * /path/to/deployment/scripts/backup_db.sh
```

### Manual Backup
```bash
pg_dump -h localhost -U casetool casetool_db > backup.sql
```

### Restore from Backup
```bash
psql -h localhost -U casetool casetool_db < backup.sql
```

---

## Updates

### Update Backend
```bash
cd backend
git pull origin main
pip install -r requirements.txt
python run.py
```

### Update Database Schema
```bash
python -m alembic upgrade head
```

---

## Health Checks

### Verify Installation
```bash
# Health check endpoint
curl http://localhost:8000/health

# API documentation
curl http://localhost:8000/docs

# Frontend access
curl http://localhost
```

---

## Performance Tuning

### PostgreSQL
```sql
-- postgresql.conf optimizations
shared_buffers = 256MB
effective_cache_size = 1GB
max_connections = 200
```

### Application
- Enable caching
- Use CDN for static assets
- Enable database connection pooling
- Monitor with Prometheus/Grafana

---

## Security Hardening

1. Change default credentials
2. Enable HTTPS/SSL
3. Configure firewall rules
4. Set up regular backups
5. Enable audit logging
6. Regular security updates
7. Use strong SECRET_KEY
8. Implement rate limiting

---

## Support

For issues and support:
- Documentation: See docs/ directory
- Issues: GitHub Issues
- Email: support@example.com
