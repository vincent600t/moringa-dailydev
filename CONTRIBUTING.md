# Contributing to Moringa Daily.dev Backend

Thank you for considering contributing to the Moringa Daily.dev Backend! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. We expect all participants to:

- Be respectful and inclusive
- Exercise empathy and kindness
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show courtesy and respect towards other community members

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Git
- Basic knowledge of Flask and SQLAlchemy

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/moringa-dailydev.git
   cd moringa-dailydev
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/moringa-dailydev.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install black flake8 pytest-cov  # Development tools
   ```

6. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

7. **Initialize database**
   ```bash
   flask db upgrade
   python seed_data.py
   ```

8. **Run tests**
   ```bash
   pytest
   ```

## Development Workflow

### Branch Naming Convention

- `feature/` - New features (e.g., `feature/user-notifications`)
- `bugfix/` - Bug fixes (e.g., `bugfix/login-error`)
- `hotfix/` - Urgent fixes for production (e.g., `hotfix/security-patch`)
- `refactor/` - Code refactoring (e.g., `refactor/auth-module`)
- `docs/` - Documentation updates (e.g., `docs/api-reference`)
- `test/` - Test additions/fixes (e.g., `test/user-endpoints`)

### Working on a Feature

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow coding standards
   - Add/update tests
   - Update documentation

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add user notification system"
   ```

   **Commit Message Format:**
   ```
   <type>: <subject>

   <body (optional)>

   <footer (optional)>
   ```

   **Types:**
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting, etc.)
   - `refactor`: Code refactoring
   - `test`: Adding or updating tests
   - `chore`: Maintenance tasks

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to GitHub and create a Pull Request
   - Fill out the PR template
   - Link related issues

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces
- **Quotes**: Single quotes for strings, except for docstrings (use triple double quotes)
- **Imports**: Organize imports in this order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application imports

### Code Formatting

Use `black` for code formatting:

```bash
# Format all code
black app tests --line-length=100

# Check formatting without making changes
black app tests --check --line-length=100
```

### Linting

Use `flake8` for linting:

```bash
flake8 app tests --max-line-length=100 --exclude=migrations
```

### Code Structure

```python
"""
Module docstring explaining the purpose
"""
import standard_library
import third_party

from app import db
from app.models import User

# Constants
MAX_RETRY_COUNT = 3

# Classes
class MyClass:
    """Class docstring"""
    
    def __init__(self, param):
        """Constructor docstring"""
        self.param = param
    
    def method(self):
        """Method docstring"""
        pass

# Functions
def my_function(param1, param2):
    """
    Function description
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Description of return value
    """
    pass
```

### Documentation Standards

- All modules, classes, and functions must have docstrings
- Use Google-style docstrings
- Document all parameters, return values, and exceptions
- Include usage examples for complex functions

Example:
```python
def create_user(username, email, password, role='user'):
    """
    Create a new user account
    
    Args:
        username (str): Unique username
        email (str): User's email address
        password (str): Plain text password (will be hashed)
        role (str, optional): User role. Defaults to 'user'.
    
    Returns:
        User: Created user object
    
    Raises:
        ValidationError: If input validation fails
        IntegrityError: If username/email already exists
    
    Example:
        >>> user = create_user('john', 'john@example.com', 'secret123')
        >>> print(user.username)
        'john'
    """
    pass
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Maintain/update tests when modifying existing code
- Aim for high code coverage (target: >80%)
- Use descriptive test names

```python
class TestUserAuthentication:
    """Test user authentication features"""
    
    def test_user_can_register_with_valid_data(self, client):
        """Test that user can register with valid credentials"""
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test@123'
        })
        
        assert response.status_code == 201
        assert 'access_token' in response.get_json()
    
    def test_registration_fails_with_duplicate_email(self, client, normal_user):
        """Test that registration fails when email already exists"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'user@test.com',  # Already exists
            'password': 'Test@123'
        })
        
        assert response.status_code == 409
        assert 'Email already exists' in response.get_json()['error']
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::TestUserAuthentication::test_user_can_register

# Run with coverage
pytest --cov=app --cov-report=html

# Run in watch mode
pytest --looponfail
```

### Test Structure

```
tests/
├── conftest.py              # Fixtures and configuration
├── test_auth.py             # Authentication tests
├── test_admin.py            # Admin feature tests
├── test_tech_writer.py      # Tech writer tests
├── test_user.py             # User feature tests
└── test_models.py           # Model tests
```

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests**
   ```bash
   pytest
   ```

3. **Check code quality**
   ```bash
   black app tests --check
   flake8 app tests
   ```

4. **Update documentation**
   - Update README if needed
   - Add/update API documentation
   - Include code comments

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests have been added/updated
- [ ] All tests pass
- [ ] Documentation has been updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] PR description is clear and complete

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #(issue number)

## Testing
Describe how you tested your changes

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Screenshots (if applicable)
Add screenshots for UI changes
```

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by at least one maintainer
3. **Testing** by reviewers if needed
4. **Approval** required before merge
5. **Squash and merge** into main branch

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify bug in latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.11]
- PostgreSQL Version: [e.g., 15]
- Browser (if applicable): [e.g., Chrome 120]

**Additional Context**
- Error messages
- Stack traces
- Screenshots
- Logs
```

## Suggesting Enhancements

### Enhancement Template

```markdown
**Feature Description**
Clear description of the feature

**Problem It Solves**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other solutions you considered

**Additional Context**
Mockups, examples, etc.
```

## Development Best Practices

### Security

- Never commit sensitive data (`.env` files, API keys, passwords)
- Use environment variables for configuration
- Validate and sanitize all user input
- Follow OWASP security guidelines
- Keep dependencies updated

### Performance

- Use database indexes appropriately
- Implement pagination for large datasets
- Use caching where appropriate
- Optimize database queries
- Profile performance-critical code

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description of changes"

# Review migration file
# Edit if necessary

# Apply migration
flask db upgrade

# Rollback if needed
flask db downgrade
```

### API Design

- Follow RESTful principles
- Use appropriate HTTP methods
- Return consistent response formats
- Include proper status codes
- Document all endpoints

## Getting Help

- **Documentation**: Check README and other docs first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Slack/Discord**: Join our community chat (if available)
- **Email**: Contact maintainers for sensitive issues

## Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Annual contributor acknowledgment

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Moringa Daily.dev! 🚀