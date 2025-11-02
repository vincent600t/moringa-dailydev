import os
from app import create_app, db
from app.models import User, Category, Content, Comment, Subscription, Wishlist, ContentReview

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'Content': Content,
        'Comment': Comment,
        'Subscription': Subscription,
        'Wishlist': Wishlist,
        'ContentReview': ContentReview
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)