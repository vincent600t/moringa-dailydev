import pytest
from tests.conftest import get_auth_header

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self, client):
        """Test user registration"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'access_token' in data
        assert 'user' in data
        assert data['user']['username'] == 'newuser'
        assert data['user']['role'] == 'user'
    
    def test_register_duplicate_username(self, client, normal_user):
        """Test registration with duplicate username"""
        response = client.post('/api/auth/register', json={
            'username': 'user',
            'email': 'different@test.com',
            'password': 'password123'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'Username already exists' in data['error']
    
    def test_register_duplicate_email(self, client, normal_user):
        """Test registration with duplicate email"""
        response = client.post('/api/auth/register', json={
            'username': 'differentuser',
            'email': 'user@test.com',
            'password': 'password123'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'Email already exists' in data['error']
    
    def test_login_success(self, client, normal_user):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'email': 'user@test.com',
            'password': 'user123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'user' in data
        assert data['user']['email'] == 'user@test.com'
    
    def test_login_invalid_credentials(self, client, normal_user):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'email': 'user@test.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Invalid credentials' in data['error']
    
    def test_get_profile(self, client, normal_user):
        """Test getting user profile"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.get('/api/auth/profile', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data
        assert data['user']['username'] == 'user'
    
    def test_update_profile(self, client, normal_user):
        """Test updating user profile"""
        headers = get_auth_header(client, 'user@test.com', 'user123')
        response = client.put('/api/auth/profile', headers=headers, json={
            'username': 'updateduser',
            'profile_data': {
                'bio': 'Updated bio'
            }
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['username'] == 'updateduser'
        assert data['user']['profile_data']['bio'] == 'Updated bio'
    
    def test_access_protected_route_without_token(self, client):
        """Test accessing protected route without token"""
        response = client.get('/api/auth/profile')
        
        assert response.status_code == 401