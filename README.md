# Social Media App

A full-stack social media application built with Django REST Framework (backend) and Vue.js (frontend).

## Features

- User authentication (login/register)
- Create, view, and delete posts
- Image upload and display
- Like and unlike posts
- Comment on posts
- Follow/unfollow users
- Search users
- Responsive design
- User profiles with avatar upload

## Tech Stack

### Backend
- **Django** - Web framework
- **Django REST Framework** - API development
- **Django CORS Headers** - Cross-origin resource sharing
- **Pillow** - Image processing
- **SQLite** - Database 

### Frontend
- **Vue.js 3** - Frontend framework
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Heroicons** - Icon library

## Project Structure

```
project-root/
├── backend/                 # Django backend
│   ├── manage.py
│   ├── home/               # Main Django project
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── app/                # Main Django app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   └── media/              # User uploads (ignored in git)
└── frontend/               # Vue.js frontend
    ├── src/
    │   ├── components/
    │   ├── views/
    │   ├── stores/
    │   ├── services/
    │   └── router/
    ├── public/
    ├── package.json
    └── vue.config.js
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup (Django)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/social-media-app.git
   cd social-media-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install django djangorestframework django-cors-headers pillow python-decouple
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Django server**
   ```bash
   python manage.py runserver
   ```

Backend will be available at `http://localhost:8000`

### Frontend Setup (Vue.js)

1. **Navigate to frontend directory**
   ```bash
   cd frontend  # or wherever your Vue.js project is located
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm run serve
   # or
   yarn serve
   ```

Frontend will be available at `http://localhost:8080`

## Environment Variables

Create a `.env` file in your Django project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## API Endpoints

### Authentication
- `POST /app/auth/login/` - User login
- `POST /app/auth/register/` - User registration
- `POST /app/auth/refresh/` - Refresh token

### Posts
- `GET /app/posts/` - Get feed posts
- `POST /app/posts/` - Create new post
- `GET /app/posts/{id}/` - Get specific post
- `POST /app/posts/{id}/like/` - Like/unlike post
- `POST /app/posts/{id}/comment/` - Add comment

### Profile
- `GET /app/profile/` - Get own profile
- `PUT /app/profile/` - Update own profile
- `GET /app/profile/{username}/` - Get user profile
- `POST /app/profile/{username}/follow/` - Follow/unfollow user

### Other
- `GET /app/search/` - Search users
- `GET /app/explore/` - Get explore posts

## Features in Detail

### User Authentication
- JWT-based authentication
- Automatic token refresh
- Protected routes

### Posts
- Create posts with images and captions
- View posts in a feed format
- Like and comment functionality
- Image upload and display

### User Profiles
- View user profiles with posts grid
- Follow/unfollow functionality
- Profile picture upload
- User statistics (posts, followers, following)

### Search & Discovery
- Search users by username
- Explore popular posts
- Responsive design for mobile and desktop
