# Omnify Fitness Class Booking System

## Overview

Omnify is a Django-based web application designed to manage fitness classes and allow users to book them. It provides a robust backend API for user authentication, class listing, and booking management.

## Features

-   **User Authentication**: Secure registration and login using JWT (JSON Web Tokens).
-   **Fitness Class Management**: Admins can create, update, and delete fitness classes with details like name, date/time, instructor, and available slots.
-   **Class Listing**: Users can view a list of upcoming fitness classes.
-   **Booking System**: Users can book available slots in fitness classes. The system prevents overbooking and duplicate bookings by the same client for the same class.
-   **Booking History**: Users can view their past and upcoming bookings.
-   **Admin Interface**: A comprehensive Django Admin panel for managing users, fitness classes, and bookings.

## Technologies Used

-   **Backend**: Django 5.2.5
-   **API**: Django REST Framework
-   **Authentication**: Django REST Framework Simple JWT
-   **Database**: SQLite3 (default, configurable)
-   **Language**: Python 3.x

## Setup Instructions

Follow these steps to get the Omnify application up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Rohit10jr/getomnify.git
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

-   **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
-   **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 4. Install Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

Apply the database migrations to create the necessary tables:

```bash
python manage.py migrate
```

### 6. Load initial data:

To populate the database with sample fitness classes and bookings for testing, run the following command. This will provide you with pre-existing data to interact with the API endpoints.

```bash
python manage.py loaddata initial_data.json
```

### 7. Create a Superuser (Admin Account)

To access the Django admin panel, you'll need to create a superuser:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin username (email), email address, and password.

## Running the Application

Once the setup is complete, you can start the Django development server:

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

## Running Tests

The project includes basic unit tests to ensure the core functionality works as expected. You can run all tests from the root directory with the following command:


```bash
python manage.py test
```
To run tests for a specific app , you can specify the app name.

```bash
python manage.py test app
```

## API Endpoints
For a detailed breakdown of all available API endpoints, their request formats, and example responses, please see the API Reference. The API endpoints are prefixed with `/api/`.

## API Endpoints
For a detailed breakdown of all available API endpoints, their request formats, and example responses, please see the **[API Reference](API_REFERENCE.md)**. The API endpoints are prefixed with `/api/`.

## Admin Panel

Access the Django administration interface at `http://127.0.0.1:8000/admin/`.

Use the superuser credentials you created earlier to log in. From here, you can:

-   Manage `CustomUser` accounts.
-   Add, modify, or delete `FitnessClass` entries.
-   View and manage `Booking` records.