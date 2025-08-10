# API Endpoints

## 1. Fitness Classes

### a. List Available Fitness Classes

-   **URL**: `/api/classes/`
-   **Method**: `GET`
-   **Description**: Retrieves a list of all upcoming fitness classes. By default, the API returns the date and time in Indian Standard Time (IST). However, you can specify a timezone in the query parameters to get the `date_time` in that timezone.
-   **Authentication**: Not Required
-   **Query Parameters (Optional)**:
    -   `timezone`: (e.g., `America/New_York`). Defaults to `Asia/Kolkata` if not provided or invalid.
-   **Success Response (200 OK)**:


#### Example 1: Default Timezone (Asia/Kolkata)
This example shows a request without a specific timezone query parameter. The response defaults to Indian Standard Time (IST).
-   **Request**: `/api/classes/`

    ```json
    [
    {
        "id": 1,
        "name": "cricket",
        "date_time": "2025-08-11T11:30:00+05:30",
        "instructor": "dhoni",
        "total_slots": 15,
        "available_slots": 5
    },
    {
        "id": 2,
        "name": "Badminton",
        "date_time": "2025-08-11T17:30:00+05:30",
        "instructor": "Lin dan",
        "total_slots": 10,
        "available_slots": 2
    }
    ]
    ```

#### Example 2: Specific Timezone (America/New_York)
This example shows how to request class times formatted for the America/New_York timezone using the timezone query parameter.
-   **Request**: `/api/classes?timezone=America/New_York`

    ```json
    [
    {
        "id": 1,
        "name": "cricket",
        "date_time": "2025-08-11T02:00:00-04:00",
        "instructor": "dhoni",
        "total_slots": 15,
        "available_slots": 5
    },
    {
        "id": 2,
        "name": "Badminton",
        "date_time": "2025-08-11T08:00:00-04:00",
        "instructor": "Lin dan",
        "total_slots": 10,
        "available_slots": 2
    }
    ]
    ```




## 2. Bookings

### a. Book a Fitness Class

-   **URL**: `/api/book/`
-   **Method**: `POST`
-   **Description**: Books a slot in a specified fitness class. Decrements `available_slots` for the class.
-   **Authentication**: Not Required
-   **Request Body (JSON)**:
    ```json
    {
        "class_id": 5,
        "client_name": "rohit",
        "client_email": "rohit@mail.com"
    }
    ```
-   **Success Response (201 Created)**:
    ```json
    {
    "class_id": 5,
    "client_name": "rohit",
    "client_email": "rohit@mail.com"
    }
    ```
-   **Error Responses**:
    -   `400 Bad Request`: If no available slots.
        ```json
        {
            "detail": "No available slots for this class."
        }
        ```
    -   `400 Bad Request`: If the client has already booked the class.
        ```json
        {
            "non_field_errors": [
                "You have already booked this class."
            ]
        }
        ```
    -   `400 Bad Request`:The Classes that are no longer available due to the time having expired.
        ```json
        {
        "detail": "This class has already expired and cannot be booked."
        }   
        ```

### b. List User Bookings

-   **URL**: `/api/bookings?client_email=rohit@mail.com`
-   **Method**: `GET`
-   **Description**: Retrieves a list of bookings for a specific client email.
-   **Authentication**: Not Required
-   **Query Parameters (Required)**:
    -   `client_email`: The email of the client whose bookings are to be retrieved. (e.g., `rohit@mail.com`)
-   **Success Response (200 OK)**:
    ```json
    [
    {
        "id": 37,
        "fitness_class": {
        "id": 9,
        "name": "Football",
        "date_time": "2025-08-14T11:30:00+05:30",
        "instructor": "Messi",
        "total_slots": 10,
        "available_slots": 1
        },
        "client_name": "rohit",
        "client_email": "rohit@mail.com",
        "booking_time": "2025-08-08T09:46:28.957000Z",
        "date_time": "2025-08-08T15:16:28.957000+05:30"
    },
    {
        "id": 34,
        "fitness_class": {
        "id": 8,
        "name": "Boxing Cardio",
        "date_time": "2025-08-13T17:30:00+05:30",
        "instructor": "M Ali",
        "total_slots": 50,
        "available_slots": 5
        },
        "client_name": "rohit",
        "client_email": "rohit@mail.com",
        "booking_time": "2025-08-08T09:45:36.663000Z",
        "date_time": "2025-08-08T15:15:36.663000+05:30"
    },
    {
        "id": 33,
        "fitness_class": {
        "id": 5,
        "name": "cricket",
        "date_time": "2025-08-11T11:30:00+05:30",
        "instructor": "dhoni",
        "total_slots": 15,
        "available_slots": 5
        },
        "client_name": "rohit",
        "client_email": "rohit@mail.com",
        "booking_time": "2025-08-08T08:30:56.576000Z",
        "date_time": "2025-08-08T14:00:56.576000+05:30"
    }
    ]
    ```