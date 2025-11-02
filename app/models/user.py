from app import db
from datetime import datetime
import bcrypt


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, tech_writer, user
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Profile information (stored as JSON)
    profile_data = db.Column(db.JSON, default={})
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    content = db.relationship(
        'Content',
        back_populates='author',
        lazy='dynamic',
        cascade='all, delete-orphan',
        foreign_keys='Content.author_id'
    )

    approved_content = db.relationship(
        'Content',
        back_populates='approver',
        lazy='dynamic',
        foreign_keys='Content.approved_by'
    )

    comments = db.relationship('Comment', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    subscriptions = db.relationship('Subscription', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    content_reviews = db.relationship('ContentReview', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, role='user', profile_data=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
        self.profile_data = profile_data or {}
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self, include_email=False):
        """Convert user object to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'is_active': self.is_active,
            'profile_data': self.profile_data,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'
