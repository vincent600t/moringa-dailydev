"""
Helper utility functions
"""
from datetime import datetime, timedelta
from flask import url_for
import secrets
import string

def generate_random_string(length=32):
    """
    Generate a random string for tokens, etc.
    
    Args:
        length: Length of the string
        
    Returns:
        str: Random string
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_slug(text):
    """
    Generate URL-friendly slug from text
    
    Args:
        text: Text to convert to slug
        
    Returns:
        str: Slug
    """
    import re
    
    # Convert to lowercase
    slug = text.lower()
    
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug

def format_datetime(dt, format_string="%Y-%m-%d %H:%M:%S"):
    """
    Format datetime object to string
    
    Args:
        dt: Datetime object
        format_string: Format string
        
    Returns:
        str: Formatted datetime
    """
    if not dt:
        return None
    
    if isinstance(dt, str):
        return dt
    
    return dt.strftime(format_string)

def parse_datetime(dt_string, format_string="%Y-%m-%d %H:%M:%S"):
    """
    Parse datetime string to datetime object
    
    Args:
        dt_string: Datetime string
        format_string: Format string
        
    Returns:
        datetime: Datetime object
    """
    try:
        return datetime.strptime(dt_string, format_string)
    except (ValueError, TypeError):
        return None

def time_ago(dt):
    """
    Convert datetime to human-readable "time ago" format
    
    Args:
        dt: Datetime object
        
    Returns:
        str: Human-readable time difference
    """
    if not dt:
        return "Unknown"
    
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"

def paginate_query(query, page, per_page):
    """
    Paginate SQLAlchemy query
    
    Args:
        query: SQLAlchemy query object
        page: Page number
        per_page: Items per page
        
    Returns:
        dict: Pagination result
    """
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'next_page': page + 1 if pagination.has_next else None,
        'prev_page': page - 1 if pagination.has_prev else None
    }

def truncate_text(text, length=100, suffix='...'):
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to append
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= length:
        return text
    
    return text[:length].rsplit(' ', 1)[0] + suffix

def get_file_extension(filename):
    """
    Get file extension from filename
    
    Args:
        filename: Filename
        
    Returns:
        str: File extension (without dot)
    """
    if '.' not in filename:
        return ''
    
    return filename.rsplit('.', 1)[1].lower()

def is_allowed_file(filename, allowed_extensions):
    """
    Check if file has allowed extension
    
    Args:
        filename: Filename
        allowed_extensions: Set of allowed extensions
        
    Returns:
        bool: True if allowed
    """
    return '.' in filename and \
           get_file_extension(filename) in allowed_extensions

def build_response(data=None, message=None, status_code=200):
    """
    Build standardized API response
    
    Args:
        data: Response data
        message: Response message
        status_code: HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {}
    
    if message:
        response['message'] = message
    
    if data is not None:
        response.update(data)
    
    return response, status_code

def build_error_response(error, status_code=400):
    """
    Build standardized error response
    
    Args:
        error: Error message
        status_code: HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    return {'error': error}, status_code

def calculate_reading_time(text, words_per_minute=200):
    """
    Calculate estimated reading time for text
    
    Args:
        text: Text content
        words_per_minute: Average reading speed
        
    Returns:
        int: Estimated reading time in minutes
    """
    if not text:
        return 0
    
    word_count = len(text.split())
    minutes = max(1, round(word_count / words_per_minute))
    
    return minutes

def get_content_type_icon(content_type):
    """
    Get icon name for content type
    
    Args:
        content_type: Content type (article, video, audio)
        
    Returns:
        str: Icon name
    """
    icons = {
        'article': 'file-text',
        'video': 'video',
        'audio': 'headphones'
    }
    
    return icons.get(content_type, 'file')

def merge_dicts(*dicts):
    """
    Merge multiple dictionaries
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        dict: Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result

def safe_int(value, default=0):
    """
    Safely convert value to integer
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        int: Converted value or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """
    Safely convert value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        float: Converted value or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def chunks(lst, n):
    """
    Yield successive n-sized chunks from list
    
    Args:
        lst: List to chunk
        n: Chunk size
        
    Yields:
        list: Chunks of size n
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def deduplicate_list(lst):
    """
    Remove duplicates from list while preserving order
    
    Args:
        lst: List with potential duplicates
        
    Returns:
        list: List without duplicates
    """
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]