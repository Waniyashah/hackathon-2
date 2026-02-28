# Project Specification — Todo AI Chatbot (Phase III)

## Objective
Build a stateless AI-powered Todo chatbot that manages tasks via natural language using Gemini API instead of OpenAI, MCP server architecture, and Spec-Kit Plus workflow.

## Core Functional Requirements

### 1. Conversational Chat Interface
- User interacts via chat UI.
- Gemini model interprets user intent.
- Natural language commands trigger MCP tools.

### 2. Stateless Chat API
Endpoint:
POST /api/{user_id}/chat

Request:
- conversation_id (optional)
- message (required)

Flow:
- Fetch conversation history from database.
- Build context messages array.
- Send to Gemini API.
- Detect intent and tool usage.
- Execute MCP tools.
- Store user + assistant messages.
- Return response, conversation_id, tool_calls.

### 3. MCP Server Tools
Expose tools:

- add_task(user_id, title, description?)
- list_tasks(user_id, status?)
- complete_task(user_id, task_id)
- delete_task(user_id, task_id)
- update_task(user_id, task_id, title?, description?)

Rules:
- Tools are stateless.
- Database handles persistence.
- Return structured JSON responses.

### 4. Agent Behavior
Gemini must:

- Detect intent categories:
  add / list / complete / delete / update
- Map natural language to MCP tool calls.
- Confirm successful actions.
- Handle missing or invalid tasks gracefully.

### 5. Database Models

**Task:**
user_id, id, title, description, completed, created_at, updated_at

**Conversation:**
user_id, id, created_at, updated_at

**Message:**
user_id, id, conversation_id, role, content, created_at

### 6. Architecture

**Frontend:**
- Chat interface (ChatKit-style or free alternative).

**Backend:**
- FastAPI server
- Gemini API service layer
- MCP server
- Database persistence.

### 7. Non-Functional Requirements

- Stateless backend.
- Conversation history restored each request.
- Free-tier tools only.
- Modular AI provider abstraction.

### 8. Deliverables

- Working AI chatbot using Gemini.
- MCP tool integration.
- Natural language todo management.
- Error handling and confirmations.

## Acceptance Criteria

### Functional Acceptance
- [ ] Users can add tasks using natural language (e.g., "Add a task to buy groceries")
- [ ] Users can list tasks using natural language (e.g., "Show my tasks", "List incomplete tasks")
- [ ] Users can complete tasks using natural language (e.g., "Complete task #1", "Mark shopping as done")
- [ ] Users can delete tasks using natural language (e.g., "Delete task #2", "Remove appointment")
- [ ] Users can update tasks using natural language (e.g., "Change task #1 to walk the dog")
- [ ] AI correctly interprets varied natural language inputs
- [ ] Conversation history is properly maintained between requests
- [ ] State is persisted in database and restored correctly

### Technical Acceptance
- [ ] MCP tools are properly exposed and accessible
- [ ] Database models are correctly implemented
- [ ] API endpoints handle requests/responses appropriately
- [ ] Gemini integration works reliably
- [ ] System maintains statelessness as designed
- [ ] Error handling covers edge cases gracefully

## Constraints

- Use only free-tier AI services (Gemini API)
- Maintain statelessness - no runtime conversation memory
- All state stored in database
- Follow Spec-Kit Plus workflow
- No manual coding outside of agentic workflow

## Dependencies

- Google Gemini API (free tier)
- FastAPI
- MCP SDK
- Database system (SQLite/PostgreSQL)
- Spec-Kit Plus tools
- Claude Code for implementation