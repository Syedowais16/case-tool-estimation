#!/bin/bash
# Production deployment script

set -e

echo "Deploying CASE Tool to Production..."

# Build Docker images
echo "Building Docker images..."
docker-compose -f deployment/docker/docker-compose.yml build

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f deployment/docker/docker-compose.yml down || true

# Pull latest code
echo "Pulling latest code..."
git pull origin main || true

# Start services
echo "Starting services..."
docker-compose -f deployment/docker/docker-compose.yml up -d

# Run migrations
echo "Running database migrations..."
docker-compose -f deployment/docker/docker-compose.yml exec -T backend python -m alembic upgrade head || true

# Seed initial data if needed
echo "Seeding initial data..."
bash deployment/scripts/init_db.sh || true

echo "Deployment completed!"
echo "Frontend: http://localhost"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
