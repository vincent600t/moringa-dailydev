"""
Logging middleware for request/response tracking
"""
import time
import logging
from flask import request, g
from functools import wraps

# Configure logger
logger = logging.getLogger(__name__)

def setup_logging(app):
    """Setup application logging"""
    if not app.debug:
        # Production logging
        handler = logging.FileHandler('app.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Moringa Daily.dev startup')

def log_request():
    """Log incoming request details"""
    g.start_time = time.time()
    logger.info(f"Request: {request.method} {request.path}")
    
    # Log request body for POST/PUT (excluding sensitive data)
    if request.method in ['POST', 'PUT', 'PATCH']:
        data = request.get_json(silent=True)
        if data:
            # Remove sensitive fields
            safe_data = {k: v for k, v in data.items() 
                        if k not in ['password', 'token', 'secret']}
            logger.debug(f"Request data: {safe_data}")

def log_response(response):
    """Log response details"""
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        logger.info(
            f"Response: {response.status_code} "
            f"for {request.method} {request.path} "
            f"took {elapsed:.2f}s"
        )
    return response

def log_error(error):
    """Log error details"""
    logger.error(
        f"Error: {str(error)} "
        f"on {request.method} {request.path}",
        exc_info=True
    )

def request_logger(f):
    """Decorator to log function execution"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.debug(f"Executing {f.__name__}")
        try:
            result = f(*args, **kwargs)
            logger.debug(f"Successfully executed {f.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            raise
    return decorated_function