# Blog API
## Overview

Blog API is a Django-based application designed for managing blog posts and comments. It features user authentication, blog post management, and commenting functionality. The project utilizes Django REST Framework for API development and JWT for authentication.

## Features

- **User Authentication**: Secure sign-up, log-in, and log-out functionality using JWT token and session management.
- **Blog Posts**: Create, view, update, and delete blog posts.
- **Comments**: Add and delete comments on blog posts. Comments are restricted to the author or blog owner.
- **Pagination**: Custom pagination for blog posts with a page size of 3.
- **Frontend Integration**: Basic frontend using Django templates with Bootstrap for styling.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Shreyyyash/BlogAPI.git

2. **Project Directory**:
   ```bash
    cd BlogAPI 
3. **Virtual Environemnt**:
    ```bash
    python -m venv myenv
4. **Activate the Virtual Environment:**
    ```bash
    myenv\Scripts\activate
5. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

6. **Apply Migrations and Migrate**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
7. **Create Super User**
    ```bash
    python manage.py createuperuser
8. **Run the Server**
   ```bash
   python manage.py runserver

## API Documentation
  **The API endpoints are documented with Swagger using DRF-Spectacular. You can view the documentation at**    
       ```http://127.0.0.1:8000/api/schema/ ```
       ```http://127.0.0.1:8000/api/swagger-docs/ ```
       ```http://127.0.0.1:8000/api/redoc/ ```

## Acknowledgements
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design. [Django](https://www.djangoproject.com/)
- **Django REST Framework**: A powerful and flexible toolkit for building Web APIs in Django. [Django REST Framework](https://www.django-rest-framework.org/)
- **DRF-Spectacular**: A tool for generating OpenAPI 3 schemas for Django REST Framework. [DRF-Spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- **Bootstrap**: A popular front-end framework for developing responsive and mobile-first websites. [Bootstrap](https://getbootstrap.com/)
- **GitHub**: A platform for version control and collaboration. [GitHub](https://github.com/)
  
