# ALX Travel App 0x02 - Chapa Payment Integration

A Django-based travel booking application with integrated Chapa payment gateway for secure online payments.

## 🚀 Features

- **Secure Payment Processing**: Integration with Chapa API for Ethiopian payment methods
- **Multiple Payment Methods**: Support for Telebirr, CBE Birr, E-Birr, and international cards
- **Real-time Payment Verification**: Automatic payment status updates via webhooks
- **Email Notifications**: Automated confirmation and failure notifications
- **Background Tasks**: Celery-powered asynchronous email processing
- **Admin Dashboard**: Comprehensive payment and booking management
- **RESTful API**: Complete API endpoints for frontend integration
- **Sandbox Testing**: Full testing capabilities with Chapa's sandbox environment

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL 12+
- Redis server
- Git
- pip (Python package manager)
- Virtual environment tool

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-pip python3-dev postgresql postgresql-contrib redis-server
```

**macOS:**
```bash
brew install python postgresql redis
```

**Windows:**
- Download and install PostgreSQL from [official website](https://www.postgresql.org/download/windows/)
- Download and install Redis from [Redis website](https://redis.io/download)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Nissau96/alx_travel_app_0x02.git
cd alx_travel_app_0x02
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Database

```bash
# Create PostgreSQL database
sudo -u postgres createdb alx_travel_app_0x02

# Create database user
sudo -u postgres createuser --interactive alx_travel_user
```

### 5. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://alx_travel_user:password@localhost:5432/alx_travel_app_0x02

# Chapa API Configuration
CHAPA_SECRET_KEY=your_chapa_secret_key
CHAPA_PUBLIC_KEY=your_chapa_public_key
CHAPA_BASE_URL=https://api.chapa.co/v1
CHAPA_WEBHOOK_SECRET=your_webhook_secret

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Frontend Configuration
FRONTEND_URL=http://localhost:3000
```

### 6. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 7. Start Services

**Terminal 1: Django Development Server**
```bash
python manage.py runserver
```

**Terminal 2: Celery Worker**
```bash
celery -A alx_travel_app worker --loglevel=info
```

**Terminal 3: Redis Server** (if not running as service)
```bash
redis-server
```

## ⚙️ Configuration

### Chapa API Setup

1. **Create Chapa Account**:
   - Visit [Chapa Developer Portal](https://developer.chapa.co/)
   - Sign up and verify your account
   - Complete business verification

2. **Get API Keys**:
   - Navigate to API Keys section
   - Copy your Secret Key and Public Key
   - Generate a webhook secret

3. **Configure Webhooks**:
   - Add webhook URL: `https://yourdomain.com/api/payments/webhook/`
   - Select events: `charge.success`, `charge.failed`

### Email Configuration

For Gmail SMTP:
1. Enable 2-factor authentication
2. Generate an app password
3. Use the app password in `EMAIL_HOST_PASSWORD`

### Redis Configuration

Default Redis configuration works for development. For production:

```bash
# Edit Redis configuration
sudo nano /etc/redis/redis.conf

# Set password
requirepass your_redis_password

# Restart Redis
sudo systemctl restart redis
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
Most endpoints require JWT authentication. Include the token in headers:
```
Authorization: Bearer your-jwt-token
```

### Endpoints

#### Listings
- `GET /listings/` - Get all listings
- `POST /listings/` - Create new listing (admin only)

#### Bookings
- `GET /bookings/` - Get user bookings
- `POST /bookings/` - Create new booking

#### Payments

**Initialize Payment**
```http
POST /payments/initialize/
Content-Type: application/json
Authorization: Bearer your-token

{
  "booking_id": "uuid-of-booking",
  "payment_method": "telebirr",
  "return_url": "https://yoursite.com/success",
  "cancel_url": "https://yoursite.com/cancel"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "payment_id": "uuid-of-payment",
    "tx_ref": "TXN_booking-id_timestamp",
    "checkout_url": "https://checkout.chapa.co/checkout/payment/...",
    "amount": "1000.00",
    "currency": "ETB"
  }
}
```

**Verify Payment**
```http
GET /payments/verify/{tx_ref}/
Authorization: Bearer your-token
```

**Response:**
```json
{
  "success": true,
  "status": "success",
  "message": "Payment verified successfully",
  "data": {
    "id": "uuid-of-payment",
    "tx_ref": "TXN_booking-id_timestamp",
    "status": "success",
    "amount": "1000.00",
    "paid_at": "2024-01-15T10:30:00Z"
  }
}
```

**Get Payment Status**
```http
GET /payments/status/{payment_id}/
Authorization: Bearer your-token
```

**Get Payment History**
```http
GET /payments/history/
Authorization: Bearer your-token
```

**Get Supported Banks**
```http
GET /payments/banks/
```

#### Webhooks

**Payment Webhook**
```http
POST /payments/webhook/
Content-Type: application/json
X-Chapa-Signature: webhook-signature

{
  "event": "charge.success",
  "data": {
    "id": "chapa-transaction-id",
    "tx_ref": "your-transaction-reference",
    "status": "success",
    "amount": "1000",
    "currency": "ETB"
  }
}
```

## 🧪 Testing

### Running Tests

**All Tests:**
```bash
python manage.py test
```

**Specific App Tests:**
```bash
python manage.py test listings
```

**Specific Test Class:**
```bash
python manage.py test listings.tests.test_payment.PaymentIntegrationTestCase
```

**With Coverage:**
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

### Manual Testing

#### 1. Test Payment Flow

1. **Create a Booking:**
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "listing": "listing-uuid",
    "check_in_date": "2024-12-01",
    "check_out_date": "2024-12-05",
    "guests": 2,
    "total_amount": "4000.00"
  }'
```

2. **Initialize Payment:**
```bash
curl -X POST http://localhost:8000/api/payments/initialize/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "booking_id": "booking-uuid",
    "payment_method": "telebirr"
  }'
```

3. **Test Webhook:**
```bash
curl -X POST http://localhost:8000/api/payments/webhook/ \
  -H "Content-Type: application/json" \
  -H "X-Chapa-Signature: test-signature" \
  -d '{
    "event": "charge.success",
    "data": {
      "tx_ref": "your-tx-ref",
      "status": "success",
      "id": "chapa-id"
    }
  }'
```

#### 2. Test Email Notifications

Monitor Celery worker logs to see email tasks:
```bash
celery -A alx_travel_app worker --loglevel=debug
```

#### 3. Sandbox Testing

Use Chapa's test cards for different scenarios:

**Success Test Card:**
- Card Number: `4000000000000002`
- Expiry: Any future date
- CVV: Any 3 digits

**Failure Test Card:**
- Card Number: `4000000000000069`
- Expiry: Any future date  
- CVV: Any 3 digits

## 🔒 Security Best Practices

### Environment Variables
- Never commit `.env` files to version control
- Use different keys for development and production
- Regularly rotate API keys

### API Security
```python
# settings.py security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

### Database Security
- Use strong database passwords
- Limit database user permissions
- Enable PostgreSQL SSL connections

### Webhook Security
- Always verify webhook signatures
- Use HTTPS for webhook URLs
- Log suspicious webhook attempts

## 🚀 Deployment

### Production Environment Setup

#### 1. Server Requirements
- **OS**: Ubuntu 20.04 LTS or higher
- **Memory**: Minimum 2GB RAM
- **Storage**: Minimum 20GB SSD
- **Network**: HTTPS-enabled domain

#### 2. Production Dependencies

```bash
# Install system dependencies
sudo apt update
sudo apt install nginx postgresql redis-server supervisor

# Install Python dependencies
pip install gunicorn psycopg2-binary
```

#### 3. Environment Configuration

**Production Settings:**
```python
# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### 4. Nginx Configuration

```nginx
# /etc/nginx/sites-available/alx_travel_app
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/your/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

#### 5. Supervisor Configuration

**Gunicorn Configuration:**
```ini
# /etc/supervisor/conf.d/alx_travel_app.conf
[program:alx_travel_app]
command=/path/to/venv/bin/gunicorn alx_travel_app.wsgi:application
directory=/path/to/your/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/alx_travel_app/gunicorn.log
environment=DJANGO_SETTINGS_MODULE=alx_travel_app.settings.production
```

**Celery Worker Configuration:**
```ini
# /etc/supervisor/conf.d/celery_worker.conf
[program:celery_worker]
command=/path/to/venv/bin/celery -A alx_travel_app worker --loglevel=info
directory=/path/to/your/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/alx_travel_app/celery_worker.log
environment=DJANGO_SETTINGS_MODULE=alx_travel_app.settings.production
```

#### 6. Deployment Script

```bash
#!/bin/bash
# deploy.sh

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo supervisorctl restart alx_travel_app
sudo supervisorctl restart celery_worker
sudo systemctl reload nginx

echo "Deployment completed successfully!"
```

### Docker Deployment (Alternative)

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "alx_travel_app.wsgi:application"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/alx_travel_app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=alx_travel_app
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

  celery:
    build: .
    command: celery -A alx_travel_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/alx_travel_app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

## 📊 Monitoring and Logging

### Application Logs

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/alx_travel_app/django.log',
            'formatter': 'verbose',
        },
        'payment_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/alx_travel_app/payments.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'listings.services': {
            'handlers': ['payment_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Performance Monitoring

Install monitoring tools:
```bash
pip install django-debug-toolbar sentry-sdk
```

Add to settings:
```python
# Performance monitoring with Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Health Check Endpoint

```python
# listings/views.py
@api_view(['GET'])
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        
        # Check Redis connection
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection()
        redis_conn.ping()
        
        return Response({
            'status': 'healthy',
            'database': 'connected',
            'redis': 'connected',
            'timestamp': timezone.now()
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now()
        }, status=500)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Payment Initialization Fails
```bash
# Check Chapa API credentials
python manage.py shell
>>> from django.conf import settings
>>> print(settings.CHAPA_SECRET_KEY)

# Verify API endpoint accessibility
curl -H "Authorization: Bearer your-secret-key" https://api.chapa.co/v1/banks
```

#### 2. Email Notifications Not Working
```bash
# Check Celery worker logs
celery -A alx_travel_app worker --loglevel=debug

# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

#### 3. Webhook Signature Verification Fails
```python
# Debug webhook in views.py
import logging
logger = logging.getLogger(__name__)

def payment_webhook(request):
    logger.info(f"Webhook headers: {request.headers}")
    logger.info(f"Webhook body: {request.body}")
    # ... rest of webhook logic
```

#### 4. Redis Connection Issues
```bash
# Check Redis status
redis-cli ping

# Check Redis configuration
redis-cli config get "*"
```

### Performance Optimization

#### 1. Database Optimization
```python
# Add database indexes
class Payment(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['tx_ref']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]
```

#### 2. Caching Strategy
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Use caching in views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
@api_view(['GET'])
def supported_banks(request):
    # ... view logic
```

## 🤝 Contributing

We welcome contributions to improve the ALX Travel App! Please follow these guidelines:

### Development Workflow

1. **Fork the Repository**
```bash
git clone https://github.com/yourusername/alx_travel_app_0x02.git
cd alx_travel_app_0x02
```

2. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make Changes**
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed

4. **Test Changes**
```bash
python manage.py test
flake8 .
black .
```

5. **Commit Changes**
```bash
git add .
git commit -m "feat: add your feature description"
```

6. **Push and Create Pull Request**
```bash
git push origin feature/your-feature-name
```

### Code Standards

- **Python**: Follow PEP 8
- **Imports**: Use `isort` for import ordering
- **Formatting**: Use `black` for code formatting
- **Testing**: Maintain >90% test coverage
- **Documentation**: Update docstrings and README

### Commit Messages

Follow conventional commit format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Testing updates
- `chore:` Maintenance tasks

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Chapa API Documentation](https://developer.chapa.co/)
- [Celery Documentation](https://docs.celeryproject.org/)

### Community
- GitHub Issues: [Report bugs or request features](https://github.com/Nissau96/alx_travel_app_0x02/issues)
- Email: ibrahim.nissau96@gmail.com

### FAQ

**Q: How do I switch between sandbox and live mode?**
A: Update the `CHAPA_BASE_URL` in your `.env` file:
- Sandbox: `https://api.chapa.co/v1`
- Live: `https://api.chapa.co/v1`

**Q: Can I use other payment providers?**
A: Yes, you can extend the `PaymentService` class to support multiple providers.

**Q: How do I handle failed payments?**
A: Failed payments are automatically handled by the webhook system and email notifications are sent to users.

**Q: Is this production-ready?**
A: Yes, but ensure you:
- Use HTTPS in production
- Set up proper monitoring
- Configure backup strategies
- Implement rate limiting

## 🔄 Version History

- **v2.0.0** - Chapa payment integration
- **v1.0.0** - Initial travel booking system

---

**Made with ❤️ by Ibrahim Nissau for ALX Software Engineering Program**

For more information, visit our [GitHub repository](https://github.com/Nissau96/alx_travel_app_0x02).