# Deployment Guide

## CASE Tool Deployment

This guide covers deployment strategies for different environments.

## Development Environment

### Quick Start
```bash
cd deployment/docker
docker-compose up -d
bash ../../deployment/scripts/init_db.sh
```

**Access:**
- Frontend: http://localhost
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Staging Environment

### Setup
```bash
# 1. Clone repository
git clone https://github.com/your-org/casetool.git
cd CaseTool

# 2. Checkout staging branch
git checkout staging

# 3. Build images
docker build -f deployment/docker/Dockerfile.backend -t casetool-backend:staging .
docker build -f deployment/docker/Dockerfile.frontend -t casetool-frontend:staging .

# 4. Tag for registry
docker tag casetool-backend:staging your-registry.azurecr.io/casetool-backend:staging
docker tag casetool-frontend:staging your-registry.azurecr.io/casetool-frontend:staging

# 5. Push to registry
docker push your-registry.azurecr.io/casetool-backend:staging
docker push your-registry.azurecr.io/casetool-frontend:staging

# 6. Deploy with Kubernetes
kubectl set image deployment/casetool-backend casetool-backend=your-registry.azurecr.io/casetool-backend:staging -n casetool
kubectl set image deployment/casetool-frontend casetool-frontend=your-registry.azurecr.io/casetool-frontend:staging -n casetool
```

---

## Production Environment

### Prerequisites
- Kubernetes cluster (1.24+)
- Docker registry (Docker Hub, ACR, ECR, etc.)
- PostgreSQL managed database (RDS, Cloud SQL, etc.)
- SSL/TLS certificates
- Domain name with DNS setup

### Deployment Strategy

#### 1. Build and Push Images
```bash
# Build with production tag
docker build -f deployment/docker/Dockerfile.backend \
  -t your-registry.azurecr.io/casetool-backend:1.0.0 .

docker build -f deployment/docker/Dockerfile.frontend \
  -t your-registry.azurecr.io/casetool-frontend:1.0.0 .

# Push to registry
docker push your-registry.azurecr.io/casetool-backend:1.0.0
docker push your-registry.azurecr.io/casetool-frontend:1.0.0
```

#### 2. Create Namespace
```bash
kubectl create namespace casetool-prod
kubectl label namespace casetool-prod environment=production
```

#### 3. Create Secrets
```bash
# Database credentials
kubectl create secret generic casetool-db-secret \
  --from-literal=DATABASE_USER=casetool \
  --from-literal=DATABASE_PASSWORD=YOUR_SECURE_PASSWORD \
  -n casetool-prod

# Application secrets
kubectl create secret generic casetool-app-secret \
  --from-literal=SECRET_KEY=YOUR_SECURE_KEY \
  -n casetool-prod

# Image registry credentials
kubectl create secret docker-registry regcred \
  --docker-server=your-registry.azurecr.io \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_PASSWORD \
  -n casetool-prod
```

#### 4. Update Manifests
Edit `deployment/kubernetes/deployment.yaml`:
```yaml
# Update image references
image: your-registry.azurecr.io/casetool-backend:1.0.0

# Update database URL
- name: DATABASE_URL
  value: "postgresql://casetool:password@prod-db-host:5432/casetool_db"

# Update host
- host: casetool.yourdomain.com
```

#### 5. Deploy
```bash
kubectl apply -f deployment/kubernetes/deployment.yaml -n casetool-prod
```

#### 6. Verify Deployment
```bash
# Check pods
kubectl get pods -n casetool-prod

# Check services
kubectl get services -n casetool-prod

# Check ingress
kubectl get ingress -n casetool-prod

# View logs
kubectl logs deployment/casetool-backend -n casetool-prod
```

### SSL/TLS Configuration

#### With cert-manager
```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Update ingress with annotation
annotations:
  cert-manager.io/cluster-issuer: letsencrypt-prod
  tls:
  - hosts:
    - casetool.yourdomain.com
    secretName: casetool-tls
```

---

## Blue-Green Deployment

### Setup
```bash
# Deploy blue environment (current)
kubectl apply -f deployment/kubernetes/deployment-blue.yaml

# Deploy green environment (new)
kubectl apply -f deployment/kubernetes/deployment-green.yaml

# Switch traffic to green
kubectl patch service casetool-frontend -p '{"spec":{"selector":{"version":"green"}}}'

# Verify green is healthy
# If issues, switch back:
kubectl patch service casetool-frontend -p '{"spec":{"selector":{"version":"blue"}}}'
```

---

## Canary Deployment

### Using Flagger
```bash
# Install Flagger
kubectl apply -k github.com/fluxcd/flagger//kustomize/istio

# Create Canary resource
kubectl apply -f - <<EOF
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: casetool-backend
  namespace: casetool-prod
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: casetool-backend
  progressDeadlineSeconds: 300
  service:
    port: 8000
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
EOF
```

---

## Database Migration

### Pre-Deployment
```bash
# Backup current database
bash deployment/scripts/backup_db.sh

# Test migration in staging
python -m alembic upgrade head --sql
```

### Post-Deployment
```bash
# Apply migrations
kubectl exec -it deployment/casetool-backend -- python -m alembic upgrade head

# Seed initial data if needed
bash deployment/scripts/init_db.sh
```

---

## Monitoring Deployment

### Health Checks
```bash
# Check backend health
kubectl exec -it deployment/casetool-backend -- curl localhost:8000/health

# Check database connection
kubectl exec -it deployment/casetool-backend -- python -c \
  "from app.db.base import SessionLocal; print('DB OK')"

# Check frontend
kubectl exec -it deployment/casetool-frontend -- curl localhost/health
```

### Logs
```bash
# View deployment logs
kubectl logs deployment/casetool-backend -n casetool-prod -f

# View previous logs (if pod restarted)
kubectl logs deployment/casetool-backend -n casetool-prod --previous

# View events
kubectl describe deployment casetool-backend -n casetool-prod
```

---

## Rollback

### Kubernetes Rollback
```bash
# Check rollout history
kubectl rollout history deployment/casetool-backend -n casetool-prod

# Rollback to previous version
kubectl rollout undo deployment/casetool-backend -n casetool-prod

# Rollback to specific revision
kubectl rollout undo deployment/casetool-backend --to-revision=2 -n casetool-prod
```

### Database Rollback
```bash
# List backups
ls -la backups/

# Restore from backup
psql -h prod-db-host -U casetool -d casetool_db < backups/casetool_backup_20260430_100000.sql
```

---

## Performance Tuning

### Pod Resources
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### Database Optimization
```sql
-- Connection pooling with PgBouncer
-- In pgbouncer.ini:
[databases]
casetool_db = host=prod-db-host port=5432 dbname=casetool_db

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### Caching
```yaml
# Add Redis for caching
- name: redis
  image: redis:7-alpine
  ports:
  - containerPort: 6379
```

---

## Backup & Recovery

### Automated Backups
```bash
# Create CronJob for daily backups
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: casetool-backup
  namespace: casetool-prod
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15-alpine
            command: ["bash", "-c", "bash /scripts/backup_db.sh"]
            volumeMounts:
            - name: scripts
              mountPath: /scripts
            - name: backups
              mountPath: /backups
          volumes:
          - name: scripts
            configMap:
              name: backup-scripts
          - name: backups
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
EOF
```

---

## Support and Troubleshooting

### Common Issues

**Pod not starting**
```bash
kubectl describe pod <pod-name> -n casetool-prod
kubectl logs <pod-name> -n casetool-prod
```

**Database connection error**
```bash
# Check database credentials
kubectl get secret casetool-db-secret -n casetool-prod -o yaml

# Test connection
kubectl exec -it deployment/casetool-backend -- \
  psql postgresql://user:password@host:5432/dbname
```

**Service not accessible**
```bash
# Check service
kubectl get svc casetool-frontend -n casetool-prod

# Test from pod
kubectl exec -it deployment/casetool-backend -- curl casetool-frontend:80
```

---

## Contact

- **Deployment Support**: devops@casetool.example.com
- **Issues**: Open GitHub issue
- **Documentation**: See docs/ directory
