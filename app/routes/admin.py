from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.user import User
from app.models.content import Content
from app.models.category import Category
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

# ==================== USER MANAGEMENT ====================

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def add_user():
    """Admin: Add a new user with specific role"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate role
    if data['role'] not in ['user', 'tech_writer', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data['role'],
        profile_data=data.get('profile_data', {})
    )
    
    try:
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict(include_email=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create user: {str(e)}'}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Admin: Get all users with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role = request.args.get('role')
    is_active = request.args.get('is_active')
    
    query = User.query
    
    # Apply filters
    if role:
        query = query.filter_by(role=role)
    if is_active is not None:
        query = query.filter_by(is_active=is_active.lower() == 'true')
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_dict(include_email=True) for user in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@admin_bp.route('/users/<int:user_id>/deactivate', methods=['PUT'])
@jwt_required()
@admin_required
def deactivate_user(user_id):
    """Admin: Deactivate a user account"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent admin from deactivating themselves
    current_user_id = get_jwt_identity()
    if user_id == current_user_id:
        return jsonify({'error': 'Cannot deactivate your own account'}), 400
    
    user.is_active = False
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User deactivated successfully',
            'user': user.to_dict(include_email=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to deactivate user: {str(e)}'}), 500

@admin_bp.route('/users/<int:user_id>/activate', methods=['PUT'])
@jwt_required()
@admin_required
def activate_user(user_id):
    """Admin: Activate a user account"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.is_active = True
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User activated successfully',
            'user': user.to_dict(include_email=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to activate user: {str(e)}'}), 500

# ==================== CONTENT MANAGEMENT ====================

@admin_bp.route('/content/pending', methods=['GET'])
@jwt_required()
@admin_required
def get_pending_content():
    """Admin: Get all pending content"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Content.query.filter_by(status='pending')\
        .order_by(Content.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'content': [content.to_dict() for content in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@admin_bp.route('/content/<int:content_id>/approve', methods=['PUT'])
@jwt_required()
@admin_required
def approve_content(content_id):
    """Admin: Approve content for publication"""
    content = Content.query.get(content_id)
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    current_user_id = get_jwt_identity()
    content.status = 'approved'
    content.approved_by = current_user_id
    content.published_at = datetime.utcnow()
    
    try:
        db.session.commit()
        
        # TODO: Send notification to subscribers
        
        return jsonify({
            'message': 'Content approved successfully',
            'content': content.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to approve content: {str(e)}'}), 500

@admin_bp.route('/content/<int:content_id>/flag', methods=['PUT'])
@jwt_required()
@admin_required
def flag_content(content_id):
    """Admin: Flag content that violates guidelines"""
    content = Content.query.get(content_id)
    data = request.get_json()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    if not data.get('flag_reason'):
        return jsonify({'error': 'Flag reason is required'}), 400
    
    content.status = 'flagged'
    content.flag_reason = data['flag_reason']
    
    try:
        db.session.commit()
        
        # TODO: Send notification to content author
        
        return jsonify({
            'message': 'Content flagged successfully',
            'content': content.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to flag content: {str(e)}'}), 500

@admin_bp.route('/content/<int:content_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def remove_content(content_id):
    """Admin: Remove content"""
    content = Content.query.get(content_id)
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    try:
        db.session.delete(content)
        db.session.commit()
        
        return jsonify({
            'message': 'Content removed successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to remove content: {str(e)}'}), 500

# ==================== CATEGORY MANAGEMENT ====================

@admin_bp.route('/categories', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    """Admin: Create a new category"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400
    
    # Check if category already exists
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 409
    
    category = Category(
        name=data['name'],
        description=data.get('description', ''),
        created_by=current_user_id,
        slug=data.get('slug')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create category: {str(e)}'}), 500

@admin_bp.route('/categories', methods=['GET'])
@jwt_required()
@admin_required
def get_all_categories():
    """Admin: Get all categories"""
    categories = Category.query.order_by(Category.name).all()
    
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    }), 200

@admin_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(category_id):
    """Admin: Update a category"""
    category = Category.query.get(category_id)
    data = request.get_json()
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    if 'name' in data:
        # Check if new name already exists
        existing = Category.query.filter_by(name=data['name']).first()
        if existing and existing.id != category_id:
            return jsonify({'error': 'Category name already exists'}), 409
        category.name = data['name']
        category.slug = Category.generate_slug(data['name'])
    
    if 'description' in data:
        category.description = data['description']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update category: {str(e)}'}), 500

@admin_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(category_id):
    """Admin: Delete a category"""
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Check if category has content
    if category.content.count() > 0:
        return jsonify({'error': 'Cannot delete category with existing content'}), 400
    
    try:
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete category: {str(e)}'}), 500