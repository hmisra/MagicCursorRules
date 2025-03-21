# Cursor Rules Architecture

This document explains the cursor rules architecture implemented in the MagicCursorrules project, which enhances AI-assisted development in Cursor.

## Overview

Cursor Rules are specialized instructions that help the AI assistant understand your project's context, coding standards, and domain-specific requirements. This project implements an advanced cursor rules structure for better organization and modularity.

## Rules Structure

The project uses two complementary approaches for cursor rules:

1. **Root-level `.cursorrules` file**
   - Located at the project root
   - Contains high-level project information and the Multi-Agent Scratchpad
   - Visible in Cursor's AI settings

2. **Modular rules in `.cursor/rules` directory**
   - Located in the `.cursor/rules` directory
   - Uses `.mdc` format with YAML frontmatter
   - Each file focuses on a specific domain or aspect
   - Allows for more granular and maintainable rules

## Available Rule Categories

The project includes rules for the following categories:

- **Frontend** (`.cursor/rules/frontend.mdc`): Guidelines for React, Next.js, TypeScript, and Tailwind development
- **Backend** (`.cursor/rules/backend.mdc`): Guidelines for Python and FastAPI development
- **AI Integration** (`.cursor/rules/ai-integration.mdc`): Patterns for integrating AI models and APIs
- **Multi-Agent** (`.cursor/rules/multi-agent.mdc`): Guidelines for implementing multi-agent systems
- **Tooling** (`.cursor/rules/tooling.mdc`): Best practices for tools and utilities

## Rule Format

Each rule file in the `.cursor/rules` directory follows this format:

```
---
description: Brief description of what these rules cover
globs: [file patterns these rules apply to]
---

# Category Title

## Subcategory
- Rule 1
- Rule 2
- Rule 3
```

The frontmatter (between `---`) contains:
- `description`: A brief explanation of what these rules cover
- `globs`: File patterns that these rules apply to (e.g., `**/*.py`, `components/**/*.tsx`)

## Using the Rules with Cursor

Cursor will automatically recognize and use both the root `.cursorrules` file and the modular rules in the `.cursor/rules` directory. The AI will apply the relevant rules based on the file you're working on.

### For New Projects

1. Copy the entire `.cursor` directory to your new project
2. Copy the `.cursorrules` file to your project root
3. Modify the contents to match your project requirements

### Extending the Rules

To add new rule categories:

1. Create a new `.mdc` file in the `.cursor/rules` directory
2. Follow the format described above
3. Add specific guidelines relevant to your domain

## Benefits of This Architecture

- **Modularity**: Rules are organized by domain and purpose
- **Maintainability**: Easier to update specific rule sets
- **Specificity**: Rules can target specific file patterns
- **Scalability**: Easy to add new rule categories
- **Compatibility**: Works with both older and newer Cursor versions

## Best Practices

- Keep rules concise and specific
- Update rules as your project evolves
- Include examples where helpful
- Maintain consistency between rule sets
- Avoid contradictions between different rule files 