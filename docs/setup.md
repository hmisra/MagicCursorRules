# MagicCursorrules Setup Guide

This guide will help you set up the MagicCursorrules environment and tools.

## Prerequisites

- Python 3.9+ installed
- pip package manager
- Cursor IDE installed
- API keys for the LLM providers you want to use

## Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MagicCursorrules.git
   cd MagicCursorrules
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

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory with your API keys:
   ```
   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Anthropic API Key
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   
   # Optional: Azure OpenAI
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
   AZURE_OPENAI_MODEL_DEPLOYMENT=gpt-4o-ms
   
   # Optional: Other providers
   SERPAPI_KEY=your_serpapi_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CX=your_google_cx_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

6. Make the Python tool scripts executable:
   ```bash
   chmod +x tools/*.py
   ```

## Using the Multi-Agent System

The Multi-Agent system uses a Planner/Executor architecture for complex tasks. Here's how to use it:

### Planner Role

The Planner analyzes tasks, breaks them down, and creates execution plans. To invoke the Planner:

```bash
venv/bin/python tools/plan_exec_llm.py --prompt "Your planning prompt here"
```

You can include file content in the analysis:

```bash
venv/bin/python tools/plan_exec_llm.py --prompt "Analyze this file" --file path/to/file.py
```

### Web Tools

Use the web scraper to fetch content from websites:

```bash
venv/bin/python tools/web_scraper.py https://example.com
```

Use the search engine to find information:

```bash
venv/bin/python tools/search_engine.py "your search query"
```

### LLM API

Query an LLM directly:

```bash
venv/bin/python tools/llm_api.py --prompt "Your prompt here" --provider openai
```

For multimodal capabilities:

```bash
venv/bin/python tools/llm_api.py --prompt "Describe this image" --provider anthropic --image path/to/image.jpg
```

## Troubleshooting

- If you encounter API key errors, ensure your `.env` file is properly set up
- If Python tools aren't executable, run `chmod +x tools/*.py`
- If you see import errors, verify your virtual environment is activated
- For connection issues, check your internet connection and API key validity

## Next Steps

After setup, copy one of the .cursorrules files to your project root:

- Main `.cursorrules` for general use
- `frontend-react-nextjs-tailwind.cursorrules` for frontend development
- `backend-python-fastapi.cursorrules` for backend development
- `ai-integration-patterns.cursorrules` for AI integration 