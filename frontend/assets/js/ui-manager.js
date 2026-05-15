const VIEW_STORAGE_KEY = "case_tool_active_view";
const PROJECT_STORAGE_KEY = "case_tool_selected_project_id";
const LANGUAGE_STORAGE_KEY = "case_tool_language";

const LANGUAGE_PACKS = {
    en: {
        dashboard: "Dashboard",
        projects: "Projects",
        estimates: "Estimates",
        scenarios: "Scenarios",
        risks: "Risks",
        resources: "Resources",
        reports: "Reports",
        intelligence: "Intelligence",
        integrations: "Integrations",
        admin: "Admin",
        settings: "Settings",
        refresh: "Refresh",
        logout: "Logout",
    },
    ur: {
        dashboard: "ڈیش بورڈ",
        projects: "پروجیکٹس",
        estimates: "تخمینے",
        scenarios: "منظرنامے",
        risks: "خطرات",
        resources: "وسائل",
        reports: "رپورٹس",
        intelligence: "انٹیلیجنس",
        integrations: "انٹیگریشنز",
        admin: "ایڈمن",
        settings: "سیٹنگز",
        refresh: "ریفریش",
        logout: "لاگ آؤٹ",
    },
};

const FIELD_HELP = {
    authApiBaseUrl: "Backend API address. Example: http://localhost:8000/api/v1. If this is wrong, login and data loading will fail.",
    loginEmail: "Your registered account email. Default seeded admin: admin@example.com.",
    loginPassword: "Your account password. Default seeded admin password is admin123 for local/demo use.",
    registerFullName: "Person's display name used in reports, audit trails, and resource ownership.",
    registerUsername: "Short unique login name. Example: project.manager.",
    registerEmail: "Unique email used for sign-in and optional email notifications.",
    registerPhone: "Optional contact number for project management records.",
    registerOrganization: "Company or university name connected to this user.",
    registerDepartment: "Department/team this user belongs to, such as PMO, IT, or Engineering.",
    registerRoleId: "Access role. It controls what the user should be allowed to manage.",
    registerPassword: "Password for the new account. Use at least 8 characters.",
    projectName: "Human-readable project title. Example: Patient Portal Upgrade.",
    projectDescription: "Scope, business goal, technology, assumptions, and major constraints. This helps explain the estimate later.",
    projectStatus: "Current delivery stage. Dashboard health and reporting use this status.",
    projectBudget: "Approved or proposed budget. Used to compare forecast cost against funding.",
    projectTeamSize: "Number of people expected on the delivery team. Team size affects duration and resource planning.",
    projectClientName: "Client, department, or sponsor requesting the software.",
    projectManager: "Person accountable for scope, estimation review, and delivery tracking.",
    projectDepartment: "Business domain or department. Dashboard trends group projects by this field.",
    projectStartDate: "Planned or actual start date. Used for scheduling and deadline alerts.",
    projectEndDate: "Planned or actual finish date. Upcoming dates can trigger deadline notifications.",
    versionNumber: "Scope version number. Increase it when requirements change.",
    versionDescription: "Short explanation of what changed in this version.",
    versionScope: "Features and boundaries included in this version of the project.",
    versionAssumptions: "Planning assumptions, such as team availability or stable APIs.",
    versionConstraints: "Limitations such as budget caps, deadlines, compliance, or vendor dependency.",
    estimateVersionId: "The project scope version this estimate belongs to. Estimates should always match a version.",
    estimateMethod: "Estimation approach: COCOMO, FPA, Hybrid, ML, or task mapping.",
    estimateStatus: "Review state of the estimate, from draft to final.",
    estimateEffort: "Estimated work hours. Higher effort usually means higher cost and longer schedule.",
    estimateDuration: "Estimated calendar duration in months. This is not the same as effort because people work in parallel.",
    estimateCost: "Predicted delivery cost based on effort, rates, tools, and contingency.",
    estimateTeamSize: "Recommended team size for this estimate.",
    estimateConfidence: "How reliable the estimate is, from 0 to 100 percent.",
    estimateConfidenceLow: "Lower effort bound for uncertainty range.",
    estimateConfidenceHigh: "Upper effort bound for uncertainty range.",
    estimateNotes: "Important explanation for reviewers and supervisors.",
    estimateAssumptions: "Conditions assumed true when the estimate was created.",
    estimateRisks: "Known risks that may increase effort, cost, or time.",
    fpIlfCount: "Internal Logical Files: business data groups maintained by the system. Example: users, invoices, claims.",
    fpIlfComplexity: "Complexity of internal data files. More fields/relationships increase function points.",
    fpEifCount: "External Interface Files: data used by this system but owned by another system.",
    fpEifComplexity: "Complexity of external referenced data.",
    fpEiCount: "External Inputs: user/API actions that add or change data. Example: create order.",
    fpEiComplexity: "Complexity of input processing and validation.",
    fpEoCount: "External Outputs: reports, exports, generated documents, or outbound messages.",
    fpEoComplexity: "Complexity of output formatting, calculations, and destinations.",
    fpEqCount: "External Inquiries: search/view requests with simple retrieval logic.",
    fpEqComplexity: "Complexity of query filters, joins, and response logic.",
    fpUnadjusted: "Raw function point total before environmental adjustment. The backend can recalculate this.",
    fpVaf: "Value Adjustment Factor from 0.65 to 1.35. It adjusts FP for technical and environmental complexity.",
    fpAdjusted: "Final adjusted function points. Used to convert functionality into effort.",
    scenarioName: "Scenario title. Example: Pessimistic integration delay.",
    scenarioDescription: "What changes in this what-if case and why it matters.",
    scenarioType: "Optimistic, realistic, pessimistic, or custom scenario category.",
    scenarioEffortAdjustment: "Multiplier for effort. 1.20 means 20 percent more work.",
    scenarioDurationAdjustment: "Multiplier for calendar duration.",
    scenarioCostAdjustment: "Multiplier for project cost.",
    scenarioTeamAdjustment: "Multiplier for team size/resource need.",
    riskDescription: "Clear description of what might go wrong.",
    riskCategory: "Risk group such as technical, schedule, resource, scope, or security.",
    riskProbability: "Chance of the risk happening from 0 to 1. Example: 0.4 means 40 percent.",
    riskImpact: "Severity if it happens from 0 to 1. Probability x impact creates exposure.",
    riskMitigation: "Plan to reduce probability or impact.",
    riskOwner: "Person responsible for monitoring and mitigation.",
    riskStatus: "Current risk state: active, mitigated, accepted, or avoided.",
    riskEffortContingency: "Extra hours reserved because of this risk.",
    riskCostContingency: "Extra budget reserved because of this risk.",
    resourceUserId: "Team member assigned to the project.",
    resourceRole: "Project role such as developer, analyst, QA, architect, or PM.",
    resourceAllocation: "Percentage of working time allocated to this project.",
    resourceHourlyRate: "Hourly cost/rate used for burn and cost planning.",
    resourceStartDate: "When this resource starts on the project.",
    resourceEndDate: "When this resource is expected to finish.",
    resourceSkills: "Relevant skills, tools, and domain knowledge.",
    resourceAvailability: "Whether the resource is available, busy, or unavailable.",
    reportTitle: "Report name shown in the project report list.",
    reportType: "Report category, such as estimate, variance, risk, ML, or comparison.",
    reportFormat: "Output format. PDF and Excel downloads are available from the backend export endpoint.",
    reportIncludeConfidence: "Include uncertainty ranges so reviewers see best/worst case effort.",
    reportIncludeRisks: "Include risks and contingencies in generated reports.",
    reportIncludeScenarios: "Include optimistic/realistic/pessimistic scenario comparisons.",
    costDriverName: "Name of factor that changes estimate effort/cost. Example: High Security.",
    costDriverDescription: "Why this driver matters and when it should be used.",
    costDriverCategory: "Driver group such as people, process, technology, data, or schedule.",
    costDriverImpact: "Overall influence factor. Typical values are 0.5 to 2.0.",
    costDriverEffort: "Multiplier applied to effort.",
    costDriverCost: "Multiplier applied to cost.",
    costDriverDuration: "Multiplier applied to duration.",
    historicalProjectName: "Completed project name used as training/reference data.",
    historicalIndustry: "Business domain of the historical project.",
    historicalType: "Type of software delivered, such as mobile app, ERP, API, or dashboard.",
    historicalExperience: "Average team experience level.",
    historicalEffort: "Actual effort spent after completion. ML learns from this.",
    historicalDuration: "Actual calendar duration after completion.",
    historicalCost: "Actual final cost after completion.",
    historicalTeamSize: "Actual team size on the historical project.",
    historicalLanguage: "Primary programming language or stack.",
    historicalDatabase: "Main database/storage used.",
    historicalArchitecture: "Architecture style, such as monolith, microservices, distributed, or native.",
    historicalProductivity: "Historical productivity metric, often FP/person-month or similar.",
    historicalDefectDensity: "Defects per size unit. Higher values may indicate quality or complexity risk.",
    historicalScope: "Short explanation of what the historical project delivered.",
    calibrationName: "Name of the calibration model for historical adjustment.",
    calibrationType: "Model family, such as COCOMO, FPA, Hybrid, or ML.",
    calibrationDataCount: "Number of historical projects used to calibrate the model.",
    calibrationOrganization: "Organization or dataset owner.",
    calibrationIndustry: "Industry/domain this calibration applies to.",
    calibrationAccuracy: "Measured model accuracy percentage.",
    calibrationCoefficients: "JSON coefficients used by the calibration model.",
    calibrationDescription: "Plain-language explanation of this calibration.",
    mlName: "Machine learning model display name.",
    mlType: "ML task type, usually regression for effort/cost prediction.",
    mlAlgorithm: "Algorithm name, such as random_forest_regressor.",
    mlTrainingCount: "Number of historical rows used to train the model.",
    mlFeatureCount: "Number of input features used by the model.",
    mlFeatureNames: "Comma-separated model features. Example: team_size, adjusted_fp, risk_score.",
    mlAccuracy: "Overall model accuracy percentage.",
    mlPrecision: "Precision metric if classification is used; for regression this can be a quality proxy.",
    mlRecall: "Recall metric if classification is used; for regression this can be a quality proxy.",
    mlF1: "Balanced model quality score if classification is used.",
    mlDescription: "Explanation of what the ML model predicts and when to trust it.",
    roleName: "Security role name.",
    roleDescription: "What this role is responsible for.",
    rolePermissions: "Comma-separated permissions. Example: projects,estimates,reports.",
    profileFullName: "Your display name in the system.",
    profileUsername: "Your unique username.",
    profileRole: "Your assigned access role.",
    profileEmail: "Your account email.",
    profilePhone: "Optional phone number.",
    profileOrganization: "Your organization.",
    profileDepartment: "Your department/team.",
    currentPassword: "Current password required before changing it.",
    newPassword: "New password with at least 8 characters.",
    confirmPassword: "Repeat the new password to avoid mistakes.",
    connectionApiBaseUrl: "Backend API address used by this browser.",
    jiraJql: "Jira Query Language filter for imported issues. Example: project = ABC ORDER BY updated DESC.",
    jiraMaxResults: "Maximum Jira issues to import in one sync, from 1 to 100.",
    trelloBoardId: "Trello board ID to import. Leave blank to use TRELLO_BOARD_ID from backend/.env.",
};

function asNumber(value) {
    if (value === null || value === undefined || value === "") {
        return null;
    }
    const parsed = Number(value);
    return Number.isNaN(parsed) ? null : parsed;
}

function asInteger(value) {
    if (value === null || value === undefined || value === "") {
        return null;
    }
    const parsed = parseInt(value, 10);
    return Number.isNaN(parsed) ? null : parsed;
}

function toList(response) {
    if (Array.isArray(response)) {
        return response;
    }
    return response?.data || [];
}

function isFulfilled(result) {
    return result.status === "fulfilled";
}

export class CaseToolApp {
    constructor(api) {
        this.api = api;
        this.state = {
            currentView: localStorage.getItem(VIEW_STORAGE_KEY) || "dashboard",
            currentUser: null,
            roles: [],
            users: [],
            projects: [],
            projectDetail: null,
            selectedProjectId: asInteger(localStorage.getItem(PROJECT_STORAGE_KEY)),
            projectVersions: [],
            estimates: [],
            selectedEstimateId: null,
            estimateDetail: null,
            functionPoints: [],
            scenarios: [],
            risks: [],
            resources: [],
            reports: [],
            costDrivers: [],
            historicalProjects: [],
            calibrationModels: [],
            mlModels: [],
            dashboardAnalytics: null,
            notifications: [],
            integrationStatus: null,
            integrationSyncs: [],
            language: localStorage.getItem(LANGUAGE_STORAGE_KEY) || "en",
        };
        this.ui = {
            busyCount: 0,
            authTab: "login",
        };
    }

    init() {
        this.cacheElements();
        this.bindEvents();
        this.syncConnectionInputs();
        this.switchAuthTab("login");
        this.installFieldHelp();
        this.installLanguageSelector();
        this.applyLanguage();
        this.bootstrap();
    }

    cacheElements() {
        this.elements = {
            authView: document.getElementById("authView"),
            workspaceShell: document.getElementById("workspaceShell"),
            loadingBar: document.getElementById("loadingBar"),
            toastStack: document.getElementById("toastStack"),
            projectSwitcher: document.getElementById("projectSwitcher"),
            userBadge: document.getElementById("userBadge"),
            selectedProjectBadge: document.getElementById("selectedProjectBadge"),
            apiStatusBadge: document.getElementById("apiStatusBadge"),
            authApiBaseUrl: document.getElementById("authApiBaseUrl"),
            connectionApiBaseUrl: document.getElementById("connectionApiBaseUrl"),
            registerRoleId: document.getElementById("registerRoleId"),
            resourceUserId: document.getElementById("resourceUserId"),
            estimateVersionId: document.getElementById("estimateVersionId"),
            profileRole: document.getElementById("profileRole"),
            dashboardMetrics: document.getElementById("dashboardMetrics"),
            dashboardAnalyticsGrid: document.getElementById("dashboardAnalyticsGrid"),
            dashboardSpotlight: document.getElementById("dashboardSpotlight"),
            recentProjectsBody: document.getElementById("recentProjectsBody"),
            recentEstimatesList: document.getElementById("recentEstimatesList"),
            dashboardRiskSummary: document.getElementById("dashboardRiskSummary"),
            projectTableBody: document.getElementById("projectTableBody"),
            versionList: document.getElementById("versionList"),
            estimateTableBody: document.getElementById("estimateTableBody"),
            estimateDetail: document.getElementById("estimateDetail"),
            functionPointList: document.getElementById("functionPointList"),
            scenarioTableBody: document.getElementById("scenarioTableBody"),
            scenarioSummary: document.getElementById("scenarioSummary"),
            riskTableBody: document.getElementById("riskTableBody"),
            riskExposureSummary: document.getElementById("riskExposureSummary"),
            resourceTableBody: document.getElementById("resourceTableBody"),
            resourceUtilizationSummary: document.getElementById("resourceUtilizationSummary"),
            reportTableBody: document.getElementById("reportTableBody"),
            reportPreview: document.getElementById("reportPreview"),
            costDriverTableBody: document.getElementById("costDriverTableBody"),
            historicalProjectTableBody: document.getElementById("historicalProjectTableBody"),
            calibrationModelTableBody: document.getElementById("calibrationModelTableBody"),
            mlModelTableBody: document.getElementById("mlModelTableBody"),
            roleTableBody: document.getElementById("roleTableBody"),
            userTableBody: document.getElementById("userTableBody"),
            estimateContextBanner: document.getElementById("estimateContextBanner"),
            scenarioContextBanner: document.getElementById("scenarioContextBanner"),
            riskContextBanner: document.getElementById("riskContextBanner"),
            resourceContextBanner: document.getElementById("resourceContextBanner"),
            reportContextBanner: document.getElementById("reportContextBanner"),
            projectsContextBanner: document.getElementById("projectsContextBanner"),
            intelligenceBanner: document.getElementById("intelligenceBanner"),
            adminBanner: document.getElementById("adminBanner"),
            integrationBanner: document.getElementById("integrationBanner"),
            integrationStatusPanel: document.getElementById("integrationStatusPanel"),
            integrationSyncTableBody: document.getElementById("integrationSyncTableBody"),
        };
    }

    bindEvents() {
        const bindAsync = (element, eventName, handler) => {
            element.addEventListener(eventName, (event) => {
                Promise.resolve(handler(event)).catch(() => {});
            });
        };

        document.querySelectorAll("[data-auth-tab]").forEach((button) => {
            button.addEventListener("click", () => this.switchAuthTab(button.dataset.authTab));
        });

        document.querySelectorAll("[data-view-target]").forEach((button) => {
            button.addEventListener("click", () => this.navigateToView(button.dataset.viewTarget));
        });

        document.querySelectorAll("[data-dashboard-view]").forEach((button) => {
            button.addEventListener("click", () => this.navigateToView(button.dataset.dashboardView));
        });

        bindAsync(document.getElementById("loginForm"), "submit", (event) => this.handleLogin(event));
        bindAsync(document.getElementById("registerForm"), "submit", (event) => this.handleRegister(event));
        bindAsync(document.getElementById("logoutBtn"), "click", () => this.handleLogout());
        bindAsync(document.getElementById("refreshWorkspaceBtn"), "click", () => this.refreshWorkspace());
        bindAsync(document.getElementById("projectSwitcher"), "change", (event) => {
            return this.selectProject(asInteger(event.target.value));
        });
        bindAsync(document.getElementById("authConnectionForm"), "submit", (event) => this.handleConnectionSave(event, "auth"));
        bindAsync(document.getElementById("connectionForm"), "submit", (event) => this.handleConnectionSave(event, "workspace"));

        bindAsync(document.getElementById("projectForm"), "submit", (event) => this.handleProjectSubmit(event));
        document.getElementById("projectFormReset").addEventListener("click", () => this.resetProjectForm());
        bindAsync(document.getElementById("versionForm"), "submit", (event) => this.handleVersionSubmit(event));
        document.getElementById("versionFormReset").addEventListener("click", () => this.resetVersionForm());

        bindAsync(document.getElementById("estimateForm"), "submit", (event) => this.handleEstimateSubmit(event));
        document.getElementById("estimateFormReset").addEventListener("click", () => this.resetEstimateForm());
        bindAsync(document.getElementById("functionPointForm"), "submit", (event) => this.handleFunctionPointSubmit(event));
        document.getElementById("functionPointFormReset").addEventListener("click", () => this.resetFunctionPointForm());

        bindAsync(document.getElementById("scenarioForm"), "submit", (event) => this.handleScenarioSubmit(event));
        document.getElementById("scenarioFormReset").addEventListener("click", () => this.resetScenarioForm());

        bindAsync(document.getElementById("riskForm"), "submit", (event) => this.handleRiskSubmit(event));
        document.getElementById("riskFormReset").addEventListener("click", () => this.resetRiskForm());

        bindAsync(document.getElementById("resourceForm"), "submit", (event) => this.handleResourceSubmit(event));
        document.getElementById("resourceFormReset").addEventListener("click", () => this.resetResourceForm());

        bindAsync(document.getElementById("reportForm"), "submit", (event) => this.handleReportSubmit(event));
        document.getElementById("reportFormReset").addEventListener("click", () => this.resetReportForm());

        bindAsync(document.getElementById("costDriverForm"), "submit", (event) => this.handleCostDriverSubmit(event));
        document.getElementById("costDriverFormReset").addEventListener("click", () => this.resetCostDriverForm());

        bindAsync(document.getElementById("historicalProjectForm"), "submit", (event) => this.handleHistoricalProjectSubmit(event));
        document.getElementById("historicalProjectFormReset").addEventListener("click", () => this.resetHistoricalProjectForm());

        bindAsync(document.getElementById("calibrationModelForm"), "submit", (event) => this.handleCalibrationModelSubmit(event));
        document.getElementById("calibrationModelFormReset").addEventListener("click", () => this.resetCalibrationModelForm());

        bindAsync(document.getElementById("mlModelForm"), "submit", (event) => this.handleMlModelSubmit(event));
        document.getElementById("mlModelFormReset").addEventListener("click", () => this.resetMlModelForm());

        bindAsync(document.getElementById("roleForm"), "submit", (event) => this.handleRoleSubmit(event));
        document.getElementById("roleFormReset").addEventListener("click", () => this.resetRoleForm());

        bindAsync(document.getElementById("jiraSyncForm"), "submit", (event) => this.handleJiraSync(event));
        bindAsync(document.getElementById("trelloSyncForm"), "submit", (event) => this.handleTrelloSync(event));

        bindAsync(document.getElementById("profileForm"), "submit", (event) => this.handleProfileSubmit(event));
        bindAsync(document.getElementById("passwordForm"), "submit", (event) => this.handlePasswordSubmit(event));

        bindAsync(this.elements.projectTableBody, "click", (event) => this.handleProjectTableClick(event));
        bindAsync(this.elements.recentProjectsBody, "click", (event) => this.handleProjectTableClick(event));
        bindAsync(this.elements.estimateTableBody, "click", (event) => this.handleEstimateTableClick(event));
        bindAsync(this.elements.scenarioTableBody, "click", (event) => this.handleScenarioTableClick(event));
        bindAsync(this.elements.riskTableBody, "click", (event) => this.handleRiskTableClick(event));
        bindAsync(this.elements.resourceTableBody, "click", (event) => this.handleResourceTableClick(event));
        bindAsync(this.elements.reportTableBody, "click", (event) => this.handleReportTableClick(event));
        bindAsync(this.elements.mlModelTableBody, "click", (event) => this.handleMlModelTableClick(event));
    }

    async bootstrap() {
        await this.refreshApiStatus();
        await this.loadPublicReferenceData();

        if (this.api.isAuthenticated()) {
            try {
                await this.startAuthenticatedSession();
                return;
            } catch (error) {
                this.api.clearTokens();
                this.showToast(`Session expired: ${error.message}`, "warning");
            }
        }

        this.showAuth();
    }

    async loadPublicReferenceData() {
        try {
            const rolesResponse = await this.api.listRoles();
            this.state.roles = toList(rolesResponse);
            this.renderRoleOptions();
        } catch (error) {
            this.state.roles = [];
            this.renderRoleOptions();
            this.showToast(`Roles unavailable: ${error.message}`, "warning");
        }
    }

    async startAuthenticatedSession() {
        await this.runTask(async () => {
            const identity = await this.api.getCurrentUser();
            const fullUser = await this.api.getUser(identity.id);
            this.state.currentUser = {
                ...identity,
                ...fullUser,
                role_name: fullUser.role?.name || this.getRoleName(identity.role_id),
            };

            await this.loadWorkspaceData();
            this.showWorkspace();
            this.navigateToView(this.state.currentView);
        }, "Loading workspace");
    }

    async loadWorkspaceData() {
        const results = await Promise.allSettled([
            this.api.listRoles(),
            this.api.listUsers(),
            this.api.getProjects(),
            this.api.listCostDrivers(),
            this.api.listHistoricalProjects(),
            this.api.listCalibrationModels(),
            this.api.listMlModels(),
            this.api.getDashboardAnalytics(),
            this.api.listNotifications(false, 20),
            this.api.getIntegrationStatus(),
            this.api.listIntegrationSyncs(),
        ]);

        const [
            rolesResponse,
            usersResponse,
            projectsResponse,
            costDriversResponse,
            historicalProjectsResponse,
            calibrationModelsResponse,
            mlModelsResponse,
            dashboardAnalyticsResponse,
            notificationsResponse,
            integrationStatusResponse,
            integrationSyncsResponse,
        ] = results;

        this.state.roles = isFulfilled(rolesResponse) ? toList(rolesResponse.value) : [];
        this.state.users = isFulfilled(usersResponse) ? toList(usersResponse.value) : [];
        this.state.projects = isFulfilled(projectsResponse) ? toList(projectsResponse.value) : [];
        this.state.costDrivers = isFulfilled(costDriversResponse) ? toList(costDriversResponse.value) : [];
        this.state.historicalProjects = isFulfilled(historicalProjectsResponse) ? toList(historicalProjectsResponse.value) : [];
        this.state.calibrationModels = isFulfilled(calibrationModelsResponse) ? toList(calibrationModelsResponse.value) : [];
        this.state.mlModels = isFulfilled(mlModelsResponse) ? toList(mlModelsResponse.value) : [];
        this.state.dashboardAnalytics = isFulfilled(dashboardAnalyticsResponse) ? dashboardAnalyticsResponse.value : null;
        this.state.notifications = isFulfilled(notificationsResponse) ? toList(notificationsResponse.value) : [];
        this.state.integrationStatus = isFulfilled(integrationStatusResponse) ? integrationStatusResponse.value : null;
        this.state.integrationSyncs = isFulfilled(integrationSyncsResponse) ? toList(integrationSyncsResponse.value) : [];

        results.forEach((result, index) => {
            if (result.status === "rejected") {
                const labels = [
                    "roles",
                    "users",
                    "projects",
                    "cost drivers",
                    "historical projects",
                    "calibration models",
                    "ML models",
                    "dashboard analytics",
                    "notifications",
                    "integration status",
                    "integration sync history",
                ];
                this.showToast(`Could not load ${labels[index]}: ${result.reason.message}`, "warning");
            }
        });

        const availableProjectIds = new Set(this.state.projects.map((project) => project.id));
        if (!availableProjectIds.has(this.state.selectedProjectId)) {
            this.state.selectedProjectId = this.state.projects[0]?.id || null;
        }

        this.renderAll();

        if (this.state.selectedProjectId) {
            await this.loadProjectScopedData(this.state.selectedProjectId);
        } else {
            this.clearProjectScopedState();
            this.renderAll();
        }
    }

    async loadProjectScopedData(projectId) {
        if (!projectId) {
            this.clearProjectScopedState();
            this.renderAll();
            return;
        }

        const results = await Promise.allSettled([
            this.api.getProject(projectId),
            this.api.listProjectVersions(projectId),
            this.api.getEstimates(projectId),
            this.api.getScenarios(projectId),
            this.api.getRisks(projectId),
            this.api.getResources(projectId),
            this.api.getReports(projectId),
        ]);

        const [
            projectDetail,
            versionsResponse,
            estimatesResponse,
            scenariosResponse,
            risksResponse,
            resourcesResponse,
            reportsResponse,
        ] = results;

        this.state.projectDetail = isFulfilled(projectDetail) ? projectDetail.value : this.state.projects.find((project) => project.id === projectId) || null;
        this.state.projectVersions = isFulfilled(versionsResponse) ? versionsResponse.value?.versions || [] : [];
        this.state.estimates = isFulfilled(estimatesResponse) ? toList(estimatesResponse.value) : [];
        this.state.scenarios = isFulfilled(scenariosResponse) ? toList(scenariosResponse.value) : [];
        this.state.risks = isFulfilled(risksResponse) ? toList(risksResponse.value) : [];
        this.state.resources = isFulfilled(resourcesResponse) ? toList(resourcesResponse.value) : [];
        this.state.reports = isFulfilled(reportsResponse) ? toList(reportsResponse.value) : [];

        results.forEach((result, index) => {
            if (result.status === "rejected") {
                const labels = [
                    "project details",
                    "project versions",
                    "estimates",
                    "scenarios",
                    "risks",
                    "resources",
                    "reports",
                ];
                this.showToast(`Could not load ${labels[index]}: ${result.reason.message}`, "warning");
            }
        });

        const projectIndex = this.state.projects.findIndex((project) => project.id === projectId);
        if (projectIndex >= 0 && this.state.projectDetail) {
            this.state.projects[projectIndex] = {
                ...this.state.projects[projectIndex],
                ...this.state.projectDetail,
            };
        }

        if (!this.state.estimates.find((estimate) => estimate.id === this.state.selectedEstimateId)) {
            this.state.selectedEstimateId = this.state.estimates[0]?.id || null;
        }

        if (this.state.selectedEstimateId) {
            await this.loadEstimateDetail(this.state.selectedEstimateId, false);
        } else {
            this.state.estimateDetail = null;
            this.state.functionPoints = [];
        }

        this.renderAll();
    }

    async loadEstimateDetail(estimateId, shouldRender = true) {
        const [estimateDetail, functionPointsResponse] = await Promise.all([
            this.api.getEstimate(estimateId),
            this.api.listFunctionPoints(estimateId),
        ]);

        this.state.selectedEstimateId = estimateId;
        this.state.estimateDetail = estimateDetail;
        this.state.functionPoints = functionPointsResponse?.function_points || [];

        if (shouldRender) {
            this.renderEstimates();
        }
    }

    clearProjectScopedState() {
        this.state.projectDetail = null;
        this.state.projectVersions = [];
        this.state.estimates = [];
        this.state.selectedEstimateId = null;
        this.state.estimateDetail = null;
        this.state.functionPoints = [];
        this.state.scenarios = [];
        this.state.risks = [];
        this.state.resources = [];
        this.state.reports = [];
    }

    navigateToView(view) {
        this.state.currentView = view;
        localStorage.setItem(VIEW_STORAGE_KEY, view);

        document.querySelectorAll("[data-view-target]").forEach((button) => {
            button.classList.toggle("active", button.dataset.viewTarget === view);
        });

        document.querySelectorAll(".view-panel").forEach((panel) => {
            panel.classList.toggle("active", panel.dataset.view === view);
        });
    }

    switchAuthTab(tabName) {
        this.ui.authTab = tabName;
        document.querySelectorAll("[data-auth-tab]").forEach((button) => {
            button.classList.toggle("active", button.dataset.authTab === tabName);
        });
        document.querySelectorAll(".auth-form").forEach((form) => {
            form.classList.toggle("active", form.dataset.authForm === tabName);
        });
    }

    showAuth() {
        this.elements.authView.classList.remove("hidden");
        this.elements.workspaceShell.classList.add("hidden");
    }

    showWorkspace() {
        this.elements.authView.classList.add("hidden");
        this.elements.workspaceShell.classList.remove("hidden");
    }

    async handleLogin(event) {
        event.preventDefault();
        const email = document.getElementById("loginEmail").value.trim();
        const password = document.getElementById("loginPassword").value;

        await this.runTask(async () => {
            await this.api.login(email, password);
            document.getElementById("loginForm").reset();
            await this.startAuthenticatedSession();
            this.showToast("Welcome back. Workspace connected.", "success");
        }, "Signing in");
    }

    async handleRegister(event) {
        event.preventDefault();
        const password = document.getElementById("registerPassword").value;
        const roleId = asInteger(this.elements.registerRoleId.value);

        if (!roleId) {
            this.showToast("Choose a role before registering.", "warning");
            return;
        }

        await this.runTask(async () => {
            await this.api.registerUser({
                email: document.getElementById("registerEmail").value.trim(),
                username: document.getElementById("registerUsername").value.trim(),
                full_name: document.getElementById("registerFullName").value.trim(),
                password,
                role_id: roleId,
                phone: document.getElementById("registerPhone").value.trim() || null,
                organization: document.getElementById("registerOrganization").value.trim() || null,
                department: document.getElementById("registerDepartment").value.trim() || null,
            });

            await this.api.login(document.getElementById("registerEmail").value.trim(), password);
            document.getElementById("registerForm").reset();
            await this.startAuthenticatedSession();
            this.showToast("Account created and signed in.", "success");
        }, "Creating account");
    }

    async handleLogout() {
        await this.api.logout();
        this.state.currentUser = null;
        this.state.projects = [];
        this.clearProjectScopedState();
        this.renderAll();
        this.showAuth();
        this.showToast("Signed out successfully.", "info");
    }

    async refreshWorkspace() {
        if (!this.api.isAuthenticated()) {
            return;
        }

        await this.runTask(async () => {
            await this.loadWorkspaceData();
            this.showToast("Workspace refreshed.", "success");
        }, "Refreshing data");
    }

    async selectProject(projectId) {
        this.state.selectedProjectId = projectId;
        if (projectId) {
            localStorage.setItem(PROJECT_STORAGE_KEY, String(projectId));
        } else {
            localStorage.removeItem(PROJECT_STORAGE_KEY);
        }

        await this.runTask(async () => {
            await this.loadProjectScopedData(projectId);
            if (this.selectedProject) {
                this.showToast(`Project selected: ${this.selectedProject.name}`, "info");
            }
        }, "Switching project");
    }

    async handleConnectionSave(event, context) {
        event.preventDefault();
        const input = context === "auth" ? this.elements.authApiBaseUrl : this.elements.connectionApiBaseUrl;
        const nextBaseUrl = input.value.trim();
        this.api.setBaseURL(nextBaseUrl);
        this.syncConnectionInputs();

        await this.runTask(async () => {
            await this.refreshApiStatus();
            await this.loadPublicReferenceData();
            if (this.api.isAuthenticated()) {
                await this.loadWorkspaceData();
            }
            this.showToast("API endpoint saved.", "success");
        }, "Saving connection");
    }

    async handleProjectSubmit(event) {
        event.preventDefault();
        const projectId = asInteger(document.getElementById("projectFormId").value);
        const payload = {
            name: document.getElementById("projectName").value.trim(),
            description: document.getElementById("projectDescription").value.trim() || null,
            status: document.getElementById("projectStatus").value,
            budget: asNumber(document.getElementById("projectBudget").value),
            team_size: asInteger(document.getElementById("projectTeamSize").value),
            client_name: document.getElementById("projectClientName").value.trim() || null,
            project_manager: document.getElementById("projectManager").value.trim() || null,
            department: document.getElementById("projectDepartment").value.trim() || null,
            start_date: this.toIsoDateTime(document.getElementById("projectStartDate").value),
            end_date: this.toIsoDateTime(document.getElementById("projectEndDate").value),
        };

        await this.runTask(async () => {
            let savedProject;
            if (projectId) {
                savedProject = await this.api.updateProject(projectId, payload);
                this.showToast("Project updated.", "success");
            } else {
                savedProject = await this.api.createProject(payload);
                this.state.selectedProjectId = savedProject.id;
                localStorage.setItem(PROJECT_STORAGE_KEY, String(savedProject.id));
                this.showToast("Project created with baseline version.", "success");
            }

            this.resetProjectForm();
            await this.loadWorkspaceData();
            await this.loadProjectScopedData(savedProject.id);
        }, projectId ? "Updating project" : "Creating project");
    }

    async handleVersionSubmit(event) {
        event.preventDefault();
        if (!this.requireProjectContext("Create a project version")) {
            return;
        }

        const payload = {
            version_number: asInteger(document.getElementById("versionNumber").value),
            description: document.getElementById("versionDescription").value.trim() || null,
            scope: document.getElementById("versionScope").value.trim() || null,
            assumptions: document.getElementById("versionAssumptions").value.trim() || null,
            constraints: document.getElementById("versionConstraints").value.trim() || null,
        };

        await this.runTask(async () => {
            await this.api.createProjectVersion(this.selectedProject.id, payload);
            this.resetVersionForm();
            await this.loadProjectScopedData(this.selectedProject.id);
            this.showToast("Project version added.", "success");
        }, "Saving version");
    }

    async handleEstimateSubmit(event) {
        event.preventDefault();
        if (!this.requireProjectContext("Create an estimate")) {
            return;
        }

        const estimateId = asInteger(document.getElementById("estimateFormId").value);
        const selectedStatus = document.getElementById("estimateStatus").value;

        await this.runTask(async () => {
            if (estimateId) {
                await this.api.updateEstimate(estimateId, {
                    status: selectedStatus,
                    estimated_effort_hours: asNumber(document.getElementById("estimateEffort").value),
                    estimated_duration_months: asNumber(document.getElementById("estimateDuration").value),
                    estimated_cost: asNumber(document.getElementById("estimateCost").value),
                    estimated_team_size: asInteger(document.getElementById("estimateTeamSize").value),
                    confidence_level: asInteger(document.getElementById("estimateConfidence").value),
                    confidence_interval_low: asNumber(document.getElementById("estimateConfidenceLow").value),
                    confidence_interval_high: asNumber(document.getElementById("estimateConfidenceHigh").value),
                    notes: document.getElementById("estimateNotes").value.trim() || null,
                });
                this.showToast("Estimate updated.", "success");
            } else {
                const createdEstimate = await this.api.createEstimate({
                    project_id: this.selectedProject.id,
                    version_id: asInteger(this.elements.estimateVersionId.value),
                    estimation_method: document.getElementById("estimateMethod").value,
                    estimated_effort_hours: asNumber(document.getElementById("estimateEffort").value),
                    estimated_duration_months: asNumber(document.getElementById("estimateDuration").value),
                    estimated_cost: asNumber(document.getElementById("estimateCost").value),
                    estimated_team_size: asInteger(document.getElementById("estimateTeamSize").value),
                    confidence_level: asInteger(document.getElementById("estimateConfidence").value),
                    confidence_interval_low: asNumber(document.getElementById("estimateConfidenceLow").value),
                    confidence_interval_high: asNumber(document.getElementById("estimateConfidenceHigh").value),
                    assumptions: document.getElementById("estimateAssumptions").value.trim() || null,
                    risks: document.getElementById("estimateRisks").value.trim() || null,
                    notes: document.getElementById("estimateNotes").value.trim() || null,
                });

                if (selectedStatus !== "draft") {
                    await this.api.updateEstimate(createdEstimate.id, { status: selectedStatus });
                }
                this.state.selectedEstimateId = createdEstimate.id;
                this.showToast("Estimate created.", "success");
            }

            this.resetEstimateForm();
            await this.loadProjectScopedData(this.selectedProject.id);
        }, estimateId ? "Updating estimate" : "Creating estimate");
    }

    async handleFunctionPointSubmit(event) {
        event.preventDefault();
        if (!this.state.selectedEstimateId) {
            this.showToast("Select an estimate before adding function points.", "warning");
            return;
        }

        const payload = {
            ilf_count: asInteger(document.getElementById("fpIlfCount").value) || 0,
            ilf_complexity: document.getElementById("fpIlfComplexity").value || null,
            eif_count: asInteger(document.getElementById("fpEifCount").value) || 0,
            eif_complexity: document.getElementById("fpEifComplexity").value || null,
            ei_count: asInteger(document.getElementById("fpEiCount").value) || 0,
            ei_complexity: document.getElementById("fpEiComplexity").value || null,
            eo_count: asInteger(document.getElementById("fpEoCount").value) || 0,
            eo_complexity: document.getElementById("fpEoComplexity").value || null,
            eq_count: asInteger(document.getElementById("fpEqCount").value) || 0,
            eq_complexity: document.getElementById("fpEqComplexity").value || null,
            unadjusted_fp: asNumber(document.getElementById("fpUnadjusted").value),
            vaf: asNumber(document.getElementById("fpVaf").value),
            adjusted_fp: asNumber(document.getElementById("fpAdjusted").value),
        };

        await this.runTask(async () => {
            await this.api.createFunctionPoints(this.state.selectedEstimateId, payload);
            this.resetFunctionPointForm();
            await this.loadEstimateDetail(this.state.selectedEstimateId);
            this.showToast("Function point analysis saved.", "success");
        }, "Saving function points");
    }

    async handleScenarioSubmit(event) {
        event.preventDefault();
        if (!this.requireProjectContext("Create a scenario")) {
            return;
        }

        const scenarioId = asInteger(document.getElementById("scenarioFormId").value);
        const payload = {
            project_id: this.selectedProject.id,
            name: document.getElementById("scenarioName").value.trim(),
            description: document.getElementById("scenarioDescription").value.trim() || null,
            scenario_type: document.getElementById("scenarioType").value,
            effort_adjustment: asNumber(document.getElementById("scenarioEffortAdjustment").value) || 1,
            duration_adjustment: asNumber(document.getElementById("scenarioDurationAdjustment").value) || 1,
            cost_adjustment: asNumber(document.getElementById("scenarioCostAdjustment").value) || 1,
            team_size_adjustment: asNumber(document.getElementById("scenarioTeamAdjustment").value) || 1,
        };

        await this.runTask(async () => {
            if (scenarioId) {
                await this.api.updateScenario(scenarioId, payload);
                this.showToast("Scenario updated.", "success");
            } else {
                await this.api.createScenario(payload);
                this.showToast("Scenario created.", "success");
            }

            this.resetScenarioForm();
            await this.loadProjectScopedData(this.selectedProject.id);
        }, scenarioId ? "Updating scenario" : "Creating scenario");
    }

    async handleRiskSubmit(event) {
        event.preventDefault();
        if (!this.requireProjectContext("Create a risk")) {
            return;
        }

        const riskId = asInteger(document.getElementById("riskFormId").value);
        const payload = {
            project_id: this.selectedProject.id,
            description: document.getElementById("riskDescription").value.trim(),
            category: document.getElementById("riskCategory").value.trim(),
            probability: asNumber(document.getElementById("riskProbability").value),
            impact: asNumber(document.getElementById("riskImpact").value),
            mitigation_strategy: document.getElementById("riskMitigation").value.trim() || null,
            owner: document.getElementById("riskOwner").value.trim() || null,
            status: document.getElementById("riskStatus").value,
            effort_contingency: asNumber(document.getElementById("riskEffortContingency").value) || 0,
            cost_contingency: asNumber(document.getElementById("riskCostContingency").value) || 0,
        };

        await this.runTask(async () => {
            if (riskId) {
                await this.api.updateRisk(riskId, payload);
                this.showToast("Risk updated.", "success");
            } else {
                await this.api.createRisk(payload);
                this.showToast("Risk logged.", "success");
            }

            this.resetRiskForm();
            await this.loadProjectScopedData(this.selectedProject.id);
        }, riskId ? "Updating risk" : "Saving risk");
    }

    async handleResourceSubmit(event) {
        event.preventDefault();
        if (!this.requireProjectContext("Create a resource allocation")) {
            return;
        }

        const resourceId = asInteger(document.getElementById("resourceFormId").value);
        const payload = {
            project_id: this.selectedProject.id,
            user_id: asInteger(this.elements.resourceUserId.value),
            role: document.getElementById("resourceRole").value.trim(),
            allocation_percentage: asNumber(document.getElementById("resourceAllocation").value),
            hourly_rate: asNumber(document.getElementById("resourceHourlyRate").value),
            start_date: this.toIsoDateTime(document.getElementById("resourceStartDate").value),
            end_date: this.toIsoDateTime(document.getElementById("resourceEndDate").value),
            skills: document.getElementById("resourceSkills").value.trim() || null,
            availability: document.getElementById("resourceAvailability").value,
        };

        await this.runTask(async () => {
            if (resourceId) {
                await this.api.updateResource(resourceId, payload);
                this.showToast("Resource updated.", "success");
            } else {
                await this.api.createResource(payload);
                this.showToast("Resource allocated.", "success");
            }

            this.resetResourceForm();
            await this.loadProjectScopedData(this.selectedProject.id);
        }, resourceId ? "Updating resource" : "Allocating resource");
    }

    async handleReportSubmit(event) {
        event.preventDefault();
        if (!this.requireProjectContext("Generate a report")) {
            return;
        }

        const format = document.getElementById("reportFormat").value;
        const report = {
            project_id: this.selectedProject.id,
            title: document.getElementById("reportTitle").value.trim(),
            report_type: document.getElementById("reportType").value,
            format,
            include_confidence_intervals: document.getElementById("reportIncludeConfidence").checked,
            include_risks: document.getElementById("reportIncludeRisks").checked,
            include_scenarios: document.getElementById("reportIncludeScenarios").checked,
            content: this.buildReportContent(format),
        };

        await this.runTask(async () => {
            const created = await this.api.createReport(report);
            this.resetReportForm();
            await this.loadProjectScopedData(this.selectedProject.id);
            this.previewReport(created.id);
            this.showToast("Report generated and stored.", "success");
        }, "Generating report");
    }

    async handleCostDriverSubmit(event) {
        event.preventDefault();
        const payload = {
            name: document.getElementById("costDriverName").value.trim(),
            description: document.getElementById("costDriverDescription").value.trim() || null,
            category: document.getElementById("costDriverCategory").value.trim(),
            impact_factor: asNumber(document.getElementById("costDriverImpact").value),
            effort_multiplier: asNumber(document.getElementById("costDriverEffort").value),
            cost_multiplier: asNumber(document.getElementById("costDriverCost").value),
            duration_multiplier: asNumber(document.getElementById("costDriverDuration").value),
            is_active: document.getElementById("costDriverActive").checked,
        };

        await this.runTask(async () => {
            await this.api.createCostDriver(payload);
            this.resetCostDriverForm();
            this.state.costDrivers = toList(await this.api.listCostDrivers());
            this.renderIntelligence();
            this.showToast("Cost driver saved.", "success");
        }, "Saving cost driver");
    }

    async handleHistoricalProjectSubmit(event) {
        event.preventDefault();
        const payload = {
            project_name: document.getElementById("historicalProjectName").value.trim(),
            industry: document.getElementById("historicalIndustry").value.trim() || null,
            project_type: document.getElementById("historicalType").value.trim() || null,
            team_experience: document.getElementById("historicalExperience").value || null,
            actual_effort_hours: asNumber(document.getElementById("historicalEffort").value),
            actual_duration_months: asNumber(document.getElementById("historicalDuration").value),
            actual_cost: asNumber(document.getElementById("historicalCost").value),
            team_size: asInteger(document.getElementById("historicalTeamSize").value),
            language: document.getElementById("historicalLanguage").value.trim() || null,
            database_type: document.getElementById("historicalDatabase").value.trim() || null,
            architecture: document.getElementById("historicalArchitecture").value.trim() || null,
            scope_description: document.getElementById("historicalScope").value.trim() || null,
            productivity: asNumber(document.getElementById("historicalProductivity").value),
            defect_density: asNumber(document.getElementById("historicalDefectDensity").value),
        };

        await this.runTask(async () => {
            await this.api.createHistoricalProject(payload);
            this.resetHistoricalProjectForm();
            this.state.historicalProjects = toList(await this.api.listHistoricalProjects());
            this.renderIntelligence();
            this.showToast("Historical project added.", "success");
        }, "Saving historical project");
    }

    async handleCalibrationModelSubmit(event) {
        event.preventDefault();
        const coefficientsText = document.getElementById("calibrationCoefficients").value.trim();
        let coefficients = null;

        if (coefficientsText) {
            try {
                coefficients = JSON.parse(coefficientsText);
            } catch (error) {
                this.showToast("Coefficients JSON is invalid.", "warning");
                return;
            }
        }

        const payload = {
            name: document.getElementById("calibrationName").value.trim(),
            description: document.getElementById("calibrationDescription").value.trim() || null,
            model_type: document.getElementById("calibrationType").value.trim(),
            organization: document.getElementById("calibrationOrganization").value.trim() || null,
            industry: document.getElementById("calibrationIndustry").value.trim() || null,
            calibration_data_count: asInteger(document.getElementById("calibrationDataCount").value),
            accuracy_percentage: asNumber(document.getElementById("calibrationAccuracy").value),
            coefficients,
        };

        await this.runTask(async () => {
            await this.api.createCalibrationModel(payload);
            this.resetCalibrationModelForm();
            this.state.calibrationModels = toList(await this.api.listCalibrationModels());
            this.renderIntelligence();
            this.showToast("Calibration model saved.", "success");
        }, "Saving calibration model");
    }

    async handleMlModelSubmit(event) {
        event.preventDefault();
        const featureNames = document.getElementById("mlFeatureNames").value
            .split(",")
            .map((feature) => feature.trim())
            .filter(Boolean);

        const payload = {
            name: document.getElementById("mlName").value.trim(),
            description: document.getElementById("mlDescription").value.trim() || null,
            model_type: document.getElementById("mlType").value.trim(),
            algorithm: document.getElementById("mlAlgorithm").value.trim(),
            training_data_count: asInteger(document.getElementById("mlTrainingCount").value),
            feature_count: asInteger(document.getElementById("mlFeatureCount").value),
            feature_names: featureNames,
            accuracy: asNumber(document.getElementById("mlAccuracy").value),
            precision: asNumber(document.getElementById("mlPrecision").value),
            recall: asNumber(document.getElementById("mlRecall").value),
            f1_score: asNumber(document.getElementById("mlF1").value),
            is_active: document.getElementById("mlIsActive").checked,
            is_production: document.getElementById("mlIsProduction").checked,
        };

        await this.runTask(async () => {
            await this.api.createMlModel(payload);
            this.resetMlModelForm();
            this.state.mlModels = toList(await this.api.listMlModels());
            this.renderIntelligence();
            this.showToast("ML model saved.", "success");
        }, "Saving ML model");
    }

    async handleRoleSubmit(event) {
        event.preventDefault();
        const payload = {
            name: document.getElementById("roleName").value.trim(),
            description: document.getElementById("roleDescription").value.trim() || null,
            permissions: document.getElementById("rolePermissions").value.trim() || null,
            is_active: document.getElementById("roleIsActive").checked,
        };

        await this.runTask(async () => {
            await this.api.createRole(payload);
            this.resetRoleForm();
            this.state.roles = toList(await this.api.listRoles());
            this.renderRoleOptions();
            this.renderAdmin();
            this.showToast("Role created.", "success");
        }, "Saving role");
    }

    async handleJiraSync(event) {
        event.preventDefault();
        const jql = document.getElementById("jiraJql").value.trim() || null;
        const maxResults = asInteger(document.getElementById("jiraMaxResults").value) || 50;

        await this.runTask(async () => {
            const response = await this.api.syncJira(jql, maxResults);
            this.state.integrationSyncs = toList(await this.api.listIntegrationSyncs());
            this.state.projects = toList(await this.api.getProjects());
            this.renderIntegrations();
            this.renderProjectSwitcher();
            this.renderDashboard();
            this.showToast(`Jira synced into project #${response.project_id}.`, "success");
        }, "Syncing Jira");
    }

    async handleTrelloSync(event) {
        event.preventDefault();
        const boardId = document.getElementById("trelloBoardId").value.trim() || null;

        await this.runTask(async () => {
            const response = await this.api.syncTrello(boardId);
            this.state.integrationSyncs = toList(await this.api.listIntegrationSyncs());
            this.state.projects = toList(await this.api.getProjects());
            this.renderIntegrations();
            this.renderProjectSwitcher();
            this.renderDashboard();
            this.showToast(`Trello synced into project #${response.project_id}.`, "success");
        }, "Syncing Trello");
    }

    async handleProfileSubmit(event) {
        event.preventDefault();
        if (!this.state.currentUser) {
            return;
        }

        const payload = {
            full_name: document.getElementById("profileFullName").value.trim(),
            username: document.getElementById("profileUsername").value.trim(),
            email: document.getElementById("profileEmail").value.trim(),
            phone: document.getElementById("profilePhone").value.trim() || null,
            organization: document.getElementById("profileOrganization").value.trim() || null,
            department: document.getElementById("profileDepartment").value.trim() || null,
        };

        await this.runTask(async () => {
            const updated = await this.api.updateUser(this.state.currentUser.id, payload);
            this.state.currentUser = {
                ...this.state.currentUser,
                ...updated,
                role_name: this.getRoleName(updated.role_id),
            };
            this.renderSettings();
            this.renderHeader();
            this.showToast("Profile updated.", "success");
        }, "Saving profile");
    }

    async handlePasswordSubmit(event) {
        event.preventDefault();
        const currentPassword = document.getElementById("currentPassword").value;
        const newPassword = document.getElementById("newPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (newPassword !== confirmPassword) {
            this.showToast("New password confirmation does not match.", "warning");
            return;
        }

        await this.runTask(async () => {
            await this.api.changePassword({
                old_password: currentPassword,
                new_password: newPassword,
            });
            document.getElementById("passwordForm").reset();
            this.showToast("Password changed.", "success");
        }, "Updating password");
    }

    async handleProjectTableClick(event) {
        const button = event.target.closest("[data-project-action]");
        if (!button) {
            return;
        }

        const projectId = asInteger(button.dataset.projectId);
        if (!projectId) {
            return;
        }

        if (button.dataset.projectAction === "select") {
            await this.selectProject(projectId);
            return;
        }

        if (button.dataset.projectAction === "edit") {
            const project = this.state.projects.find((item) => item.id === projectId);
            if (project) {
                this.populateProjectForm(project);
                this.navigateToView("projects");
            }
            return;
        }

        if (button.dataset.projectAction === "delete" && window.confirm("Delete this project and its linked data?")) {
            await this.runTask(async () => {
                await this.api.deleteProject(projectId);
                if (this.state.selectedProjectId === projectId) {
                    this.state.selectedProjectId = null;
                    localStorage.removeItem(PROJECT_STORAGE_KEY);
                }
                await this.loadWorkspaceData();
                this.showToast("Project deleted.", "success");
            }, "Deleting project");
        }
    }

    async handleEstimateTableClick(event) {
        const button = event.target.closest("[data-estimate-action]");
        if (!button) {
            return;
        }

        const estimateId = asInteger(button.dataset.estimateId);
        if (!estimateId) {
            return;
        }

        if (button.dataset.estimateAction === "view") {
            await this.runTask(async () => {
                await this.loadEstimateDetail(estimateId);
                this.showToast("Estimate details loaded.", "info");
            }, "Loading estimate");
            return;
        }

        if (button.dataset.estimateAction === "edit") {
            const estimate = this.state.estimates.find((item) => item.id === estimateId);
            if (estimate) {
                this.populateEstimateForm(estimate);
            }
            return;
        }

        if (button.dataset.estimateAction === "delete" && window.confirm("Delete this estimate?")) {
            await this.runTask(async () => {
                await this.api.deleteEstimate(estimateId);
                if (this.state.selectedEstimateId === estimateId) {
                    this.state.selectedEstimateId = null;
                }
                await this.loadProjectScopedData(this.selectedProject.id);
                this.showToast("Estimate deleted.", "success");
            }, "Deleting estimate");
        }
    }

    async handleScenarioTableClick(event) {
        const button = event.target.closest("[data-scenario-action]");
        if (!button) {
            return;
        }

        const scenarioId = asInteger(button.dataset.scenarioId);
        const scenario = this.state.scenarios.find((item) => item.id === scenarioId);
        if (!scenario) {
            return;
        }

        if (button.dataset.scenarioAction === "edit") {
            this.populateScenarioForm(scenario);
            return;
        }

        if (button.dataset.scenarioAction === "delete" && window.confirm("Delete this scenario?")) {
            await this.runTask(async () => {
                await this.api.deleteScenario(scenarioId);
                await this.loadProjectScopedData(this.selectedProject.id);
                this.showToast("Scenario deleted.", "success");
            }, "Deleting scenario");
        }
    }

    async handleRiskTableClick(event) {
        const button = event.target.closest("[data-risk-action]");
        if (!button) {
            return;
        }

        const riskId = asInteger(button.dataset.riskId);
        const risk = this.state.risks.find((item) => item.id === riskId);
        if (!risk) {
            return;
        }

        if (button.dataset.riskAction === "edit") {
            this.populateRiskForm(risk);
            return;
        }

        if (button.dataset.riskAction === "delete" && window.confirm("Delete this risk?")) {
            await this.runTask(async () => {
                await this.api.deleteRisk(riskId);
                await this.loadProjectScopedData(this.selectedProject.id);
                this.showToast("Risk deleted.", "success");
            }, "Deleting risk");
        }
    }

    async handleResourceTableClick(event) {
        const button = event.target.closest("[data-resource-action]");
        if (!button) {
            return;
        }

        const resourceId = asInteger(button.dataset.resourceId);
        const resource = this.state.resources.find((item) => item.id === resourceId);
        if (!resource) {
            return;
        }

        if (button.dataset.resourceAction === "edit") {
            this.populateResourceForm(resource);
            return;
        }

        if (button.dataset.resourceAction === "delete" && window.confirm("Delete this resource allocation?")) {
            await this.runTask(async () => {
                await this.api.deleteResource(resourceId);
                await this.loadProjectScopedData(this.selectedProject.id);
                this.showToast("Resource deleted.", "success");
            }, "Deleting resource");
        }
    }

    async handleReportTableClick(event) {
        const button = event.target.closest("[data-report-action]");
        if (!button) {
            return;
        }

        const reportId = asInteger(button.dataset.reportId);
        if (!reportId) {
            return;
        }

        if (button.dataset.reportAction === "preview") {
            this.previewReport(reportId);
            return;
        }

        if (button.dataset.reportAction === "download-pdf" || button.dataset.reportAction === "download-xlsx") {
            if (!this.requireProjectContext("Downloading a report")) {
                return;
            }
            const format = button.dataset.reportAction === "download-pdf" ? "pdf" : "xlsx";
            await this.runTask(async () => {
                const filename = await this.api.downloadProjectReport(this.selectedProject.id, format);
                this.showToast(`Downloaded ${filename}.`, "success");
            }, "Downloading report");
            return;
        }

        if (button.dataset.reportAction === "delete" && window.confirm("Delete this report?")) {
            await this.runTask(async () => {
                await this.api.deleteReport(reportId);
                await this.loadProjectScopedData(this.selectedProject.id);
                this.elements.reportPreview.innerHTML = this.emptyStateCard("Choose a report to preview its content.");
                this.showToast("Report deleted.", "success");
            }, "Deleting report");
        }
    }

    async handleMlModelTableClick(event) {
        const button = event.target.closest("[data-ml-action]");
        if (!button) {
            return;
        }

        const modelId = asInteger(button.dataset.mlId);
        if (!modelId) {
            return;
        }

        if (button.dataset.mlAction === "promote") {
            await this.runTask(async () => {
                const productionModels = this.state.mlModels.filter((model) => model.is_production && model.id !== modelId);
                for (const model of productionModels) {
                    await this.api.setMlModelProduction(model.id, false);
                }
                await this.api.setMlModelProduction(modelId, true);
                this.state.mlModels = toList(await this.api.listMlModels());
                this.renderIntelligence();
                this.showToast("Production model updated.", "success");
            }, "Updating production model");
        }
    }

    renderAll() {
        this.renderHeader();
        this.renderRoleOptions();
        this.renderUserOptions();
        this.renderProjectSwitcher();
        this.renderProjectContextBanners();
        this.renderDashboard();
        this.renderProjects();
        this.renderEstimates();
        this.renderScenarios();
        this.renderRisks();
        this.renderResources();
        this.renderReports();
        this.renderIntelligence();
        this.renderIntegrations();
        this.renderAdmin();
        this.renderSettings();
    }

    renderHeader() {
        if (!this.state.currentUser) {
            return;
        }

        this.elements.userBadge.textContent = `${this.state.currentUser.full_name} - ${this.state.currentUser.role_name || this.getRoleName(this.state.currentUser.role_id)}`;
        this.elements.selectedProjectBadge.textContent = this.selectedProject
            ? `Project: ${this.selectedProject.name}`
            : "Project: none selected";
        const notificationsButton = document.getElementById("notificationsBtn");
        if (notificationsButton) {
            const unreadCount = this.state.notifications.filter((notification) => !notification.is_read).length;
            notificationsButton.textContent = `Alerts ${unreadCount}`;
            notificationsButton.classList.toggle("warning", unreadCount > 0);
        }
    }

    renderRoleOptions() {
        this.populateSelect(this.elements.registerRoleId, this.state.roles, {
            placeholder: "Choose a role",
            valueField: "id",
            labelField: "name",
        });
    }

    renderUserOptions() {
        this.populateSelect(this.elements.resourceUserId, this.state.users, {
            placeholder: "Select a team member",
            valueField: "id",
            labelField: (user) => `${user.full_name} (${user.username})`,
        });
    }

    renderProjectSwitcher() {
        const currentValue = this.state.selectedProjectId ? String(this.state.selectedProjectId) : "";
        this.populateSelect(this.elements.projectSwitcher, this.state.projects, {
            placeholder: this.state.projects.length ? "Select project" : "No projects yet",
            valueField: "id",
            labelField: "name",
            selectedValue: currentValue,
        });
    }

    renderProjectContextBanners() {
        const projectText = this.selectedProject
            ? `${this.selectedProject.name} - ${this.selectedProject.status.replaceAll("_", " ")} - ${this.state.projectVersions.length} versions`
            : "Choose a project from the workspace header to activate project-specific modules.";

        this.elements.projectsContextBanner.textContent = projectText;
        this.elements.estimateContextBanner.textContent = projectText;
        this.elements.scenarioContextBanner.textContent = projectText;
        this.elements.riskContextBanner.textContent = projectText;
        this.elements.resourceContextBanner.textContent = projectText;
        this.elements.reportContextBanner.textContent = projectText;
        this.elements.intelligenceBanner.textContent = `Global reference data - ${this.state.costDrivers.length} cost drivers - ${this.state.mlModels.length} ML models`;
        this.elements.integrationBanner.textContent = "Connect Jira/Trello work items to local project estimates, progress, and analytics.";
        this.elements.adminBanner.textContent = `Users: ${this.state.users.length} - Roles: ${this.state.roles.length}`;
    }

    renderDashboard() {
        const totalProjects = this.state.projects.length;
        const activeProjects = this.state.projects.filter((project) => ["planning", "in_progress", "on_hold"].includes(project.status)).length;
        const portfolioBudget = this.sum(this.state.projects, (project) => project.budget || 0);
        const selectedEstimateCount = this.state.estimates.length;
        const averageConfidence = selectedEstimateCount
            ? this.sum(this.state.estimates, (estimate) => estimate.confidence_level || 0) / selectedEstimateCount
            : 0;
        const riskExposure = this.sum(this.state.risks, (risk) => (risk.probability || 0) * (risk.impact || 0));
        const monthlyBurn = this.sum(this.state.resources, (resource) => ((resource.hourly_rate || 0) * (resource.allocation_percentage || 0) / 100) * 160);

        const metrics = [
            { label: "Portfolio projects", value: totalProjects, tone: "teal" },
            { label: "Active projects", value: activeProjects, tone: "amber" },
            { label: "Selected estimates", value: selectedEstimateCount, tone: "clay" },
            { label: "Average confidence", value: `${averageConfidence.toFixed(0)}%`, tone: "ink" },
            { label: "Portfolio budget", value: this.formatCurrency(portfolioBudget), tone: "teal" },
            { label: "Selected burn / month", value: this.formatCurrency(monthlyBurn), tone: "amber" },
            { label: "Risk exposure", value: `${(riskExposure * 100).toFixed(1)}%`, tone: "clay" },
            { label: "Reports stored", value: this.state.reports.length, tone: "ink" },
        ];

        this.elements.dashboardMetrics.innerHTML = metrics.map((metric) => `
            <article class="metric-card ${metric.tone}">
                <p>${metric.label}</p>
                <strong>${metric.value}</strong>
            </article>
        `).join("");

        const analytics = this.state.dashboardAnalytics;
        if (analytics) {
            const methodRows = (analytics.estimation_comparison || []).map((item) => `
                <div class="bar-row">
                    <span>${this.escapeHtml(item.method)}</span>
                    <div class="bar-track"><i style="width:${Math.min(100, item.average_confidence || 0)}%"></i></div>
                    <strong>${item.average_confidence || 0}%</strong>
                </div>
            `).join("") || "<p class=\"subtle\">No saved estimates yet.</p>";
            const riskRows = (analytics.risk_analysis?.distribution || []).map((item) => `
                <div class="bar-row">
                    <span>${this.escapeHtml(item.label)}</span>
                    <div class="bar-track amber"><i style="width:${Math.min(100, item.value * 12)}%"></i></div>
                    <strong>${item.value}</strong>
                </div>
            `).join("") || "<p class=\"subtle\">No risks logged yet.</p>";
            const mlSummary = analytics.ml_summary?.available
                ? `Training rows: ${analytics.ml_summary.training_data_count}. Effort accuracy: ${analytics.ml_summary.metrics?.estimated_effort_hours?.accuracy || "N/A"}%.`
                : analytics.ml_summary?.message || "ML insights unavailable.";
            const healthRows = (analytics.project_health || []).slice(0, 5).map((item) => `
                <li>
                    <strong>${this.escapeHtml(item.name)}</strong>
                    <span>Health ${item.health_score}% - risk ${(item.risk_exposure * 100).toFixed(0)}%</span>
                </li>
            `).join("") || "<li class=\"empty-list\">No project health data yet.</li>";

            this.elements.dashboardAnalyticsGrid.innerHTML = `
                <article class="panel analytic-card">
                    <div class="panel-head"><h2>Estimation Confidence</h2></div>
                    ${methodRows}
                </article>
                <article class="panel analytic-card">
                    <div class="panel-head"><h2>Risk Analysis</h2></div>
                    ${riskRows}
                    <p class="subtle">Total exposure: ${analytics.risk_analysis?.total_exposure || 0}</p>
                </article>
                <article class="panel analytic-card">
                    <div class="panel-head"><h2>ML Prediction Summary</h2></div>
                    <p>${this.escapeHtml(mlSummary)}</p>
                    <ul class="plain-list">${healthRows}</ul>
                </article>
            `;
        } else {
            this.elements.dashboardAnalyticsGrid.innerHTML = "";
        }

        if (this.selectedProject) {
            this.elements.dashboardSpotlight.innerHTML = `
                <div class="hero-panel">
                    <div>
                        <span class="eyebrow">Project spotlight</span>
                        <h3>${this.escapeHtml(this.selectedProject.name)}</h3>
                        <p>${this.escapeHtml(this.selectedProject.description || "No description recorded yet.")}</p>
                    </div>
                    <div class="hero-actions">
                        <button class="btn btn-primary" type="button" data-dashboard-view="estimates">Open Estimates</button>
                        <button class="btn btn-secondary" type="button" data-dashboard-view="reports">Generate Report</button>
                    </div>
                </div>
            `;
            this.elements.dashboardSpotlight.querySelectorAll("[data-dashboard-view]").forEach((button) => {
                button.addEventListener("click", () => this.navigateToView(button.dataset.dashboardView));
            });
        } else {
            this.elements.dashboardSpotlight.innerHTML = this.emptyStateCard("Create a project to unlock estimates, risks, resources, and reporting.");
        }

        const recentProjects = [...this.state.projects]
            .sort((left, right) => new Date(right.created_at || 0) - new Date(left.created_at || 0))
            .slice(0, 5);

        this.elements.recentProjectsBody.innerHTML = recentProjects.length
            ? recentProjects.map((project) => `
                <tr>
                    <td>${this.escapeHtml(project.name)}</td>
                    <td><span class="status-pill">${this.humanize(project.status)}</span></td>
                    <td>${this.formatCurrency(project.budget || 0)}</td>
                    <td>${project.team_size || "N/A"}</td>
                    <td class="table-actions">
                        <button class="btn btn-ghost" type="button" data-project-action="select" data-project-id="${project.id}">Select</button>
                    </td>
                </tr>
            `).join("")
            : this.emptyRow("No projects have been created yet.", 5);

        this.elements.recentEstimatesList.innerHTML = this.state.estimates.length
            ? this.state.estimates.map((estimate) => `
                <li>
                    <strong>${this.escapeHtml(estimate.estimation_method)}</strong>
                    <span>${this.formatCurrency(estimate.estimated_cost)} - ${estimate.estimated_effort_hours}h - ${this.humanize(estimate.status)}</span>
                </li>
            `).join("")
            : "<li class=\"empty-list\">No estimates for the selected project yet.</li>";

        this.elements.dashboardRiskSummary.innerHTML = this.state.risks.length
            ? this.state.risks.map((risk) => `
                <li>
                    <strong>${this.escapeHtml(risk.category)}</strong>
                    <span>${this.escapeHtml(risk.description)}</span>
                </li>
            `).join("")
            : "<li class=\"empty-list\">No risks logged for the selected project.</li>";
    }

    renderProjects() {
        this.elements.projectTableBody.innerHTML = this.state.projects.length
            ? this.state.projects.map((project) => `
                <tr class="${project.id === this.state.selectedProjectId ? "row-selected" : ""}">
                    <td>${this.escapeHtml(project.name)}</td>
                    <td><span class="status-pill">${this.humanize(project.status)}</span></td>
                    <td>${this.escapeHtml(project.client_name || "Internal")}</td>
                    <td>${this.formatCurrency(project.budget || 0)}</td>
                    <td>${project.team_size || "N/A"}</td>
                    <td>${project.versions?.length || (project.id === this.selectedProject?.id ? this.state.projectVersions.length : 0)}</td>
                    <td class="table-actions">
                        <button class="btn btn-ghost" type="button" data-project-action="select" data-project-id="${project.id}">Select</button>
                        <button class="btn btn-ghost" type="button" data-project-action="edit" data-project-id="${project.id}">Edit</button>
                        <button class="btn btn-danger-soft" type="button" data-project-action="delete" data-project-id="${project.id}">Delete</button>
                    </td>
                </tr>
            `).join("")
            : this.emptyRow("No projects available yet.", 7);

        this.elements.versionList.innerHTML = this.state.projectVersions.length
            ? this.state.projectVersions.map((version) => `
                <article class="list-card">
                    <div class="list-card-head">
                        <strong>Version ${version.version_number}</strong>
                        <span>${this.formatDate(version.created_at)}</span>
                    </div>
                    <p>${this.escapeHtml(version.description || "No version description")}</p>
                    <p class="subtle">${this.escapeHtml(version.scope || "Scope not defined")}</p>
                </article>
            `).join("")
            : this.emptyStateCard("Select a project and add scope versions as requirements evolve.");

        this.populateSelect(this.elements.estimateVersionId, this.state.projectVersions, {
            placeholder: this.state.projectVersions.length ? "Select version" : "Create a version first",
            valueField: "id",
            labelField: (version) => `Version ${version.version_number}`,
            selectedValue: this.elements.estimateVersionId.value,
        });

        if (!document.getElementById("versionNumber").value) {
            document.getElementById("versionNumber").value = String((this.state.projectVersions[this.state.projectVersions.length - 1]?.version_number || 0) + 1);
        }
    }

    renderEstimates() {
        this.elements.estimateTableBody.innerHTML = this.state.estimates.length
            ? this.state.estimates.map((estimate) => `
                <tr class="${estimate.id === this.state.selectedEstimateId ? "row-selected" : ""}">
                    <td>${this.escapeHtml(estimate.estimation_method)}</td>
                    <td><span class="status-pill">${this.humanize(estimate.status)}</span></td>
                    <td>${this.formatCurrency(estimate.estimated_cost)}</td>
                    <td>${estimate.estimated_effort_hours}</td>
                    <td>${estimate.estimated_duration_months}</td>
                    <td>${estimate.confidence_level !== null && estimate.confidence_level !== undefined ? `${estimate.confidence_level}%` : "N/A"}</td>
                    <td class="table-actions">
                        <button class="btn btn-ghost" type="button" data-estimate-action="view" data-estimate-id="${estimate.id}">View</button>
                        <button class="btn btn-ghost" type="button" data-estimate-action="edit" data-estimate-id="${estimate.id}">Edit</button>
                        <button class="btn btn-danger-soft" type="button" data-estimate-action="delete" data-estimate-id="${estimate.id}">Delete</button>
                    </td>
                </tr>
            `).join("")
            : this.emptyRow("No estimates exist for the selected project.", 7);

        if (this.state.estimateDetail) {
            const estimate = this.state.estimateDetail;
            this.elements.estimateDetail.innerHTML = `
                <article class="detail-card">
                    <div class="list-card-head">
                        <strong>${this.escapeHtml(estimate.estimation_method)} estimate</strong>
                        <span>${this.humanize(estimate.status)}</span>
                    </div>
                    <dl class="detail-grid">
                        <div><dt>Version</dt><dd>${estimate.version_id}</dd></div>
                        <div><dt>Effort</dt><dd>${estimate.estimated_effort_hours} hours</dd></div>
                        <div><dt>Duration</dt><dd>${estimate.estimated_duration_months} months</dd></div>
                        <div><dt>Cost</dt><dd>${this.formatCurrency(estimate.estimated_cost)}</dd></div>
                        <div><dt>Team size</dt><dd>${estimate.estimated_team_size || "N/A"}</dd></div>
                        <div><dt>Confidence</dt><dd>${estimate.confidence_level !== null && estimate.confidence_level !== undefined ? `${estimate.confidence_level}%` : "N/A"}</dd></div>
                    </dl>
                    <p>${this.escapeHtml(estimate.notes || "No notes on this estimate.")}</p>
                </article>
            `;
        } else {
            this.elements.estimateDetail.innerHTML = this.emptyStateCard("Select an estimate to inspect its details and function points.");
        }

        this.elements.functionPointList.innerHTML = this.state.functionPoints.length
            ? this.state.functionPoints.map((functionPoint) => `
                <article class="list-card">
                    <div class="list-card-head">
                        <strong>FP analysis #${functionPoint.id}</strong>
                        <span>${this.formatDate(functionPoint.created_at)}</span>
                    </div>
                    <p>Adjusted FP: ${functionPoint.adjusted_fp} - Unadjusted FP: ${functionPoint.unadjusted_fp}</p>
                    <p class="subtle">ILF ${functionPoint.ilf_count}, EIF ${functionPoint.eif_count}, EI ${functionPoint.ei_count}, EO ${functionPoint.eo_count}, EQ ${functionPoint.eq_count}</p>
                </article>
            `).join("")
            : this.emptyStateCard("No function point analysis has been stored for the selected estimate.");
    }

    renderScenarios() {
        const baselineEstimate = this.getBaselineEstimate();
        this.elements.scenarioTableBody.innerHTML = this.state.scenarios.length
            ? this.state.scenarios.map((scenario) => {
                const computedEffort = scenario.estimated_effort || (baselineEstimate ? baselineEstimate.estimated_effort_hours * scenario.effort_adjustment : null);
                const computedDuration = scenario.estimated_duration || (baselineEstimate ? baselineEstimate.estimated_duration_months * scenario.duration_adjustment : null);
                const computedCost = scenario.estimated_cost || (baselineEstimate ? baselineEstimate.estimated_cost * scenario.cost_adjustment : null);
                return `
                    <tr>
                        <td>${this.escapeHtml(scenario.name)}</td>
                        <td>${this.humanize(scenario.scenario_type)}</td>
                        <td>${computedEffort ? `${computedEffort.toFixed(1)}h` : "N/A"}</td>
                        <td>${computedDuration ? `${computedDuration.toFixed(1)}m` : "N/A"}</td>
                        <td>${computedCost ? this.formatCurrency(computedCost) : "N/A"}</td>
                        <td class="table-actions">
                            <button class="btn btn-ghost" type="button" data-scenario-action="edit" data-scenario-id="${scenario.id}">Edit</button>
                            <button class="btn btn-danger-soft" type="button" data-scenario-action="delete" data-scenario-id="${scenario.id}">Delete</button>
                        </td>
                    </tr>
                `;
            }).join("")
            : this.emptyRow("No scenarios recorded yet.", 6);

        this.elements.scenarioSummary.innerHTML = baselineEstimate
            ? `<p>Scenario projections are being previewed against the latest estimate baseline of ${this.formatCurrency(baselineEstimate.estimated_cost)}.</p>`
            : "<p>Add an estimate first to see projected scenario outcomes.</p>";
    }

    renderRisks() {
        const totalCostContingency = this.sum(this.state.risks, (risk) => risk.cost_contingency || 0);
        const totalEffortContingency = this.sum(this.state.risks, (risk) => risk.effort_contingency || 0);

        this.elements.riskTableBody.innerHTML = this.state.risks.length
            ? this.state.risks.map((risk) => `
                <tr>
                    <td>${this.escapeHtml(risk.category)}</td>
                    <td>${this.escapeHtml(risk.description)}</td>
                    <td>${(risk.probability * 100).toFixed(0)}%</td>
                    <td>${(risk.impact * 100).toFixed(0)}%</td>
                    <td>${this.escapeHtml(risk.owner || "Unassigned")}</td>
                    <td>${this.escapeHtml(risk.status)}</td>
                    <td class="table-actions">
                        <button class="btn btn-ghost" type="button" data-risk-action="edit" data-risk-id="${risk.id}">Edit</button>
                        <button class="btn btn-danger-soft" type="button" data-risk-action="delete" data-risk-id="${risk.id}">Delete</button>
                    </td>
                </tr>
            `).join("")
            : this.emptyRow("No risks logged.", 7);

        this.elements.riskExposureSummary.innerHTML = `
            <div class="inline-summary">
                <span>${this.state.risks.length} risks</span>
                <span>${totalEffortContingency.toFixed(1)} effort hours contingency</span>
                <span>${this.formatCurrency(totalCostContingency)} cost contingency</span>
            </div>
        `;
    }

    renderResources() {
        const totalAllocation = this.sum(this.state.resources, (resource) => resource.allocation_percentage || 0);
        const loadedUsers = new Map(this.state.users.map((user) => [user.id, user]));

        this.elements.resourceTableBody.innerHTML = this.state.resources.length
            ? this.state.resources.map((resource) => {
                const user = loadedUsers.get(resource.user_id);
                return `
                    <tr>
                        <td>${this.escapeHtml(user?.full_name || `User #${resource.user_id}`)}</td>
                        <td>${this.escapeHtml(resource.role)}</td>
                        <td>${resource.allocation_percentage}%</td>
                        <td>${this.formatCurrency(resource.hourly_rate || 0)}</td>
                        <td>${this.escapeHtml(resource.availability)}</td>
                        <td>${resource.skills ? this.escapeHtml(resource.skills) : "N/A"}</td>
                        <td class="table-actions">
                            <button class="btn btn-ghost" type="button" data-resource-action="edit" data-resource-id="${resource.id}">Edit</button>
                            <button class="btn btn-danger-soft" type="button" data-resource-action="delete" data-resource-id="${resource.id}">Delete</button>
                        </td>
                    </tr>
                `;
            }).join("")
            : this.emptyRow("No resource allocations yet.", 7);

        this.elements.resourceUtilizationSummary.innerHTML = `
            <div class="inline-summary">
                <span>${this.state.resources.length} allocations</span>
                <span>${totalAllocation.toFixed(1)}% total allocation</span>
                <span>${this.state.resources.filter((resource) => resource.availability === "available").length} available</span>
            </div>
        `;
    }

    renderReports() {
        this.elements.reportTableBody.innerHTML = this.state.reports.length
            ? this.state.reports.map((report) => `
                <tr>
                    <td>${this.escapeHtml(report.title)}</td>
                    <td>${this.humanize(report.report_type)}</td>
                    <td>${this.escapeHtml(report.format)}</td>
                    <td>${this.formatDate(report.created_at)}</td>
                    <td class="table-actions">
                        <button class="btn btn-ghost" type="button" data-report-action="preview" data-report-id="${report.id}">Preview</button>
                        <button class="btn btn-ghost" type="button" data-report-action="download-pdf" data-report-id="${report.id}">PDF</button>
                        <button class="btn btn-ghost" type="button" data-report-action="download-xlsx" data-report-id="${report.id}">Excel</button>
                        <button class="btn btn-danger-soft" type="button" data-report-action="delete" data-report-id="${report.id}">Delete</button>
                    </td>
                </tr>
            `).join("")
            : this.emptyRow("No reports created for the selected project.", 5);

        if (!this.state.reports.length) {
            this.elements.reportPreview.innerHTML = this.emptyStateCard("Generate a report to see a formatted project summary here.");
        }
    }

    renderIntelligence() {
        this.elements.costDriverTableBody.innerHTML = this.state.costDrivers.length
            ? this.state.costDrivers.map((driver) => `
                <tr>
                    <td>${this.escapeHtml(driver.name)}</td>
                    <td>${this.escapeHtml(driver.category)}</td>
                    <td>${driver.impact_factor}</td>
                    <td>${driver.effort_multiplier}</td>
                    <td>${driver.cost_multiplier}</td>
                </tr>
            `).join("")
            : this.emptyRow("No cost drivers have been added.", 5);

        this.elements.historicalProjectTableBody.innerHTML = this.state.historicalProjects.length
            ? this.state.historicalProjects.map((project) => `
                <tr>
                    <td>${this.escapeHtml(project.project_name)}</td>
                    <td>${this.escapeHtml(project.industry || "N/A")}</td>
                    <td>${project.actual_effort_hours}</td>
                    <td>${project.actual_duration_months}</td>
                    <td>${this.formatCurrency(project.actual_cost)}</td>
                </tr>
            `).join("")
            : this.emptyRow("No historical benchmarks stored yet.", 5);

        this.elements.calibrationModelTableBody.innerHTML = this.state.calibrationModels.length
            ? this.state.calibrationModels.map((model) => `
                <tr>
                    <td>${this.escapeHtml(model.name)}</td>
                    <td>${this.escapeHtml(model.model_type)}</td>
                    <td>${model.calibration_data_count}</td>
                    <td>${model.accuracy_percentage ? `${model.accuracy_percentage}%` : "N/A"}</td>
                    <td>${model.r_squared ?? "N/A"}</td>
                </tr>
            `).join("")
            : this.emptyRow("No calibration models stored.", 5);

        this.elements.mlModelTableBody.innerHTML = this.state.mlModels.length
            ? this.state.mlModels.map((model) => `
                <tr class="${model.is_production ? "row-selected" : ""}">
                    <td>${this.escapeHtml(model.name)}</td>
                    <td>${this.escapeHtml(model.algorithm)}</td>
                    <td>${model.training_data_count}</td>
                    <td>${model.accuracy ? `${model.accuracy}%` : "N/A"}</td>
                    <td>${model.is_production ? "Production" : "Candidate"}</td>
                    <td class="table-actions">
                        <button class="btn btn-ghost" type="button" data-ml-action="promote" data-ml-id="${model.id}">Set Production</button>
                    </td>
                </tr>
            `).join("")
            : this.emptyRow("No ML models stored.", 6);
    }

    renderIntegrations() {
        if (!this.elements.integrationStatusPanel) {
            return;
        }

        const status = this.state.integrationStatus || {};
        const jira = status.jira || {};
        const trello = status.trello || {};
        this.elements.integrationStatusPanel.innerHTML = `
            <div class="integration-status">
                <article class="mini-panel">
                    <h3>Jira</h3>
                    <p><span class="status-pill">${jira.configured ? "Configured" : "Needs backend .env"}</span></p>
                    <p class="subtle">${this.escapeHtml(jira.base_url || "Set JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN")}</p>
                </article>
                <article class="mini-panel">
                    <h3>Trello</h3>
                    <p><span class="status-pill">${trello.configured ? "Configured" : "Needs backend .env"}</span></p>
                    <p class="subtle">${this.escapeHtml(trello.board_id || "Set TRELLO_API_KEY, TRELLO_API_TOKEN, optional TRELLO_BOARD_ID")}</p>
                </article>
            </div>
        `;

        this.elements.integrationSyncTableBody.innerHTML = this.state.integrationSyncs.length
            ? this.state.integrationSyncs.map((sync) => {
                const project = this.state.projects.find((item) => item.id === sync.mapped_project_id);
                return `
                    <tr>
                        <td>${this.escapeHtml(sync.provider)}</td>
                        <td>${this.escapeHtml(sync.external_id || "N/A")}</td>
                        <td>${this.escapeHtml(project?.name || sync.mapped_project_id || "N/A")}</td>
                        <td>${sync.task_count || 0}</td>
                        <td>${sync.completed_count || 0}</td>
                        <td>${sync.progress_percentage || 0}%</td>
                        <td>${this.formatDate(sync.created_at)}</td>
                    </tr>
                `;
            }).join("")
            : this.emptyRow("No integration syncs yet. Configure credentials in backend/.env, then run Jira or Trello sync.", 7);
    }

    renderAdmin() {
        this.elements.roleTableBody.innerHTML = this.state.roles.length
            ? this.state.roles.map((role) => `
                <tr>
                    <td>${this.escapeHtml(role.name)}</td>
                    <td>${this.escapeHtml(role.description || "N/A")}</td>
                    <td>${this.escapeHtml(role.permissions || "N/A")}</td>
                    <td>${role.is_active ? "Active" : "Inactive"}</td>
                </tr>
            `).join("")
            : this.emptyRow("No roles found.", 4);

        this.elements.userTableBody.innerHTML = this.state.users.length
            ? this.state.users.map((user) => `
                <tr>
                    <td>${this.escapeHtml(user.full_name)}</td>
                    <td>${this.escapeHtml(user.email)}</td>
                    <td>${this.escapeHtml(user.username)}</td>
                    <td>${this.escapeHtml(this.getRoleName(user.role_id))}</td>
                    <td>${user.is_active ? "Active" : "Inactive"}</td>
                </tr>
            `).join("")
            : this.emptyRow("No users have been registered.", 5);
    }

    renderSettings() {
        if (!this.state.currentUser) {
            return;
        }

        document.getElementById("profileFullName").value = this.state.currentUser.full_name || "";
        document.getElementById("profileUsername").value = this.state.currentUser.username || "";
        document.getElementById("profileEmail").value = this.state.currentUser.email || "";
        document.getElementById("profilePhone").value = this.state.currentUser.phone || "";
        document.getElementById("profileOrganization").value = this.state.currentUser.organization || "";
        document.getElementById("profileDepartment").value = this.state.currentUser.department || "";
        this.elements.profileRole.value = this.state.currentUser.role_name || this.getRoleName(this.state.currentUser.role_id);
        this.syncConnectionInputs();
    }

    previewReport(reportId) {
        const report = this.state.reports.find((item) => item.id === reportId);
        if (!report) {
            this.elements.reportPreview.innerHTML = this.emptyStateCard("Report not found.");
            return;
        }

        if (report.format === "json") {
            this.elements.reportPreview.innerHTML = `
                <pre class="report-code">${this.escapeHtml(report.content || "{}")}</pre>
            `;
        } else {
            this.elements.reportPreview.innerHTML = report.content || this.emptyStateCard("This report does not contain previewable content.");
        }
    }

    buildReportContent(format) {
        const project = this.selectedProject;
        if (!project) {
            return "";
        }

        const reportPayload = {
            project: {
                name: project.name,
                status: project.status,
                budget: project.budget,
                client: project.client_name,
                manager: project.project_manager,
            },
            versions: this.state.projectVersions.map((version) => ({
                version_number: version.version_number,
                description: version.description,
                scope: version.scope,
            })),
            estimates: this.state.estimates.map((estimate) => ({
                method: estimate.estimation_method,
                status: estimate.status,
                cost: estimate.estimated_cost,
                effort: estimate.estimated_effort_hours,
                duration: estimate.estimated_duration_months,
                confidence: estimate.confidence_level,
            })),
            scenarios: this.state.scenarios.map((scenario) => ({
                name: scenario.name,
                type: scenario.scenario_type,
                effort_adjustment: scenario.effort_adjustment,
                cost_adjustment: scenario.cost_adjustment,
            })),
            risks: this.state.risks.map((risk) => ({
                description: risk.description,
                category: risk.category,
                probability: risk.probability,
                impact: risk.impact,
                owner: risk.owner,
            })),
            resources: this.state.resources.map((resource) => ({
                user_id: resource.user_id,
                role: resource.role,
                allocation_percentage: resource.allocation_percentage,
                availability: resource.availability,
            })),
        };

        if (format === "json") {
            return JSON.stringify(reportPayload, null, 2);
        }

        return `
            <article class="generated-report">
                <header>
                    <span class="eyebrow">CASE Tool report</span>
                    <h2>${this.escapeHtml(project.name)}</h2>
                    <p>Status: ${this.humanize(project.status)} - Budget: ${this.formatCurrency(project.budget || 0)}</p>
                </header>
                <section>
                    <h3>Version baseline</h3>
                    <ul>${this.state.projectVersions.map((version) => `<li>Version ${version.version_number}: ${this.escapeHtml(version.description || "No description")}</li>`).join("") || "<li>No versions stored.</li>"}</ul>
                </section>
                <section>
                    <h3>Estimate portfolio</h3>
                    <ul>${this.state.estimates.map((estimate) => `<li>${this.escapeHtml(estimate.estimation_method)} - ${this.formatCurrency(estimate.estimated_cost)} - ${estimate.estimated_effort_hours} hours</li>`).join("") || "<li>No estimates stored.</li>"}</ul>
                </section>
                <section>
                    <h3>Risk outlook</h3>
                    <ul>${this.state.risks.map((risk) => `<li>${this.escapeHtml(risk.category)} - ${this.escapeHtml(risk.description)}</li>`).join("") || "<li>No risks stored.</li>"}</ul>
                </section>
                <section>
                    <h3>Resource plan</h3>
                    <ul>${this.state.resources.map((resource) => `<li>${this.escapeHtml(resource.role)} - ${resource.allocation_percentage}% allocation</li>`).join("") || "<li>No resources stored.</li>"}</ul>
                </section>
            </article>
        `;
    }

    populateProjectForm(project) {
        document.getElementById("projectFormId").value = project.id;
        document.getElementById("projectName").value = project.name || "";
        document.getElementById("projectDescription").value = project.description || "";
        document.getElementById("projectStatus").value = project.status || "planning";
        document.getElementById("projectBudget").value = project.budget ?? "";
        document.getElementById("projectTeamSize").value = project.team_size ?? "";
        document.getElementById("projectClientName").value = project.client_name || "";
        document.getElementById("projectManager").value = project.project_manager || "";
        document.getElementById("projectDepartment").value = project.department || "";
        document.getElementById("projectStartDate").value = this.toInputDateTime(project.start_date);
        document.getElementById("projectEndDate").value = this.toInputDateTime(project.end_date);
    }

    populateEstimateForm(estimate) {
        document.getElementById("estimateFormId").value = estimate.id;
        this.elements.estimateVersionId.value = String(estimate.version_id);
        document.getElementById("estimateMethod").value = estimate.estimation_method;
        document.getElementById("estimateStatus").value = estimate.status || "draft";
        document.getElementById("estimateEffort").value = estimate.estimated_effort_hours ?? "";
        document.getElementById("estimateDuration").value = estimate.estimated_duration_months ?? "";
        document.getElementById("estimateCost").value = estimate.estimated_cost ?? "";
        document.getElementById("estimateTeamSize").value = estimate.estimated_team_size ?? "";
        document.getElementById("estimateConfidence").value = estimate.confidence_level ?? "";
        document.getElementById("estimateConfidenceLow").value = estimate.confidence_interval_low ?? "";
        document.getElementById("estimateConfidenceHigh").value = estimate.confidence_interval_high ?? "";
        document.getElementById("estimateAssumptions").value = estimate.assumptions || "";
        document.getElementById("estimateRisks").value = estimate.risks || "";
        document.getElementById("estimateNotes").value = estimate.notes || "";
        this.navigateToView("estimates");
    }

    populateScenarioForm(scenario) {
        document.getElementById("scenarioFormId").value = scenario.id;
        document.getElementById("scenarioName").value = scenario.name || "";
        document.getElementById("scenarioType").value = scenario.scenario_type || "realistic";
        document.getElementById("scenarioDescription").value = scenario.description || "";
        document.getElementById("scenarioEffortAdjustment").value = scenario.effort_adjustment ?? 1;
        document.getElementById("scenarioDurationAdjustment").value = scenario.duration_adjustment ?? 1;
        document.getElementById("scenarioCostAdjustment").value = scenario.cost_adjustment ?? 1;
        document.getElementById("scenarioTeamAdjustment").value = scenario.team_size_adjustment ?? 1;
        this.navigateToView("scenarios");
    }

    populateRiskForm(risk) {
        document.getElementById("riskFormId").value = risk.id;
        document.getElementById("riskDescription").value = risk.description || "";
        document.getElementById("riskCategory").value = risk.category || "";
        document.getElementById("riskProbability").value = risk.probability ?? "";
        document.getElementById("riskImpact").value = risk.impact ?? "";
        document.getElementById("riskMitigation").value = risk.mitigation_strategy || "";
        document.getElementById("riskOwner").value = risk.owner || "";
        document.getElementById("riskStatus").value = risk.status || "active";
        document.getElementById("riskEffortContingency").value = risk.effort_contingency ?? 0;
        document.getElementById("riskCostContingency").value = risk.cost_contingency ?? 0;
        this.navigateToView("risks");
    }

    populateResourceForm(resource) {
        document.getElementById("resourceFormId").value = resource.id;
        this.elements.resourceUserId.value = String(resource.user_id);
        document.getElementById("resourceRole").value = resource.role || "";
        document.getElementById("resourceAllocation").value = resource.allocation_percentage ?? "";
        document.getElementById("resourceHourlyRate").value = resource.hourly_rate ?? "";
        document.getElementById("resourceStartDate").value = this.toInputDateTime(resource.start_date);
        document.getElementById("resourceEndDate").value = this.toInputDateTime(resource.end_date);
        document.getElementById("resourceSkills").value = resource.skills || "";
        document.getElementById("resourceAvailability").value = resource.availability || "available";
        this.navigateToView("resources");
    }

    resetProjectForm() {
        document.getElementById("projectForm").reset();
        document.getElementById("projectFormId").value = "";
        document.getElementById("projectStatus").value = "planning";
    }

    resetVersionForm() {
        document.getElementById("versionForm").reset();
        document.getElementById("versionNumber").value = String((this.state.projectVersions[this.state.projectVersions.length - 1]?.version_number || 0) + 1);
    }

    resetEstimateForm() {
        document.getElementById("estimateForm").reset();
        document.getElementById("estimateFormId").value = "";
        document.getElementById("estimateStatus").value = "draft";
        const latestVersionId = this.state.projectVersions[this.state.projectVersions.length - 1]?.id;
        this.elements.estimateVersionId.value = latestVersionId ? String(latestVersionId) : "";
    }

    resetFunctionPointForm() {
        document.getElementById("functionPointForm").reset();
        document.getElementById("fpIlfCount").value = "0";
        document.getElementById("fpEifCount").value = "0";
        document.getElementById("fpEiCount").value = "0";
        document.getElementById("fpEoCount").value = "0";
        document.getElementById("fpEqCount").value = "0";
    }

    resetScenarioForm() {
        document.getElementById("scenarioForm").reset();
        document.getElementById("scenarioFormId").value = "";
        document.getElementById("scenarioType").value = "realistic";
        document.getElementById("scenarioEffortAdjustment").value = "1";
        document.getElementById("scenarioDurationAdjustment").value = "1";
        document.getElementById("scenarioCostAdjustment").value = "1";
        document.getElementById("scenarioTeamAdjustment").value = "1";
    }

    resetRiskForm() {
        document.getElementById("riskForm").reset();
        document.getElementById("riskFormId").value = "";
        document.getElementById("riskStatus").value = "active";
        document.getElementById("riskEffortContingency").value = "0";
        document.getElementById("riskCostContingency").value = "0";
    }

    resetResourceForm() {
        document.getElementById("resourceForm").reset();
        document.getElementById("resourceFormId").value = "";
        document.getElementById("resourceAvailability").value = "available";
    }

    resetReportForm() {
        document.getElementById("reportForm").reset();
        document.getElementById("reportFormat").value = "html";
        document.getElementById("reportIncludeConfidence").checked = true;
        document.getElementById("reportIncludeRisks").checked = true;
        document.getElementById("reportIncludeScenarios").checked = true;
    }

    resetCostDriverForm() {
        document.getElementById("costDriverForm").reset();
        document.getElementById("costDriverImpact").value = "1";
        document.getElementById("costDriverEffort").value = "1";
        document.getElementById("costDriverCost").value = "1";
        document.getElementById("costDriverDuration").value = "1";
        document.getElementById("costDriverActive").checked = true;
    }

    resetHistoricalProjectForm() {
        document.getElementById("historicalProjectForm").reset();
    }

    resetCalibrationModelForm() {
        document.getElementById("calibrationModelForm").reset();
    }

    resetMlModelForm() {
        document.getElementById("mlModelForm").reset();
        document.getElementById("mlIsActive").checked = true;
    }

    resetRoleForm() {
        document.getElementById("roleForm").reset();
        document.getElementById("roleIsActive").checked = true;
    }

    requireProjectContext(actionLabel) {
        if (this.selectedProject) {
            return true;
        }
        this.showToast(`${actionLabel} requires an active project.`, "warning");
        return false;
    }

    populateSelect(element, items, config) {
        if (!element) {
            return;
        }

        const {
            placeholder,
            valueField,
            labelField,
            selectedValue = "",
        } = config;

        const currentValue = selectedValue || element.value || "";
        const options = [`<option value="">${this.escapeHtml(placeholder)}</option>`];
        items.forEach((item) => {
            const value = typeof valueField === "function" ? valueField(item) : item[valueField];
            const label = typeof labelField === "function" ? labelField(item) : item[labelField];
            const selected = String(value) === String(currentValue) ? "selected" : "";
            options.push(`<option value="${this.escapeHtml(String(value))}" ${selected}>${this.escapeHtml(String(label))}</option>`);
        });
        element.innerHTML = options.join("");
    }

    installFieldHelp() {
        const attachHelp = (label, fieldId) => {
            if (!label || label.querySelector(".field-help")) {
                return;
            }
            const labelText = label.textContent.trim() || fieldId;
            const helpText = FIELD_HELP[fieldId] || `${labelText}: enter the value requested by this field. It is stored by the backend and may affect dashboard analytics, reports, validation, or estimation workflow.`;
            const helpButton = document.createElement("button");
            helpButton.className = "field-help";
            helpButton.type = "button";
            helpButton.textContent = "?";
            helpButton.title = helpText;
            helpButton.dataset.tooltip = helpText;
            helpButton.setAttribute("aria-label", `Help for ${labelText}`);
            helpButton.addEventListener("click", (event) => {
                event.preventDefault();
                this.showToast(helpText, "info");
            });
            label.appendChild(helpButton);
        };

        document.querySelectorAll("label[for]").forEach((label) => attachHelp(label, label.htmlFor));
        document.querySelectorAll(".checkbox-grid label").forEach((label) => {
            const input = label.querySelector("input[id]");
            if (input) {
                attachHelp(label, input.id);
            }
        });
    }

    installLanguageSelector() {
        const topbarStatus = document.querySelector(".topbar-status");
        if (!topbarStatus || document.getElementById("languageSelector")) {
            return;
        }
        const wrapper = document.createElement("label");
        wrapper.className = "compact-field language-field";
        wrapper.innerHTML = `
            <span>Language</span>
            <select id="languageSelector">
                <option value="en">English</option>
                <option value="ur">اردو</option>
            </select>
        `;
        topbarStatus.insertBefore(wrapper, topbarStatus.firstChild);
        const alertsButton = document.createElement("button");
        alertsButton.className = "status-badge neutral notification-chip";
        alertsButton.type = "button";
        alertsButton.id = "notificationsBtn";
        alertsButton.textContent = "Alerts 0";
        alertsButton.title = "Refresh in-app deadline, risk, and review notifications.";
        alertsButton.addEventListener("click", async () => {
            await this.runTask(async () => {
                await this.api.refreshNotifications(false);
                this.state.notifications = toList(await this.api.listNotifications(false, 20));
                this.renderHeader();
                this.renderDashboard();
                this.showToast("Notifications refreshed.", "success");
            }, "Refreshing alerts");
        });
        topbarStatus.insertBefore(alertsButton, wrapper.nextSibling);
        const selector = document.getElementById("languageSelector");
        selector.value = this.state.language;
        selector.addEventListener("change", () => {
            this.state.language = selector.value;
            localStorage.setItem(LANGUAGE_STORAGE_KEY, this.state.language);
            this.applyLanguage();
        });
    }

    applyLanguage() {
        const pack = LANGUAGE_PACKS[this.state.language] || LANGUAGE_PACKS.en;
        document.documentElement.lang = this.state.language === "ur" ? "ur" : "en";
        document.documentElement.dir = this.state.language === "ur" ? "rtl" : "ltr";
        document.querySelectorAll("[data-view-target]").forEach((button) => {
            const key = button.dataset.viewTarget;
            if (pack[key]) {
                button.textContent = pack[key];
            }
        });
        const refreshButton = document.getElementById("refreshWorkspaceBtn");
        const logoutButton = document.getElementById("logoutBtn");
        if (refreshButton) {
            refreshButton.textContent = pack.refresh;
        }
        if (logoutButton) {
            logoutButton.textContent = pack.logout;
        }
    }

    syncConnectionInputs() {
        const baseURL = this.api.getBaseURL();
        if (this.elements.authApiBaseUrl) {
            this.elements.authApiBaseUrl.value = baseURL;
        }
        if (this.elements.connectionApiBaseUrl) {
            this.elements.connectionApiBaseUrl.value = baseURL;
        }
    }

    async refreshApiStatus() {
        try {
            const status = await this.api.healthCheck();
            this.elements.apiStatusBadge.textContent = `API healthy - v${status.version}`;
            this.elements.apiStatusBadge.className = "status-badge online";
        } catch (error) {
            this.elements.apiStatusBadge.textContent = "API unreachable";
            this.elements.apiStatusBadge.className = "status-badge offline";
        }
    }

    get selectedProject() {
        return this.state.projectDetail || this.state.projects.find((project) => project.id === this.state.selectedProjectId) || null;
    }

    getBaselineEstimate() {
        if (!this.state.estimates.length) {
            return null;
        }
        return [...this.state.estimates].sort((left, right) => new Date(right.created_at || 0) - new Date(left.created_at || 0))[0];
    }

    getRoleName(roleId) {
        return this.state.roles.find((role) => role.id === roleId)?.name || `Role #${roleId}`;
    }

    sum(items, resolver) {
        return items.reduce((total, item) => total + (resolver(item) || 0), 0);
    }

    formatCurrency(value) {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 0,
        }).format(value || 0);
    }

    formatDate(value) {
        if (!value) {
            return "N/A";
        }
        return new Intl.DateTimeFormat("en-US", {
            dateStyle: "medium",
            timeStyle: "short",
        }).format(new Date(value));
    }

    humanize(value) {
        return String(value || "")
            .replaceAll("_", " ")
            .replace(/\b\w/g, (match) => match.toUpperCase());
    }

    escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll("\"", "&quot;")
            .replaceAll("'", "&#39;");
    }

    emptyRow(message, colspan) {
        return `<tr><td colspan="${colspan}" class="empty-cell">${this.escapeHtml(message)}</td></tr>`;
    }

    emptyStateCard(message) {
        return `<div class="empty-state">${this.escapeHtml(message)}</div>`;
    }

    toIsoDateTime(value) {
        return value ? new Date(value).toISOString() : null;
    }

    toInputDateTime(value) {
        if (!value) {
            return "";
        }
        const date = new Date(value);
        const offset = date.getTimezoneOffset();
        const normalized = new Date(date.getTime() - offset * 60 * 1000);
        return normalized.toISOString().slice(0, 16);
    }

    showToast(message, tone = "info") {
        const toast = document.createElement("div");
        toast.className = `toast ${tone}`;
        toast.textContent = message;
        this.elements.toastStack.appendChild(toast);

        window.setTimeout(() => {
            toast.classList.add("leaving");
            window.setTimeout(() => toast.remove(), 250);
        }, 3200);
    }

    beginBusy() {
        this.ui.busyCount += 1;
        this.elements.loadingBar.classList.add("active");
    }

    endBusy() {
        this.ui.busyCount = Math.max(0, this.ui.busyCount - 1);
        if (!this.ui.busyCount) {
            this.elements.loadingBar.classList.remove("active");
        }
    }

    async runTask(task, label = "Working") {
        this.beginBusy();
        try {
            return await task();
        } catch (error) {
            this.showToast(`${label} failed: ${error.message}`, "error");
            throw error;
        } finally {
            this.endBusy();
        }
    }
}
