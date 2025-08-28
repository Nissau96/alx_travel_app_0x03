# ALX Travel App (0x03: Background Jobs for Email Notifications)

## Project Overview
This is an enhanced version of the ALX Travel App, focusing on asynchronous background processing using Celery and RabbitMQ. The key feature is sending booking confirmation emails without blocking the UI/API response, improving performance and user experience.

### Learning Objectives
- Integrate Celery with RabbitMQ in Django.
- Configure async tasks for emails.
- Trigger tasks from DRF views.
- Test async operations.

### Tech Stack
- **Backend**: Django 4.x
- **Task Queue**: Celery 5.3.1
- **Broker**: RabbitMQ 3.12+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **API**: Django REST Framework
- **Email**: Django SMTP backend (Gmail example)

### Setup Instructions
Follow these steps to get your development environment set up.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd alx_travel_app_0x03
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```
*(Note: You should create a `requirements.txt` file by running `pip freeze > requirements.txt`)*

### 4. Set Up RabbitMQ with Docker

We use Docker to run our message broker in a container.

```bash
docker run -d -p 5672:5672 -p 15672:15672 --name my-rabbitmq rabbitmq:3-management
```
-   The broker will be available at `amqp://localhost:5672`.
-   You can access the management UI at [http://localhost:15672](http://localhost:15672) (user: `guest`, pass: `guest`).

### 5. Run Database Migrations

Apply the database schema changes.

```bash
python manage.py migrate
```

## Running the Application

To run the application, you need to start three services in separate terminal windows.

### Terminal 1: Start the Celery Worker

The worker listens for and executes background tasks.

```bash
celery -A alx_travel_app worker -l info
```

### Terminal 2: Start the Django Development Server

This runs the main web application.

```bash
python manage.py runserver
```

### Terminal 3: (Optional) Monitor RabbitMQ

Your RabbitMQ container should already be running. You can check its status with `docker ps`.

## Testing the Email Notification

1.  Ensure all three services (RabbitMQ, Celery Worker, Django Server) are running.
2.  Obtain an authentication token by logging in or registering a new user.
3.  Use an API client like Postman or `curl` to send a `POST` request to the booking endpoint: `/api/bookings/`.

**Example `curl` Request:**

```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ \
-H "Authorization: Token YOUR_AUTH_TOKEN_HERE" \
-H "Content-Type: application/json" \
-d '{
    "listing": 1, 
    "check_in_date": "2025-10-15",
    "check_out_date": "2025-10-20",
    "guests": 2
}'
```

4.  **Check the output**:
    -   You will receive an immediate `201 Created` response.
    -   The Celery worker terminal will show logs for the task being received and executed.
    -   The Django server terminal will display the content of the sent email, as it's configured to use the console email backend for development.
