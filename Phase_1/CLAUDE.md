# Claude Code Usage Instructions

This project was developed using Claude Code and Spec-Kit Plus following a spec-driven, agentic development workflow.

## Development Workflow

The project follows this sequence:
1. Write Specification → Generate Plan → Break into Tasks → Implement via Claude Code
2. All implementation originates from written specifications
3. No implementation code is written manually - all code generation occurs through Claude Code agents
4. Adjustments and fixes are achieved by improving specifications rather than direct code manipulation

## Project Constitution

The development is governed by the following principles:
- Spec-Driven Development: All implementation must originate from written specifications
- Agentic Development Workflow: Follow the sequence Write Spec → Generate Plan → Tasks → Implementation
- No Manual Coding: Developers are strictly prohibited from writing implementation code manually
- Clean Code Practices: Maintain readable structure, modular design, clear naming conventions
- Simplicity and Reliability: Focus on core CLI functionality with predictable behavior
- Python Excellence: Use Python 3.13+ with modern language features and best practices

## Technology Stack

- Language: Python 3.13+
- Environment: Standard Python library only (no external dependencies)
- Application Type: Command-line interface (CLI) with console interaction
- Data Storage: In-memory only (no persistent storage)

## Architecture

The application follows a clean, modular architecture:
- Models: Handle data structures (Task entity)
- Services: Handle business logic (TaskService with CRUD operations)
- CLI: Handle user interface and input/output

## File Structure

- `src/` - Contains all source code
- `specs/` - Contains all specification documents
- `history/prompts/` - Contains prompt history records
- `README.md` - Project overview and usage instructions
- `CLAUDE.md` - Claude Code usage instructions
- `.specify/` - Spec-Kit Plus configuration and templates