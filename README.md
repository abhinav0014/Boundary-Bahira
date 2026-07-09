# Boundary Bahira

Boundary Bahira is a modern Django-based news website focused on Nepal and Associate cricket. The project combines a clean, responsive frontend with a powerful admin workflow for publishing articles, managing images, and sharing content to Facebook.

## Project Overview

This project was built to provide a polished platform for cricket news content with:

- A homepage with featured and latest news sections
- A news listing and detail experience
- Article creation, editing, and deletion workflows
- Image upload support for news posts
- An admin dashboard for content management and analytics
- Facebook sharing integration for published content

## Features

- Responsive UI with Tailwind CSS
- Django class-based views for content management
- Custom forms for news and image uploads
- Authentication and protected admin workflows
- SEO-friendly metadata and site configuration
- Media handling for uploaded news images
- Social sharing integration via Facebook Graph API

## Tech Stack

- Python
- Django 5.2
- HTML, CSS, JavaScript
- Tailwind CSS
- PostgreSQL-ready database configuration via dj-database-url
- Pillow for image handling
- Gunicorn for production deployment
- Django admin and authentication system

## Skills Used

This project demonstrates a strong mix of backend and frontend development skills, including:

- Django web development and project structure
- Model design and database relationships
- Class-based views and URL routing
- Form handling and validation
- Authentication and role-based access control
- Template rendering and UI integration
- Static and media file management
- Social API integration
- Admin dashboard customization
- Problem solving and full-stack implementation

## Project Structure

- app/ — main Django application containing models, views, forms, and URLs
- boundarybahira/ — project settings and routing
- templates/ — HTML templates for the frontend
- static/ — CSS, images, and frontend assets
- media/ — uploaded images

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/abhinav0014/Boundary-Bahira.git
   cd Boundary-Bahira
   ```

2. Create and activate a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```bash
   python manage.py migrate
   ```

5. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server
   ```bash
   python manage.py runserver
   ```

## Environment Variables

If you want Facebook sharing features enabled, configure the following environment variables:

- FACEBOOK_PAGE_ACCESS_TOKEN
- FACEBOOK_PAGE_ID
- DATABASE_URL (optional, if using a database other than the default)

## Future Improvements

Possible enhancements for this project include:

- Search functionality
- Commenting system
- Newsletter integration
- REST API for mobile or external use
- Improved analytics and reporting

## Author

Built by Abhinav as a personal full-stack web development project.
