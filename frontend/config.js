/**
 * Bharat Biz - Central Configuration
 * This file manages the API connection string for all frontend modules.
 */
const CONFIG = {
    // URL for the FastAPI backend. 
    // Defaults to localhost for development.
    // Replace the production URL with your actual deployed backend URL (e.g. Railway/Render).
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://localhost:8000/api/v1' 
        : 'https://bharat-biz-backend.up.railway.app/api/v1' // Placeholder - update this after backend deployment
};

// Global export
window.APP_CONFIG = CONFIG;
