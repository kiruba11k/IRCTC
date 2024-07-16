# Railway Management System

## Introduction

This is a Railway Management System built using Django REST Framework. It allows users to manage trains, including  trains with detailed information such as arrival and departure times, sections, and seats.



## Installation

Follow the steps below to set up the project:

### 1. Clone the Repository

```bash
git clone https://github.com/kiruba11k/IRCTC.git
cd railway_management
```

### 2. Create a Virtual Environment
Create a virtual environment to isolate project dependencies.

```bash

python -m venv venv
```
Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```
On macOS/Linux:

```bash

source venv/bin/activate
```
### 3. Install Dependencies
Install the required packages using pip:

```bash

pip install -r requirements.txt
```
### 4. Configure the Database
Update the settings.py file to configure your database settings. The project uses PostgreSQL by default.

railway_management/settings.py
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
### 5. Run Migrations
Apply the database migrations to set up the database schema.

```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Create a Superuser
Create a superuser to access the Django admin interface.

```bash
python manage.py createsuperuser
```
Follow the prompts to create the superuser account.

### 7. Run the Development Server
Start the development server to run the project locally.

```bash
python manage.py runserver
```
Access the application at http://127.0.0.1:8000.

#### API Endpoints
#### 1. Register a User
 Create an endpoint for registering a user.

 Endpoint: [/api/register/](http://127.0.0.1:8000/api/register/)

Method: POST

Request Body:
```bash
{
    "username":"Peter",
    "password":"123"
}
```
response
```bash
{
    "message": "User registered successfully"
}
```
#### 2. Login User
 Provide the ability to the user to log into his account
 Endpoint: [/api/login/](http://127.0.0.1:8000/api/login/)

Method: POST

Request Body:
```bash
{
    "username":"Peter",
    "password":"123"
}
```
response
```bash
{
    "message": "Login successful",
    "token": "kv26cfcrwz6528t6llc543w4ips08xuy"
}
```
 #### 3. Add a New Train(Only by Admin)
 An endpoint for the admin to create a new train with a source and destination

Endpoint: [/api/add_train/](http://127.0.0.1:8000/api/add_train/)

Method: POST

Headers:
```bash
Key : API-KEY , Value:5h2143fqakc5tg8m0g96bjbh5717i704
```
Note: API-KEY can be generated while login as admin,copy the token id and also update manually in api_adminapikey fields.

Request Body:

```bash
{
    "name": "Kovai Intercity",
    "source": "Chennai",
    "destination": "Coimbatore",
    "total_seats": 100,
    "arrival_time": "06.20",
    "departure_time": "13.20",
    "date": "2024-07-17",
    "schedule": "DAILY",
    "sections": {
        "Sleeper": 50,
        "Upper Berth": 20,
        "Lower Berth": 20,
        "AC Coach": 10
    }
}
```
response
```bash
{"message": "Train added successfully"}
```
If added by normal user
response
```bash
Unauthorized
```
#### 4. Get Seat Availability
 Create an endpoint for the users where they can enter the source and destination and fetch all the trains between that route with their 
availabilities
 Endpoint: [/api/get_seat_availability/](http://127.0.0.1:8000/api/get_seat_availability/)

Method: GET

Request Params:
```bash
Key - source , Value - Chennai
Key - destination , Value - Coimbatore
```
response
```bash
{[
    {
        "train_id": 1,
        "train": "Kovai Intercity",
        "source": "Chennai",
        "destination": "Coimbatore",
        "total_seats": 100,
        "available_seats": 96,
        "available_seats_per_section": {
            "All": 0,
            "Sleeper": 50,
            "Upper Berth": 16,
            "Lower Berth": 20,
            "AC Coach": 10
        }
    }
]
}
```
#### 5. Book a Seat
 An endpoint for the users to book a seat on a particular train
 Endpoint: [/api/book_seat/](http://127.0.0.1:8000/api/book_seat/)

Method: POST

Request Body
```bash
{
    "train_id": 1,
    "seats": 4,
    "section": "Upper Berth"
}
```

response
```bash
{
    "message": "Seat booked successfully",
    "ticket": {
        "ticket_id": 1,
        "train_name": "Kovai Intercity",
        "train_id": 1,
        "section": "Upper Berth",
        "seat_number": 1,
        "train_arrival": "2024-07-17 06:00:00",
        "train_departure": "2024-07-17 13:00:00",
        "booking_time": "2024-07-16 16:37:33",
        "user": "Peter",
        "status": "Booked"
    }
}
```

#### 6. Get Specific Booking Details
 An endpoint for the users to book a seat on a particular train

  Endpoint: [/api/get_booking_details/](http://127.0.0.1:8000/api/get_booking_details/)

Method: GET

Request Body
```bash
{
    "train_id": "1",
    "seats_booked": 4
}
```

response
```bash
[{"ticket_id": 1, "train_name": "Kovai Intercity", "train_id": 1, "section": "Upper Berth", "seat_number": 1, "train_arrival": "2024-07-17 06:00:00", "train_departure": "2024-07-17 13:00:00", "booking_time": "2024-07-16 16:37:33", "user": "Peter", "status": "Booked"}]
```
### Contributing
If you wish to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit them (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request.
