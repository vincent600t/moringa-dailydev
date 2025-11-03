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
        
        # Refresh to ensure it's in the session
        db.session.refresh(user)
        user_id = user.id  # Store the ID
        
    # Return a fresh query for the user
    with app.app_context():
        return db.session.get(User, user_id)

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
        
        user_id = user.id
        
    with app.app_context():
        return db.session.get(User, user_id)

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
        
        user_id = user.id
        
    with app.app_context():
        return db.session.get(User, user_id)

@pytest.fixture
def category(app, admin_user):
    """Create a test category"""
    with app.app_context():
        # Get fresh admin_user in this context
        admin = db.session.get(User, admin_user.id)
        
        cat = Category(
            name='DevOps',
            description='DevOps content',
            created_by=admin.id
        )
        db.session.add(cat)
        db.session.commit()
        
        cat_id = cat.id
        
    with app.app_context():
        return db.session.get(Category, cat_id)

@pytest.fixture
def content(app, tech_writer, category):
    """Create test content"""
    with app.app_context():
        # Get fresh objects in this context
        writer = db.session.get(User, tech_writer.id)
        cat = db.session.get(Category, category.id)
        
        cont = Content(
            title='Test Article',
            content_type='article',
            author_id=writer.id,
            category_id=cat.id,
            description='Test description',
            body='Test body content'
        )
        cont.status = 'approved'
        db.session.add(cont)
        db.session.commit()
        
        cont_id = cont.id
        
    with app.app_context():
        return db.session.get(Content, cont_id)

def get_auth_header(client, email, password):
    """Helper function to get authentication header"""
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    data = response.get_json()
    token = data.get('access_token')
    return {'Authorization': f'Bearer {token}'}