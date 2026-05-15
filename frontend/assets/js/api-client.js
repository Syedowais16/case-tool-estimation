const API_BASE_URL_STORAGE_KEY = "case_tool_api_base_url";
const ACCESS_TOKEN_STORAGE_KEY = "access_token";
const REFRESH_TOKEN_STORAGE_KEY = "refresh_token";

function normalizeBaseUrl(url) {
    const trimmed = (url || "").trim().replace(/\/+$/, "");
    if (!trimmed) {
        return "http://localhost:8000/api/v1";
    }

    if (trimmed.endsWith("/api/v1")) {
        return trimmed;
    }

    return `${trimmed}/api/v1`;
}

function toQueryString(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
            query.append(key, value);
        }
    });
    const serialized = query.toString();
    return serialized ? `?${serialized}` : "";
}

export class APIClient {
    constructor(baseURL = localStorage.getItem(API_BASE_URL_STORAGE_KEY) || "http://localhost:8000/api/v1") {
        this.baseURL = normalizeBaseUrl(baseURL);
        this.token = localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY);
        this.refreshToken = localStorage.getItem(REFRESH_TOKEN_STORAGE_KEY);
    }

    getRootUrl() {
        return this.baseURL.replace(/\/api\/v1$/, "");
    }

    getBaseURL() {
        return this.baseURL;
    }

    setBaseURL(url) {
        this.baseURL = normalizeBaseUrl(url);
        localStorage.setItem(API_BASE_URL_STORAGE_KEY, this.baseURL);
    }

    setTokens(accessToken, refreshToken) {
        this.token = accessToken;
        this.refreshToken = refreshToken;
        localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, accessToken);
        localStorage.setItem(REFRESH_TOKEN_STORAGE_KEY, refreshToken);
    }

    clearTokens() {
        this.token = null;
        this.refreshToken = null;
        localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
        localStorage.removeItem(REFRESH_TOKEN_STORAGE_KEY);
    }

    isAuthenticated() {
        return Boolean(this.token);
    }

    async request(endpoint, options = {}) {
        const {
            method = "GET",
            data,
            headers = {},
            retryOnAuthError = true,
        } = options;

        const requestHeaders = { ...headers };
        const init = { method, headers: requestHeaders };

        if (this.token) {
            requestHeaders.Authorization = `Bearer ${this.token}`;
        }

        if (data !== undefined) {
            requestHeaders["Content-Type"] = "application/json";
            init.body = JSON.stringify(data);
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, init);

        if (
            response.status === 401 &&
            retryOnAuthError &&
            this.refreshToken &&
            endpoint !== "/auth/login" &&
            endpoint !== "/auth/refresh"
        ) {
            await this.refreshAccessToken();
            return this.request(endpoint, {
                ...options,
                retryOnAuthError: false,
            });
        }

            if (!response.ok) {
                let message = `Request failed with status ${response.status}`;
                try {
                    const errorPayload = await response.json();
                    if (Array.isArray(errorPayload.detail)) {
                        message = errorPayload.detail
                            .map((item) => {
                                const location = Array.isArray(item.loc) ? item.loc.join(".") : "request";
                                return `${location}: ${item.msg}`;
                            })
                            .join("; ");
                    } else {
                        message = errorPayload.detail || errorPayload.message || message;
                    }
                } catch (error) {
                    message = response.statusText || message;
                }
                throw new Error(message);
            }

        if (response.status === 204) {
            return null;
        }

        const contentType = response.headers.get("content-type") || "";
        if (contentType.includes("application/json")) {
            return response.json();
        }

        return response.text();
    }

    get(endpoint) {
        return this.request(endpoint);
    }

    post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: "POST",
            data,
        });
    }

    put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: "PUT",
            data,
        });
    }

    delete(endpoint) {
        return this.request(endpoint, {
            method: "DELETE",
        });
    }

    async healthCheck() {
        const response = await fetch(`${this.getRootUrl()}/health`);
        if (!response.ok) {
            throw new Error("API health check failed");
        }
        return response.json();
    }

    async login(email, password) {
        const response = await this.post("/auth/login", { email, password });
        this.setTokens(response.access_token, response.refresh_token);
        return response;
    }

    async logout() {
        this.clearTokens();
        return true;
    }

    async refreshAccessToken() {
        if (!this.refreshToken) {
            throw new Error("Refresh token is missing");
        }

        const response = await this.post("/auth/refresh", {
            refresh_token: this.refreshToken,
        });
        this.setTokens(response.access_token, response.refresh_token);
        return response;
    }

    getCurrentUser() {
        return this.get("/auth/me");
    }

    changePassword(payload) {
        return this.post("/auth/change-password", payload);
    }

    registerUser(payload) {
        return this.post("/users/register", payload);
    }

    listUsers(skip = 0, limit = 100) {
        return this.get(`/users${toQueryString({ skip, limit })}`);
    }

    getUser(userId) {
        return this.get(`/users/${userId}`);
    }

    updateUser(userId, payload) {
        return this.put(`/users/${userId}`, payload);
    }

    listRoles(skip = 0, limit = 100) {
        return this.get(`/users/roles${toQueryString({ skip, limit })}`);
    }

    createRole(payload) {
        return this.post("/users/roles", payload);
    }

    getProjects(skip = 0, limit = 100, statusFilter = null) {
        return this.get(`/projects${toQueryString({ skip, limit, status_filter: statusFilter })}`);
    }

    getProject(projectId) {
        return this.get(`/projects/${projectId}`);
    }

    createProject(payload) {
        return this.post("/projects/", payload);
    }

    updateProject(projectId, payload) {
        return this.put(`/projects/${projectId}`, payload);
    }

    deleteProject(projectId) {
        return this.delete(`/projects/${projectId}`);
    }

    listProjectVersions(projectId) {
        return this.get(`/projects/${projectId}/versions`);
    }

    createProjectVersion(projectId, payload) {
        return this.post(`/projects/${projectId}/versions`, payload);
    }

    getEstimates(projectId, skip = 0, limit = 100) {
        return this.get(`/estimates/project/${projectId}${toQueryString({ skip, limit })}`);
    }

    getEstimate(estimateId) {
        return this.get(`/estimates/${estimateId}`);
    }

    createEstimate(payload) {
        return this.post("/estimates/", payload);
    }

    updateEstimate(estimateId, payload) {
        return this.put(`/estimates/${estimateId}`, payload);
    }

    deleteEstimate(estimateId) {
        return this.delete(`/estimates/${estimateId}`);
    }

    listCostDrivers(skip = 0, limit = 100) {
        return this.get(`/estimates/cost-drivers${toQueryString({ skip, limit })}`);
    }

    createCostDriver(payload) {
        return this.post("/estimates/cost-drivers", payload);
    }

    listFunctionPoints(estimateId) {
        return this.get(`/estimates/${estimateId}/function-points`);
    }

    createFunctionPoints(estimateId, payload) {
        return this.post(`/estimates/${estimateId}/function-points`, payload);
    }

    listHistoricalProjects(skip = 0, limit = 100) {
        return this.get(`/estimates/historical-projects${toQueryString({ skip, limit })}`);
    }

    createHistoricalProject(payload) {
        return this.post("/estimates/historical-projects", payload);
    }

    getScenarios(projectId, skip = 0, limit = 100) {
        return this.get(`/projects/${projectId}/scenarios${toQueryString({ skip, limit })}`);
    }

    createScenario(payload) {
        return this.post("/scenarios", payload);
    }

    updateScenario(scenarioId, payload) {
        return this.put(`/scenarios/${scenarioId}`, payload);
    }

    deleteScenario(scenarioId) {
        return this.delete(`/scenarios/${scenarioId}`);
    }

    getRisks(projectId, skip = 0, limit = 100) {
        return this.get(`/projects/${projectId}/risks${toQueryString({ skip, limit })}`);
    }

    createRisk(payload) {
        return this.post("/risks", payload);
    }

    updateRisk(riskId, payload) {
        return this.put(`/risks/${riskId}`, payload);
    }

    deleteRisk(riskId) {
        return this.delete(`/risks/${riskId}`);
    }

    getResources(projectId, skip = 0, limit = 100) {
        return this.get(`/projects/${projectId}/resources${toQueryString({ skip, limit })}`);
    }

    createResource(payload) {
        return this.post("/resources", payload);
    }

    updateResource(resourceId, payload) {
        return this.put(`/resources/${resourceId}`, payload);
    }

    deleteResource(resourceId) {
        return this.delete(`/resources/${resourceId}`);
    }

    getReports(projectId, skip = 0, limit = 100) {
        return this.get(`/projects/${projectId}/reports${toQueryString({ skip, limit })}`);
    }

    createReport(payload) {
        return this.post("/reports", payload);
    }

    getReport(reportId) {
        return this.get(`/reports/${reportId}`);
    }

    deleteReport(reportId) {
        return this.delete(`/reports/${reportId}`);
    }

    listCalibrationModels(skip = 0, limit = 100) {
        return this.get(`/calibration-models${toQueryString({ skip, limit })}`);
    }

    createCalibrationModel(payload) {
        return this.post("/calibration-models", payload);
    }

    listMlModels(skip = 0, limit = 100, isProduction = null) {
        return this.get(`/ml-models${toQueryString({ skip, limit, is_production: isProduction })}`);
    }

    createMlModel(payload) {
        return this.post("/ml-models", payload);
    }

    setMlModelProduction(modelId, isProduction) {
        return this.request(`/ml-models/${modelId}/set-production${toQueryString({ is_production: isProduction })}`, {
            method: "PUT",
        });
    }

    getDashboardAnalytics() {
        return this.get("/dashboard/analytics");
    }

    calculateCocomo(payload) {
        return this.post("/estimates/calculate/cocomo", payload);
    }

    calculateFpa(payload) {
        return this.post("/estimates/calculate/fpa", payload);
    }

    calculateHybrid(payload) {
        return this.post("/estimates/calculate/hybrid", payload);
    }

    predictMlEstimate(payload) {
        return this.post("/estimates/ml/predict", payload);
    }

    getMlInsights() {
        return this.get("/estimates/ml/insights");
    }

    listNotifications(unreadOnly = false, limit = 50) {
        return this.get(`/notifications${toQueryString({ unread_only: unreadOnly, limit })}`);
    }

    refreshNotifications(sendEmail = false) {
        return this.post(`/notifications/refresh${toQueryString({ send_email: sendEmail })}`);
    }

    markNotificationRead(notificationId) {
        return this.request(`/notifications/${notificationId}/read`, {
            method: "PUT",
        });
    }

    getIntegrationStatus() {
        return this.get("/integrations/status");
    }

    listIntegrationSyncs(provider = null) {
        return this.get(`/integrations/syncs${toQueryString({ provider })}`);
    }

    syncJira(jql = null, maxResults = 50) {
        return this.post(`/integrations/jira/sync${toQueryString({ jql, max_results: maxResults })}`);
    }

    syncTrello(boardId = null) {
        return this.post(`/integrations/trello/sync${toQueryString({ board_id: boardId })}`);
    }

    getProjectReportDownloadUrl(projectId, format = "pdf") {
        return `${this.baseURL}/reports/projects/${projectId}/export${toQueryString({ format })}`;
    }

    async downloadProjectReport(projectId, format = "pdf") {
        const response = await fetch(this.getProjectReportDownloadUrl(projectId, format), {
            headers: this.token ? { Authorization: `Bearer ${this.token}` } : {},
        });
        if (!response.ok) {
            let message = `Report download failed with status ${response.status}`;
            try {
                const payload = await response.json();
                message = payload.detail || payload.message || message;
            } catch (error) {
                message = response.statusText || message;
            }
            throw new Error(message);
        }

        const blob = await response.blob();
        const contentDisposition = response.headers.get("content-disposition") || "";
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/i);
        const filename = filenameMatch?.[1] || `case_tool_report.${format}`;
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
        return filename;
    }
}

const apiClient = new APIClient();

export default apiClient;
