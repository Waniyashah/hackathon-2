<!-- SYNC IMPACT REPORT:
Version change: N/A (initial) → 1.0.0
Modified principles: None (initial creation)
Added sections: All sections added
Removed sections: None
Templates requiring updates: ⚠ pending - plan-template.md, spec-template.md, tasks-template.md
Follow-up TODOs: None
-->

# Todo Evolution Constitution

## Core Principles

### I. Spec-Driven Development
All implementation must originate from written specifications. Code must be generated through Claude Code based on refined specs. No implementation code shall be written manually; adjustments must be achieved by improving specifications.

### II. Agentic Development Workflow
Follow the sequence: Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code. All development work must flow through this structured workflow to ensure traceability between requirements and implementation.

### III. No Manual Coding (NON-NEGOTIABLE)
Developers are strictly prohibited from writing implementation code manually. All code generation must occur through Claude Code agents. Any adjustments or fixes must be achieved by improving specifications rather than direct code manipulation.

### IV. Clean Code Practices
Maintain readable structure, modular design, clear naming conventions, and separation of responsibilities. Code must be maintainable, well-organized, and follow established Python best practices and conventions.

### V. Simplicity and Reliability
Focus on core CLI functionality with clear console interaction and predictable behavior. Prioritize stable, reliable functionality over complex features. Embrace minimal viable implementation that meets requirements.

### VI. Python Excellence
Use Python 3.13+ with modern language features and best practices. Leverage appropriate standard library components and maintain high code quality with proper error handling and clear documentation.

## Additional Constraints

Technology Stack: Python 3.13+, UV environment manager, Claude Code, Spec-Kit Plus
Application Type: Command-line interface (CLI) with console interaction
Data Storage: In-memory only (no persistent storage)
Project Structure: /src for Python source, /specs_history for all specification versions
Required Files: README.md, CLAUDE.md, and proper project organization

## Development Workflow

All implementation must use the agentic workflow through Claude Code
Specifications must precede all implementation work
Proper testing and validation at each stage
Clean, incremental commits following the workflow
Traceability between specs and generated implementation

## Governance

This constitution governs all development activities for the Todo application. All code generation must comply with the spec-driven, agentic workflow. Any deviation from these principles requires explicit constitutional amendment. All generated code must follow clean code practices, maintain simplicity and reliability, and be produced through Claude Code agents without manual intervention. The development team must verify compliance with these principles during all development activities.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06