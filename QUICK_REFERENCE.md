# Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Complete setup in one command
make init-project

# Or manually:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
flask db upgrade
python seed_data.py
python run.py
```

## 📝 Common Development Commands

### Using Makefile

```bash
make help              # Show all available commands
make install           # Install dependencies
make setup            # Setup environment
make run              # Run development server
make test             # Run tests
make test-cov         # Run tests with coverage
make db-upgrade       # Apply migrations
make db-seed          # Seed database
make clean            # Clean generated files
make lint             # Check code quality
make format           # Format code
```

### Manual Commands

```bash
# Run application
python run.py

# Run tests
pytest
pytest -v                    # Verbose
pytest tests/test_auth.py   # Specific file
pytest --cov=app            # With coverage

# Database
flask db migrate -m "message"  # Create migration
flask db upgrade               # Apply migrations
flask db downgrade            # Rollback
python seed_data.py           # Seed data

# Flask shell
flask shell
>>> from app.models import *
>>> User.query.all()
```

## 🔐 Test Accounts (After Seeding)

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@moringa.com | Admin@123 |
| Tech Writer | writer1@moringa.com | Writer@123 |
| User | john@example.com | User@123 |

## 📡 API Endpoints Quick Reference

### Authentication
```bash
POST   /api/auth/register       # Register
POST   /api/auth/login          # Login
GET    /api/auth/profile        # Get profile (auth)
PUT    /api/auth/profile        # Update profile (auth)
```

### Admin
```bash
POST   /api/admin/users              # Create user
GET    /api/admin/users              # List users
PUT    /api/admin/users/:id/deactivate  # Deactivate user
POST   /api/admin/categories         # Create category
GET    /api/admin/content/pending    # Pending content
PUT    /api/admin/content/:id/approve  # Approve content
PUT    /api/admin/content/:id/flag   # Flag content
DELETE /api/admin/content/:id        # Remove content
```

### Tech Writer
```bash
POST   /api/writer/content           # Create content
PUT    /api/writer/content/:id       # Update content
GET    /api/writer/content           # List own content
DELETE /api/writer/content/:id       # Delete content
PUT    /api/writer/content/:id/approve  # Approve content
POST   /api/writer/content/:id/review  # Review content
POST   /api/writer/categories        # Create category
```

### User
```bash
GET    /api/content                  # Browse content
GET    /api/content/:id              # Get content details
POST   /api/content                  # Submit content
POST   /api/content/:id/comments     # Comment
GET    /api/content/:id/comments     # Get comments
POST   /api/subscriptions            # Subscribe
GET    /api/subscriptions            # List subscriptions
POST   /api/wishlist                 # Add to wishlist
GET    /api/wishlist                 # Get wishlist
POST   /api/content/:id/review       # Like/dislike
GET    /api/recommendations          # Get recommendations
GET    /api/categories               # List categories
```

## 🧪 Quick Testing Examples

### Test Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"Test@123"}'
```

### Test Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@moringa.com","password":"Admin@123"}'
```

### Test with Auth
```bash
TOKEN="your-access-token"
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer $TOKEN"
```

## 🐛 Common Issues & Fixes

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
psql -U postgres -l

# Recreate database
flask db upgrade
```

### Port Already in Use
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Module Not Found
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Migration Error
```bash
# Reset migrations
rm -rf migrations
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

## 📊 Database Quick Reference

### Models Overview
- **User**: Authentication and profiles
- **Category**: Content categorization
- **Content**: Articles, videos, audio
- **Comment**: Threaded comments
- **Subscription**: Category subscriptions
- **Wishlist**: Saved content
- **ContentReview**: Likes/dislikes

### Relationships
```
User 1---* Content (author)
User 1---* Comment
User *---* Category (via Subscription)
Content 1---* Comment
Content *---1 Category
Comment *---1 Comment (parent)
```

## 🎯 Development Workflow

### Adding a New Feature

1. **Create branch**
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Write code + tests**
   ```python
   # app/routes/new_feature.py
   # tests/test_new_feature.py
   ```

3. **Test locally**
   ```bash
   pytest
   make lint
   ```

4. **Create migration (if needed)**
   ```bash
   flask db migrate -m "Add new feature"
   flask db upgrade
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/feature-name
   ```

### Adding a New Model

1. **Create model file**
   ```python
   # app/models/new_model.py
   from app import db
   
   class NewModel(db.Model):
       __tablename__ = 'new_models'
       id = db.Column(db.Integer, primary_key=True)
       # ... fields
   ```

2. **Import in models/__init__.py**
   ```python
   from app.models.new_model import NewModel
   __all__ = [..., 'NewModel']
   ```

3. **Create migration**
   ```bash
   flask db migrate -m "Add NewModel"
   flask db upgrade
   ```

4. **Write tests**
   ```python
   # tests/test_new_model.py
   def test_create_new_model():
       pass
   ```

## 🔒 Security Checklist

- [ ] Strong SECRET_KEY and JWT_SECRET_KEY
- [ ] HTTPS enabled in production
- [ ] CORS configured for frontend only
- [ ] Input validation on all endpoints
- [ ] SQL injection prevented (using ORM)
- [ ] Rate limiting implemented
- [ ] Passwords hashed with bcrypt
- [ ] JWT tokens expire (1 hour)
- [ ] Sensitive data not logged
- [ ] Dependencies updated regularly

## 📦 Docker Quick Commands

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Execute command in container
docker-compose exec app flask db upgrade

# Stop containers
docker-compose down

# Remove volumes
docker-compose down -v
```

## 🌐 Environment Variables Reference

```bash
# Required
FLASK_ENV=development|production
SECRET_KEY=<secret>
JWT_SECRET_KEY=<secret>
DATABASE_URL=postgresql://user:pass@host:5432/db

# Optional
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=email@example.com
MAIL_PASSWORD=password
CORS_ORIGINS=https://frontend.com
```

## 📈 Performance Tips

```bash
# Add database indexes
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_content_published ON content(published_at);

# Use pagination
GET /api/content?page=1&per_page=20

# Cache static data
# Use Redis for sessions/cache

# Optimize queries
# Use .join() for relationships
# Use .filter() instead of filter_by() when possible
```

## 🔍 Debugging Commands

```bash
# Python debugging
python -m pdb run.py

# Flask shell
flask shell
>>> from app import db
>>> db.engine.execute("SELECT * FROM users")

# Check routes
flask routes

# SQL logging
# In config.py: SQLALCHEMY_ECHO = True

# View logs
tail -f app.log
```

## 📞 Need Help?

1. Check documentation files
2. Search existing issues on GitHub
3. Run `make help` for commands
4. Check logs: `tail -f app.log`
5. Open new issue with details

---

**Quick Links:**
- [Setup Guide](SETUP_GUIDE.md)
- [API Docs](API_DOCUMENTATION.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Contributing](CONTRIBUTING.md)