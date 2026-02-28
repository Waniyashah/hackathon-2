# Todo AI Chatbot (Phase III)

This project implements a stateless AI-powered Todo chatbot that manages tasks via natural language. It utilizes the Google Gemini API, a FastAPI backend, and MCP server architecture, following a spec-driven development methodology.

## Features

- 🤖 **AI-Powered**: Uses Google Gemini API for natural language understanding
- 📝 **Task Management**: Add, list, complete, delete, and update tasks via chat
- 💬 **Conversational**: Natural language interface for intuitive interaction
- 🔄 **Stateless Architecture**: Conversation history persisted in database
- 🛠️ **MCP Integration**: Model Context Protocol for tool execution
- 🎨 **Modern UI**: Clean, responsive chat interface

## Project Structure

```
├── backend/                 # FastAPI backend application
│   ├── src/
│   │   ├── api/            # API routes and endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic services
│   │   ├── tools/          # MCP tool implementations
│   │   ├── database.py     # Database configuration
│   │   ├── mcp_server.py   # MCP server setup
│   │   └── main.py         # FastAPI application entry point
│   ├── alembic/            # Database migrations
│   ├── requirements.txt    # Python dependencies
│   └── pyproject.toml      # Project configuration
├── frontend/               # Chat UI
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── index.html         # Main HTML file
├── specs/                 # Project specifications
│   └── todo-chatbot/
│       ├── spec.md        # Feature specification
│       ├── plan.md        # Implementation plan
│       └── tasks.md       # Task breakdown
└── .env                   # Environment variables (create this)
```

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Git

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd phase-3
   ```

2. **Create and configure environment variables**:
   Create a `.env` file in the project root with:
   ```env
   GEMINI_API_KEY="your_gemini_api_key_here"
   DATABASE_URL="sqlite+aiosqlite:///./backend/sql_app.db"
   ```

3. **Create a virtual environment and install dependencies**:
   ```bash
   cd backend
   python -m venv .venv

   # On Windows:
   .venv\Scripts\activate

   # On macOS/Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   # The database will be automatically initialized on first run
   # Or manually run migrations:
   alembic upgrade head
   ```

5. **Start the FastAPI server**:
   ```bash
   # From the backend directory:
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Open the frontend**:
   Simply open `frontend/index.html` in your web browser, or use a local server:

   ```bash
   # Using Python's built-in server:
   cd frontend
   python -m http.server 3000
   ```

   Then navigate to `http://localhost:3000`

2. **Configure API endpoint** (if needed):
   Edit `frontend/js/chat.js` and update the `API_BASE_URL` if your backend is running on a different host/port.

## Usage

### Starting a Conversation

1. Open the chat interface in your browser
2. Type a natural language message to manage your tasks
3. The AI will detect your intent and execute the appropriate action

### Example Commands

**Adding Tasks:**
- "Add a task to buy groceries"
- "Create a task: finish the report"
- "Remember to call mom"

**Listing Tasks:**
- "Show my tasks"
- "List all tasks"
- "What are my incomplete tasks?"

**Completing Tasks:**
- "Mark task 1 as done"
- "Complete the first task"
- "Finish task about groceries"

**Deleting Tasks:**
- "Delete task 2"
- "Remove the task about the report"

**Updating Tasks:**
- "Change task 1 to walk the dog"
- "Update task 3 title to buy milk"

### API Endpoints

**Chat Endpoint:**
```
POST /api/{user_id}/chat
```

Request body:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-conversation-id"
}
```

Response:
```json
{
  "response": "✓ Added task: buy groceries",
  "conversation_id": "uuid",
  "tool_executed": true,
  "tool_name": "add_task",
  "intent": "add_task"
}
```

**Get Conversation History:**
```
GET /api/{user_id}/conversations/{conversation_id}/history
```

## Architecture

### Stateless Design

The backend maintains no runtime conversation memory. All state is persisted in the database:
- **Conversations**: Track user conversation sessions
- **Messages**: Store all user and assistant messages
- **Tasks**: Persist user tasks

Each request reconstructs context from the database, enabling:
- Horizontal scaling
- Server restarts without data loss
- Conversation resumption across sessions

### MCP Tools

The system exposes five stateless tools via the Model Context Protocol:
- `add_task`: Create new tasks
- `list_tasks`: Retrieve tasks with optional filtering
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks
- `update_task`: Modify task details

### AI Intent Detection

The system uses a hybrid approach:
1. **Pattern Matching**: Fast regex-based intent detection for common patterns
2. **AI Fallback**: Gemini API for complex or ambiguous inputs

## Development

### Development Workflow

This project follows Spec-Driven Development (SDD):
1. Constitution defines principles
2. Specification defines requirements
3. Plan outlines architecture
4. Tasks break down implementation
5. Implementation follows tasks

### Running Tests

```bash
cd backend
pytest
```

### Code Formatting

```bash
# Format code
black src/
isort src/

# Type checking
mypy src/
```

## Troubleshooting

**Database Issues:**
- Delete `backend/sql_app.db` and restart the server to reset the database

**API Connection Issues:**
- Ensure the backend is running on port 8000
- Check CORS settings in `backend/src/main.py`
- Verify the `API_BASE_URL` in `frontend/js/chat.js`

**Gemini API Errors:**
- Verify your API key is correct in `.env`
- Check API quota and rate limits
- Ensure you have internet connectivity

## Contributing

Refer to the project's constitution (`.specify/memory/constitution.md`) for development philosophy and guidelines.

## License

This project is part of a hackathon submission.

## Acknowledgments

- Built with FastAPI, Google Gemini API, and SQLAlchemy
- Follows the Model Context Protocol (MCP) specification
- Developed using Spec-Kit Plus and Claude Code
