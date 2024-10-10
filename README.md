# inventory_management

Setup Instructions

Follow these steps to set up the project:

1. Create the Project Directory:

    mkdir inventory_management_project

2. Clone the Repository:

    git clone https://github.com/rakn7032/inventory_management.git

   cd inventory_management

4. Create and Activate a Virtual Environment:
    On macOS, use the following commands:

    python -m venv venv   # Create a virtual environment
    source venv/bin/activate   # Activate the virtual environment

5. Install Dependencies:

    pip install -r requirements.txt

6. Set Up the PostgreSQL Database:

    Create a PostgreSQL database and a user with the following commands:

    CREATE DATABASE inventory_management;
    CREATE USER admin1 WITH PASSWORD 'admin@123';
    GRANT ALL PRIVILEGES ON DATABASE inventory_management TO admin1;

    Then, ensure the database settings in your settings.py file match the following:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'inventory_management',
            'USER': 'admin1',
            'PASSWORD': 'admin@123',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

7. Apply Migrations:

    python manage.py makemigrations
    python manage.py migrate

8. Run the Development Server Locally: 

    python manage.py runserver


API Documentation and Endpoints:
    For the full API documentation and details about all API endpoints, please refer to the following link:

        https://drive.google.com/file/d/1mMwXn157vub9nRNJYA6PpBeP8fxYB3ce/view?usp=drivesdk  
