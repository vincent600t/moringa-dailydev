from app import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Track who created the category
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    content = db.relationship('Content', back_populates='category', lazy='dynamic')
    subscriptions = db.relationship('Subscription', back_populates='category', lazy='dynamic', cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def __init__(self, name, description, created_by, slug=None):
        self.name = name
        self.description = description
        self.created_by = created_by
        self.slug = slug or self.generate_slug(name)
    
    @staticmethod
    def generate_slug(name):
        """Generate URL-friendly slug from name"""
        return name.lower().replace(' ', '-').replace('_', '-')
    
    def to_dict(self):
        """Convert category object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'content_count': self.content.count()
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'