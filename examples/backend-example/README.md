# Backend Example

This example demonstrates how to use the backend-python-fastapi.cursorrules file for a FastAPI project.

## Setup

1. Copy the `backend-python-fastapi.cursorrules` file to your project root:
   ```bash
   cp ../../cursorrules/backend-python-fastapi.cursorrules ./.cursorrules
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy alembic pydantic psycopg2-binary python-jose
   ```

4. Create the project structure:
   ```bash
   mkdir -p app/api/v1 app/core/config app/core/security app/db/models app/db/migrations app/schemas app/services app/utils tests
   ```

## Example Questions for AI

Once your project is set up with the .cursorrules file, you can ask the AI contextual questions about the project:

1. "Create a user model with SQLAlchemy"
2. "Implement JWT authentication"
3. "Create a CRUD API for posts"
4. "Add pagination to the API endpoints"
5. "Implement database migrations with Alembic"
6. "Create a service for handling user registration"
7. "Add input validation for the API endpoints"

## Benefits

Using the specialized cursorrules file, the AI will:

- Follow the project structure defined in the cursorrules
- Implement proper error handling
- Use async/await for I/O-bound operations
- Follow RESTful API design principles
- Use Pydantic models for request/response validation
- Implement proper security practices 