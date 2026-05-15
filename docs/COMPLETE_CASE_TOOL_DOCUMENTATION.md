# CASE Tool / Software Project Estimation System Documentation

## 1. Project Overview

This project is a full-stack CASE Tool for software project estimation and delivery planning. It helps a project manager create projects, define scope versions, calculate estimates, compare estimation methods, track risks/resources/scenarios, use historical data, generate reports, and import planning data from Jira or Trello.

The system has three main layers:

- Frontend: a browser-based single-page application in `frontend/index.html` with JavaScript modules in `frontend/assets/js`.
- Backend: a FastAPI REST API in `backend/app` with authentication, database models, business endpoints, estimation services, reporting, notifications, and integrations.
- Database: SQLite for local/demo use through `backend/case_tool.db`; the settings also support PostgreSQL-style deployment.

Default local login:

- Email: `admin@example.com`
- Password: `admin123`

## 2. Problem Statement

Software estimation often fails because teams guess effort without enough historical evidence, ignore risk, confuse effort with duration, underestimate requirement change, or use one estimation method for every project. This tool solves that by connecting estimation formulas, project history, risk exposure, resource planning, ML prediction, and reporting in one workflow.

## 3. Objectives

- Provide structured project and version management.
- Support COCOMO, Function Point Analysis, Hybrid, and ML-based estimation.
- Store realistic historical project records for calibration and ML training.
- Show dashboard analytics for effort, cost, risk, productivity, and model quality.
- Explain every important UI field through tooltips.
- Support English and Urdu UI navigation architecture.
- Generate professional PDF/Excel/HTML/JSON reports.
- Support real Jira and Trello imports when credentials are configured.
- Provide beginner-friendly documentation for academic presentation.

## 4. Folder Structure

`backend/app/main.py` starts the FastAPI application, configures CORS, logging middleware, health checks, and the API router.

`backend/app/api/v1/router.py` combines all API modules under `/api/v1`.

`backend/app/api/v1/endpoints/auth.py` handles login, token refresh, current user lookup, and password changes.

`backend/app/api/v1/endpoints/users.py` manages users and roles.

`backend/app/api/v1/endpoints/projects.py` manages projects and project versions. When a project is created, an initial version is created automatically.

`backend/app/api/v1/endpoints/estimates.py` manages saved estimates, function points, historical projects, and calculation endpoints for COCOMO, FPA, Hybrid, and ML.

`backend/app/api/v1/endpoints/scenario_risk_resource.py` manages what-if scenarios, risks, and resource allocations.

`backend/app/api/v1/endpoints/reports.py` stores reports and exports project reports as PDF, Excel, HTML, or JSON.

`backend/app/api/v1/endpoints/dashboard.py` creates dynamic dashboard analytics from live database records.

`backend/app/api/v1/endpoints/notifications.py` creates in-app deadline, risk, reminder, and review notifications; email sending works when SMTP settings are configured.

`backend/app/api/v1/endpoints/integrations.py` connects to Jira and Trello APIs, imports work items, maps them to local projects, and stores sync history.

`backend/app/models` contains SQLAlchemy database tables.

`backend/app/schemas` contains Pydantic request/response validation models.

`backend/app/services/estimation_engine.py` contains the core COCOMO, FPA, Hybrid, and ML logic.

`backend/app/services/report_export_service.py` builds downloadable reports.

`backend/app/db/base.py` configures the database engine, creates tables, applies SQLite schema upgrades, seeds roles/admin user, and loads demo data.

`backend/app/db/seed_data.py` inserts 50+ realistic historical software project records plus projects, estimates, function points, risks, scenarios, resources, reports, calibration model metadata, ML metadata, and a starter notification.

`frontend/index.html` is the full SPA layout. It contains login/register screens, sidebar navigation, dashboard, projects, estimates, risks, resources, reports, intelligence, integrations, admin, and settings views.

`frontend/assets/js/api-client.js` is the API wrapper. It stores tokens, attaches Authorization headers, refreshes tokens, and exposes methods for every backend module.

`frontend/assets/js/ui-manager.js` controls rendering, forms, buttons, state, navigation, dashboard updates, tooltips, language selector, and frontend workflows.

`frontend/assets/css/style.css` defines the visual system, responsive layouts, cards, forms, dashboard charts, tooltips, alerts, and RTL support.

## 5. Database Flow

The database uses SQLAlchemy models. On startup:

1. `main.py` calls `init_db()` inside the FastAPI lifespan handler.
2. `init_db()` imports all models so SQLAlchemy relationships can resolve.
3. `Base.metadata.create_all()` creates missing tables.
4. SQLite schema upgrade logic adds new historical-project columns to older local databases.
5. Default roles are inserted if missing.
6. Default admin user is inserted if no users exist.
7. `seed_demo_portfolio()` ensures the system has realistic historical records and dashboard data.

Important tables:

- `users`, `roles`: authentication and role-based access structure.
- `projects`, `project_versions`: project setup and versioned scope.
- `estimates`, `function_points`: estimation records and FPA details.
- `historical_projects`: historical actuals used for comparison and ML training.
- `risks`, `scenarios`, `resources`: planning controls.
- `reports`: generated report records.
- `calibration_models`, `ml_models`: model metadata.
- `notifications`: in-app/email alert events.
- `integration_syncs`: Jira/Trello import history and mapping.

## 6. Authentication Flow

When the user signs in:

1. The frontend reads email/password from `loginForm`.
2. `ui-manager.js` calls `apiClient.login(email, password)`.
3. `api-client.js` sends `POST /api/v1/auth/login`.
4. `auth.py` verifies the user password using hashed password logic.
5. Backend returns access and refresh tokens.
6. The frontend saves tokens in local storage.
7. The frontend calls `/auth/me`, `/users/{id}`, roles, users, projects, historical data, ML metadata, dashboard analytics, notifications, integrations status, and sync history.
8. The workspace is shown only after authenticated data loads.

The earlier `422` happened because `/estimates/historical-projects` was being interpreted as `/estimates/{estimate_id}`. Static estimate routes now appear before dynamic ID routes, so historical projects load correctly after sign-in.

## 7. Estimation Workflow

The normal user journey is:

1. Create a project.
2. The backend automatically creates project version 1.
3. Add or review scope, assumptions, and constraints.
4. Create an estimate manually or use calculation endpoints.
5. Add function point analysis if using FPA.
6. Add risks and contingencies.
7. Add scenarios for optimistic, realistic, and pessimistic cases.
8. Add resources and rates.
9. Generate/download reports.
10. Compare estimates with actuals when the project completes.

## 8. COCOMO Logic

COCOMO estimates effort from code size.

Formula:

`Effort(person-months) = a x KLOC^b x effort_multipliers`

`Duration(months) = c x Effort^d`

The backend supports organic, semi-detached, and embedded modes. Complexity, risk, and effort multipliers adjust the result.

Use COCOMO when the team can estimate approximate code size, modules, or technical size.

Advantages:

- Good for engineering-heavy systems.
- Easy to explain mathematically.
- Useful for early cost and staffing estimates.

Disadvantages:

- Needs a size assumption.
- Less natural for UI/business-process projects before design is complete.

## 9. Function Point Analysis Logic

FPA estimates based on user-visible functionality, not code lines.

Components:

- ILF: internal logical files maintained by the system.
- EIF: external files referenced by the system.
- EI: external inputs that create/update data.
- EO: external outputs such as reports or exports.
- EQ: external inquiries such as search/view screens.

Formula:

`Unadjusted FP = sum(component_count x complexity_weight)`

`Adjusted FP = Unadjusted FP x Value Adjustment Factor`

`Effort(person-months) = Adjusted FP / productivity`

Use FPA when requirements are known but code size is not.

## 10. Hybrid Estimation Logic

Hybrid estimation blends COCOMO, FPA, and optional ML predictions.

Formula:

`Hybrid = weighted(COCOMO, FPA, ML) x risk/volatility adjustment`

This is useful because one model may be biased. COCOMO sees technical size, FPA sees functional size, and ML sees historical organizational behavior.

## 11. ML Estimation Logic

The ML module trains in memory from `historical_projects`.

Features include:

- adjusted function points
- team size
- complexity score
- risk score
- requirement volatility score
- team experience score
- architecture score
- productivity
- defect density

Targets predicted:

- effort hours
- duration months
- cost

The service uses `RandomForestRegressor`, measures accuracy/MAPE/MAE/R-squared, returns confidence intervals, and exposes feature importance for dashboard visualization.

## 12. Historical Data Usage

Historical data matters because it converts estimation from guessing into evidence-based forecasting. The seeded database now contains 62 historical records, including realistic project domains, complexity, risk, technology stack, FPA values, COCOMO values, hybrid values, estimated vs actual values, success status, client type, volatility, assumptions, and scenario summaries.

The system uses historical data for:

- ML training
- productivity metrics
- calibration metadata
- estimation accuracy analysis
- dashboard trends
- academic demonstration data

## 13. Business Logic

Organizations need estimation systems because software projects require budget approval, staffing, scheduling, risk planning, and stakeholder commitment before development finishes.

Estimation fails when:

- requirements change late
- risks are ignored
- team experience is overestimated
- historical productivity is not used
- effort is confused with calendar duration
- integrations and testing are underestimated
- estimates are not compared with actual delivery

Risk affects estimation because probability multiplied by impact creates exposure. Higher exposure means more contingency hours, cost buffer, and management attention.

Complexity changes calculations because complex architecture, integrations, security, and business rules increase effort multipliers.

Team size affects delivery because more people can reduce duration only up to a point. Large teams also add communication overhead.

Hybrid estimation is useful because it combines multiple perspectives and reduces single-method bias.

ML improves accuracy by learning from completed projects rather than relying only on textbook formulas.

The system supports project managers by giving them a repeatable workflow: define scope, estimate, compare models, identify risks, allocate resources, report, and improve with historical actuals.

## 14. Dashboard Workflow

The dashboard loads from `/api/v1/dashboard/analytics`.

It shows:

- portfolio project count
- active project count
- historical record count
- total estimates
- risk exposure
- reports
- average accuracy when actuals exist
- method comparison
- risk distribution
- ML model summary
- project health indicators
- productivity metrics

The frontend renders this as metric cards, mini bar charts, and project health lists.

## 15. Reports

Reports can be stored in the `reports` table and downloaded from:

- `GET /api/v1/reports/projects/{project_id}/export?format=pdf`
- `GET /api/v1/reports/projects/{project_id}/export?format=xlsx`
- `GET /api/v1/reports/projects/{project_id}/export?format=html`
- `GET /api/v1/reports/projects/{project_id}/export?format=json`

The PDF is generated server-side as a valid PDF. The Excel export is generated as a valid `.xlsx` workbook with Summary, Estimates, Risks, Scenarios, and Resources sheets.

## 16. Notifications

Notifications support:

- deadline alerts
- risk alerts
- reminders
- estimation review notifications
- in-app dashboard alerts
- email sending when SMTP is configured

The frontend top-bar `Alerts` button refreshes notifications by calling `/api/v1/notifications/refresh`.

## 17. Jira and Trello Integrations

Jira integration uses Jira Cloud REST API with email/API-token authentication. Configure:

- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- optional `JIRA_PROJECT_KEY`

Trello integration uses Trello API key/token authentication. Configure:

- `TRELLO_API_KEY`
- `TRELLO_API_TOKEN`
- optional `TRELLO_BOARD_ID`

When sync runs:

1. Backend calls the external API.
2. Work items/cards are imported.
3. Completed count and progress are calculated.
4. A local project is created or updated.
5. A baseline version and task-mapping estimate are created if needed.
6. Sync history is stored in `integration_syncs`.
7. The frontend shows provider, task counts, progress, mapped project, and sync time.

## 18. Localization

The frontend has a language selector with English and Urdu navigation labels. The architecture stores the selected language in local storage and applies document direction (`ltr` or `rtl`). More translations can be added by extending `LANGUAGE_PACKS` in `ui-manager.js`.

## 19. Tooltip Help System

`ui-manager.js` automatically scans every `label[for]` and checkbox label, then appends a question-mark help button. Each tooltip explains:

- what the field means
- why it matters
- example values
- how it affects estimation, reports, dashboard, or workflow

If a future field is added without custom help text, the system still attaches a fallback explanation.

## 20. Complete Internal Execution Flow

Application startup:

1. Backend starts through `uvicorn app.main:app`.
2. FastAPI creates the app and registers middleware/router.
3. Lifespan startup calls `init_db()`.
4. Tables are created/upgraded.
5. Admin, roles, seed portfolio, reports, ML metadata, and notifications are ensured.
6. Frontend is served by a static HTTP server.
7. Browser loads `frontend/index.html`.
8. `app.js` creates `CaseToolApp`.
9. `ui-manager.js` caches DOM elements, binds events, installs tooltips, installs language selector, checks API health, and loads public roles.

Sign-in flow:

1. User clicks `Enter Workspace`.
2. Frontend sends credentials to `/auth/login`.
3. Backend validates password and returns JWT tokens.
4. Frontend stores tokens.
5. Frontend loads current user and workspace data.
6. Dashboard and all modules render.

Estimate flow:

1. User selects a project and version.
2. User enters estimate values or calls backend calculation endpoints.
3. Backend validates data with Pydantic schemas.
4. SQLAlchemy stores estimate rows.
5. Dashboard recalculates totals and analytics.
6. Reports can include the estimate.

Function point flow:

1. User enters ILF, EIF, EI, EO, EQ counts and complexities.
2. Frontend posts to `/estimates/{estimate_id}/function-points`.
3. Backend recalculates contributions, unadjusted FP, VAF, and adjusted FP.
4. Results are stored and shown in estimate details.

ML flow:

1. Backend reads historical projects.
2. Feature vectors are built.
3. Random forest models train for effort, duration, and cost.
4. Prediction and confidence interval are returned.
5. Dashboard shows model quality and feature importance.

Report flow:

1. User creates or opens reports.
2. User clicks PDF or Excel.
3. Frontend fetches the export endpoint with JWT header.
4. Backend collects project, estimates, risks, scenarios, resources.
5. Backend streams PDF/XLSX.
6. Browser downloads the file.

Integration flow:

1. User opens Integrations.
2. Frontend checks `/integrations/status`.
3. User runs Jira or Trello sync.
4. Backend calls real external APIs using configured credentials.
5. Imported items are mapped to a local project.
6. Progress and task count are stored.
7. Dashboard/project list updates.

Notification flow:

1. User clicks Alerts.
2. Backend scans deadlines and active high-exposure risks.
3. Missing notifications are inserted.
4. If SMTP is enabled and requested, email is sent.
5. Frontend updates unread count.

## 21. Security Features

- JWT access and refresh tokens.
- Password hashing.
- Role records and permission metadata.
- Auth-required protected endpoints.
- CORS restricted to configured origins.
- No fake Jira/Trello data: integrations require real credentials.
- No hardcoded production secrets; local demo credentials are only for development.

## 22. Scalability Considerations

- FastAPI endpoints are modular by domain.
- SQLAlchemy supports moving from SQLite to PostgreSQL.
- ML currently trains in memory for academic/demo use; production can persist trained models.
- Integrations store sync audit records for traceability.
- Report generation is stateless and can be moved to background jobs for large portfolios.

## 23. Future Improvements

- Add Alembic migrations for all schema changes.
- Add background workers for email/report/integration jobs.
- Add full Urdu translation coverage for every label and message.
- Add OAuth-based Jira/Trello flows for enterprise deployments.
- Persist trained ML model artifacts to `ML_MODEL_PATH`.
- Add granular role permission enforcement per endpoint.
- Add visual chart library if richer chart interactivity is required.

