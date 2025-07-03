# Newsletter-Celery-Redis-Postgres-Dockerapp

A Django-based newsletter application enhanced with PostgreSQL, Docker, Celery, and Redis for asynchronous task processing and containerized deployment.

## Features

- User registration with email confirmation
- Double opt-in newsletter subscription
- Admin panel for creating and sending newsletters
- Asynchronous email sending using Celery
- Redis as message broker for Celery
- PostgreSQL database backend
- Containerized with Docker and Docker Compose
- Secure email confirmation and sending limits

## Technologies

- Python 3.10+
- Django 5.1+
- PostgreSQL
- Celery
- Redis
- Docker & Docker Compose
- SMTP for email sending

## Installation

1. Clone the repository:

git clone https://github.com/Domino0D/Newsletter-Celery-Redis-Postgres-Dockerapp.git
cd Newsletter-Celery-Redis-Postgres-Dockerapp


2. Build and start the Docker containers:

docker compose up --build


3. Run database migrations inside the Django container:

docker compose exec web python manage.py migrate


4. Create a superuser for admin access:

docker compose exec web python manage.py createsuperuser


5. Access the application at [http://localhost:8000](http://localhost:8000)

## Usage

- Users can register and confirm their email addresses.
- Users can subscribe to newsletters with double opt-in confirmation.
- Admins can create and send newsletters asynchronously via the admin panel.
- Email sending tasks are handled asynchronously by Celery workers using Redis as the broker.

## Configuration

- Environment variables (database credentials, Redis URL, SMTP settings, secret keys) are configured in the `.env` file.
- Docker Compose orchestrates the services: Django web app, PostgreSQL, Redis, and Celery workers.

## About `tasks.py`

The `newsapp/tasks.py` file contains Celery asynchronous tasks responsible for:

- Sending feedback emails asynchronously.
- Sending individual newsletter emails based on newsletter ID and recipient.
- Sending newsletters globally to all confirmed and active subscribers using blind carbon copy (BCC).
- Sending activation emails with confirmation links for subscription and account registration.

These tasks use Django's email utilities and Celery's `@shared_task` decorator to run in the background, improving application responsiveness.

## Contributing

Contributions are welcome! Please open issues or pull requests.

## License

MIT License
