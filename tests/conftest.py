import pytest
from app import create_app, db
from app.models import User, Category, Content

@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """Create a CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
    """Create an admin user for testing"""
    with app.app_context():
        user = User(
            username='admin',
            email='admin@test.com',
            password='admin123',
            role='admin'
        )
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def tech_writer(app):
    """Create a tech writer for testing"""
    with app.app_context():
        user = User(
            username='writer',
            email='writer@test.com',
            password='writer123',
            role='tech_writer'
        )
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def normal_user(app):
    """Create a normal user for testing"""
    with app.app_context():
        user = User(
            username='user',
            email='user@test.com',
            password='user123',
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def category(app, admin_user):
    """Create a test category"""
    with app.app_context():
        cat = Category(
            name='DevOps',
            description='DevOps content',
            created_by=admin_user.id
        )
        db.session.add(cat)
        db.session.commit()
        return cat

@pytest.fixture
def content(app, tech_writer, category):
    """Create test content"""
    with app.app_context():
        cont = Content(
            title='Test Article',
            content_type='article',
            author_id=tech_writer.id,
            category_id=category.id,
            description='Test description',
            body='Test body content'
        )
        cont.status = 'approved'
        db.session.add(cont)
        db.session.commit()
        return cont

def get_auth_header(client, email, password):
    """Helper function to get authentication header"""
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    data = response.get_json()
    token = data.get('access_token')
    return {'Authorization': f'Bearer {token}'}