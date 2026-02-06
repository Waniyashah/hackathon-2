# Todo App - Phase II Specification

## Overview
Evolution of Todo – Phase II (Full-Stack Web Application). Build a multi-user, full-stack Todo web application that extends the Phase I console app into a persistent, authenticated system using a spec-driven, agentic development workflow.

## Primary Users
Authenticated users managing their personal todo tasks via a web interface.

## System Architecture

### Frontend Components
- Responsive web UI built with Next.js 16+ (App Router)
- User authentication using Better Auth
- Task management interface (create, view, update, delete, complete)
- API communication via JWT-secured requests

### Backend Components
- FastAPI REST service
- SQLModel ORM for database interaction
- Neon Serverless PostgreSQL for persistent storage
- JWT verification middleware
- User-scoped task filtering on every request

## Functional Requirements

### 1. Authentication System
**Requirement ID:** AUTH-001
**Description:** User authentication using Better Auth
**Acceptance Criteria:**
- [ ] Users can sign up with email and password
- [ ] Users can sign in with email and password
- [ ] JWT tokens are issued upon successful authentication
- [ ] JWT tokens are securely stored and transmitted

**Requirement ID:** AUTH-002
**Description:** JWT Token Management
**Acceptance Criteria:**
- [ ] JWT tokens are attached to all API requests
- [ ] Invalid tokens are rejected with 401 status
- [ ] Expired tokens are handled gracefully
- [ ] Tokens are verified on backend for each request

### 2. Task Management System
**Requirement ID:** TASK-001
**Description:** Create Task
**Acceptance Criteria:**
- [ ] Users can create tasks with required title field
- [ ] Description field is optional
- [ ] Created tasks are associated with authenticated user
- [ ] API returns 201 Created with task details

**Requirement ID:** TASK-002
**Description:** List Tasks
**Acceptance Criteria:**
- [ ] Users can view tasks belonging to authenticated user only
- [ ] Tasks are filtered by user_id at API level
- [ ] Pagination support (if needed)
- [ ] API returns 200 OK with tasks array

**Requirement ID:** TASK-003
**Description:** Retrieve Task Details
**Acceptance Criteria:**
- [ ] Users can retrieve specific task by ID
- [ ] Only tasks owned by user are accessible
- [ ] API returns 404 for non-existent tasks
- [ ] API returns 401 for unauthorized access attempts

**Requirement ID:** TASK-004
**Description:** Update Task
**Acceptance Criteria:**
- [ ] Users can update their tasks by ID
- [ ] Only tasks owned by user can be updated
- [ ] Partial updates are supported
- [ ] API returns 200 OK with updated task

**Requirement ID:** TASK-005
**Description:** Delete Task
**Acceptance Criteria:**
- [ ] Users can delete their tasks by ID
- [ ] Only tasks owned by user can be deleted
- [ ] API returns 204 No Content on successful deletion
- [ ] API returns 404 for non-existent tasks

**Requirement ID:** TASK-006
**Description:** Toggle Task Completion
**Acceptance Criteria:**
- [ ] Users can toggle completion status of their tasks
- [ ] Only tasks owned by user can be modified
- [ ] API returns 200 OK with updated task
- [ ] Completion status is toggled correctly

## API Specifications

### Authentication Endpoints
```
POST /api/auth/signup    - User registration
POST /api/auth/signin    - User login
POST /api/auth/signout   - User logout
```

### Task Management Endpoints
```
GET    /api/users/{user_id}/tasks                    - List user's tasks
POST   /api/users/{user_id}/tasks                    - Create new task
GET    /api/users/{user_id}/tasks/{id}              - Get specific task
PUT    /api/users/{user_id}/tasks/{id}              - Update task
DELETE /api/users/{user_id}/tasks/{id}              - Delete task
PATCH  /api/users/{user_id}/tasks/{id}/complete     - Toggle completion
```

### Request/Response Format
- All endpoints require `Authorization: Bearer <JWT>` header
- User ID in JWT token must match `user_id` in request path
- Requests accept JSON content with `Content-Type: application/json`
- Responses return JSON with appropriate HTTP status codes
- Error responses follow consistent format: `{ "error": "message" }`

## Data Model

### User Entity
```
Table: users
- id (UUID, primary key)
- email (string, unique, required)
- password_hash (string, required)
- created_at (timestamp)
- updated_at (timestamp)
```

### Task Entity
```
Table: tasks
- id (UUID, primary key)
- user_id (UUID, foreign key to users.id, required)
- title (string, required)
- description (text, optional)
- completed (boolean, default: false)
- created_at (timestamp)
- updated_at (timestamp)
```

## Security Requirements

### Authentication & Authorization
- [ ] JWT token validation on every API request
- [ ] User ID in token must match user_id in request path
- [ ] Unauthorized requests return 401 Unauthorized
- [ ] Cross-site request forgery (CSRF) protection
- [ ] Password hashing using secure algorithm

### Data Protection
- [ ] Database queries use parameterized statements to prevent SQL injection
- [ ] Input validation on all user inputs
- [ ] Sanitization of user-generated content
- [ ] User data isolation - users can only access their own data

## Persistence Requirements

### Database Schema
- [ ] Tasks stored in Neon PostgreSQL database
- [ ] Each task associated with user_id for proper scoping
- [ ] Proper indexing on user_id for efficient querying
- [ ] Foreign key constraint between tasks and users

### Data Integrity
- [ ] Referential integrity maintained between tables
- [ ] Required fields validated at database level
- [ ] Unique constraints where appropriate
- [ ] Timestamps automatically managed for created/updated times

## Technical Constraints

### Development Methodology
- [ ] Spec-driven development only - all code generated from specs
- [ ] No manual coding outside of spec generation
- [ ] Claude Code must generate all implementation
- [ ] Specs organized under /specs using Spec-Kit conventions

### Technology Stack
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: FastAPI (Python), SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Project Structure: Monorepo with clear separation

## Success Criteria

### Functional Acceptance
- [ ] Fully working authenticated todo web app
- [ ] Secure REST API with JWT verification
- [ ] Data persistence across sessions
- [ ] User isolation enforced at API and DB level
- [ ] Frontend and backend generated from specs

### Quality Assurance
- [ ] All API endpoints tested for functionality
- [ ] Authentication flow properly implemented
- [ ] Error handling implemented consistently
- [ ] Performance acceptable under load
- [ ] Security measures validated

## Out of Scope
- AI chatbot features
- Task prioritization, reminders, or filtering
- Kubernetes or cloud deployment
- Messaging or event-driven architecture

## Assumptions & Dependencies

### Assumptions
- Neon PostgreSQL database is available and properly configured
- Better Auth library provides necessary authentication functionality
- Network connectivity available for database connections
- User devices support modern browsers with JavaScript enabled

### Dependencies
- Next.js framework and related ecosystem
- FastAPI and Python ecosystem
- SQLModel and SQLAlchemy
- Better Auth library
- Neon database service