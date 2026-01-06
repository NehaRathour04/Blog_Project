# Django Blog Platform

A full-featured blog application built with Django and Bootstrap that enables users to create, manage, and interact with blog posts through an intuitive interface.

## Features

### User Authentication
- User registration with secure password hashing
- Login/logout functionality
- Token-based authentication
- Support for login with username or email

### Blog Management
- **Create Blogs**: Write and publish blog posts with rich content
- **Edit Blogs**: Update existing posts with full editing capabilities
- **Delete Blogs**: Remove unwanted posts
- **Image Upload**: Add up to 3 images per blog post
- **Category System**: Organize blogs by categories (Web Development, Mobile App Development, Data Science, Cybersecurity, Blockchain)

### User Features
- **Personal Dashboard**: View all your published blogs in one place
- **Profile Management**: Track and manage your content
- **Comment System**: Engage with blog posts through comments
- **Edit/Delete Comments**: Full control over your comments

### Discovery & Navigation
- **Search Functionality**: Find blogs by title, content, category, or author
- **Category Filtering**: Browse blogs by specific categories
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Real-time Previews**: Preview images before uploading

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Authentication**: Django Auth + REST Framework Token Authentication
- **Database**: Django ORM (SQLite/PostgreSQL compatible)
- **API**: Django REST Framework

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blog-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## Key Functionalities

### Blog Operations
- View individual blog posts with images and comments
- Create new posts with multiple images
- Edit existing posts (author only)
- Delete posts (author only)
- Search across titles, content, and authors
- Filter by category

### Comment System
- Add comments to blog posts
- Edit your own comments
- Delete your own comments
- View all comments on a blog post

### Image Management
- Upload up to 3 images per blog
- Preview images before submission
- Delete images when editing posts
- Automatic image handling and storage

## API Endpoints

- `GET /` - Homepage with all blogs
- `GET /blog/<id>/` - Single blog detail
- `POST /blog/<id>/comment/` - Add comment
- `GET /search/?query=<term>` - Search blogs
- `GET /filter/<category>/` - Filter by category
- `GET /user/blogs/` - User's personal blogs
- `GET/POST /blog/new/` - Create new blog
- `GET/POST /blog/<id>/edit/` - Edit blog
- `GET /blog/<id>/delete/` - Delete blog

## Security Features

- Password hashing using Django's built-in security
- CSRF protection on all forms
- Authentication required for sensitive operations
- User authorization checks (users can only edit/delete their own content)
- Token-based API authentication

## Usage

1. **Register** a new account or **login** with existing credentials
2. **Browse blogs** on the homepage
3. **Search or filter** to find specific content
4. **Create your own blog** with the "Create New Blog" button
5. **Add comments** to engage with other users' posts
6. **Manage your content** through "My Blogs" dashboard

## Future Enhancements

- Like/unlike functionality
- Blog sharing on social media
- Rich text editor for content creation
- Tags system
- User profiles with avatars
- Email notifications
- Blog drafts and scheduling

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open-source and available for educational purposes.
