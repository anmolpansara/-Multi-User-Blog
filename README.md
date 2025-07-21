# Multi-User Blog Backend

A scalable Django REST API backend for a multi-user blog platform with role-based access control, JWT authentication, and comprehensive blog management features.

## Features

- **Role-based Access Control**: Admin, Editor, and Reader roles with different permissions
- **JWT Authentication**: Secure token-based authentication
- **Blog Management**: Create, read, update, delete posts with categories and tags
- **Content Filtering**: Filter posts by category, tags, status, and author
- **Search Functionality**: Full-text search across post titles and content
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **RESTful Architecture**: Clean and intuitive API endpoints

## Tech Stack

- **Django 4.2+**: Web framework
- **Django REST Framework**: API framework
- **JWT Authentication**: Token-based authentication
- **PostgreSQL**: Database (configurable)
- **Swagger/OpenAPI**: API documentation
- **Django Filters**: Advanced filtering capabilities

## User Roles

### Admin
- Full CRUD access to all posts, categories, and tags
- Can manage all user content
- Access to all post statuses (draft, published, archived)

### Editor
- Can create, edit, and delete their own posts
- Can view all published posts
- Can access categories and tags

### Reader
- Can view published posts only
- Read-only access to categories and tags
- Can register and manage their profile

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- PostgreSQL (optional, SQLite used by default)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Multi_User_Blog_Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample categories and tags**
   ```bash
   python manage.py populate_categories_tags
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - API Base URL: `http://localhost:8000/api/`
   - Swagger Documentation: `http://localhost:8000/swagger/`
   - ReDoc Documentation: `http://localhost:8000/redoc/`
   - Django Admin: `http://localhost:8000/admin/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/refresh/` - Refresh JWT token

### User Profile
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/` - Update user profile
- `GET /api/my-posts/` - Get current user's posts

### Posts
- `GET /api/posts/` - List posts (with filtering and search)
- `POST /api/posts/` - Create new post (Admin/Editor only)
- `GET /api/posts/{id}/` - Get specific post
- `PUT /api/posts/{id}/` - Update post (Owner/Admin only)
- `DELETE /api/posts/{id}/` - Delete post (Owner/Admin only)

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category (Admin only)
- `GET /api/categories/{id}/` - Get specific category
- `PUT /api/categories/{id}/` - Update category (Admin only)
- `DELETE /api/categories/{id}/` - Delete category (Admin only)

### Tags
- `GET /api/tags/` - List tags
- `POST /api/tags/` - Create tag (Admin only)
- `GET /api/tags/{id}/` - Get specific tag
- `PUT /api/tags/{id}/` - Update tag (Admin only)
- `DELETE /api/tags/{id}/` - Delete tag (Admin only)

## API Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "strongpassword123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "editor"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "strongpassword123"
  }'
```

### 3. Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my blog post...",
    "category": 1,
    "tag_ids": [1, 2, 3],
    "status": "published"
  }'
```

### 4. Filter Posts
```bash
# Filter by category
curl "http://localhost:8000/api/posts/?category=1"

# Search posts
curl "http://localhost:8000/api/posts/?search=django"

# Filter by multiple criteria
curl "http://localhost:8000/api/posts/?category=1&status=published&ordering=-created_at"
```

## Database Schema

### UserProfile
- user (OneToOne with Django User)
- role (admin/editor/reader)
- bio
- created_at

### Post
- title
- content
- author (ForeignKey to User)
- category (ForeignKey to Category)
- tags (ManyToMany with Tag)
- status (draft/published/archived)
- created_at, updated_at, published_at

### Category
- name (unique)
- description
- created_at

### Tag
- name (unique)
- created_at

## Development

### Running Tests
```bash
python manage.py test
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### Management Commands

#### Populate Sample Data
```bash
# Add sample categories and tags
python manage.py populate_categories_tags

# Clear existing data and add fresh samples
python manage.py populate_categories_tags --clear
```