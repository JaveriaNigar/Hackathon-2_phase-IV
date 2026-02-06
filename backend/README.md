# Todo Backend API

Backend API for the Phase II Todo Full-Stack Web Application with JWT authentication and PostgreSQL database.

## Features

- JWT-based authentication using Better Auth
- Full CRUD operations for tasks
- User isolation - users can only access their own tasks
- RESTful API endpoints
- PostgreSQL database with Neon

## Prerequisites

- Python 3.11+
- PostgreSQL database (or access to Neon PostgreSQL)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # Or if using Poetry: poetry install
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/taskdb
   BETTER_AUTH_SECRET=your-better-auth-secret
   BETTER_AUTH_URL=http://localhost:3000
   ```

5. Run database migrations (when available)

6. Start the development server:
   ```bash
   uvicorn src.main:app --reload --port 8001
   ```

## API Usage

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

For detailed API documentation, visit `/docs` when the server is running.