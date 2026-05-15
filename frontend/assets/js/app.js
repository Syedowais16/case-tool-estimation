import apiClient from "./api-client.js";
import { CaseToolApp } from "./ui-manager.js";

window.addEventListener("DOMContentLoaded", () => {
    const app = new CaseToolApp(apiClient);
    window.caseToolApp = app;
    app.init();
});
