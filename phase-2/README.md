# Todo App - Phase II

A multi-user, full-stack Todo web application with authentication and secure API.

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python), SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT-based with custom middleware
- **Project Structure**: Monorepo with /frontend and /backend directories

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- PostgreSQL or Neon Database account

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

   Update the `.env` file with your database URL and secret keys.

6. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   ```

   Update the `.env.local` file with your backend API URL.

4. Run the frontend server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout

### Task Management
- `GET    /api/users/{user_id}/tasks`                     - List user's tasks
- `POST   /api/users/{user_id}/tasks`                     - Create new task
- `GET    /api/users/{user_id}/tasks/{id}`               - Get specific task
- `PUT    /api/users/{user_id}/tasks/{id}`               - Update task
- `DELETE /api/users/{user_id}/tasks/{id}`               - Delete task
- `PATCH  /api/users/{user_id}/tasks/{id}/complete`      - Toggle completion

### Health Check
- `GET /health` - Health check endpoint

## Security Features

- JWT-based authentication for all API endpoints
- User data isolation - users can only access their own tasks
- Input validation using Pydantic schemas
- Password hashing using bcrypt
- SQL injection prevention using parameterized queries
- Rate limiting on authentication endpoints

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API route definitions
│   │   ├── models/         # SQLModel data models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── database/       # Database configuration
│   │   ├── middleware/     # Authentication and security middleware
│   │   └── services/       # Business logic services
│   ├── main.py             # Application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/                # App Router pages
│   ├── components/         # Reusable UI components
│   ├── lib/                # Utilities and API client
│   ├── types/              # TypeScript type definitions
│   ├── package.json        # Dependencies
│   └── tailwind.config.js  # Tailwind CSS configuration
├── specs/                  # Project specifications
│   └── todo-app/
│       ├── spec.md         # Functional specifications
│       ├── plan.md         # Architecture plan
│       └── tasks.md        # Task breakdown
└── README.md               # This file
```

## Environment Variables

Create `.env` files in both backend and frontend directories:

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running Tests

Coming soon - test setup and execution instructions.

## Deployment

Coming soon - deployment instructions for different environments.