"""
Comprehensive error handlers for the application
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from jwt.exceptions import InvalidTokenError
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register all error handlers with the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        logger.warning(f"Bad Request: {error}")
        return jsonify({
            'error': 'Bad Request',
            'message': str(error.description) if hasattr(error, 'description') else 'Invalid request'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors"""
        logger.warning(f"Unauthorized: {error}")
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required or token invalid'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors"""
        logger.warning(f"Forbidden: {error}")
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        logger.info(f"Not Found: {error}")
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        logger.warning(f"Method Not Allowed: {error}")
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for this endpoint'
        }), 405
    
    @app.errorhandler(409)
    def conflict(error):
        """Handle 409 Conflict errors"""
        logger.warning(f"Conflict: {error}")
        return jsonify({
            'error': 'Conflict',
            'message': str(error.description) if hasattr(error, 'description') else 'Resource conflict'
        }), 409
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle 422 Unprocessable Entity errors"""
        logger.warning(f"Unprocessable Entity: {error}")
        return jsonify({
            'error': 'Unprocessable Entity',
            'message': 'The request was well-formed but contains semantic errors'
        }), 422
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle 429 Too Many Requests errors"""
        logger.warning(f"Rate Limit Exceeded: {error}")
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        from app import db
        db.session.rollback()
        logger.error(f"Internal Server Error: {error}", exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable errors"""
        logger.error(f"Service Unavailable: {error}")
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'The service is temporarily unavailable'
        }), 503
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle all other HTTP exceptions"""
        logger.warning(f"HTTP Exception: {error}")
        return jsonify({
            'error': error.name,
            'message': error.description
        }), error.code
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Handle database integrity errors"""
        from app import db
        db.session.rollback()
        logger.error(f"Database Integrity Error: {error}", exc_info=True)
        
        # Parse common integrity errors
        error_msg = str(error.orig)
        
        if 'unique' in error_msg.lower():
            return jsonify({
                'error': 'Duplicate Entry',
                'message': 'A record with this information already exists'
            }), 409
        elif 'foreign key' in error_msg.lower():
            return jsonify({
                'error': 'Invalid Reference',
                'message': 'The referenced resource does not exist'
            }), 400
        else:
            return jsonify({
                'error': 'Database Error',
                'message': 'A database constraint was violated'
            }), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        """Handle SQLAlchemy errors"""
        from app import db
        db.session.rollback()
        logger.error(f"SQLAlchemy Error: {error}", exc_info=True)
        return jsonify({
            'error': 'Database Error',
            'message': 'A database error occurred. Please try again.'
        }), 500
    
    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(error):
        """Handle JWT token errors"""
        logger.warning(f"Invalid Token: {error}")
        return jsonify({
            'error': 'Invalid Token',
            'message': 'The provided token is invalid or expired'
        }), 401
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Handle ValueError exceptions"""
        logger.warning(f"Value Error: {error}")
        return jsonify({
            'error': 'Invalid Value',
            'message': str(error)
        }), 400
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handle all other unhandled exceptions"""
        from app import db
        db.session.rollback()
        logger.error(f"Unhandled Exception: {error}", exc_info=True)
        
        # In development, show the actual error
        if app.config.get('DEBUG'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(error),
                'type': type(error).__name__
            }), 500
        
        # In production, hide error details
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please contact support.'
        }), 500

class APIError(Exception):
    """Custom API exception class"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Convert exception to dictionary"""
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

class ValidationError(APIError):
    """Validation error exception"""
    def __init__(self, message, field=None):
        super().__init__(message, status_code=400)
        self.field = field

class AuthenticationError(APIError):
    """Authentication error exception"""
    def __init__(self, message='Authentication failed'):
        super().__init__(message, status_code=401)

class AuthorizationError(APIError):
    """Authorization error exception"""
    def __init__(self, message='Access denied'):
        super().__init__(message, status_code=403)

class ResourceNotFoundError(APIError):
    """Resource not found exception"""
    def __init__(self, message='Resource not found'):
        super().__init__(message, status_code=404)

class ConflictError(APIError):
    """Conflict error exception"""
    def __init__(self, message='Resource conflict'):
        super().__init__(message, status_code=409)