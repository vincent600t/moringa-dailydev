from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from app import db
from app.models.content import Content
from app.models.category import Category
from app.models.comment import Comment
from app.models.subscription import Subscription
from app.models.wishlist import Wishlist
from app.models.content_review import ContentReview
from app.utils.decorators import active_user_required

user_bp = Blueprint('user', __name__)

# ==================== CONTENT BROWSING ====================

@user_bp.route('/content', methods=['GET'])
def get_content():
    """Get all published content with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category_id = request.args.get('category_id', type=int)
    content_type = request.args.get('content_type')
    search = request.args.get('search')
    
    # Base query - only approved content
    query = Content.query.filter_by(status='approved')
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if content_type:
        query = query.filter_by(content_type=content_type)
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Content.title.ilike(search_term),
                Content.description.ilike(search_term)
            )
        )
    
    # Order by most recent
    pagination = query.order_by(Content.published_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'content': [content.to_dict() for content in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@user_bp.route('/content/<int:content_id>', methods=['GET'])
def get_content_detail(content_id):
    """Get single content with full details"""
    content = Content.query.get(content_id)
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    # Only show approved content to non-authors
    if content.status != 'approved':
        # Check if user is authenticated and is the author
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            if not current_user_id or content.author_id != current_user_id:
                return jsonify({'error': 'Content not available'}), 404
        except:
            return jsonify({'error': 'Content not available'}), 404
    
    # Increment view count
    content.increment_views()
    
    return jsonify({
        'content': content.to_dict(include_body=True)
    }), 200

# ==================== USER CONTENT CREATION ====================

@user_bp.route('/content', methods=['POST'])
@jwt_required()
@active_user_required
def create_user_content():
    """User: Create new content"""
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
    
    # Create content with pending status
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
    
    content.status = 'pending'  # User content needs approval
    
    try:
        db.session.add(content)
        db.session.commit()
        
        return jsonify({
            'message': 'Content submitted for approval',
            'content': content.to_dict(include_body=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create content: {str(e)}'}), 500

# ==================== COMMENTS ====================

@user_bp.route('/content/<int:content_id>/comments', methods=['POST'])
@jwt_required()
@active_user_required
def create_comment(content_id):
    """Create a comment on content"""
    content = Content.query.get(content_id)
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    if not data.get('comment_text'):
        return jsonify({'error': 'Comment text is required'}), 400
    
    # Validate parent comment if provided
    parent_comment_id = data.get('parent_comment_id')
    if parent_comment_id:
        parent_comment = Comment.query.get(parent_comment_id)
        if not parent_comment or parent_comment.content_id != content_id:
            return jsonify({'error': 'Invalid parent comment'}), 400
    
    comment = Comment(
        comment_text=data['comment_text'],
        content_id=content_id,
        user_id=current_user_id,
        parent_comment_id=parent_comment_id
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create comment: {str(e)}'}), 500

@user_bp.route('/content/<int:content_id>/comments', methods=['GET'])
def get_comments(content_id):
    """Get all comments for content with threading"""
    content = Content.query.get(content_id)
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    # Get only top-level comments (no parent)
    top_level_comments = Comment.query.filter_by(
        content_id=content_id,
        parent_comment_id=None
    ).order_by(Comment.created_at.desc()).all()
    
    return jsonify({
        'comments': [comment.to_dict(include_replies=True) for comment in top_level_comments],
        'total': content.comments.count()
    }), 200

@user_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
@active_user_required
def update_comment(comment_id):
    """Update own comment"""
    comment = Comment.query.get(comment_id)
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    if comment.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to edit this comment'}), 403
    
    if not data.get('comment_text'):
        return jsonify({'error': 'Comment text is required'}), 400
    
    comment.comment_text = data['comment_text']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Comment updated successfully',
            'comment': comment.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update comment: {str(e)}'}), 500

@user_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
@active_user_required
def delete_comment(comment_id):
    """Delete own comment"""
    comment = Comment.query.get(comment_id)
    current_user_id = get_jwt_identity()
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    if comment.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to delete this comment'}), 403
    
    try:
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete comment: {str(e)}'}), 500

# ==================== SUBSCRIPTIONS ====================

@user_bp.route('/subscriptions', methods=['POST'])
@jwt_required()
@active_user_required
def subscribe_to_category():
    """Subscribe to a category"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not data.get('category_id'):
        return jsonify({'error': 'Category ID is required'}), 400
    
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Check if already subscribed
    existing = Subscription.query.filter_by(
        user_id=current_user_id,
        category_id=data['category_id']
    ).first()
    
    if existing:
        return jsonify({'error': 'Already subscribed to this category'}), 409
    
    subscription = Subscription(
        user_id=current_user_id,
        category_id=data['category_id'],
        notify_on_new_content=data.get('notify_on_new_content', True)
    )
    
    try:
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({
            'message': 'Subscribed successfully',
            'subscription': subscription.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to subscribe: {str(e)}'}), 500

@user_bp.route('/subscriptions', methods=['GET'])
@jwt_required()
@active_user_required
def get_subscriptions():
    """Get user's subscriptions"""
    current_user_id = get_jwt_identity()
    
    subscriptions = Subscription.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'subscriptions': [sub.to_dict() for sub in subscriptions]
    }), 200

@user_bp.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
@jwt_required()
@active_user_required
def unsubscribe(subscription_id):
    """Unsubscribe from a category"""
    current_user_id = get_jwt_identity()
    
    subscription = Subscription.query.filter_by(
        id=subscription_id,
        user_id=current_user_id
    ).first()
    
    if not subscription:
        return jsonify({'error': 'Subscription not found'}), 404
    
    try:
        db.session.delete(subscription)
        db.session.commit()
        
        return jsonify({
            'message': 'Unsubscribed successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to unsubscribe: {str(e)}'}), 500

@user_bp.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
@jwt_required()
@active_user_required
def update_subscription(subscription_id):
    """Update subscription preferences"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    subscription = Subscription.query.filter_by(
        id=subscription_id,
        user_id=current_user_id
    ).first()
    
    if not subscription:
        return jsonify({'error': 'Subscription not found'}), 404
    
    if 'notify_on_new_content' in data:
        subscription.notify_on_new_content = data['notify_on_new_content']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Subscription updated successfully',
            'subscription': subscription.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update subscription: {str(e)}'}), 500

# ==================== WISHLIST ====================

@user_bp.route('/wishlist', methods=['POST'])
@jwt_required()
@active_user_required
def add_to_wishlist():
    """Add content to wishlist"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not data.get('content_id'):
        return jsonify({'error': 'Content ID is required'}), 400
    
    content = Content.query.get(data['content_id'])
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(
        user_id=current_user_id,
        content_id=data['content_id']
    ).first()
    
    if existing:
        return jsonify({'error': 'Content already in wishlist'}), 409
    
    wishlist = Wishlist(
        user_id=current_user_id,
        content_id=data['content_id']
    )
    
    try:
        db.session.add(wishlist)
        db.session.commit()
        
        return jsonify({
            'message': 'Added to wishlist',
            'wishlist': wishlist.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add to wishlist: {str(e)}'}), 500

@user_bp.route('/wishlist', methods=['GET'])
@jwt_required()
@active_user_required
def get_wishlist():
    """Get user's wishlist"""
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Wishlist.query.filter_by(user_id=current_user_id)\
        .order_by(Wishlist.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'wishlist': [item.to_dict(include_content=True) for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@user_bp.route('/wishlist/<int:wishlist_id>', methods=['DELETE'])
@jwt_required()
@active_user_required
def remove_from_wishlist(wishlist_id):
    """Remove content from wishlist"""
    current_user_id = get_jwt_identity()
    
    wishlist = Wishlist.query.filter_by(
        id=wishlist_id,
        user_id=current_user_id
    ).first()
    
    if not wishlist:
        return jsonify({'error': 'Wishlist item not found'}), 404
    
    try:
        db.session.delete(wishlist)
        db.session.commit()
        
        return jsonify({
            'message': 'Removed from wishlist'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to remove from wishlist: {str(e)}'}), 500

# ==================== CONTENT REVIEWS (Like/Dislike) ====================

@user_bp.route('/content/<int:content_id>/review', methods=['POST'])
@jwt_required()
@active_user_required
def review_content(content_id):
    """Review content (like/dislike)"""
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
            'message': 'Review submitted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to submit review: {str(e)}'}), 500

# ==================== RECOMMENDATIONS ====================

@user_bp.route('/recommendations', methods=['GET'])
@jwt_required()
@active_user_required
def get_recommendations():
    """Get personalized content recommendations"""
    current_user_id = get_jwt_identity()
    limit = request.args.get('limit', 10, type=int)
    
    # Get user's subscribed categories
    subscriptions = Subscription.query.filter_by(user_id=current_user_id).all()
    subscribed_category_ids = [sub.category_id for sub in subscriptions]
    
    if not subscribed_category_ids:
        # No subscriptions, return popular content
        recommendations = Content.query.filter_by(status='approved')\
            .order_by(desc(Content.views_count))\
            .limit(limit).all()
    else:
        # Get content from subscribed categories
        recommendations = Content.query\
            .filter(Content.status == 'approved')\
            .filter(Content.category_id.in_(subscribed_category_ids))\
            .order_by(desc(Content.published_at))\
            .limit(limit).all()
    
    return jsonify({
        'recommendations': [content.to_dict() for content in recommendations]
    }), 200

# ==================== CATEGORIES ====================

@user_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = Category.query.order_by(Category.name).all()
    
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    }), 200

@user_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get category details"""
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    return jsonify({
        'category': category.to_dict()
    }), 200