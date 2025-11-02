from app import db
from datetime import datetime

class ContentReview(db.Model):
    __tablename__ = 'content_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    content = db.relationship('Content', back_populates='reviews')
    user = db.relationship('User', back_populates='content_reviews')
    
    # Unique constraint - one review per user per content
    __table_args__ = (
        db.UniqueConstraint('user_id', 'content_id', name='unique_user_content_review'),
    )
    
    def __init__(self, content_id, user_id, review_type):
        self.content_id = content_id
        self.user_id = user_id
        self.review_type = review_type
    
    def to_dict(self):
        """Convert review object to dictionary"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'user_id': self.user_id,
            'review_type': self.review_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def update_content_counts(content_id):
        """Update like and dislike counts for content"""
        from app.models.content import Content
        
        content = Content.query.get(content_id)
        if content:
            content.likes_count = ContentReview.query.filter_by(
                content_id=content_id, review_type='like'
            ).count()
            content.dislikes_count = ContentReview.query.filter_by(
                content_id=content_id, review_type='dislike'
            ).count()
            db.session.commit()
    
    def __repr__(self):
        return f'<ContentReview {self.review_type} by User:{self.user_id} on Content:{self.content_id}>'