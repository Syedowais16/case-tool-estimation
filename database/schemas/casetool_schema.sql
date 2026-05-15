-- CASE Tool Database Schema
-- PostgreSQL DDL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS uuid-ossp;

-- Roles table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    phone VARCHAR(20),
    organization VARCHAR(255),
    department VARCHAR(255),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'planning' NOT NULL,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    budget FLOAT,
    team_size INTEGER,
    client_name VARCHAR(255),
    project_manager VARCHAR(255),
    department VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Project Versions table
CREATE TABLE IF NOT EXISTS project_versions (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    description TEXT,
    scope TEXT,
    assumptions TEXT,
    constraints TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(project_id, version_number)
);

-- Estimates table
CREATE TABLE IF NOT EXISTS estimates (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version_id INTEGER NOT NULL REFERENCES project_versions(id),
    created_by INTEGER NOT NULL REFERENCES users(id),
    estimation_method VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft' NOT NULL,
    estimated_effort_hours FLOAT NOT NULL,
    estimated_duration_months FLOAT NOT NULL,
    estimated_cost FLOAT NOT NULL,
    estimated_team_size INTEGER,
    confidence_level INTEGER,
    confidence_interval_low FLOAT,
    confidence_interval_high FLOAT,
    actual_effort_hours FLOAT,
    actual_duration_months FLOAT,
    actual_cost FLOAT,
    actual_team_size INTEGER,
    notes TEXT,
    assumptions TEXT,
    risks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Cost Drivers table
CREATE TABLE IF NOT EXISTS cost_drivers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    impact_factor FLOAT NOT NULL,
    effort_multiplier FLOAT NOT NULL,
    cost_multiplier FLOAT NOT NULL,
    duration_multiplier FLOAT DEFAULT 1.0 NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Scale Factors table
CREATE TABLE IF NOT EXISTS scale_factors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    factor_value FLOAT NOT NULL,
    factor_type VARCHAR(100) NOT NULL,
    applies_to VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Function Points table
CREATE TABLE IF NOT EXISTS function_points (
    id SERIAL PRIMARY KEY,
    estimate_id INTEGER NOT NULL REFERENCES estimates(id) ON DELETE CASCADE,
    ilf_count INTEGER NOT NULL DEFAULT 0,
    ilf_complexity VARCHAR(20),
    ilf_contribution FLOAT,
    eif_count INTEGER NOT NULL DEFAULT 0,
    eif_complexity VARCHAR(20),
    eif_contribution FLOAT,
    ei_count INTEGER NOT NULL DEFAULT 0,
    ei_complexity VARCHAR(20),
    ei_contribution FLOAT,
    eo_count INTEGER NOT NULL DEFAULT 0,
    eo_complexity VARCHAR(20),
    eo_contribution FLOAT,
    eq_count INTEGER NOT NULL DEFAULT 0,
    eq_complexity VARCHAR(20),
    eq_contribution FLOAT,
    unadjusted_fp FLOAT NOT NULL,
    vaf FLOAT,
    adjusted_fp FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Estimate Cost Drivers junction table
CREATE TABLE IF NOT EXISTS estimate_cost_drivers (
    estimate_id INTEGER NOT NULL REFERENCES estimates(id) ON DELETE CASCADE,
    cost_driver_id INTEGER NOT NULL REFERENCES cost_drivers(id),
    PRIMARY KEY(estimate_id, cost_driver_id)
);

-- Estimate Scale Factors junction table
CREATE TABLE IF NOT EXISTS estimate_scale_factors (
    estimate_id INTEGER NOT NULL REFERENCES estimates(id) ON DELETE CASCADE,
    scale_factor_id INTEGER NOT NULL REFERENCES scale_factors(id),
    PRIMARY KEY(estimate_id, scale_factor_id)
);

-- Historical Projects table
CREATE TABLE IF NOT EXISTS historical_projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    project_type VARCHAR(100),
    team_experience VARCHAR(50),
    actual_effort_hours FLOAT NOT NULL,
    actual_duration_months FLOAT NOT NULL,
    actual_cost FLOAT NOT NULL,
    team_size INTEGER NOT NULL,
    language VARCHAR(100),
    database_type VARCHAR(100),
    architecture VARCHAR(100),
    scope_description TEXT,
    productivity FLOAT,
    defect_density FLOAT,
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Scenarios table
CREATE TABLE IF NOT EXISTS scenarios (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    scenario_type VARCHAR(50) NOT NULL,
    effort_adjustment FLOAT DEFAULT 1.0,
    duration_adjustment FLOAT DEFAULT 1.0,
    cost_adjustment FLOAT DEFAULT 1.0,
    team_size_adjustment FLOAT DEFAULT 1.0,
    estimated_effort FLOAT,
    estimated_duration FLOAT,
    estimated_cost FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Risks table
CREATE TABLE IF NOT EXISTS risks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    probability FLOAT NOT NULL,
    impact FLOAT NOT NULL,
    mitigation_strategy TEXT,
    owner VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    effort_contingency FLOAT DEFAULT 0,
    cost_contingency FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Resources table
CREATE TABLE IF NOT EXISTS resources (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    role VARCHAR(100) NOT NULL,
    allocation_percentage FLOAT NOT NULL,
    hourly_rate FLOAT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    skills TEXT,
    availability VARCHAR(50) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    content TEXT,
    format VARCHAR(20) DEFAULT 'html',
    generated_by INTEGER REFERENCES users(id),
    include_confidence_intervals BOOLEAN DEFAULT TRUE,
    include_risks BOOLEAN DEFAULT TRUE,
    include_scenarios BOOLEAN DEFAULT TRUE,
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Audit Logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id INTEGER NOT NULL,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Calibration Models table
CREATE TABLE IF NOT EXISTS calibration_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    model_type VARCHAR(100) NOT NULL,
    organization VARCHAR(255),
    industry VARCHAR(100),
    calibration_data_count INTEGER NOT NULL,
    accuracy_percentage FLOAT,
    coefficients JSONB,
    r_squared FLOAT,
    rmse FLOAT,
    mae FLOAT,
    last_calibration_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ML Models table
CREATE TABLE IF NOT EXISTS ml_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    model_type VARCHAR(100) NOT NULL,
    algorithm VARCHAR(100) NOT NULL,
    training_data_count INTEGER NOT NULL,
    feature_count INTEGER NOT NULL,
    feature_names JSONB,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    model_path VARCHAR(500),
    model_version VARCHAR(50),
    training_date TIMESTAMP,
    last_retraining_date TIMESTAMP,
    next_retraining_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_production BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_projects_created_by ON projects(created_by);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_estimates_project_id ON estimates(project_id);
CREATE INDEX idx_estimates_status ON estimates(status);
CREATE INDEX idx_function_points_estimate_id ON function_points(estimate_id);
CREATE INDEX idx_scenarios_project_id ON scenarios(project_id);
CREATE INDEX idx_risks_project_id ON risks(project_id);
CREATE INDEX idx_resources_project_id ON resources(project_id);
CREATE INDEX idx_resources_user_id ON resources(user_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);

-- Create Comments for documentation
COMMENT ON TABLE roles IS 'User roles for RBAC (Role-Based Access Control)';
COMMENT ON TABLE users IS 'User accounts and authentication';
COMMENT ON TABLE projects IS 'Software projects to be estimated';
COMMENT ON TABLE estimates IS 'Cost and effort estimates for projects';
COMMENT ON TABLE cost_drivers IS 'Factors affecting project costs';
COMMENT ON TABLE function_points IS 'Function point analysis data';
COMMENT ON TABLE historical_projects IS 'Historical project data for calibration';
COMMENT ON TABLE scenarios IS 'What-if scenarios for sensitivity analysis';
COMMENT ON TABLE risks IS 'Project risks and contingencies';
COMMENT ON TABLE audit_logs IS 'Audit trail for compliance';
