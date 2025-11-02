from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.content import Content
from app.models.category import Category
from app.models.content_review import ContentReview
from app.utils.decorators import tech_writer_or_admin_required

writer_bp = Blueprint('tech_writer', __name__)

# ==================== CONTENT MANAGEMENT ====================

@writer_bp.route('/content', methods=['POST'])
@jwt_required()
@tech_writer_or_admin_required
def create_content():
    """Tech Writer: Create new content"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['title', 'content_type', 'category_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate content type
    if data['content_type'] not in ['video', 'audio', 'article']:
        return jsonify({'error': 'Invalid content type'}), 400
    
    # Validate category exists
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Create content
    content = Content(
        title=data['title'],
        content_type=data['content_type'],
        author_id=current_user_id,
        category_id=data['category_id'],
        description=data.get('description'),
        content_url=data.get('content_url'),
        body=data.get('body'),
        thumbnail_url=data.get('thumbnail_url')
    )
    
    # Set initial status
    content.status = data.get('status', 'draft')
    if content.status == 'pending':
        # Content submitted for approval
        pass
    
    try:
        db.session.add(content)
        db.session.commit()
        
        return jsonify({
            'message': 'Content created successfully',
            'content': content.to_dict(include_body=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create content: {str(e)}'}), 500

@writer_bp.route('/content/<int:content_id>', methods=['PUT'])
@jwt_required()
@tech_writer_or_admin_required
def update_content(content_id):
    """Tech Writer: Update content"""
    content = Content.query.get(content_id)
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    # Check if user is the author or admin
    from app.models.user import User
    current_user = User.query.get(current_user_id)
    
    if content.author_id != current_user_id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to edit this content'}), 403
    
    # Update fields
    if 'title' in data:
        content.title = data['title']
    if 'description' in data:
        content.description = data['description']
    if 'content_type' in data and data['content_type'] in ['video', 'audio', 'article']:
        content.content_type = data['content_type']
    if 'content_url' in data:
        content.content_url = data['content_url']
    if 'body' in data:
        content.body = data['body']
    if 'thumbnail_url' in data:
        content.thumbnail_url = data['thumbnail_url']
    if 'category_id' in data:
        category = Category.query.get(data['category_id'])
        if category:
            content.category_id = data['category_id']
    if 'status' in data and data['status'] in ['draft', 'pending']:
        content.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Content updated successfully',
            'content': content.to_dict(include_body=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update content: {str(e)}'}), 500

@writer_bp.route('/content/<int:content_id>', methods=['DELETE'])
@jwt_required()
@tech_writer_or_admin_required
def delete_content(content_id):
    """Tech Writer: Delete own content"""
    content = Content.query.get(content_id)
    current_user_id = get_jwt_identity()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    # Check if user is the author or admin
    from app.models.user import User
    current_user = User.query.get(current_user_id)
    
    if content.author_id != current_user_id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to delete this content'}), 403
    
    try:
        db.session.delete(content)
        db.session.commit()
        
        return jsonify({
            'message': 'Content deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete content: {str(e)}'}), 500

@writer_bp.route('/content', methods=['GET'])
@jwt_required()
@tech_writer_or_admin_required
def get_my_content():
    """Tech Writer: Get own content"""
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    
    query = Content.query.filter_by(author_id=current_user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(Content.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'content': [content.to_dict() for content in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

# ==================== CONTENT APPROVAL (Tech Writer can approve) ====================

@writer_bp.route('/content/<int:content_id>/approve', methods=['PUT'])
@jwt_required()
@tech_writer_or_admin_required
def approve_content(content_id):
    """Tech Writer: Approve content for publication"""
    content = Content.query.get(content_id)
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    if content.status != 'pending':
        return jsonify({'error': 'Only pending content can be approved'}), 400
    
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

@writer_bp.route('/content/<int:content_id>/flag', methods=['PUT'])
@jwt_required()
@tech_writer_or_admin_required
def flag_content(content_id):
    """Tech Writer: Flag content that violates guidelines"""
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
        
        # TODO: Send notification to content author and admin
        
        return jsonify({
            'message': 'Content flagged successfully',
            'content': content.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to flag content: {str(e)}'}), 500

# ==================== CONTENT REVIEWS (Like/Dislike) ====================

@writer_bp.route('/content/<int:content_id>/review', methods=['POST'])
@jwt_required()
@tech_writer_or_admin_required
def review_content(content_id):
    """Tech Writer: Review content (like/dislike)"""
    content = Content.query.get(content_id)
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    if not data.get('review_type') or data['review_type'] not in ['like', 'dislike']:
        return jsonify({'error': 'Invalid review type'}), 400
    
    # Check if user already reviewed
    existing_review = ContentReview.query.filter_by(
        content_id=content_id,
        user_id=current_user_id
    ).first()
    
    try:
        if existing_review:
            # Update existing review
            existing_review.review_type = data['review_type']
        else:
            # Create new review
            review = ContentReview(
                content_id=content_id,
                user_id=current_user_id,
                review_type=data['review_type']
            )
            db.session.add(review)
        
        db.session.commit()
        
        # Update content counts
        ContentReview.update_content_counts(content_id)
        
        return jsonify({
            'message': 'Review submitted successfully',
            'content': content.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to submit review: {str(e)}'}), 500

@writer_bp.route('/content/<int:content_id>/review', methods=['DELETE'])
@jwt_required()
@tech_writer_or_admin_required
def remove_review(content_id):
    """Tech Writer: Remove own review"""
    current_user_id = get_jwt_identity()
    
    review = ContentReview.query.filter_by(
        content_id=content_id,
        user_id=current_user_id
    ).first()
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    try:
        db.session.delete(review)
        db.session.commit()
        
        # Update content counts
        ContentReview.update_content_counts(content_id)
        
        return jsonify({
            'message': 'Review removed successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to remove review: {str(e)}'}), 500

# ==================== CATEGORY MANAGEMENT ====================

@writer_bp.route('/categories', methods=['POST'])
@jwt_required()
@tech_writer_or_admin_required
def create_category():
    """Tech Writer: Create a new category"""
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

@writer_bp.route('/categories', methods=['GET'])
@jwt_required()
@tech_writer_or_admin_required
def get_categories():
    """Tech Writer: Get all categories"""
    categories = Category.query.order_by(Category.name).all()
    
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    }), 200