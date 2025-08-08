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

### 6. Create a Superuser (Admin Account)

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

The API endpoints are prefixed with `/api/`.

### 1. Fitness Classes

#### a. List Available Fitness Classes

-   **URL**: `/api/classes/`
-   **Method**: `GET`
-   **Description**: Retrieves a list of all upcoming fitness classes. You can specify a timezone in the query parameters to get the `date_time` in that timezone.
-   **Authentication**: Not Required
-   **Query Parameters (Optional)**:
    -   `timezone`: (e.g., `Asia/Kolkata`, `America/New_York`). Defaults to `Asia/Kolkata` if not provided or invalid.
-   **Success Response (200 OK)**:
    ```json
    [
        {
            "id": 3,
            "name": "HIIT",
            "date_time": "2025-08-08T23:30:00+05:30",
            "instructor": "vriat",
            "total_slots": 10,
            "available_slots": 9
        },
        {
            "id": 2,
            "name": "Zumba",
            "date_time": "2025-08-18T15:30:00+05:30",
            "instructor": "rashmika",
            "total_slots": 3,
            "available_slots": 0
        }
    ]
    ```

### 2. Bookings

#### a. Book a Fitness Class

-   **URL**: `/api/book/`
-   **Method**: `POST`
-   **Description**: Books a slot in a specified fitness class. Decrements `available_slots` for the class.
-   **Authentication**: Not Required
-   **Request Body (JSON)**:
    ```json
    {
        "class_id": 5,
        "client_name": "j",
        "client_email": "j@mail.com"
    }
    ```
-   **Success Response (201 Created)**:
    ```json
    {
        "class_id": 5,
        "client_name": "j",
        "client_email": "j@mail.com"
    }
    ```
-   **Error Responses**:
    -   `400 Bad Request`: If no available slots.
        ```json
        {
            "detail": "No available slots for this class."
        }
        ```
    -   `409 Conflict`: If the client has already booked the class.
        ```json
        {
            "non_field_errors": [
                "You have already booked this class."
            ]
        }
        ```

#### b. List User Bookings

-   **URL**: `/api/bookings/`
-   **Method**: `GET`
-   **Description**: Retrieves a list of bookings for a specific client email.
-   **Authentication**: Not Required
-   **Query Parameters (Required)**:
    -   `client_email`: The email of the client whose bookings are to be retrieved. (e.g., `j@mail.com`)
-   **Success Response (200 OK)**:
    ```json
    [
        {
            "id": 32,
            "fitness_class": {
                "id": 2,
                "name": "Zumba",
                "date_time": "2025-08-18T15:30:00+05:30",
                "instructor": "rashmika",
                "total_slots": 3,
                "available_slots": 0
            },
            "client_name": "j",
            "client_email": "j@mail.com",
            "booking_time": "2025-08-08T06:26:21.173594Z"
        },
        {
            "id": 25,
            "fitness_class": {
                "id": 5,
                "name": "cricket",
                "date_time": "2025-08-08T11:30:00+05:30",
                "instructor": "dhoni",
                "total_slots": 15,
                "available_slots": 4
            },
            "client_name": "j",
            "client_email": "j@mail.com",
            "booking_time": "2025-08-08T04:52:54.695258Z"
        },
        {
            "id": 24,
            "fitness_class": {
                "id": 3,
                "name": "HIIT",
                "date_time": "2025-08-08T23:30:00+05:30",
                "instructor": "vriat",
                "total_slots": 10,
                "available_slots": 9
            },
            "client_name": "j",
            "client_email": "j@mail.com",
            "booking_time": "2025-08-08T04:50:18.248894Z"
        }
    ]
    ```

## Admin Panel

Access the Django administration interface at `http://127.0.0.1:8000/admin/`.

Use the superuser credentials you created earlier to log in. From here, you can:

-   Manage `CustomUser` accounts.
-   Add, modify, or delete `FitnessClass` entries.
-   View and manage `Booking` records.