# Product Search API

A Django-based REST API for searching food products with full-text search and trigram similarity, supporting English and Arabic queries. The application uses PostgreSQL for data storage, Redis for caching, and Docker for deployment. It includes a robust search endpoint, admin interface, and pytest suite for testing.

---

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Configuration](#environment-configuration)
  - [Docker Setup](#docker-setup)
  - [Populate Test Data](#populate-test-data)
  - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
  - [Search Endpoint](#search-endpoint)
  - [Query Parameters](#query-parameters)
  - [Response Format](#response-format)
---

## Features

- **Bilingual Search**: Supports English and Arabic queries using PostgreSQL full-text search (`tsvector`, `tsquery`) and trigram similarity (`pg_trgm`) for exact matches and typo tolerance.
- **Efficient Caching**: Uses Redis to cache search results, improving performance for repeated queries.
- **Scalable Data Model**: Manages products, brands, and categories with a `JSONField` for nutrition facts and a `SearchVectorField` for full-text search.
- **Admin Interface**: Django admin for managing products, brands, and categories.
- **Comprehensive Testing**: Pytest suite covering search functionality, including full-text and trigram searches.
- **Dockerized Deployment**: Runs in a Docker Compose environment with Django, PostgreSQL, and Redis containers.
- **Debug Toolbar**: Includes `django-debug-toolbar` for debugging in development mode.

---

## Technologies

- **Backend**: Django 5.2.1, Django REST Framework 3.15.2
- **Database**: PostgreSQL 16 with `pg_trgm` and `unaccent` extensions
- **Caching**: Redis 7
- **Testing**: Pytest 8.3.2, pytest-django 4.8.0
- **Containerization**: Docker, Docker Compose
- **Dependencies**: `faker` for test data, `django-debug-toolbar` for debugging
- **Python**: 3.12.10

---

## Setup Instructions

### Prerequisites

- **Docker** and **Docker Compose**: Install from [Docker's official site](https://docs.docker.com/get-docker/).
- **Git**: For cloning the repository.
- **Python 3.12**: Optional, for running scripts outside Docker.
- **curl** or **Postman**: For testing API endpoints.

### Clone the Repository

```bash
git clone https://github.com/yaaa3ser/product-search-api.git
cd product-search-api
```

### Environment Configuration
Create a `.env` file in the root directory with the following variables:

```env
# .env
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=postgres
DEBUG=True
```

### Docker Setup
Build and start the Docker containers:

```bash
docker-compose up --build
```
This command will build the images and start the containers for Django, PostgreSQL, and Redis. The application will be accessible at `http://localhost:8000`.

### Populate Test Data
To populate the database with test data, run the following command:

```bash
docker exec product_search_django python manage.py insert_products
```

### Running the Application
The application will be available at `http://localhost:8000`. You can access the Django admin interface at `http://localhost:8000/admin` using the superuser credentials you set up during the initial migration.
To create a superuser, run:

```bash
docker exec -it product_search_django python manage.py createsuperuser
```
You will be prompted to enter a username, email, and password.

---

## API Documentation

### Search Endpoint

**GET** `/api/search/`

Searches products by name, brand, or category, supporting English and Arabic queries with full-text search and trigram similarity for typo tolerance.

### Query Parameters

| Parameter     | Type   | Description                                      | Required |
|---------------|--------|--------------------------------------------------|----------|
| `q`           | String | Search query (e.g., "milk", "حليب")              | Yes      |
| `category_id` | Integer| Filter by category ID                           | No       |
| `brand_id`    | Integer| Filter by brand ID                              | No       |

### Response Format

- **Status**: 200 OK
- **Content-Type**: application/json
- **Body**:

```json
{
  "results": [
    {
      "id": 1,
      "name": "Chocolate Milk",
      "name_ar": "حليب بالشوكولاتة",
      "brand": {
        "id": 1,
        "name": "Nestlé",
        "name_ar": "نستله"
      },
      "category": {
        "id": 1,
        "name": "Dairy",
        "name_ar": "منتجات الألبان"
      },
      "nutrition_facts": {
        "calories": 150,
        "fat": 8.0,
        "protein": 7.0,
        "carbohydrates": 20.0,
        "sugar": 15.0
      }
    }
  ]
}
```