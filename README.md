# MagicCursorrules

A collection of powerful cursorrules for enhancing AI-assisted development in Cursor.

## Overview

This repository contains a carefully curated set of cursorrules files designed to enhance the capabilities of AI-assisted development in Cursor. Each cursorrule file provides specialized instructions and guidance for different development scenarios.

## Cursorrules Collection

### Main Cursorrule

The main [.cursorrules](./.cursorrules) file includes:

- Core principles and guidelines
- Multi-Agent Scratchpad functionality
- Project structure conventions
- Code style guidelines
- Common tools and libraries
- AI optimization techniques
- Advanced features

### Specialized Cursorrules

#### Frontend Development

The [frontend-react-nextjs-tailwind.cursorrules](./cursorrules/frontend-react-nextjs-tailwind.cursorrules) file provides:

- Guidelines for React, Next.js, TypeScript, and Tailwind CSS
- Project structure recommendations
- Component design principles
- Performance optimization techniques
- State management patterns
- Accessibility best practices

#### Backend Development

The [backend-python-fastapi.cursorrules](./cursorrules/backend-python-fastapi.cursorrules) file includes:

- Guidelines for Python, FastAPI, and SQLAlchemy
- Project structure recommendations
- API design principles
- Database design patterns
- Authentication and security best practices
- Performance optimization techniques

#### AI Integration Patterns

The [ai-integration-patterns.cursorrules](./cursorrules/ai-integration-patterns.cursorrules) file covers:

- Prompt engineering techniques
- Model selection guidelines
- RAG implementation patterns
- Chain-of-thought reasoning approaches
- AI system architecture recommendations
- Security and privacy considerations

## Tools and Utilities

The repository includes several Python-based tools to support the Multi-Agent system:

### LLM Integration

- **[tools/plan_exec_llm.py](./tools/plan_exec_llm.py)**: Connects to powerful LLMs for planning and reasoning tasks
- **[tools/llm_api.py](./tools/llm_api.py)**: A unified interface for querying different LLM providers (OpenAI, Anthropic, etc.)

### Web Utilities

- **[tools/web_scraper.py](./tools/web_scraper.py)**: Extracts content from web pages
- **[tools/search_engine.py](./tools/search_engine.py)**: Performs web searches using various search engines

## Examples

The repository includes example setups for each specialized cursorrule:

- **[Frontend Example](./examples/frontend-example/)**: Demonstrates how to use the frontend cursorrules in a Next.js project
- **[Backend Example](./examples/backend-example/)**: Shows how to apply the backend cursorrules in a FastAPI project
- **[AI Integration Example](./examples/ai-integration-example/)**: Illustrates the use of AI integration patterns

## Getting Started

See the [setup guide](./docs/setup.md) for detailed instructions on setting up and using MagicCursorrules.

## Usage

1. Clone this repository
2. Copy the desired .cursorrules file to your project's root directory
3. Customize the file to fit your project's specific needs
4. Enjoy enhanced AI-assisted development in Cursor!

## Sources and Inspiration

These cursorrules were developed based on analysis of the [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) repository and best practices in AI-assisted development.