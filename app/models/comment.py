from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    
    # Foreign keys
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    content = db.relationship('Content', back_populates='comments')
    user = db.relationship('User', back_populates='comments')
    
    # Self-referential relationship for threading
    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, comment_text, content_id, user_id, parent_comment_id=None):
        self.comment_text = comment_text
        self.content_id = content_id
        self.user_id = user_id
        self.parent_comment_id = parent_comment_id
    
    def to_dict(self, include_replies=True, max_depth=3, current_depth=0):
        """Convert comment object to dictionary with nested replies"""
        data = {
            'id': self.id,
            'comment_text': self.comment_text,
            'content_id': self.content_id,
            'user': {
                'id': self.user.id,
                'username': self.user.username
            },
            'parent_comment_id': self.parent_comment_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'replies_count': self.replies.count()
        }
        
        # Include nested replies if requested and not exceeding max depth
        if include_replies and current_depth < max_depth:
            data['replies'] = [
                reply.to_dict(include_replies=True, max_depth=max_depth, current_depth=current_depth + 1)
                for reply in self.replies.order_by(Comment.created_at.desc()).all()
            ]
        
        return data
    
    def get_all_replies_recursive(self):
        """Get all replies recursively (flattened list)"""
        replies = []
        for reply in self.replies.all():
            replies.append(reply)
            replies.extend(reply.get_all_replies_recursive())
        return replies
    
    def __repr__(self):
        return f'<Comment {self.id} by User {self.user_id}>'