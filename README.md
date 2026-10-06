# Hestia

Hestia is a room reservation system built with Django and PostgreSQL.

The project is designed as a simple but structured backend application, focusing on Django fundamentals, clean organization, repository pattern, custom authentication, permissions, and relational data modeling.

## Tech Stack

* Python 3.14
* Django 6.1.2
* PostgreSQL 18
* Docker
* `psycopg`
* `python-dotenv`

## Project Structure

```text
hestia/
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── src/
│   ├── categories/
│   ├── permissions/
│   ├── permissionsUser/
│   ├── reservations/
│   ├── room_types/
│   ├── rooms/
│   ├── shared/
│   └── users/
│
├── .env
├── .gitignore
├── docker-compose.yml
├── manage.py
└── README.md
```

### Configuration

The `config` package contains the global Django configuration.

It is responsible for:

* Django settings
* URL configuration
* WSGI
* ASGI

### Applications

The `src` directory contains the application's domain modules.

| Application       | Responsibility                     |
| ----------------- | ---------------------------------- |
| `users`           | User management and authentication |
| `permissions`     | Application permissions            |
| `permissionsUser` | User-permission relationships      |
| `categories`      | Room categories                    |
| `room_types`      | Room type management               |
| `rooms`           | Room management                    |
| `reservations`    | Room reservations                  |
| `shared`          | Shared models and infrastructure   |

## Domain Model

The main entities are:

```text
User
 │
 ├──< PermissionUser >── Permission
 │
 └──< Reservation >── Room
                       │
                       ├── RoomType
                       └── Category
```

### User

Users can authenticate using their email address and have permissions assigned through the `PermissionUser` relationship.

### Permission

Permissions represent specific application capabilities.

Examples:

```text
user.list
user.read
user.create
user.update
user.delete
```

### Room

A room belongs to:

* one category
* one room type

A room can have multiple reservations.

### Reservation

A reservation belongs to:

* one user
* one room

Reservations contain a start time, end time, and status.

Supported statuses:

```text
scheduled
cancelled
completed
```

The system must prevent overlapping reservations for the same room.

## Repository Pattern

Hestia uses a repository layer to isolate data access from the rest of the application.

The generic repository provides common operations:

```python
get_by_id()
get_all()
filter()
create()
update()
delete()
delete_all()
exists_by_id()
```

Entity-specific repositories extend the base repository when additional queries are required.

Example:

```python
class ReservationRepository(BaseRepository[Reservation]):
    def __init__(self) -> None:
        super().__init__(Reservation)
```

This allows generic persistence operations to remain centralized while keeping domain-specific queries inside their respective repositories.

## Base Model

Common model fields are centralized in a shared abstract model.

The base model provides:

```text
id
version
created_at
updated_at
```

Entity identifiers use UUIDs.

This avoids duplicating common persistence fields across every model.

## Authentication

Hestia uses Django's custom user model.

The user model:

* uses email as the username field
* stores passwords using Django's password hashing
* supports staff users
* supports superusers
* integrates with the application's custom permission system

The configured user model is:

```python
AUTH_USER_MODEL = "users.User"
```

## Permissions

Hestia uses a custom permission system instead of Django's default group-based permission model.

Users can have multiple permissions:

```text
User N:N Permission
```

through:

```text
permission_user
```

Superusers bypass permission checks.

Regular users are authorized through permission slugs.

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd hestia
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install the main dependencies manually:

```bash
pip install django psycopg[binary] python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=hestia
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Never commit the `.env` file to version control.

### 5. Start PostgreSQL

The project provides PostgreSQL through Docker:

```bash
docker compose up -d
```

Check the container:

```bash
docker compose ps
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## Useful Commands

Run Django checks:

```bash
python manage.py check
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Start PostgreSQL:

```bash
docker compose up -d
```

Stop PostgreSQL:

```bash
docker compose down
```

View PostgreSQL logs:

```bash
docker compose logs -f postgres
```

## Development Principles

The project follows a few core principles:

* Keep Django applications organized by domain.
* Keep shared infrastructure in `src/shared`.
* Use repositories for data-access operations.
* Reuse common model fields through an abstract base model.
* Use UUIDs as entity identifiers.
* Keep configuration outside the source code through environment variables.
* Prefer explicit and strongly typed Python code.
* Keep the architecture simple and avoid unnecessary abstractions.

## License

This project is intended for educational and portfolio purposes.
