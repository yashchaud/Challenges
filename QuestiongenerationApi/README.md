# Question Generation API

Basic Flask API with user authentication. Uses MySQL for data storage.

## Setup

1. Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install and start MySQL server, then update .env file with your database credentials:

```
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=question_api
```

5. Run the app:

```bash
python run.py
```

The app will create the users table automatically on first run.

## API Endpoints

### POST /auth/register

Register a new user.

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### POST /auth/login

Login and get JWT token.

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### GET /auth/me

Get current user info (requires Authorization header).

```
Authorization: Bearer your_jwt_token_here
```

## Project Structure

The app uses a standard Flask structure with separate folders for different components:

- `backend/` - main application code
- `backend/models/` - database models (user.py)
- `backend/routes/` - API endpoints (auth.py)
- `backend/middleware/` - authentication middleware
- `backend/utils/` - helper functions and database connection
- `config.py` - app configuration
- `run.py` - entry point
- `.env` - environment variables

App runs on http://127.0.0.1:5000 by default.
