# Moringa Daily.dev Backend - Setup Guide

## Prerequisites

Before starting, ensure you have the following installed:
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- virtualenv (recommended)

## Step 1: Clone and Setup Project Structure

Create the project directory structure:

```bash
mkdir moringa-dailydev
cd moringa-dailydev
```

Create all the necessary directories:
```bash
mkdir -p app/models app/routes app/schemas app/middleware app/utils tests migrations
```

## Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

## Step 3: Install Dependencies

Create a `requirements.txt` file with the dependencies provided in the artifacts, then install:

```bash
pip install -r requirements.txt
```

## Step 4: Setup PostgreSQL Database

1. **Install PostgreSQL** (if not already installed):
   - Ubuntu/Debian: `sudo apt-get install postgresql postgresql-contrib`
   - Mac: `brew install postgresql`
   - Windows: Download from https://www.postgresql.org/download/

2. **Create Database**:

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE moringa_dailydev;
CREATE DATABASE moringa_dailydev_test;
CREATE USER moringa_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE moringa_dailydev TO moringa_user;
GRANT ALL PRIVILEGES ON DATABASE moringa_dailydev_test TO moringa_user;
\q
```

## Step 5: Configure Environment Variables

1. Copy the `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Edit `.env` file with your actual values:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-generate-a-strong-one
JWT_SECRET_KEY=your-jwt-secret-key-here-generate-a-strong-one

DATABASE_URL=postgresql://moringa_user:your_password@localhost:5432/moringa_dailydev
TEST_DATABASE_URL=postgresql://moringa_user:your_password@localhost:5432/moringa_dailydev_test
```

**Generate strong secret keys** using Python:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Step 6: Create All Python Files

Copy all the code from the artifacts into their respective files:

### Core Files
- `config.py`
- `run.py`
- `requirements.txt`
- `.env`

### App Files
- `app/__init__.py`
- `app/models/__init__.py`
- `app/models/user.py`
- `app/models/category.py`
- `app/models/content.py`
- `app/models/comment.py`
- `app/models/subscription.py`
- `app/models/wishlist.py`
- `app/models/content_review.py`
- `app/routes/__init__.py`
- `app/routes/auth.py`
- `app/routes/admin.py`
- `app/routes/tech_writer.py`
- `app/routes/user.py`
- `app/utils/decorators.py`

### Test Files
- `tests/conftest.py`
- `tests/test_auth.py`
- `tests/test_admin.py`
- `tests/test_user.py`

## Step 7: Initialize Database

```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

## Step 8: Create Admin User

You can create an admin user in two ways:

### Option 1: Using Flask Shell

```bash
flask shell
```

```python
from app import db
from app.models import User

admin = User(
    username='admin',
    email='admin@moringa.com',
    password='Admin@123',
    role='admin'
)

db.session.add(admin)
db.session.commit()
exit()
```

### Option 2: Using Registration Endpoint

The first user registered through the API with admin role will be allowed:

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@moringa.com",
    "password": "Admin@123",
    "role": "admin"
  }'
```

## Step 9: Run the Application

```bash
python run.py
```

The application will be available at: `http://localhost:5000`

Check if it's running:
```bash
curl http://localhost:5000/health
```

You should see: `{"status":"healthy"}`

## Step 10: Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/profile` - Get profile (requires auth)
- `PUT /api/auth/profile` - Update profile (requires auth)

### Admin Endpoints
- `POST /api/admin/users` - Create user
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/:id/deactivate` - Deactivate user
- `PUT /api/admin/users/:id/activate` - Activate user
- `POST /api/admin/categories` - Create category
- `GET /api/admin/categories` - Get all categories
- `PUT /api/admin/content/:id/approve` - Approve content
- `PUT /api/admin/content/:id/flag` - Flag content
- `DELETE /api/admin/content/:id` - Remove content

### Tech Writer Endpoints
- `POST /api/writer/content` - Create content
- `PUT /api/writer/content/:id` - Update content
- `DELETE /api/writer/content/:id` - Delete content
- `GET /api/writer/content` - Get own content
- `PUT /api/writer/content/:id/approve` - Approve content
- `PUT /api/writer/content/:id/flag` - Flag content
- `POST /api/writer/content/:id/review` - Review content
- `POST /api/writer/categories` - Create category

### User Endpoints
- `GET /api/content` - Get all content
- `GET /api/content/:id` - Get single content
- `POST /api/content` - Create content (pending approval)
- `POST /api/content/:id/comments` - Create comment
- `GET /api/content/:id/comments` - Get comments
- `POST /api/subscriptions` - Subscribe to category
- `GET /api/subscriptions` - Get subscriptions
- `DELETE /api/subscriptions/:id` - Unsubscribe
- `POST /api/wishlist` - Add to wishlist
- `GET /api/wishlist` - Get wishlist
- `DELETE /api/wishlist/:id` - Remove from wishlist
- `POST /api/content/:id/review` - Like/dislike content
- `GET /api/recommendations` - Get personalized recommendations
- `GET /api/categories` - Get all categories

## Testing API with cURL

### Register a user:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test@123"
  }'
```

### Login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@123"
  }'
```

### Use the token for authenticated requests:
```bash
TOKEN="your_access_token_here"

curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer $TOKEN"
```

## Common Issues and Solutions

### Issue 1: Database Connection Error
**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if not running
sudo systemctl start postgresql
```

### Issue 2: Module Not Found Error
**Solution**: Ensure virtual environment is activated and all dependencies are installed.

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue 3: Migration Error
**Solution**: Delete migrations folder and reinitialize.

```bash
rm -rf migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Issue 4: Port Already in Use
**Solution**: Change port in `run.py` or kill the process using the port.

```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

## Production Deployment Checklist

- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure proper PostgreSQL user with limited privileges
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure CORS for your frontend domain
- [ ] Set up database backups
- [ ] Use a production WSGI server (gunicorn)
- [ ] Set up monitoring and error tracking
- [ ] Configure rate limiting
- [ ] Set up CDN for media files

## Next Steps

1. Test all endpoints using Postman or cURL
2. Create seed data for testing
3. Integrate with a frontend application
4. Set up file upload for content
5. Implement email notifications
6. Add more comprehensive logging
7. Set up CI/CD pipeline

## Support

For issues or questions, refer to:
- Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy documentation: https://docs.sqlalchemy.org/
- PostgreSQL documentation: https://www.postgresql.org/docs/