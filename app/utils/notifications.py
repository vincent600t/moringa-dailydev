"""
Notification system for sending updates to users
"""
from datetime import datetime
from app import db
from app.models.subscription import Subscription
from app.models.content import Content

class NotificationService:
    """Service for handling notifications"""
    
    @staticmethod
    def notify_new_content(content_id):
        """
        Notify subscribers when new content is published
        
        Args:
            content_id: ID of the published content
        """
        content = Content.query.get(content_id)
        if not content or content.status != 'approved':
            return
        
        # Get all subscribers of this category
        subscriptions = Subscription.query.filter_by(
            category_id=content.category_id,
            notify_on_new_content=True
        ).all()
        
        notifications = []
        for subscription in subscriptions:
            notification = {
                'user_id': subscription.user_id,
                'content_id': content_id,
                'type': 'new_content',
                'title': f"New {content.content_type} in {content.category.name}",
                'message': f"'{content.title}' has been published",
                'link': f"/content/{content_id}",
                'created_at': datetime.utcnow().isoformat()
            }
            notifications.append(notification)
        
        # TODO: Implement actual notification delivery
        # Options: Email, Push notifications, In-app notifications
        # For now, we'll just return the notifications that should be sent
        return notifications
    
    @staticmethod
    def notify_content_approved(content_id, author_id):
        """
        Notify author when their content is approved
        
        Args:
            content_id: ID of the approved content
            author_id: ID of the content author
        """
        content = Content.query.get(content_id)
        if not content:
            return None
        
        notification = {
            'user_id': author_id,
            'content_id': content_id,
            'type': 'content_approved',
            'title': 'Your content has been approved!',
            'message': f"'{content.title}' is now published",
            'link': f"/content/{content_id}",
            'created_at': datetime.utcnow().isoformat()
        }
        
        # TODO: Send email or push notification
        return notification
    
    @staticmethod
    def notify_content_flagged(content_id, author_id, reason):
        """
        Notify author when their content is flagged
        
        Args:
            content_id: ID of the flagged content
            author_id: ID of the content author
            reason: Reason for flagging
        """
        content = Content.query.get(content_id)
        if not content:
            return None
        
        notification = {
            'user_id': author_id,
            'content_id': content_id,
            'type': 'content_flagged',
            'title': 'Your content has been flagged',
            'message': f"'{content.title}' was flagged: {reason}",
            'link': f"/content/{content_id}",
            'created_at': datetime.utcnow().isoformat()
        }
        
        # TODO: Send email notification
        return notification
    
    @staticmethod
    def notify_new_comment(comment_id, content_author_id):
        """
        Notify content author of new comment
        
        Args:
            comment_id: ID of the new comment
            content_author_id: ID of the content author
        """
        from app.models.comment import Comment
        
        comment = Comment.query.get(comment_id)
        if not comment:
            return None
        
        notification = {
            'user_id': content_author_id,
            'comment_id': comment_id,
            'content_id': comment.content_id,
            'type': 'new_comment',
            'title': 'New comment on your content',
            'message': f"{comment.user.username} commented: {comment.comment_text[:50]}...",
            'link': f"/content/{comment.content_id}#comment-{comment_id}",
            'created_at': datetime.utcnow().isoformat()
        }
        
        return notification
    
    @staticmethod
    def notify_comment_reply(comment_id, parent_author_id):
        """
        Notify user when someone replies to their comment
        
        Args:
            comment_id: ID of the reply comment
            parent_author_id: ID of the parent comment author
        """
        from app.models.comment import Comment
        
        comment = Comment.query.get(comment_id)
        if not comment or not comment.parent_comment_id:
            return None
        
        notification = {
            'user_id': parent_author_id,
            'comment_id': comment_id,
            'content_id': comment.content_id,
            'type': 'comment_reply',
            'title': 'New reply to your comment',
            'message': f"{comment.user.username} replied: {comment.comment_text[:50]}...",
            'link': f"/content/{comment.content_id}#comment-{comment_id}",
            'created_at': datetime.utcnow().isoformat()
        }
        
        return notification
    
    @staticmethod
    def notify_account_deactivated(user_id, reason=None):
        """
        Notify user when their account is deactivated
        
        Args:
            user_id: ID of the deactivated user
            reason: Optional reason for deactivation
        """
        notification = {
            'user_id': user_id,
            'type': 'account_deactivated',
            'title': 'Your account has been deactivated',
            'message': f"Reason: {reason}" if reason else "Contact admin for details",
            'created_at': datetime.utcnow().isoformat()
        }
        
        return notification

# Helper function to send email notifications (placeholder)
def send_email_notification(user_email, subject, body):
    """
    Send email notification to user
    
    Args:
        user_email: Email address
        subject: Email subject
        body: Email body
    
    TODO: Implement with Flask-Mail or SendGrid
    """
    # Placeholder for email sending
    print(f"[EMAIL] To: {user_email}")
    print(f"[EMAIL] Subject: {subject}")
    print(f"[EMAIL] Body: {body}")
    print("-" * 50)
    return True