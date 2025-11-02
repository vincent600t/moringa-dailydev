"""
App Models Package
------------------
This module centralizes all SQLAlchemy models so they can be imported easily
and ensures they're registered when Flask-Migrate runs.
"""

from app import db

# Import models explicitly to register them with SQLAlchemy
from app.models.user import User
from app.models.category import Category
from app.models.content import Content
from app.models.comment import Comment
from app.models.subscription import Subscription
from app.models.wishlist import Wishlist
from app.models.content_review import ContentReview

# Exported symbols
__all__ = [
    "db",
    "User",
    "Category",
    "Content",
    "Comment",
    "Subscription",
    "Wishlist",
    "ContentReview",
]
