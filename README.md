# WhoppahBridge

A Django-based application for managing order logistics and courier services for Whoppah.

## Features

- Secure user authentication with role-based access control
- Order management and tracking
- Courier service integration
- Real-time webhook support for updates from Whoppah CMS
- Custom admin interface with UnfoldAdmin theme
- Comprehensive API integrations
- Courier dashboard for shipment management

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository
```
git clone <repository-url>
cd whoppah-bridge
```

2. Create a virtual environment and activate it
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Create a `.env` file based on the `.env.example` template
```
cp .env.example .env
```

5. Update the `.env` file with your database credentials and other settings

6. Run migrations
```
python manage.py migrate
```

7. Create a superuser
```
python manage.py createsuperuser
```

8. Run the development server
```
python manage.py runserver
```

9. Access the application at http://127.0.0.1:8000/

## Development

### Project Structure

- `accounts` - User management and authentication
- `core` - Core functionality and base models
- `courier` - Courier service management
- `orders` - Order management
- `integration` - External API integrations

### Running Tests

```
python manage.py test
```

## Deployment

For production deployment, please follow the steps in the deployment documentation.

## License

This project is proprietary and confidential.
