# Project Constitution — Evolution of Todo Phase III (AI Chatbot with MCP)

## Purpose
Define architectural principles, constraints, and development standards for building a stateless AI-powered Todo chatbot using free AI services and spec-driven development methodology.

## Development Philosophy

### 1. Spec-Driven Development
- All implementation follows Agentic Dev Stack workflow: Constitution → Specify → Plan → Tasks → Implementation.
- No manual coding; all code generated through Claude Code.
- Specifications act as single source of truth.

### 2. AI Provider Strategy (Free Tier First)
- Primary AI model provider: Google Gemini API (free tier).
- Replace OpenAI Agents SDK functionality using:
  - Gemini conversational reasoning
  - Structured tool-calling via MCP tools.
- AI integration must be abstracted via service layer to allow future provider swapping.

### 3. MCP Architecture Principles
- Official MCP SDK used to expose application tools.
- MCP tools remain stateless.
- Tools persist state only through database operations.
- AI agent interacts with system exclusively through MCP tools.

### 4. Stateless Server Design
- Backend holds no runtime conversation memory.
- Conversation state persisted in database:
  - Conversation model
  - Message history
- Each request reconstructs context dynamically.

### 5. Core System Architecture

#### Frontend:
- Chat UI (ChatKit-style interface but implemented using free UI components if OpenAI ChatKit unavailable).

#### Backend:
- FastAPI server
- Gemini AI service layer
- MCP server exposing task tools
- Database persistence layer.

### 6. Database Models
- Task: user_id, id, title, description, completed, timestamps
- Conversation: user_id, id, timestamps
- Message: role, content, conversation_id, timestamps

### 7. MCP Tool Standards
Tools exposed:

- add_task
- list_tasks
- complete_task
- delete_task
- update_task

Rules:
- Tools must be deterministic.
- Tools never maintain internal state.
- All validation occurs before execution.

### 8. Agent Behavior Guidelines
Gemini AI must:

- Detect user intent from natural language.
- Select correct MCP tool based on intent.
- Chain tools if required.
- Confirm actions with friendly responses.
- Handle errors gracefully.

Intent Mapping:

- Add/create/remember → add_task
- Show/list/view → list_tasks
- Done/complete → complete_task
- Delete/remove → delete_task
- Change/update → update_task

### 9. Security Standards
- API keys stored in environment variables only.
- Never hardcode credentials.
- Validate user input before tool execution.

### 10. Technology Stack

#### Backend:
- Python 3.13+
- FastAPI
- Gemini API (free tier)
- Official MCP SDK
- UV package manager

#### Frontend:
- Chat UI (custom or free ChatKit alternative)

#### Development:
- Spec-Kit Plus
- Claude Code

### 11. Deliverables Structure

```
/frontend
/backend
/specs
/src
README.md
CLAUDE.md
```

### 12. Success Criteria

- Stateless AI chatbot managing todos via natural language.
- Gemini-powered agent invoking MCP tools correctly.
- Persistent conversation history.
- Resumable conversations after server restart.
- Fully reproducible setup.

### Constraints:

- Free AI services only.
- Spec-first development mandatory.
- No manual coding outside agentic workflow.
