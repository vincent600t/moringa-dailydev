import pytest
from tests.conftest import get_auth_header

class TestAdminFeatures:
    """Test admin-specific features"""
    
    def test_admin_create_user(self, client, admin_user):
        """Test admin creating a new user"""
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.post('/api/admin/users', headers=headers, json={
            'username': 'newwriter',
            'email': 'newwriter@test.com',
            'password': 'writer123',
            'role': 'tech_writer'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['role'] == 'tech_writer'
    
    def test_non_admin_cannot_create_user(self, client, normal_user):
        """Test that non-admin cannot create users"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.post('/api/admin/users', headers=headers, json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'role': 'user'
        })
        
        assert response.status_code == 403
    
    def test_admin_deactivate_user(self, client, admin_user, normal_user):
        """Test admin deactivating a user"""
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.put(f'/api/admin/users/{normal_user.id}/deactivate', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['is_active'] is False
    
    def test_admin_cannot_deactivate_self(self, client, admin_user):
        """Test admin cannot deactivate their own account"""
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.put(f'/api/admin/users/{admin_user.id}/deactivate', headers=headers)
        
        assert response.status_code == 400
    
    def test_admin_create_category(self, client, admin_user):
        """Test admin creating a category"""
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.post('/api/admin/categories', headers=headers, json={
            'name': 'Frontend',
            'description': 'Frontend development'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['category']['name'] == 'Frontend'
        assert data['category']['slug'] == 'frontend'
    
    def test_admin_approve_content(self, client, admin_user, content):
        """Test admin approving content"""
        # Set content to pending first
        from app import db
        content.status = 'pending'
        db.session.commit()
        
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.put(f'/api/admin/content/{content.id}/approve', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['content']['status'] == 'approved'
    
    def test_admin_flag_content(self, client, admin_user, content):
        """Test admin flagging content"""
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.put(f'/api/admin/content/{content.id}/flag', headers=headers, json={
            'flag_reason': 'Inappropriate content'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['content']['status'] == 'flagged'
        assert 'flag_reason' in data['content']
    
    def test_admin_remove_content(self, client, admin_user, content):
        """Test admin removing content"""
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.delete(f'/api/admin/content/{content.id}', headers=headers)
        
        assert response.status_code == 200
    
    def test_admin_get_users(self, client, admin_user, normal_user, tech_writer):
        """Test admin getting all users"""
        headers = get_auth_header(client, 'admin@test.com', 'admin123')
        response = client.get('/api/admin/users', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'users' in data
        assert len(data['users']) >= 3