from app import db
from datetime import datetime

class Content(db.Model):
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # video, audio, article
    content_url = db.Column(db.String(500))  # URL for video/audio or main content
    description = db.Column(db.Text)
    body = db.Column(db.Text)  # For articles/blogs
    thumbnail_url = db.Column(db.String(500))
    
    # Status management
    status = db.Column(db.String(20), default='pending', nullable=False)  # draft, pending, approved, flagged, removed
    flag_reason = db.Column(db.Text)  # Reason for flagging
    tags = db.Column(db.ARRAY(db.String), default=[])

    # Foreign keys
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Metrics
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    dislikes_count = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    published_at = db.Column(db.DateTime)

    # Relationships
    author = db.relationship('User', foreign_keys=[author_id], back_populates='content')
    approver = db.relationship('User', foreign_keys=[approved_by], back_populates='approved_content')
    category = db.relationship('Category', back_populates='content')
    comments = db.relationship('Comment', back_populates='content', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('ContentReview', back_populates='content', lazy='dynamic', cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', back_populates='content', lazy='dynamic', cascade='all, delete-orphan')

    # ✅ Updated constructor (Option 2)
    def __init__(self, title, content_type, author_id, category_id, description=None, 
                 content_url=None, body=None, thumbnail_url=None, status='pending', 
                 approved_by=None, tags=None, views_count=0, likes_count=0, dislikes_count=0):
        self.title = title
        self.content_type = content_type
        self.author_id = author_id
        self.category_id = category_id
        self.description = description
        self.content_url = content_url
        self.body = body
        self.thumbnail_url = thumbnail_url
        self.status = status
        self.approved_by = approved_by
        self.tags = tags or []
        self.views_count = views_count
        self.likes_count = likes_count
        self.dislikes_count = dislikes_count

    def to_dict(self, include_body=False):
        """Convert content object to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'content_type': self.content_type,
            'content_url': self.content_url,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'status': self.status,
            'flag_reason': self.flag_reason,
            'tags': self.tags,
            'author': {
                'id': self.author.id,
                'username': self.author.username
            },
            'category': {
                'id': self.category.id,
                'name': self.category.name,
                'slug': self.category.slug
            },
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'dislikes_count': self.dislikes_count,
            'comments_count': self.comments.count(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'approved_by': self.approved_by
        }
        
        if include_body and self.body:
            data['body'] = self.body
        
        return data
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        db.session.commit()
    
    def __repr__(self):
        return f'<Content {self.title} ({self.status})>'
