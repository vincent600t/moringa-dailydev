from app import db
from datetime import datetime

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Notification preferences
    notify_on_new_content = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='subscriptions')
    category = db.relationship('Category', back_populates='subscriptions')
    
    # Unique constraint to prevent duplicate subscriptions
    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_id', name='unique_user_category_subscription'),
    )
    
    def __init__(self, user_id, category_id, notify_on_new_content=True):
        self.user_id = user_id
        self.category_id = category_id
        self.notify_on_new_content = notify_on_new_content
    
    def to_dict(self):
        """Convert subscription object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': {
                'id': self.category.id,
                'name': self.category.name,
                'slug': self.category.slug
            },
            'notify_on_new_content': self.notify_on_new_content,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Subscription User:{self.user_id} Category:{self.category_id}>'