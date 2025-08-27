# Alx Travel App API (0x01)

This project provides a comprehensive REST API for managing travel listings and bookings, built with Django and the Django REST Framework.

## Project Overview

The primary objective of this project is to expose CRUD (Create, Retrieve, Update, Delete) operations for `Listing` and `Booking` models through a well-structured and documented API. It uses `ModelViewSet` for rapid development and `drf-yasg` for automatic Swagger/OpenAPI documentation.

## Features

- **CRUD Operations for Listings**: Manage hotel, apartment, or other accommodation listings.
- **CRUD Operations for Bookings**: Manage user bookings for listings.
- **RESTful Endpoints**: Clean, predictable, and resource-oriented URLs.
- **API Documentation**: Automatically generated, interactive API documentation using Swagger UI.

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Django 4.x
- Django REST Framework
- `drf-yasg` for API documentation

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd alx_travel_app_0x01
    ```

2.  **Create a virtual environment and activate it:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a `requirements.txt` file using `pip freeze > requirements.txt`)*

4.  **Apply database migrations:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000`.

---

## API Endpoints and Documentation

The API endpoints are accessible under the `/api/` prefix. Interactive documentation is available through Swagger UI.

-   **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
-   **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

### Listings

| Method | Endpoint                  | Description                     |
| :----- | :------------------------ | :------------------------------ |
| `GET`  | `/api/listings/`          | Retrieve a list of all listings |
| `POST` | `/api/listings/`          | Create a new listing            |
| `GET`  | `/api/listings/{id}/`     | Retrieve a specific listing     |
| `PUT`  | `/api/listings/{id}/`     | Update a specific listing       |
| `PATCH`| `/api/listings/{id}/`     | Partially update a listing      |
| `DELETE`| `/api/listings/{id}/`     | Delete a specific listing       |

### Bookings

| Method | Endpoint                  | Description                     |
| :----- | :------------------------ | :------------------------------ |
| `GET`  | `/api/bookings/`          | Retrieve a list of all bookings |
| `POST` | `/api/bookings/`          | Create a new booking            |
| `GET`  | `/api/bookings/{id}/`     | Retrieve a specific booking     |
| `PUT`  | `/api/bookings/{id}/`     | Update a specific booking       |
| `PATCH`| `/api/bookings/{id}/`     | Partially update a booking      |
| `DELETE`| `/api/bookings/{id}/`     | Delete a specific booking       |

---

## Built With

-   [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines.
-   [Django REST Framework](https://www.django-rest-framework.org/) - A powerful and flexible toolkit for building Web APIs.
-   [drf-yasg](https://drf-yasg.readthedocs.io/) - Yet another Swagger generator.