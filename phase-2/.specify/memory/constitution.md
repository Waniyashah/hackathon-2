# Todo App - Phase II Constitution
<!-- Evolution of Todo – Phase II (Full-Stack Web Application) -->

## Core Principles

### I. Spec-Driven Development
<!-- All features must originate from written specifications inside /specs. No manual coding allowed -->
Implementation must originate from written specifications in /specs directory. All code generation must come from Claude Code using Spec-Kit Plus. No manual implementation without corresponding spec documentation.

### II. Full-Stack Architecture
<!-- Separation of concerns between frontend UI, backend API, authentication, and database layers -->
Maintain clear separation between Next.js frontend and FastAPI backend. Use REST API as the communication layer. Keep business logic in appropriate layers (UI for presentation, API for business rules, DB for persistence).

### III. Test-First (NON-NEGOTIABLE)
<!-- TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->
All features require tests before implementation. Write test cases for API endpoints, UI components, and database operations. Verify authentication and authorization flows with tests. Enforce Red-Green-Refactor cycle.

### IV. Security-First Design
<!-- Focus on authentication, authorization, and data protection -->
Implement JWT-based authentication for all API endpoints. Ensure users can only access their own tasks. Validate and sanitize all inputs. Use parameterized queries to prevent SQL injection. Secure API endpoints with proper authentication middleware.

### V. Clean Architecture & Modularity
<!-- Separation of concerns, dependency inversion, maintainable code -->
Follow clean architecture principles with clear boundaries between layers. Maintain loose coupling and high cohesion. Use dependency injection where appropriate. Keep components modular and reusable.

### VI. Type Safety & Validation
<!-- Strong typing and data validation throughout the application -->
Use TypeScript for frontend with strict typing. Implement Pydantic models for API validation. Validate all data transfers between frontend and backend. Use runtime validation for all user inputs and API payloads.

## Technology Standards & Constraints
<!-- Technology stack requirements, database design, authentication -->
Frontend: Next.js 16+, TypeScript, Tailwind CSS
Backend: FastAPI (Python), SQLModel ORM
Database: Neon Serverless PostgreSQL
Authentication: Better Auth with JWT tokens
API: RESTful design with proper HTTP status codes
Project Structure: Monorepo with /frontend and /backend directories

## Development Workflow
<!-- Implementation workflow, review process, quality gates -->
Spec → Plan → Task Breakdown → Implementation via Claude Code → Test → Iterate
All changes must be traceable to specifications
Use feature branches with descriptive names
Code reviews required for all PRs
Automated testing required before merge
Follow REST conventions for API endpoints

## Governance
Specifications in /specs directory supersede all other practices. Any deviation from these principles requires explicit documentation and approval. All implementation must be justified by corresponding specification.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
