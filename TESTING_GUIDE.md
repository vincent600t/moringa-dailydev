# Testing Guide - Moringa Daily.dev API

This guide provides step-by-step instructions for testing all API endpoints.

## Prerequisites

- Application running at `http://localhost:5000`
- Database seeded with `python seed_data.py`
- A REST client (Postman, Thunder Client, or cURL)

## Test Workflow

### 1. Health Check

Verify the API is running:

```bash
GET http://localhost:5000/health
```

Expected Response:
```json
{
  "status": "healthy"
}
```

---

## 2. Authentication Flow

### A. Register New User

```bash
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "Test@123",
  "profile_data": {
    "bio": "Test user bio",
    "interests": ["Python", "Flask"]
  }
}
```

**Save the `access_token` from the response!**

### B. Login

```bash
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "admin@moringa.com",
  "password": "Admin@123"
}
```

**Save this token for admin operations!**

### C. Get Profile

```bash
GET http://localhost:5000/api/auth/profile
Authorization: Bearer <your_token>
```

### D. Update Profile

```bash
PUT http://localhost:5000/api/auth/profile
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "username": "updated_username",
  "profile_data": {
    "bio": "Updated bio",
    "skills": ["Python", "Flask", "React"]
  }
}
```

---

## 3. Admin Operations

**Login as admin first!**
```bash
Email: admin@moringa.com
Password: Admin@123
```

### A. Create New User

```bash
POST http://localhost:5000/api/admin/users
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "username": "new_writer",
  "email": "newwriter@example.com",
  "password": "Writer@123",
  "role": "tech_writer"
}
```

### B. Get All Users

```bash
GET http://localhost:5000/api/admin/users?page=1&per_page=20
Authorization: Bearer <admin_token>
```

Filter by role:
```bash
GET http://localhost:5000/api/admin/users?role=tech_writer
Authorization: Bearer <admin_token>
```

### C. Deactivate User

```bash
PUT http://localhost:5000/api/admin/users/4/deactivate
Authorization: Bearer <admin_token>
```

### D. Create Category

```bash
POST http://localhost:5000/api/admin/categories
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Blockchain",
  "description": "Blockchain and Web3 development"
}
```

### E. Get Pending Content

```bash
GET http://localhost:5000/api/admin/content/pending
Authorization: Bearer <admin_token>
```

### F. Approve Content

```bash
PUT http://localhost:5000/api/admin/content/7/approve
Authorization: Bearer <admin_token>
```

Note: Content ID 7 should be pending (check with seed data)

### G. Flag Content

```bash
PUT http://localhost:5000/api/admin/content/1/flag
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "flag_reason": "Contains outdated information"
}
```

### H. Remove Content

```bash
DELETE http://localhost:5000/api/admin/content/1
Authorization: Bearer <admin_token>
```

---

## 4. Tech Writer Operations

**Login as tech writer:**
```bash
Email: writer1@moringa.com
Password: Writer@123
```

### A. Create Content

```bash
POST http://localhost:5000/api/writer/content
Authorization: Bearer <writer_token>
Content-Type: application/json

{
  "title": "Advanced Python Decorators",
  "content_type": "article",
  "category_id": 1,
  "description": "Deep dive into Python decorators",
  "body": "Python decorators are a powerful feature...",
  "status": "draft",
  "thumbnail_url": "https://picsum.photos/800/400"
}
```

Content types: `article`, `video`, `audio`
Status options: `draft`, `pending`

### B. Get My Content

```bash
GET http://localhost:5000/api/writer/content?page=1
Authorization: Bearer <writer_token>
```

Filter by status:
```bash
GET http://localhost:5000/api/writer/content?status=draft
Authorization: Bearer <writer_token>
```

### C. Update Content

```bash
PUT http://localhost:5000/api/writer/content/1
Authorization: Bearer <writer_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  "status": "pending"
}
```

### D. Approve Content

```bash
PUT http://localhost:5000/api/writer/content/7/approve
Authorization: Bearer <writer_token>
```

### E. Flag Content

```bash
PUT http://localhost:5000/api/writer/content/1/flag
Authorization: Bearer <writer_token>
Content-Type: application/json

{
  "flag_reason": "Needs review for accuracy"
}
```

### F. Review Content (Like/Dislike)

```bash
POST http://localhost:5000/api/writer/content/1/review
Authorization: Bearer <writer_token>
Content-Type: application/json

{
  "review_type": "like"
}
```

Review types: `like`, `dislike`

### G. Create Category

```bash
POST http://localhost:5000/api/writer/categories
Authorization: Bearer <writer_token>
Content-Type: application/json

{
  "name": "Cybersecurity",
  "description": "Security best practices"
}
```

---

## 5. User Operations

**Login as regular user:**
```bash
Email: john@example.com
Password: User@123
```

### A. Browse Content

Get all content:
```bash
GET http://localhost:5000/api/content?page=1&per_page=20
```

Filter by category:
```bash
GET http://localhost:5000/api/content?category_id=1
```

Filter by content type:
```bash
GET http://localhost:5000/api/content?content_type=article
```

Search content:
```bash
GET http://localhost:5000/api/content?search=docker
```

Combined filters:
```bash
GET http://localhost:5000/api/content?category_id=1&content_type=article&search=python
```

### B. Get Content Detail

```bash
GET http://localhost:5000/api/content/1
```

### C. Create Content (User Submission)

```bash
POST http://localhost:5000/api/content
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "title": "My Learning Journey",
  "content_type": "article",
  "category_id": 8,
  "description": "Sharing my experience learning web development",
  "body": "When I started learning web development..."
}
```

Note: User-created content will have `pending` status

### D. Create Comment

```bash
POST http://localhost:5000/api/content/1/comments
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "comment_text": "Excellent article! Very helpful."
}
```

### E. Reply to Comment

```bash
POST http://localhost:5000/api/content/1/comments
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "comment_text": "I agree! This helped me understand the concept.",
  "parent_comment_id": 1
}
```

### F. Get Comments

```bash
GET http://localhost:5000/api/content/1/comments
```

This returns threaded comments (like Reddit)

### G. Update Comment

```bash
PUT http://localhost:5000/api/comments/1
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "comment_text": "Updated comment text"
}
```

### H. Delete Comment

```bash
DELETE http://localhost:5000/api/comments/1
Authorization: Bearer <user_token>
```

### I. Subscribe to Category

```bash
POST http://localhost:5000/api/subscriptions
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "category_id": 1,
  "notify_on_new_content": true
}
```

### J. Get Subscriptions

```bash
GET http://localhost:5000/api/subscriptions
Authorization: Bearer <user_token>
```

### K. Update Subscription

```bash
PUT http://localhost:5000/api/subscriptions/1
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "notify_on_new_content": false
}
```

### L. Unsubscribe

```bash
DELETE http://localhost:5000/api/subscriptions/1
Authorization: Bearer <user_token>
```

### M. Add to Wishlist

```bash
POST http://localhost:5000/api/wishlist
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "content_id": 2
}
```

### N. Get Wishlist

```bash
GET http://localhost:5000/api/wishlist?page=1
Authorization: Bearer <user_token>
```

### O. Remove from Wishlist

```bash
DELETE http://localhost:5000/api/wishlist/1
Authorization: Bearer <user_token>
```

### P. Like/Dislike Content

Like content:
```bash
POST http://localhost:5000/api/content/1/review
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "review_type": "like"
}
```

Change to dislike:
```bash
POST http://localhost:5000/api/content/1/review
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "review_type": "dislike"
}
```

### Q. Get Recommendations

```bash
GET http://localhost:5000/api/recommendations?limit=10
Authorization: Bearer <user_token>
```

### R. Get Categories

```bash
GET http://localhost:5000/api/categories
```

---

## 6. Testing Complete User Journey

### Journey 1: New User Onboarding

1. **Register**
   ```bash
   POST /api/auth/register
   ```

2. **Subscribe to interests**
   ```bash
   POST /api/subscriptions (category_id: 1)
   POST /api/subscriptions (category_id: 2)
   ```

3. **Browse content**
   ```bash
   GET /api/content?category_id=1
   ```

4. **Read article**
   ```bash
   GET /api/content/1
   ```

5. **Like article**
   ```bash
   POST /api/content/1/review
   ```

6. **Comment**
   ```bash
   POST /api/content/1/comments
   ```

7. **Add to wishlist**
   ```bash
   POST /api/wishlist
   ```

8. **Get recommendations**
   ```bash
   GET /api/recommendations
   ```

### Journey 2: Tech Writer Workflow

1. **Login as writer**
   ```bash
   POST /api/auth/login
   ```

2. **Create draft**
   ```bash
   POST /api/writer/content (status: draft)
   ```

3. **Review and edit**
   ```bash
   PUT /api/writer/content/X
   ```

4. **Submit for approval**
   ```bash
   PUT /api/writer/content/X (status: pending)
   ```

5. **Approve own content** (or admin approves)
   ```bash
   PUT /api/writer/content/X/approve
   ```

### Journey 3: Admin Moderation

1. **Login as admin**
   ```bash
   POST /api/auth/login
   ```

2. **Review pending content**
   ```bash
   GET /api/admin/content/pending
   ```

3. **Approve good content**
   ```bash
   PUT /api/admin/content/X/approve
   ```

4. **Flag inappropriate content**
   ```bash
   PUT /api/admin/content/Y/flag
   ```

5. **Create new category**
   ```bash
   POST /api/admin/categories
   ```

---

## 7. Error Testing

### Test Invalid Authentication

```bash
GET http://localhost:5000/api/auth/profile
# No Authorization header - expect 401
```

### Test Insufficient Permissions

```bash
POST http://localhost:5000/api/admin/users
Authorization: Bearer <user_token>
# User trying admin endpoint - expect 403
```

### Test Not Found

```bash
GET http://localhost:5000/api/content/99999
# Non-existent content - expect 404
```

### Test Duplicate Registration

```bash
POST http://localhost:5000/api/auth/register
{
  "username": "admin",
  "email": "admin@moringa.com",
  "password": "Test@123"
}
# Duplicate username/email - expect 409
```

### Test Validation Errors

```bash
POST http://localhost:5000/api/auth/register
{
  "username": "test"
  # Missing email and password - expect 400
}
```

---

## 8. Performance Testing

### Test Pagination

```bash
GET http://localhost:5000/api/content?page=1&per_page=5
GET http://localhost:5000/api/content?page=2&per_page=5
```

### Test Complex Queries

```bash
GET http://localhost:5000/api/content?category_id=1&content_type=article&search=docker&page=1&per_page=10
```

---

## Common Testing Scenarios

### Scenario 1: Complete Comment Thread

1. Create parent comment
2. Create 2-3 replies to parent
3. Create reply to reply (nested)
4. Get all comments and verify threading
5. Update a comment
6. Delete a comment

### Scenario 2: Content Lifecycle

1. Tech writer creates draft
2. Tech writer edits draft
3. Tech writer submits (status: pending)
4. Admin reviews
5. Admin approves (status: approved, gets published_at)
6. Users can now see it
7. Users interact (view, like, comment)
8. Optional: Admin flags if needed

### Scenario 3: User Engagement

1. User subscribes to 3 categories
2. User browses content from subscribed categories
3. User adds 5 items to wishlist
4. User likes 3 articles
5. User comments on 2 articles
6. User gets personalized recommendations
7. User customizes interests (update profile)

---

## Tips for Testing

1. **Use Environment Variables in Postman:**
   - Set `base_url = http://localhost:5000`
   - Set `admin_token`, `writer_token`, `user_token`
   - Use `{{base_url}}{{admin_token}}` in requests

2. **Test in Order:**
   - Start with authentication
   - Then test each role separately
   - Finally test interactions between roles

3. **Save Important IDs:**
   - User IDs
   - Category IDs
   - Content IDs
   - Comment IDs
   - Use them in subsequent requests

4. **Check Database:**
   ```bash
   flask shell
   >>> from app.models import *
   >>> User.query.all()
   >>> Content.query.filter_by(status='approved').count()
   ```

5. **Monitor Logs:**
   - Check console output for errors
   - Verify SQL queries in development mode

---

## Expected Results Summary

- All authentication endpoints should return tokens
- All protected endpoints should require valid tokens
- Admin-only endpoints should reject non-admin users
- Content submissions by users should be pending
- Comments should support threading (Reddit-style)
- Subscriptions should prevent duplicates
- Wishlists should prevent duplicates
- Reviews should allow updating (change like to dislike)
- All list endpoints should support pagination
- Search should work across title and description

---

## Troubleshooting

**Issue: 401 Unauthorized**
- Check if token is included in Authorization header
- Verify token hasn't expired (default: 1 hour)
- Use refresh token endpoint if needed

**Issue: 403 Forbidden**
- Verify user has correct role
- Check if account is active

**Issue: 404 Not Found**
- Verify resource ID exists
- Check if content is approved (for non-authors)

**Issue: 409 Conflict**
- Check for duplicates (username, email, subscriptions)

**Issue: 500 Internal Server Error**
- Check application logs
- Verify database connection
- Check for validation errors

---

Happy Testing! 🧪