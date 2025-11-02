# Moringa Daily.dev - Backend API

A comprehensive content platform backend for Moringa School where students can access authentic and verified information, inspiration, and advice about the tech space through videos, audio, and articles.

## 🚀 Features

### Multi-Role Authentication System
- **Admin**: Full system control
- **Tech Writers**: Content creation and moderation
- **Users**: Content consumption and interaction

### Admin Capabilities
- ✅ User management (create, deactivate, activate)
- ✅ Content moderation (approve, flag, remove)
- ✅ Category management
- ✅ System oversight

### Tech Writer Capabilities
- ✅ Create and manage content (articles, videos, audio)
- ✅ Create categories
- ✅ Approve content
- ✅ Flag inappropriate content
- ✅ Review content (like/dislike)
- ✅ Edit own content

### User Capabilities
- ✅ Browse and search content
- ✅ Create profile with interests
- ✅ Subscribe to categories
- ✅ Submit content (pending approval)
- ✅ Comment with threading (Reddit-style)
- ✅ Like/dislike content
- ✅ Wishlist functionality
- ✅ Personalized recommendations
- ✅ Share content
- ✅ Receive notifications

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🛠 Tech Stack

- **Backend Framework**: Flask 3.0
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Flask-JWT-Extended)
- **Migrations**: Flask-Migrate (Alembic)
- **Testing**: Pytest
- **Password Hashing**: Bcrypt
- **API Documentation**: Markdown

## 📦 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip
- virtualenv (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd moringa-dailydev
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

2. **Generate secret keys**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Update `.env` with your values**
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=<generated-secret-key>
   JWT_SECRET_KEY=<generated-jwt-secret>
   DATABASE_URL=postgresql://username:password@localhost:5432/moringa_dailydev
   TEST_DATABASE_URL=postgresql://username:password@localhost:5432/moringa_dailydev_test
   ```

## 🗄️ Database Setup

1. **Create PostgreSQL databases**
   ```sql
   CREATE DATABASE moringa_dailydev;
   CREATE DATABASE moringa_dailydev_test;
   CREATE USER moringa_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE moringa_dailydev TO moringa_user;
   GRANT ALL PRIVILEGES ON DATABASE moringa_dailydev_test TO moringa_user;
   ```

2. **Run migrations**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

3. **Seed database with sample data** (optional)
   ```bash
   python seed_data.py
   ```

## 🚀 Running the Application

**Development mode:**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

**Check health:**
```bash
curl http://localhost:5000/health
```

## 🧪 Testing

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=app tests/
```

**Run specific test file:**
```bash
pytest tests/test_auth.py -v
```

**Run specific test:**
```bash
pytest tests/test_auth.py::TestAuthentication::test_register_user -v
```

## 📚 API Documentation

Full API documentation is available in [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Quick Examples

**Register:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test@123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@123"
  }'
```

**Get Content (with auth):**
```bash
curl -X GET http://localhost:5000/api/content \
  -H "Authorization: Bearer <your_token>"
```

## 📁 Project Structure

```
moringa-dailydev/
├── app/
│   ├── __init__.py              # App factory with error handling
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── content.py
│   │   ├── comment.py
│   │   ├── subscription.py
│   │   ├── wishlist.py
│   │   └── content_review.py
│   ├── routes/                  # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── tech_writer.py
│   │   └── user.py
│   ├── middleware/              # Middleware components
│   │   └── logging_middleware.py
│   └── utils/                   # Utilities
│       ├── decorators.py
│       ├── validators.py
│       ├── helpers.py
│       ├── notifications.py
│       └── error_handlers.py
├── tests/                       # Test files
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_admin.py
│   └── test_user.py
├── migrations/                  # Database migrations
├── .github/                     # GitHub workflows
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── config.py                    # Configuration
├── run.py                       # Application entry point
├── seed_data.py                 # Database seeding
├── requirements.txt             # Dependencies
├── Makefile                     # Development commands
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose setup
├── nginx.conf                   # Nginx configuration
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
├── README.md                    # This file
├── SETUP_GUIDE.md              # Detailed setup guide
├── API_DOCUMENTATION.md        # Complete API reference
├── TESTING_GUIDE.md            # Testing instructions
├── DEPLOYMENT.md               # Deployment guide
├── CONTRIBUTING.md             # Contribution guidelines
└── PROJECT_SUMMARY.md          # Project overview
```

## 🔑 Test Accounts (After Seeding)

### Admin
- Email: `admin@moringa.com`
- Password: `Admin@123`

### Tech Writers
- Email: `writer1@moringa.com` / Password: `Writer@123`
- Email: `writer2@moringa.com` / Password: `Writer@123`

### Users
- Email: `john@example.com` / Password: `User@123`
- Email: `jane@example.com` / Password: `User@123`
- Email: `alex@example.com` / Password: `User@123`

## 🎯 MVP Features Checklist

### Authentication ✅
- [x] Multi-user type authentication (Admin, Tech Writer, User)
- [x] JWT-based authentication
- [x] Profile management
- [x] Role-based access control

### Admin Features ✅
- [x] Add users with specific roles
- [x] Deactivate/activate users
- [x] Create and manage categories
- [x] Approve content for publication
- [x] Flag/remove content
- [x] View all pending content

### Tech Writer Features ✅
- [x] Create profile
- [x] Create categories
- [x] Post content (articles, videos, audio)
- [x] Edit content
- [x] Approve content
- [x] Flag content
- [x] Review content (like/dislike)

### User Features ✅
- [x] Create profile with interests
- [x] Subscribe to categories
- [x] Customize interests
- [x] Submit content (pending approval)
- [x] Browse/search content
- [x] Comment with threading (Reddit-style)
- [x] View all comments and threads
- [x] Wishlist functionality
- [x] Share/recommend content
- [x] Personalized recommendations
- [x] Notification system ready
- [x] Like/dislike content

## 🐛 Known Issues & Future Enhancements

### To Be Implemented:
- [ ] Email notifications (structure in place)
- [ ] File upload for media content
- [ ] Real-time notifications (WebSockets)
- [ ] Advanced search with filters
- [ ] Content analytics dashboard
- [ ] Rate limiting
- [ ] API documentation with Swagger/OpenAPI
- [ ] Redis caching
- [ ] Content recommendation algorithm improvements
- [ ] Social sharing integration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines:
- Write tests for new features
- Follow PEP 8 style guide
- Update documentation
- Use meaningful commit messages

## 📄 License

This project is part of Moringa School curriculum.

## 👥 Authors

Developed as part of Moringa School Project

## 🙏 Acknowledgments

- Moringa School for the project requirements
- Flask documentation and community
- All contributors and testers

## 📞 Support

For issues or questions:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
3. Open an issue in the repository
4. Contact your Moringa School instructors

---

**Happy Coding! 🚀**