"""
Input validation utilities
"""
import re
from functools import wraps
from flask import request, jsonify

def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength
    Requires: 8+ chars, 1 uppercase, 1 lowercase, 1 number
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

def validate_username(username):
    """
    Validate username format
    Alphanumeric and underscores only, 3-30 characters
    
    Args:
        username: Username string to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 30:
        return False, "Username must be at most 30 characters long"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Username is valid"

def validate_content_type(content_type):
    """
    Validate content type
    
    Args:
        content_type: Content type string
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_types = ['article', 'video', 'audio']
    return content_type in valid_types

def validate_url(url):
    """
    Validate URL format
    
    Args:
        url: URL string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^https?://[^\s]+$'
    return re.match(pattern, url) is not None

def validate_role(role):
    """
    Validate user role
    
    Args:
        role: Role string
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_roles = ['admin', 'tech_writer', 'user']
    return role in valid_roles

def validate_review_type(review_type):
    """
    Validate review type
    
    Args:
        review_type: Review type string
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_types = ['like', 'dislike']
    return review_type in valid_types

def validate_content_status(status):
    """
    Validate content status
    
    Args:
        status: Status string
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_statuses = ['draft', 'pending', 'approved', 'flagged', 'removed']
    return status in valid_statuses

def require_fields(*required_fields):
    """
    Decorator to validate required fields in request JSON
    
    Args:
        *required_fields: Field names that must be present
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'Request body must be JSON'}), 400
            
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    'error': f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_pagination(page, per_page, max_per_page=100):
    """
    Validate pagination parameters
    
    Args:
        page: Page number
        per_page: Items per page
        max_per_page: Maximum items per page
        
    Returns:
        tuple: (page, per_page, error_message)
    """
    error = None
    
    if page < 1:
        page = 1
        error = "Page must be at least 1"
    
    if per_page < 1:
        per_page = 20
        error = "Items per page must be at least 1"
    
    if per_page > max_per_page:
        per_page = max_per_page
        error = f"Items per page cannot exceed {max_per_page}"
    
    return page, per_page, error

def sanitize_input(text, max_length=None):
    """
    Sanitize text input
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)