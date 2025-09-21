# Question Generation API

Flask API with user auth and question generation using Google FLAN-T5.

## Setup

1. Create venv and activate:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install packages:

```bash
pip install -r requirements.txt
```

3. Setup MySQL and create .env file:

```
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=question_api
```

4. Run:

```bash
python run.py
```

## Endpoints

**Auth:**

- `POST /auth/register` - signup
- `POST /auth/login` - get token
- `GET /auth/me` - user info (needs Bearer token)

**Questions:**

- `GET /generate-question?text=your_text` - get ~3 questions

Example:

```
GET /generate-question?text=Machine learning helps computers learn from data
```

Returns:

```json
{
  "questions": [
    "What is machine learning?",
    "How do computers learn?",
    "What is used for learning?"
  ],
  "count": 3
}
```
