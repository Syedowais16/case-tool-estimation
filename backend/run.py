#!/usr/bin/env python
"""Entry point for the CASE Tool application"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.core.config.settings import get_settings
    
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers
    )
