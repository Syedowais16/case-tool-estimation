"""Realistic CASE Tool seed data for demos, ML training, and academic review."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

from sqlalchemy.orm import Session

from app.models.estimation_models import CostDriver, Estimate, FunctionPoint, HistoricalProject
from app.models.project_models import Project, ProjectStatus, ProjectVersion
from app.models.report_models import CalibrationModel, MLModel, Notification, Report
from app.models.scenario_models import Resource, Risk, Scenario
from app.models.user_models import User
from app.services.estimation_engine import calculate_cocomo, calculate_fpa, calculate_hybrid


PROJECT_BLUEPRINTS: List[Dict[str, str]] = [
    {"name": "Atlas Claims Platform", "domain": "Insurance", "type": "Workflow Platform", "stack": "Java, Spring Boot, PostgreSQL, React"},
    {"name": "Nexus Retail Marketplace", "domain": "Retail", "type": "E-Commerce", "stack": "Node.js, Next.js, MongoDB, Stripe"},
    {"name": "PulseCare Telemedicine Suite", "domain": "Healthcare", "type": "SaaS Platform", "stack": "Python, FastAPI, PostgreSQL, React Native"},
    {"name": "Harbor Freight Optimizer", "domain": "Logistics", "type": "Optimization System", "stack": "C#, .NET, SQL Server, Angular"},
    {"name": "FinSight Risk Ledger", "domain": "Finance", "type": "Analytics Platform", "stack": "Python, Kafka, PostgreSQL, Vue"},
    {"name": "CivicPermit Portal", "domain": "Government", "type": "Citizen Portal", "stack": "Java, Oracle, React"},
    {"name": "LearnSphere LMS", "domain": "Education", "type": "Learning Management", "stack": "PHP, Laravel, MySQL, Vue"},
    {"name": "GridWatch IoT Monitor", "domain": "Energy", "type": "IoT Monitoring", "stack": "Go, MQTT, TimescaleDB, Svelte"},
    {"name": "MediStock Inventory", "domain": "Healthcare", "type": "Inventory System", "stack": "C#, .NET, SQL Server, Blazor"},
    {"name": "AeroOps Maintenance Hub", "domain": "Aviation", "type": "Asset Management", "stack": "Java, Kafka, PostgreSQL, React"},
    {"name": "FarmLink Advisory App", "domain": "Agriculture", "type": "Mobile App", "stack": "Kotlin, Swift, Firebase"},
    {"name": "LegalFlow Case Manager", "domain": "Legal", "type": "Case Management", "stack": "Ruby on Rails, PostgreSQL, Hotwire"},
    {"name": "BuildTrack Contractor CRM", "domain": "Construction", "type": "CRM", "stack": "Python, Django, PostgreSQL, HTMX"},
    {"name": "SecureVault IAM", "domain": "Cybersecurity", "type": "Identity Platform", "stack": "Go, PostgreSQL, React, OIDC"},
    {"name": "Streamline OTT Console", "domain": "Media", "type": "Streaming Admin", "stack": "Node.js, GraphQL, Redis, React"},
    {"name": "HotelSync Booking Engine", "domain": "Hospitality", "type": "Booking Platform", "stack": "Java, Spring Boot, MySQL, Angular"},
    {"name": "TransitPulse Ridership BI", "domain": "Transportation", "type": "Business Intelligence", "stack": "Python, Airflow, Snowflake, Superset"},
    {"name": "CharityConnect Donor Hub", "domain": "Nonprofit", "type": "Donor Management", "stack": "Python, Django, PostgreSQL, React"},
    {"name": "FactoryLine MES", "domain": "Manufacturing", "type": "Manufacturing Execution", "stack": "C++, .NET, SQL Server, WPF"},
    {"name": "PayBridge Gateway", "domain": "FinTech", "type": "Payment Gateway", "stack": "Java, Kafka, PostgreSQL, Kubernetes"},
    {"name": "EcoTrace Compliance", "domain": "Sustainability", "type": "Compliance Platform", "stack": "Python, FastAPI, PostgreSQL, React"},
    {"name": "ClinicQueue Scheduler", "domain": "Healthcare", "type": "Scheduling App", "stack": "Node.js, PostgreSQL, React Native"},
    {"name": "TalentGraph HR Analytics", "domain": "HR", "type": "Analytics Platform", "stack": "Python, Pandas, PostgreSQL, Dash"},
    {"name": "FleetMate Driver App", "domain": "Logistics", "type": "Mobile App", "stack": "Flutter, Firebase, Cloud Functions"},
    {"name": "BankCore Loan Origination", "domain": "Banking", "type": "Core Banking Module", "stack": "Java, Oracle, Angular"},
    {"name": "SmartCampus Access", "domain": "Education", "type": "IoT Access Control", "stack": "Go, MQTT, PostgreSQL, React"},
    {"name": "PharmaTrial EDC", "domain": "Pharmaceutical", "type": "Clinical Data Capture", "stack": "Python, PostgreSQL, React"},
    {"name": "NewsRoom CMS", "domain": "Media", "type": "Content Management", "stack": "Node.js, MongoDB, React"},
    {"name": "SolarBid Estimator", "domain": "Energy", "type": "Estimation Tool", "stack": "Python, FastAPI, PostgreSQL, Vue"},
    {"name": "PortClear Customs API", "domain": "Logistics", "type": "Integration API", "stack": "Java, Spring Boot, Oracle"},
    {"name": "InsureBot Service Desk", "domain": "Insurance", "type": "AI Support Bot", "stack": "Python, LangChain, PostgreSQL, React"},
    {"name": "FoodTrace QR Platform", "domain": "Food Safety", "type": "Traceability Platform", "stack": "Node.js, PostgreSQL, React"},
    {"name": "CityWaste Route Planner", "domain": "Government", "type": "Optimization System", "stack": "Python, OR-Tools, PostgreSQL, Angular"},
    {"name": "MedImage Review Workbench", "domain": "Healthcare", "type": "Imaging Workflow", "stack": "Python, DICOM, PostgreSQL, React"},
    {"name": "RetailDemand Forecaster", "domain": "Retail", "type": "ML Forecasting", "stack": "Python, scikit-learn, Snowflake, Streamlit"},
    {"name": "AssetPro Field Service", "domain": "Utilities", "type": "Field Service", "stack": "C#, .NET, SQL Server, Xamarin"},
    {"name": "GovGrants Portal", "domain": "Government", "type": "Grant Management", "stack": "Java, PostgreSQL, React"},
    {"name": "FinRecon Automation", "domain": "Finance", "type": "Reconciliation System", "stack": "Python, Celery, PostgreSQL, React"},
    {"name": "ShopLoyalty Engine", "domain": "Retail", "type": "Loyalty Platform", "stack": "Node.js, Redis, PostgreSQL, Vue"},
    {"name": "UniAdmissions CRM", "domain": "Education", "type": "Admissions CRM", "stack": "Ruby on Rails, PostgreSQL, React"},
    {"name": "MineSafe Incident Tracker", "domain": "Mining", "type": "Safety Platform", "stack": "C#, SQL Server, Angular"},
    {"name": "WaterGrid Sensor Lake", "domain": "Utilities", "type": "IoT Data Lake", "stack": "Python, Kafka, TimescaleDB, Grafana"},
    {"name": "LegalAI Contract Review", "domain": "Legal", "type": "AI Document Analysis", "stack": "Python, PostgreSQL, React"},
    {"name": "EventPro Ticketing", "domain": "Entertainment", "type": "Ticketing Platform", "stack": "Node.js, PostgreSQL, Next.js"},
    {"name": "WarehouseVision WMS", "domain": "Logistics", "type": "Warehouse Management", "stack": "Java, PostgreSQL, React"},
    {"name": "PatientBilling RCM", "domain": "Healthcare", "type": "Revenue Cycle", "stack": "C#, SQL Server, Angular"},
    {"name": "TravelWise Itinerary Builder", "domain": "Travel", "type": "Travel Planning", "stack": "Python, FastAPI, PostgreSQL, Vue"},
    {"name": "OpenBanking Aggregator", "domain": "FinTech", "type": "API Aggregator", "stack": "Go, Kafka, PostgreSQL, React"},
    {"name": "CampusExam Proctoring", "domain": "Education", "type": "Proctoring Platform", "stack": "Node.js, WebRTC, MongoDB, React"},
    {"name": "AutoParts DealerNet", "domain": "Automotive", "type": "Dealer Portal", "stack": "Java, MySQL, Angular"},
    {"name": "SmartMeter Billing", "domain": "Utilities", "type": "Billing Engine", "stack": "Java, Kafka, Oracle, React"},
    {"name": "MuseumArchive Digital Vault", "domain": "Culture", "type": "Digital Archive", "stack": "Python, PostgreSQL, Django"},
    {"name": "SportsLeague Scheduler", "domain": "Sports", "type": "Scheduling System", "stack": "C#, SQL Server, Blazor"},
    {"name": "AgriLoan Risk Engine", "domain": "Banking", "type": "Risk Scoring", "stack": "Python, scikit-learn, PostgreSQL, React"},
    {"name": "ProcureFlow Vendor Portal", "domain": "Procurement", "type": "Vendor Portal", "stack": "Java, PostgreSQL, Vue"},
    {"name": "TelecomChurn Predictor", "domain": "Telecom", "type": "ML Analytics", "stack": "Python, Spark, Snowflake, Tableau"},
    {"name": "LabTrack LIMS", "domain": "Research", "type": "Laboratory Management", "stack": "Python, FastAPI, PostgreSQL, React"},
    {"name": "MaritimeCrew Planner", "domain": "Maritime", "type": "Resource Planning", "stack": "C#, SQL Server, React"},
    {"name": "CinemaOps POS", "domain": "Entertainment", "type": "Point of Sale", "stack": "Node.js, PostgreSQL, React Native"},
    {"name": "RealEstate Valuation Hub", "domain": "Real Estate", "type": "Analytics Platform", "stack": "Python, PostGIS, React"},
]


def _seed_cost_drivers(db: Session) -> None:
    if db.query(CostDriver).count() >= 12:
        return
    drivers = [
        ("Very High Reliability", "Mission-critical uptime and auditability requirements.", "reliability", 1.40, 1.40, 1.40, 1.20),
        ("High Security", "Strong authentication, encryption, penetration testing, and compliance controls.", "security", 1.32, 1.32, 1.28, 1.14),
        ("Complex Business Rules", "Dense validation rules, workflow branches, and exception handling.", "complexity", 1.30, 1.30, 1.25, 1.18),
        ("Legacy Integration", "Integrates with older systems or undocumented APIs.", "integration", 1.24, 1.24, 1.20, 1.16),
        ("Cloud Native Architecture", "Containerization, observability, scaling, and CI/CD maturity.", "architecture", 1.12, 1.12, 1.10, 1.08),
        ("Tight Timeline", "Reduced schedule flexibility and parallel delivery pressure.", "schedule", 1.18, 1.18, 1.16, 1.28),
        ("Junior Team", "Lower average experience increases communication and rework.", "people", 1.36, 1.36, 1.25, 1.22),
        ("Senior Team", "Experienced team with strong domain knowledge.", "people", 0.82, 0.82, 0.88, 0.92),
        ("Stable Requirements", "Clear backlog and low expected change rate.", "requirements", 0.88, 0.88, 0.90, 0.92),
        ("High Volatility", "Frequent requirement change and stakeholder uncertainty.", "requirements", 1.27, 1.27, 1.18, 1.22),
        ("Automated Testing", "High automated regression coverage reduces downstream defects.", "quality", 0.92, 0.92, 0.96, 0.95),
        ("Large Data Volume", "Heavy migration, reporting, indexing, and performance needs.", "data", 1.22, 1.22, 1.18, 1.12),
    ]
    for name, description, category, impact, effort, cost, duration in drivers:
        if db.query(CostDriver).filter(CostDriver.name == name).first():
            continue
        db.add(CostDriver(
            name=name,
            description=description,
            category=category,
            impact_factor=impact,
            effort_multiplier=effort,
            cost_multiplier=cost,
            duration_multiplier=duration,
            is_active=True,
        ))


def _experience(index: int) -> str:
    return ["senior", "mixed", "mid", "junior"][index % 4]


def _complexity(index: int) -> str:
    return ["medium", "high", "low", "medium", "complex"][index % 5]


def _risk(index: int) -> str:
    return ["medium", "high", "low", "medium", "critical", "medium"][index % 6]


def _volatility(index: int) -> str:
    return ["medium", "low", "high", "medium", "critical"][index % 5]


def _success(index: int) -> str:
    if index % 17 == 0:
        return "failed"
    if index % 5 == 0:
        return "challenged"
    return "successful"


def _architecture(stack: str, index: int) -> str:
    if "Kafka" in stack or "MQTT" in stack:
        return "Distributed"
    if "React Native" in stack or "Flutter" in stack or "Swift" in stack:
        return "Native"
    if index % 4 == 0:
        return "Microservices"
    if index % 4 == 1:
        return "Layered"
    return "Monolith"


def seed_demo_portfolio(db: Session) -> None:
    """Seed 50+ realistic records, reference data, estimates, and analytics metadata."""
    admin = db.query(User).order_by(User.id.asc()).first()
    if not admin:
        return

    _seed_cost_drivers(db)

    created_projects = 0
    for index, blueprint in enumerate(PROJECT_BLUEPRINTS, start=1):
        existing_history = db.query(HistoricalProject).filter(HistoricalProject.project_name == blueprint["name"]).first()
        if existing_history:
            continue

        complexity = _complexity(index)
        risk_level = _risk(index)
        volatility = _volatility(index)
        team_experience = _experience(index)
        success_status = _success(index)
        team_size = 3 + (index % 8)
        cost_per_pm = 7200 + (index % 7) * 850

        fpa = calculate_fpa(
            ilf_count=2 + index % 8,
            ilf_complexity="complex" if complexity in {"high", "complex"} else "average",
            eif_count=1 + index % 5,
            eif_complexity="average",
            ei_count=5 + index % 11,
            ei_complexity="complex" if index % 3 == 0 else "average",
            eo_count=3 + index % 9,
            eo_complexity="average",
            eq_count=2 + index % 7,
            eq_complexity="simple" if complexity == "low" else "average",
            value_adjustment_factor=0.85 + (index % 9) * 0.04,
            productivity_fp_per_person_month=14 + (index % 8),
            cost_per_person_month=cost_per_pm,
            risk_level=risk_level,
        )
        kloc = max(6.0, fpa["adjusted_fp"] * (38 + (index % 6) * 8) / 1000)
        mode = "embedded" if risk_level == "critical" or complexity == "complex" else "semi_detached" if complexity == "high" else "organic"
        cocomo = calculate_cocomo(
            size_kloc=kloc,
            mode=mode,
            effort_multiplier=0.92 + (index % 6) * 0.06,
            cost_per_person_month=cost_per_pm,
            risk_level=risk_level,
            complexity=complexity,
        )
        hybrid = calculate_hybrid(
            cocomo,
            fpa,
            risk_level=risk_level,
            requirement_volatility=volatility,
        )
        variance = 0.82 + (index % 9) * 0.055
        if success_status == "failed":
            variance += 0.35
        elif success_status == "challenged":
            variance += 0.18
        actual_effort = round(hybrid["estimated_effort_hours"] * variance, 2)
        actual_duration = round(hybrid["estimated_duration_months"] * (0.9 + (index % 7) * 0.055), 2)
        actual_cost = round(hybrid["estimated_cost"] * variance * (0.96 + (index % 4) * 0.025), 2)
        productivity = round(fpa["adjusted_fp"] / max(actual_effort / 152, 1), 2)
        defect_density = round(0.6 + (index % 8) * 0.42 + (0.9 if success_status == "failed" else 0), 2)

        assumptions = (
            f"Stable product owner availability; {team_experience} delivery team; "
            f"{volatility} requirement volatility; reusable components available for common authentication and reporting."
        )
        scenario_summary = (
            "Optimistic: scope freeze and senior team availability. "
            "Realistic: normal backlog change and planned QA cycles. "
            "Pessimistic: integration delay, late compliance changes, or key resource turnover."
        )

        history = HistoricalProject(
            project_name=blueprint["name"],
            domain=blueprint["domain"],
            industry=blueprint["domain"],
            project_type=blueprint["type"],
            complexity=complexity,
            risk_level=risk_level,
            technology_stack=blueprint["stack"],
            client_type=["Enterprise", "SME", "Government", "Startup"][index % 4],
            requirement_volatility=volatility,
            success_status=success_status,
            team_experience=team_experience,
            estimated_effort_hours=hybrid["estimated_effort_hours"],
            estimated_duration_months=hybrid["estimated_duration_months"],
            estimated_cost=hybrid["estimated_cost"],
            actual_effort_hours=actual_effort,
            actual_duration_months=actual_duration,
            actual_cost=actual_cost,
            team_size=team_size,
            language=blueprint["stack"].split(",")[0],
            database_type="PostgreSQL" if "PostgreSQL" in blueprint["stack"] else "SQL Server" if "SQL Server" in blueprint["stack"] else "MongoDB" if "MongoDB" in blueprint["stack"] else "Oracle" if "Oracle" in blueprint["stack"] else "Firebase" if "Firebase" in blueprint["stack"] else "Mixed",
            architecture=_architecture(blueprint["stack"], index),
            scope_description=f"{blueprint['type']} for {blueprint['domain']} teams with dashboards, role-based access, workflow automation, integrations, and operational reporting.",
            productivity=productivity,
            defect_density=defect_density,
            fpa_unadjusted=fpa["unadjusted_fp"],
            fpa_adjusted=fpa["adjusted_fp"],
            cocomo_effort=cocomo["estimated_effort_hours"],
            cocomo_duration=cocomo["estimated_duration_months"],
            cocomo_cost=cocomo["estimated_cost"],
            hybrid_effort=hybrid["estimated_effort_hours"],
            hybrid_duration=hybrid["estimated_duration_months"],
            hybrid_cost=hybrid["estimated_cost"],
            assumptions=assumptions,
            scenario_summary=scenario_summary,
            source="seeded_realistic_portfolio",
        )
        db.add(history)

        if created_projects < 24 and not db.query(Project).filter(Project.name == blueprint["name"]).first():
            start_date = datetime.utcnow() - timedelta(days=420 - index * 9)
            end_date = start_date + timedelta(days=max(60, int(actual_duration * 30)))
            project = Project(
                name=blueprint["name"],
                description=(
                    f"Domain: {blueprint['domain']}\n"
                    f"Project type: {blueprint['type']}\n"
                    f"Complexity: {complexity}\n"
                    f"Risk level: {risk_level}\n"
                    f"Technology stack: {blueprint['stack']}\n"
                    f"Client type: {history.client_type}\n"
                    f"Requirement volatility: {volatility}\n"
                    f"Outcome: {success_status}\n"
                    f"Business goal: improve planning accuracy, delivery visibility, and management reporting."
                ),
                created_by=admin.id,
                status=ProjectStatus.COMPLETED if success_status in {"successful", "challenged"} and index % 3 == 0 else ProjectStatus.IN_PROGRESS if index % 3 == 1 else ProjectStatus.PLANNING,
                start_date=start_date,
                end_date=end_date if index % 3 == 0 else None,
                budget=round(hybrid["estimated_cost"] * 1.12, 2),
                team_size=team_size,
                client_name=f"{blueprint['domain']} Client {index:02d}",
                project_manager=admin.full_name,
                department=blueprint["domain"],
            )
            db.add(project)
            db.flush()

            version = ProjectVersion(
                project_id=project.id,
                version_number=1,
                description="Initial baseline version from seeded portfolio data.",
                scope=history.scope_description,
                assumptions=assumptions,
                constraints="Budget approval, stakeholder availability, third-party API limits, and release calendar commitments.",
            )
            db.add(version)
            db.flush()

            estimate = Estimate(
                project_id=project.id,
                version_id=version.id,
                created_by=admin.id,
                estimation_method="Hybrid",
                estimated_effort_hours=hybrid["estimated_effort_hours"],
                estimated_duration_months=hybrid["estimated_duration_months"],
                estimated_cost=hybrid["estimated_cost"],
                estimated_team_size=hybrid["estimated_team_size"],
                confidence_level=hybrid["confidence_level"],
                confidence_interval_low=hybrid["confidence_interval_low"],
                confidence_interval_high=hybrid["confidence_interval_high"],
                actual_effort_hours=actual_effort if project.status == ProjectStatus.COMPLETED else None,
                actual_duration_months=actual_duration if project.status == ProjectStatus.COMPLETED else None,
                actual_cost=actual_cost if project.status == ProjectStatus.COMPLETED else None,
                actual_team_size=team_size if project.status == ProjectStatus.COMPLETED else None,
                notes=f"Seeded baseline using COCOMO {round(cocomo['estimated_effort_hours'])}h, FPA {round(fpa['estimated_effort_hours'])}h, and risk-adjusted hybrid blend.",
                assumptions=assumptions,
                risks=f"{risk_level} risk due to integration, requirements, team availability, and compliance factors.",
            )
            db.add(estimate)
            db.flush()

            db.add(FunctionPoint(
                estimate_id=estimate.id,
                ilf_count=2 + index % 8,
                ilf_complexity="complex" if complexity in {"high", "complex"} else "average",
                ilf_contribution=fpa["ilf_contribution"],
                eif_count=1 + index % 5,
                eif_complexity="average",
                eif_contribution=fpa["eif_contribution"],
                ei_count=5 + index % 11,
                ei_complexity="complex" if index % 3 == 0 else "average",
                ei_contribution=fpa["ei_contribution"],
                eo_count=3 + index % 9,
                eo_complexity="average",
                eo_contribution=fpa["eo_contribution"],
                eq_count=2 + index % 7,
                eq_complexity="simple" if complexity == "low" else "average",
                eq_contribution=fpa["eq_contribution"],
                unadjusted_fp=fpa["unadjusted_fp"],
                vaf=fpa["vaf"],
                adjusted_fp=fpa["adjusted_fp"],
            ))

            exposure = {"low": 0.15, "medium": 0.32, "high": 0.52, "critical": 0.76}.get(risk_level, 0.32)
            db.add(Risk(
                project_id=project.id,
                description=f"{blueprint['type']} delivery may be affected by requirement change, integration availability, or performance constraints.",
                category="technical" if index % 2 else "schedule",
                probability=min(0.9, exposure),
                impact=min(0.95, exposure + 0.18),
                mitigation_strategy="Maintain risk register, use phased releases, validate integrations early, and keep contingency budget visible.",
                owner=admin.full_name,
                status="active" if project.status != ProjectStatus.COMPLETED else "mitigated",
                effort_contingency=round(actual_effort * exposure * 0.12, 2),
                cost_contingency=round(actual_cost * exposure * 0.08, 2),
            ))
            for scenario_type, multiplier in [("optimistic", 0.86), ("realistic", 1.0), ("pessimistic", 1.22)]:
                db.add(Scenario(
                    project_id=project.id,
                    name=f"{scenario_type.title()} delivery case",
                    description=f"{scenario_type.title()} scenario for scope, team availability, and integration stability.",
                    scenario_type=scenario_type,
                    effort_adjustment=multiplier,
                    duration_adjustment=multiplier + (0.03 if scenario_type == "pessimistic" else 0),
                    cost_adjustment=multiplier,
                    team_size_adjustment=1.0 if scenario_type != "pessimistic" else 1.12,
                    estimated_effort=round(hybrid["estimated_effort_hours"] * multiplier, 2),
                    estimated_duration=round(hybrid["estimated_duration_months"] * multiplier, 2),
                    estimated_cost=round(hybrid["estimated_cost"] * multiplier, 2),
                ))
            db.add(Resource(
                project_id=project.id,
                user_id=admin.id,
                role="Project Manager / Estimation Owner",
                allocation_percentage=35 if project.status == ProjectStatus.IN_PROGRESS else 15,
                hourly_rate=round(cost_per_pm / 152, 2),
                start_date=start_date,
                end_date=end_date,
                skills="planning, estimation, risk management, stakeholder communication",
                availability="available",
            ))
            db.add(Report(
                project_id=project.id,
                title=f"{blueprint['name']} Estimation Summary",
                report_type="estimate",
                content=f"<h1>{blueprint['name']}</h1><p>Hybrid effort: {hybrid['estimated_effort_hours']} hours. Risk: {risk_level}. Outcome: {success_status}.</p>",
                format="html",
                generated_by=admin.id,
                include_confidence_intervals=True,
                include_risks=True,
                include_scenarios=True,
            ))
            created_projects += 1

    if not db.query(CalibrationModel).filter(CalibrationModel.name == "Seeded Hybrid Calibration").first():
        history_count = db.query(HistoricalProject).count()
        db.add(CalibrationModel(
            name="Seeded Hybrid Calibration",
            description="Calibration model built from seeded industry-style portfolio records.",
            model_type="Hybrid",
            organization="CASE Tool Demo Portfolio",
            industry="Cross-industry",
            calibration_data_count=history_count,
            accuracy_percentage=82.5,
            last_calibration_date=datetime.utcnow(),
            coefficients={"cocomo_weight": 0.35, "fpa_weight": 0.40, "ml_weight": 0.25},
            r_squared=0.78,
            rmse=420.0,
            mae=315.0,
            is_active=True,
        ))

    if not db.query(MLModel).filter(MLModel.name == "Historical Effort Random Forest").first():
        history_count = db.query(HistoricalProject).count()
        db.add(MLModel(
            name="Historical Effort Random Forest",
            description="Regression model metadata for effort, duration, and cost predictions trained on historical project features.",
            model_type="regression",
            algorithm="random_forest_regressor",
            training_data_count=history_count,
            feature_count=9,
            feature_names=[
                "adjusted_fp",
                "team_size",
                "complexity_score",
                "risk_score",
                "volatility_score",
                "experience_score",
                "architecture_score",
                "productivity",
                "defect_density",
            ],
            accuracy=82.5,
            precision=81.2,
            recall=80.4,
            f1_score=80.8,
            model_version="seeded-1.0",
            training_date=datetime.utcnow(),
            last_retraining_date=datetime.utcnow(),
            next_retraining_date=datetime.utcnow() + timedelta(days=30),
            is_active=True,
            is_production=True,
        ))

    if db.query(Notification).filter(Notification.title == "Review high-risk estimates").first() is None:
        db.add(Notification(
            user_id=admin.id,
            title="Review high-risk estimates",
            message="Seeded portfolio includes high and critical risk projects. Open the dashboard risk analysis before approving final estimates.",
            notification_type="risk",
            severity="warning",
            channel="in_app",
            due_at=datetime.utcnow() + timedelta(days=2),
            event_metadata={"source": "seed_demo_portfolio"},
        ))

    db.commit()
