# Moringa Daily.dev API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

---

## 1. Authentication Endpoints

### 1.1 Register User
Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "role": "user",
  "profile_data": {
    "bio": "Tech enthusiast",
    "interests": ["DevOps", "Frontend"]
  }
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "role": "user",
    "is_active": true,
    "profile_data": {
      "bio": "Tech enthusiast",
      "interests": ["DevOps", "Frontend"]
    },
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "email": "john@example.com"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 1.2 Login
Authenticate and receive access tokens.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "role": "user",
    "is_active": true,
    "email": "john@example.com"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 1.3 Get Profile
Get current user's profile.

**Endpoint:** `GET /auth/profile`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "profile_data": {}
  }
}
```

### 1.4 Update Profile
Update current user's profile.

**Endpoint:** `PUT /auth/profile`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "username": "john_updated",
  "profile_data": {
    "bio": "Updated bio",
    "skills": ["Python", "Flask", "React"]
  }
}
```

**Response:** `200 OK`

---

## 2. Admin Endpoints

### 2.1 Create User
Admin creates a new user with specific role.

**Endpoint:** `POST /admin/users`

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "username": "newwriter",
  "email": "writer@example.com",
  "password": "Writer123!",
  "role": "tech_writer",
  "profile_data": {}
}
```

**Response:** `201 Created`

### 2.2 Get All Users
Get list of all users with filtering.

**Endpoint:** `GET /admin/users`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20)
- `role` (optional): Filter by role (user, tech_writer, admin)
- `is_active` (optional): Filter by active status (true/false)

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`
```json
{
  "users": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "user",
      "is_active": true
    }
  ],
  "total": 50,
  "pages": 3,
  "current_page": 1
}
```

### 2.3 Deactivate User
Deactivate a user account.

**Endpoint:** `PUT /admin/users/<user_id>/deactivate`

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`

### 2.4 Activate User
Reactivate a user account.

**Endpoint:** `PUT /admin/users/<user_id>/activate`

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`

### 2.5 Create Category
Create a new content category.

**Endpoint:** `POST /admin/categories`

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "name": "DevOps",
  "description": "DevOps best practices and tools",
  "slug": "devops"
}
```

**Response:** `201 Created`

### 2.6 Get Pending Content
Get all content pending approval.

**Endpoint:** `GET /admin/content/pending`

**Query Parameters:**
- `page` (optional): Page number
- `per_page` (optional): Items per page

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`

### 2.7 Approve Content
Approve content for publication.

**Endpoint:** `PUT /admin/content/<content_id>/approve`

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`

### 2.8 Flag Content
Flag content that violates guidelines.

**Endpoint:** `PUT /admin/content/<content_id>/flag`

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "flag_reason": "Contains inappropriate content"
}
```

**Response:** `200 OK`

### 2.9 Remove Content
Permanently delete content.

**Endpoint:** `DELETE /admin/content/<content_id>`

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`

---

## 3. Tech Writer Endpoints

### 3.1 Create Content
Create new content.

**Endpoint:** `POST /writer/content`

**Headers:** `Authorization: Bearer <writer_token>`

**Request Body:**
```json
{
  "title": "Introduction to Docker",
  "content_type": "article",
  "category_id": 1,
  "description": "A beginner's guide to Docker containerization",
  "body": "Docker is a platform...",
  "content_url": "https://example.com/docker-guide",
  "thumbnail_url": "https://example.com/images/docker.jpg",
  "status": "draft"
}
```

**Content Types:** `video`, `audio`, `article`

**Status Options:** `draft`, `pending`

**Response:** `201 Created`

### 3.2 Update Content
Update existing content.

**Endpoint:** `PUT /writer/content/<content_id>`

**Headers:** `Authorization: Bearer <writer_token>`

**Request Body:** (same as create, all fields optional)

**Response:** `200 OK`

### 3.3 Delete Content
Delete own content.

**Endpoint:** `DELETE /writer/content/<content_id>`

**Headers:** `Authorization: Bearer <writer_token>`

**Response:** `200 OK`

### 3.4 Get My Content
Get all content created by the tech writer.

**Endpoint:** `GET /writer/content`

**Query Parameters:**
- `page` (optional): Page number
- `per_page` (optional): Items per page
- `status` (optional): Filter by status

**Headers:** `Authorization: Bearer <writer_token>`

**Response:** `200 OK`

### 3.5 Approve Content
Tech writers can approve content.

**Endpoint:** `PUT /writer/content/<content_id>/approve`

**Headers:** `Authorization: Bearer <writer_token>`

**Response:** `200 OK`

### 3.6 Flag Content
Flag inappropriate content.

**Endpoint:** `PUT /writer/content/<content_id>/flag`

**Headers:** `Authorization: Bearer <writer_token>`

**Request Body:**
```json
{
  "flag_reason": "Reason for flagging"
}
```

**Response:** `200 OK`

### 3.7 Review Content (Like/Dislike)
Like or dislike content.

**Endpoint:** `POST /writer/content/<content_id>/review`

**Headers:** `Authorization: Bearer <writer_token>`

**Request Body:**
```json
{
  "review_type": "like"
}
```

**Review Types:** `like`, `dislike`

**Response:** `200 OK`

### 3.8 Create Category
Tech writers can create categories.

**Endpoint:** `POST /writer/categories`

**Headers:** `Authorization: Bearer <writer_token>`

**Request Body:**
```json
{
  "name": "Frontend Development",
  "description": "All about frontend technologies"
}
```

**Response:** `201 Created`

---

## 4. User Endpoints

### 4.1 Get All Content
Browse all published content.

**Endpoint:** `GET /content`

**Query Parameters:**
- `page` (optional): Page number
- `per_page` (optional): Items per page
- `category_id` (optional): Filter by category
- `content_type` (optional): Filter by type (video, audio, article)
- `search` (optional): Search in title and description

**Response:** `200 OK`
```json
{
  "content": [
    {
      "id": 1,
      "title": "Introduction to Docker",
      "content_type": "article",
      "description": "A beginner's guide",
      "status": "approved",
      "author": {
        "id": 2,
        "username": "techwriter1"
      },
      "category": {
        "id": 1,
        "name": "DevOps",
        "slug": "devops"
      },
      "views_count": 150,
      "likes_count": 45,
      "dislikes_count": 2,
      "comments_count": 12,
      "created_at": "2024-01-15T10:00:00",
      "published_at": "2024-01-15T11:00:00"
    }
  ],
  "total": 100,
  "pages": 5,
  "current_page": 1
}
```

### 4.2 Get Content Detail
Get single content with full details.

**Endpoint:** `GET /content/<content_id>`

**Response:** `200 OK`
```json
{
  "content": {
    "id": 1,
    "title": "Introduction to Docker",
    "content_type": "article",
    "body": "Full article content...",
    "description": "A beginner's guide",
    "content_url": "https://example.com/docker",
    "thumbnail_url": "https://example.com/thumb.jpg",
    "status": "approved",
    "author": {
      "id": 2,
      "username": "techwriter1"
    },
    "category": {
      "id": 1,
      "name": "DevOps",
      "slug": "devops"
    },
    "views_count": 150,
    "likes_count": 45,
    "dislikes_count": 2,
    "comments_count": 12,
    "created_at": "2024-01-15T10:00:00",
    "published_at": "2024-01-15T11:00:00"
  }
}
```

### 4.3 Create Content
Users can submit content for approval.

**Endpoint:** `POST /content`

**Headers:** `Authorization: Bearer <token>`

**Request Body:** (same as tech writer create content)

**Response:** `201 Created` (status will be 'pending')

### 4.4 Create Comment
Comment on content.

**Endpoint:** `POST /content/<content_id>/comments`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "comment_text": "Great article!",
  "parent_comment_id": null
}
```

**Response:** `201 Created`

### 4.5 Get Comments
Get all comments for content with threading.

**Endpoint:** `GET /content/<content_id>/comments`

**Response:** `200 OK`
```json
{
  "comments": [
    {
      "id": 1,
      "comment_text": "Great article!",
      "user": {
        "id": 3,
        "username": "john"
      },
      "parent_comment_id": null,
      "created_at": "2024-01-15T12:00:00",
      "replies_count": 2,
      "replies": [
        {
          "id": 2,
          "comment_text": "Thanks!",
          "user": {
            "id": 2,
            "username": "techwriter1"
          },
          "parent_comment_id": 1,
          "created_at": "2024-01-15T12:30:00"
        }
      ]
    }
  ],
  "total": 15
}
```

### 4.6 Update Comment
Update own comment.

**Endpoint:** `PUT /comments/<comment_id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "comment_text": "Updated comment text"
}
```

**Response:** `200 OK`

### 4.7 Delete Comment
Delete own comment.

**Endpoint:** `DELETE /comments/<comment_id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

### 4.8 Subscribe to Category
Subscribe to receive updates.

**Endpoint:** `POST /subscriptions`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "category_id": 1,
  "notify_on_new_content": true
}
```

**Response:** `201 Created`

### 4.9 Get Subscriptions
Get user's subscriptions.

**Endpoint:** `GET /subscriptions`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

### 4.10 Update Subscription
Update notification preferences.

**Endpoint:** `PUT /subscriptions/<subscription_id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "notify_on_new_content": false
}
```

**Response:** `200 OK`

### 4.11 Unsubscribe
Remove subscription.

**Endpoint:** `DELETE /subscriptions/<subscription_id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

### 4.12 Add to Wishlist
Save content for later.

**Endpoint:** `POST /wishlist`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "content_id": 1
}
```

**Response:** `201 Created`

### 4.13 Get Wishlist
Get saved content.

**Endpoint:** `GET /wishlist`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

### 4.14 Remove from Wishlist
Remove content from wishlist.

**Endpoint:** `DELETE /wishlist/<wishlist_id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

### 4.15 Review Content
Like or dislike content.

**Endpoint:** `POST /content/<content_id>/review`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "review_type": "like"
}
```

**Response:** `200 OK`

### 4.16 Get Recommendations
Get personalized content recommendations.

**Endpoint:** `GET /recommendations`

**Query Parameters:**
- `limit` (optional): Number of recommendations (default: 10)

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

### 4.17 Get Categories
Get all categories.

**Endpoint:** `GET /categories`

**Response:** `200 OK`

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

### Common HTTP Status Codes

- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST request
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (duplicate)
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Currently no rate limiting is implemented. For production, implement rate limiting per user/IP.

## Pagination

Endpoints that return lists support pagination:
- Default `per_page`: 20
- Maximum `per_page`: 100

Response includes:
```json
{
  "data": [],
  "total": 150,
  "pages": 8,
  "current_page": 1
}
```