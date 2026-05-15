"""Logging middleware for request/response tracking"""
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging API requests and responses"""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Log request and response details"""
        # Start timing
        start_time = time.time()
        
        # Log request
        logger.info(f"{request.method} {request.url.path} - IP: {request.client.host if request.client else 'Unknown'}")
        
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration:.2f}s")
            
            return response
            
        except Exception as exc:
            # Log exceptions
            duration = time.time() - start_time
            logger.error(f"{request.method} {request.url.path} - Error: {str(exc)} - Duration: {duration:.2f}s")
            raise
