from app import db
from datetime import datetime

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='wishlists')
    content = db.relationship('Content', back_populates='wishlists')
    
    # Unique constraint to prevent duplicate wishlist entries
    __table_args__ = (
        db.UniqueConstraint('user_id', 'content_id', name='unique_user_content_wishlist'),
    )
    
    def __init__(self, user_id, content_id):
        self.user_id = user_id
        self.content_id = content_id
    
    def to_dict(self, include_content=True):
        """Convert wishlist object to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'content_id': self.content_id,
            'created_at': self.created_at.isoformat()
        }
        
        if include_content:
            data['content'] = self.content.to_dict()
        
        return data
    
    def __repr__(self):
        return f'<Wishlist User:{self.user_id} Content:{self.content_id}>'