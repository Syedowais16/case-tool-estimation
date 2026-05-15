"""Application Settings and Configuration"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """Application Configuration Settings"""
    
    # App Settings
    app_name: str = "CASE Tool - Enterprise Software Cost Estimation"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # API Settings
    api_prefix: str = "/api/v1"
    api_title: str = "CASE Tool API"
    api_description: str = "Enterprise Software Cost Estimation API"
    
    # Server Settings
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    workers: int = 4
    
    # Database Settings
    database_url: str = "postgresql://casetool:casetool@localhost:5432/casetool_db"
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Security Settings
    secret_key: str = "your-secret-key-change-in-production-env"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS Settings
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:5500"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # Email Settings
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[str] = None

    # Jira Integration
    jira_base_url: Optional[str] = None
    jira_email: Optional[str] = None
    jira_api_token: Optional[str] = None
    jira_project_key: Optional[str] = None

    # Trello Integration
    trello_api_key: Optional[str] = None
    trello_api_token: Optional[str] = None
    trello_board_id: Optional[str] = None
    
    # Logging Settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # File Upload Settings
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    upload_directory: str = "./uploads"
    allowed_file_types: List[str] = ["csv", "xlsx", "json"]
    
    # ML Model Settings
    ml_model_path: str = "./models"
    enable_ml_predictions: bool = True
    
    # Cache Settings
    cache_ttl: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
