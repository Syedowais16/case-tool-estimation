# Database Schema Documentation

## CASE Tool Database Schema

### Overview
- **Database System**: PostgreSQL 15+
- **Total Tables**: 16
- **Total Indexes**: 44+
- **Relationships**: Foreign keys with cascade operations
- **Extensions**: UUID support

---

## Table Descriptions

### 1. roles
**Purpose**: Define user roles and permissions

```sql
CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  permissions TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Roles**:
- `admin`: Full system access
- `project_manager`: Project management
- `estimator`: Estimation creation
- `analyst`: Analysis and reporting
- `viewer`: Read-only access

---

### 2. users
**Purpose**: User accounts and authentication

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(100) UNIQUE NOT NULL,
  full_name VARCHAR(255),
  hashed_password VARCHAR(255) NOT NULL,
  role_id INTEGER REFERENCES roles(id),
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes**:
- `idx_users_email`: For login performance
- `idx_users_username`: For unique validation

---

### 3. projects
**Purpose**: Software projects being estimated

```sql
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  created_by INTEGER REFERENCES users(id),
  status VARCHAR(50),
  budget DECIMAL(15, 2),
  team_size INTEGER,
  client_name VARCHAR(255),
  project_manager VARCHAR(255),
  department VARCHAR(100),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Status Values**:
- `planning`: Initial phase
- `in_progress`: Active development
- `completed`: Finished
- `on_hold`: Temporarily paused
- `archived`: Historical

---

### 4. project_versions
**Purpose**: Track project version history

```sql
CREATE TABLE project_versions (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  version_number VARCHAR(50),
  description TEXT,
  created_by INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 5. estimates
**Purpose**: Cost and effort estimates

```sql
CREATE TABLE estimates (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  version_id INTEGER REFERENCES project_versions(id),
  estimation_method VARCHAR(50),
  estimated_effort_hours DECIMAL(10, 2),
  estimated_duration_months DECIMAL(10, 2),
  estimated_cost DECIMAL(15, 2),
  estimated_team_size INTEGER,
  confidence_level INTEGER,
  confidence_interval_low DECIMAL(15, 2),
  confidence_interval_high DECIMAL(15, 2),
  notes TEXT,
  assumptions TEXT,
  status VARCHAR(50),
  created_by INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Methods**:
- `COCOMO`: Constructive Cost Model
- `FPA`: Function Points Analysis
- `Hybrid`: Combined approach

---

### 6. function_points
**Purpose**: Function point analysis data

```sql
CREATE TABLE function_points (
  id SERIAL PRIMARY KEY,
  estimate_id INTEGER REFERENCES estimates(id) ON DELETE CASCADE,
  ilf_count INTEGER,
  ilf_complexity VARCHAR(50),
  eif_count INTEGER,
  eif_complexity VARCHAR(50),
  ei_count INTEGER,
  ei_complexity VARCHAR(50),
  eo_count INTEGER,
  eo_complexity VARCHAR(50),
  eq_count INTEGER,
  eq_complexity VARCHAR(50),
  unadjusted_fp DECIMAL(10, 2),
  vaf DECIMAL(5, 2),
  adjusted_fp DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 7. cost_drivers
**Purpose**: Configurable cost multiplier factors

```sql
CREATE TABLE cost_drivers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  category VARCHAR(50),
  impact_factor DECIMAL(5, 2),
  effort_multiplier DECIMAL(5, 2),
  cost_multiplier DECIMAL(5, 2),
  duration_multiplier DECIMAL(5, 2),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Categories**:
- reliability
- database_size
- complexity
- time_constraints
- team_experience
- tools
- methodology
- integration
- architecture
- security

---

### 8. scale_factors
**Purpose**: Scaling adjustment factors

```sql
CREATE TABLE scale_factors (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  factor_value DECIMAL(5, 2),
  factor_type VARCHAR(50),
  applies_to VARCHAR(50),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 9. historical_projects
**Purpose**: Historical data for calibration

```sql
CREATE TABLE historical_projects (
  id SERIAL PRIMARY KEY,
  project_name VARCHAR(255),
  industry VARCHAR(100),
  project_type VARCHAR(100),
  team_experience VARCHAR(50),
  actual_effort_hours DECIMAL(10, 2),
  actual_duration_months DECIMAL(10, 2),
  actual_cost DECIMAL(15, 2),
  team_size INTEGER,
  language VARCHAR(100),
  database_type VARCHAR(100),
  architecture VARCHAR(100),
  scope_description TEXT,
  productivity DECIMAL(10, 2),
  defect_density DECIMAL(10, 4),
  source VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 10. estimate_cost_drivers (Junction)
**Purpose**: Association between estimates and cost drivers

```sql
CREATE TABLE estimate_cost_drivers (
  id SERIAL PRIMARY KEY,
  estimate_id INTEGER REFERENCES estimates(id) ON DELETE CASCADE,
  cost_driver_id INTEGER REFERENCES cost_drivers(id) ON DELETE CASCADE,
  multiplier DECIMAL(5, 2),
  UNIQUE(estimate_id, cost_driver_id)
);
```

---

### 11. estimate_scale_factors (Junction)
**Purpose**: Association between estimates and scale factors

```sql
CREATE TABLE estimate_scale_factors (
  id SERIAL PRIMARY KEY,
  estimate_id INTEGER REFERENCES estimates(id) ON DELETE CASCADE,
  scale_factor_id INTEGER REFERENCES scale_factors(id) ON DELETE CASCADE,
  multiplier DECIMAL(5, 2),
  UNIQUE(estimate_id, scale_factor_id)
);
```

---

### 12. scenarios
**Purpose**: What-if scenarios

```sql
CREATE TABLE scenarios (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  scenario_type VARCHAR(50),
  effort_adjustment DECIMAL(5, 2),
  duration_adjustment DECIMAL(5, 2),
  cost_adjustment DECIMAL(5, 2),
  team_size_adjustment DECIMAL(5, 2),
  created_by INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 13. risks
**Purpose**: Project risk management

```sql
CREATE TABLE risks (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  category VARCHAR(50),
  probability DECIMAL(5, 2),
  impact DECIMAL(5, 2),
  mitigation_strategy TEXT,
  owner VARCHAR(255),
  status VARCHAR(50),
  effort_contingency DECIMAL(10, 2),
  cost_contingency DECIMAL(15, 2),
  created_by INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 14. resources
**Purpose**: Team allocation and resources

```sql
CREATE TABLE resources (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id),
  role VARCHAR(100),
  allocation_percentage INTEGER,
  start_date DATE,
  end_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 15. reports
**Purpose**: Generated reports

```sql
CREATE TABLE reports (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  report_type VARCHAR(50),
  format VARCHAR(20),
  content BYTEA,
  created_by INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 16. audit_logs
**Purpose**: Compliance and audit trail

```sql
CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  action VARCHAR(255),
  resource_type VARCHAR(100),
  resource_id INTEGER,
  old_values JSONB,
  new_values JSONB,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Indexes

### Performance Indexes
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_projects_created_by ON projects(created_by);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_estimates_project_id ON estimates(project_id);
CREATE INDEX idx_estimates_version_id ON estimates(version_id);
CREATE INDEX idx_estimates_status ON estimates(status);
CREATE INDEX idx_function_points_estimate_id ON function_points(estimate_id);
CREATE INDEX idx_cost_drivers_active ON cost_drivers(is_active);
CREATE INDEX idx_historical_projects_industry ON historical_projects(industry);
CREATE INDEX idx_scenarios_project_id ON scenarios(project_id);
CREATE INDEX idx_risks_project_id ON risks(project_id);
CREATE INDEX idx_resources_project_id ON resources(project_id);
CREATE INDEX idx_resources_user_id ON resources(user_id);
CREATE INDEX idx_reports_project_id ON reports(project_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

## Constraints

### Foreign Keys
All foreign keys use `ON DELETE CASCADE` for orphan prevention.

### Unique Constraints
- `users.email` - Globally unique
- `users.username` - Globally unique
- `roles.name` - Globally unique
- `cost_drivers.name` - Globally unique
- `scale_factors.name` - Globally unique

---

## Performance Considerations

### Query Optimization
1. **Join Optimization**: Use proper indexes on foreign keys
2. **Pagination**: Always use LIMIT with OFFSET
3. **Selective Projections**: Only SELECT needed columns
4. **Connection Pooling**: PgBouncer recommended

### Typical Query Performance
- Simple SELECT: < 5ms
- JOIN (2 tables): < 10ms
- Complex JOIN (4+ tables): < 50ms
- Aggregate queries: < 100ms

---

## Backup Strategy

### Regular Backups
- Full backup daily at 2 AM
- Incremental backups every 4 hours
- 7-day retention policy
- Test restore weekly

### Backup Location
- Primary: Encrypted storage
- Secondary: Cloud backup (AWS S3, Azure Blob)

---

## Maintenance

### Vacuum & Analyze
```sql
-- Daily maintenance
VACUUM ANALYZE;

-- Full vacuum (weekly)
VACUUM FULL;
```

### Statistics Update
```sql
-- Update table statistics
ANALYZE;
```

---

## Migration Path

### Adding New Tables
1. Create migration script
2. Test in development
3. Apply in staging
4. Backup production
5. Apply in production

### Removing Tables
1. Archive data (if needed)
2. Create backup
3. Drop table
4. Update application

---

**Version**: 1.0.0
**Last Updated**: April 30, 2026
