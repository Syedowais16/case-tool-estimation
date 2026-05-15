#!/bin/bash
# Database initialization script

set -e

echo "Initializing CASE Tool Database..."

# Database credentials
DB_USER="${DB_USER:-casetool}"
DB_PASSWORD="${DB_PASSWORD:-casetool}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-casetool_db}"

echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Host: $DB_HOST:$DB_PORT"

# Wait for PostgreSQL
until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "\q" 2>/dev/null; do
    echo 'Waiting for PostgreSQL...'
    sleep 1
done

echo "PostgreSQL is ready!"

# Create schema
echo "Creating database schema..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f ./database/schemas/casetool_schema.sql

echo "Seeding initial data..."

# Seed roles
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME <<EOF
COPY roles (name, description, permissions) FROM STDIN WITH (FORMAT CSV, HEADER);
$(tail -n +2 ./database/seeds/roles.csv)
EOF

# Seed cost drivers
echo "Seeding cost drivers..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME <<EOF
COPY cost_drivers (name, description, category, impact_factor, effort_multiplier, cost_multiplier, duration_multiplier) FROM STDIN WITH (FORMAT CSV, HEADER);
$(tail -n +2 ./database/seeds/cost_drivers.csv)
EOF

# Seed scale factors
echo "Seeding scale factors..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME <<EOF
COPY scale_factors (name, description, factor_value, factor_type, applies_to) FROM STDIN WITH (FORMAT CSV, HEADER);
$(tail -n +2 ./database/seeds/scale_factors.csv)
EOF

# Seed historical projects
echo "Seeding historical projects..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME <<EOF
COPY historical_projects (project_name, industry, project_type, team_experience, actual_effort_hours, actual_duration_months, actual_cost, team_size, language, database_type, architecture, scope_description, productivity, defect_density, source) FROM STDIN WITH (FORMAT CSV, HEADER);
$(tail -n +2 ./database/seeds/historical_projects.csv)
EOF

echo "Database initialization complete!"
