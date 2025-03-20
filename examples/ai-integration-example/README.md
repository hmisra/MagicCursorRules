# AI Integration Example

This example demonstrates how to use the ai-integration-patterns.cursorrules file for building AI-enhanced applications.

## Setup

1. Copy the `ai-integration-patterns.cursorrules` file to your project root:
   ```bash
   cp ../../cursorrules/ai-integration-patterns.cursorrules ./.cursorrules
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install openai langchain tiktoken faiss-cpu python-dotenv pydantic pillow requests
   ```

4. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Create the project structure:
   ```bash
   mkdir -p src/api src/vectorstore src/prompts src/models src/utils tests
   ```

## Example Questions for AI

Once your project is set up with the .cursorrules file, you can ask the AI contextual questions about the project:

1. "Create a RAG system for answering questions from a PDF document"
2. "Implement a prompt template for a customer service chatbot"
3. "Build an API endpoint that uses OpenAI's API to summarize text"
4. "Create a system for processing and analyzing images with AI"
5. "Implement a caching mechanism for LLM responses"
6. "Create a chain-of-thought reasoning system for complex problem-solving"
7. "Build a system for fine-tuning an LLM on custom data"

## Benefits

Using the specialized cursorrules file, the AI will:

- Follow the integration patterns defined in the cursorrules
- Implement proper error handling for AI services
- Use best practices for prompt engineering
- Create efficient and cost-effective AI integrations
- Implement proper security practices for AI services
- Follow ethical guidelines for AI use 