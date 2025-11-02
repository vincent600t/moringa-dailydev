import pytest
from tests.conftest import get_auth_header

class TestUserFeatures:
    """Test user-specific features"""
    
    def test_get_content_list(self, client, content):
        """Test getting list of content"""
        response = client.get('/api/content')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'content' in data
        assert len(data['content']) > 0
    
    def test_get_content_detail(self, client, content):
        """Test getting single content"""
        response = client.get(f'/api/content/{content.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'content' in data
        assert data['content']['title'] == 'Test Article'
        assert 'body' in data['content']
    
    def test_user_create_content(self, client, normal_user, category):
        """Test user creating content"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.post('/api/content', headers=headers, json={
            'title': 'User Article',
            'content_type': 'article',
            'category_id': category.id,
            'description': 'User created content',
            'body': 'Article body'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['content']['status'] == 'pending'
    
    def test_create_comment(self, client, normal_user, content):
        """Test creating a comment"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.post(f'/api/content/{content.id}/comments', 
                             headers=headers, json={
            'comment_text': 'Great article!'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['comment']['comment_text'] == 'Great article!'
    
    def test_create_reply_comment(self, client, normal_user, content):
        """Test creating a reply to a comment"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        
        # Create parent comment
        response = client.post(f'/api/content/{content.id}/comments', 
                             headers=headers, json={
            'comment_text': 'Parent comment'
        })
        parent_id = response.get_json()['comment']['id']
        
        # Create reply
        response = client.post(f'/api/content/{content.id}/comments', 
                             headers=headers, json={
            'comment_text': 'Reply to comment',
            'parent_comment_id': parent_id
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['comment']['parent_comment_id'] == parent_id
    
    def test_get_comments(self, client, normal_user, content):
        """Test getting comments for content"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        
        # Create a comment first
        client.post(f'/api/content/{content.id}/comments', 
                   headers=headers, json={
            'comment_text': 'Test comment'
        })
        
        # Get comments
        response = client.get(f'/api/content/{content.id}/comments')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'comments' in data
        assert len(data['comments']) > 0
    
    def test_subscribe_to_category(self, client, normal_user, category):
        """Test subscribing to a category"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.post('/api/subscriptions', headers=headers, json={
            'category_id': category.id
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['subscription']['category']['id'] == category.id
    
    def test_get_subscriptions(self, client, normal_user, category):
        """Test getting user subscriptions"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        
        # Subscribe first
        client.post('/api/subscriptions', headers=headers, json={
            'category_id': category.id
        })
        
        # Get subscriptions
        response = client.get('/api/subscriptions', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'subscriptions' in data
        assert len(data['subscriptions']) > 0
    
    def test_unsubscribe_from_category(self, client, normal_user, category):
        """Test unsubscribing from a category"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        
        # Subscribe first
        response = client.post('/api/subscriptions', headers=headers, json={
            'category_id': category.id
        })
        subscription_id = response.get_json()['subscription']['id']
        
        # Unsubscribe
        response = client.delete(f'/api/subscriptions/{subscription_id}', headers=headers)
        
        assert response.status_code == 200
    
    def test_add_to_wishlist(self, client, normal_user, content):
        """Test adding content to wishlist"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.post('/api/wishlist', headers=headers, json={
            'content_id': content.id
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['wishlist']['content_id'] == content.id
    
    def test_get_wishlist(self, client, normal_user, content):
        """Test getting user wishlist"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        
        # Add to wishlist first
        client.post('/api/wishlist', headers=headers, json={
            'content_id': content.id
        })
        
        # Get wishlist
        response = client.get('/api/wishlist', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'wishlist' in data
        assert len(data['wishlist']) > 0
    
    def test_remove_from_wishlist(self, client, normal_user, content):
        """Test removing content from wishlist"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        
        # Add to wishlist first
        response = client.post('/api/wishlist', headers=headers, json={
            'content_id': content.id
        })
        wishlist_id = response.get_json()['wishlist']['id']
        
        # Remove from wishlist
        response = client.delete(f'/api/wishlist/{wishlist_id}', headers=headers)
        
        assert response.status_code == 200
    
    def test_like_content(self, client, normal_user, content):
        """Test liking content"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.post(f'/api/content/{content.id}/review', 
                             headers=headers, json={
            'review_type': 'like'
        })
        
        assert response.status_code == 200
    
    def test_get_recommendations(self, client, normal_user, category, content):
        """Test getting personalized recommendations"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        
        # Subscribe to category first
        client.post('/api/subscriptions', headers=headers, json={
            'category_id': category.id
        })
        
        # Get recommendations
        response = client.get('/api/recommendations', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'recommendations' in data
    
    def test_get_categories(self, client, category):
        """Test getting all categories"""
        response = client.get('/api/categories')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'categories' in data
        assert len(data['categories']) > 0