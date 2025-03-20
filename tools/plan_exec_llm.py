#!/usr/bin/env python3
"""
plan_exec_llm.py - A tool for planning and execution operations using external LLMs.
This script helps the Multi-Agent system's Planner role to generate high-quality plans
using powerful LLM models.
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

# Default API configurations
DEFAULT_MODEL = "gpt-4o"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def load_file_content(file_path: str) -> str:
    """Load content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def query_openai(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Query the OpenAI API with the given prompt."""
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"Error querying OpenAI API: {e}", file=sys.stderr)
        return f"Error: {str(e)}"

def query_anthropic(prompt: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    """Query the Anthropic API with the given prompt."""
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json().get("content", [{}])[0].get("text", "")
    except Exception as e:
        print(f"Error querying Anthropic API: {e}", file=sys.stderr)
        return f"Error: {str(e)}"

def generate_planning_prompt(prompt: str, file_content: Optional[str] = None) -> str:
    """Generate a planning prompt with optional file content."""
    base_prompt = f"""
You are an expert AI development planner helping with a programming task.
Your role is to analyze requirements, break down complex tasks, and provide
detailed guidance. Focus on:

1. Thorough analysis of the problem
2. Breaking down tasks into manageable steps
3. Identifying potential challenges and solutions
4. Suggesting specific implementation approaches
5. Providing concrete code structure recommendations

TASK DESCRIPTION:
{prompt}

"""
    
    if file_content:
        base_prompt += f"""
RELEVANT FILE CONTENT:
```
{file_content}
```

Based on the above file content and task description, provide a detailed plan.
"""
    
    return base_prompt

def main():
    parser = argparse.ArgumentParser(description="Planning and execution tool using external LLMs")
    parser.add_argument("--prompt", required=True, help="The prompt for the planning operation")
    parser.add_argument("--file", help="Optional file to include in the analysis")
    parser.add_argument("--model", default="o1", help="The model to use (default: o1)")
    parser.add_argument("--provider", default="openai", choices=["openai", "anthropic"], 
                        help="The API provider to use (default: openai)")
    
    args = parser.parse_args()
    
    file_content = None
    if args.file:
        file_content = load_file_content(args.file)
    
    planning_prompt = generate_planning_prompt(args.prompt, file_content)
    
    if args.provider == "openai":
        response = query_openai(planning_prompt, args.model)
    else:
        response = query_anthropic(planning_prompt)
    
    print("\n----- PLANNING RESULT -----\n")
    print(response)
    print("\n--------------------------\n")

if __name__ == "__main__":
    main() 