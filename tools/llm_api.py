#!/usr/bin/env python3
"""
llm_api.py - A utility for interacting with various LLM APIs.
This script provides a unified interface for querying different LLM providers.
"""

import os
import sys
import json
import argparse
import requests
from typing import Dict, Any, Optional, List, Union
import logging
import base64

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("llm_api")

# API Key configurations
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_MODEL_DEPLOYMENT = os.environ.get("AZURE_OPENAI_MODEL_DEPLOYMENT", "gpt-4o-ms")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {e}")
        raise

def query_openai(
    prompt: str, 
    model: str = "gpt-4o", 
    temperature: float = 0.7, 
    max_tokens: int = 4000,
    image_path: Optional[str] = None
) -> str:
    """Query the OpenAI API."""
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable not set")
        return "Error: OPENAI_API_KEY environment variable not set"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    messages = [{"role": "user", "content": []}]
    
    # Add text content
    messages[0]["content"].append({
        "type": "text",
        "text": prompt
    })
    
    # Add image content if provided
    if image_path:
        try:
            base64_image = encode_image_to_base64(image_path)
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return f"Error processing image: {str(e)}"
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        logger.debug(f"Querying OpenAI API with model {model}")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        logger.error(f"Error querying OpenAI API: {e}")
        return f"Error: {str(e)}"

def query_azure_openai(
    prompt: str, 
    temperature: float = 0.7, 
    max_tokens: int = 4000,
    image_path: Optional[str] = None
) -> str:
    """Query the Azure OpenAI API."""
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
        logger.error("Azure OpenAI credentials not set")
        return "Error: Azure OpenAI credentials not set"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    
    messages = [{"role": "user", "content": []}]
    
    # Add text content
    messages[0]["content"].append({
        "type": "text",
        "text": prompt
    })
    
    # Add image content if provided
    if image_path:
        try:
            base64_image = encode_image_to_base64(image_path)
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return f"Error processing image: {str(e)}"
    
    data = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        logger.debug(f"Querying Azure OpenAI API with deployment {AZURE_OPENAI_MODEL_DEPLOYMENT}")
        # Azure OpenAI endpoint format: {endpoint}/openai/deployments/{deployment-id}/chat/completions?api-version=2023-05-15
        api_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_MODEL_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
        response = requests.post(
            api_url,
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        logger.error(f"Error querying Azure OpenAI API: {e}")
        return f"Error: {str(e)}"

def query_anthropic(
    prompt: str, 
    model: str = "claude-3-5-sonnet-20241022", 
    temperature: float = 0.7, 
    max_tokens: int = 4000,
    image_path: Optional[str] = None
) -> str:
    """Query the Anthropic API."""
    if not ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        return "Error: ANTHROPIC_API_KEY environment variable not set"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    message_content = [
        {"type": "text", "text": prompt}
    ]
    
    # Add image if provided
    if image_path:
        try:
            with open(image_path, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode('utf-8')
                message_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64_image
                    }
                })
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return f"Error processing image: {str(e)}"
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": message_content}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        logger.debug(f"Querying Anthropic API with model {model}")
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json().get("content", [{}])[0].get("text", "")
    except Exception as e:
        logger.error(f"Error querying Anthropic API: {e}")
        return f"Error: {str(e)}"

def query_deepseek(
    prompt: str, 
    temperature: float = 0.7, 
    max_tokens: int = 4000
) -> str:
    """Query the DeepSeek API."""
    if not DEEPSEEK_API_KEY:
        logger.error("DEEPSEEK_API_KEY environment variable not set")
        return "Error: DEEPSEEK_API_KEY environment variable not set"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        logger.debug("Querying DeepSeek API")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        logger.error(f"Error querying DeepSeek API: {e}")
        return f"Error: {str(e)}"

def query_gemini(
    prompt: str, 
    temperature: float = 0.7, 
    max_tokens: int = 4000,
    image_path: Optional[str] = None
) -> str:
    """Query the Google Gemini API."""
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable not set")
        return "Error: GEMINI_API_KEY environment variable not set"
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    parts = [{"text": prompt}]
    
    # Add image if provided
    if image_path:
        try:
            with open(image_path, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64_image
                    }
                })
                # When using an image, switch to gemini-pro-vision
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return f"Error processing image: {str(e)}"
    
    data = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }
    
    try:
        logger.debug("Querying Gemini API")
        response = requests.post(
            url,
            json=data
        )
        response.raise_for_status()
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except Exception as e:
        logger.error(f"Error querying Gemini API: {e}")
        return f"Error: {str(e)}"

def query_llm(
    prompt: str, 
    provider: str = "openai", 
    model: Optional[str] = None,
    temperature: float = 0.7, 
    max_tokens: int = 4000,
    image_path: Optional[str] = None
) -> str:
    """
    Query an LLM provider with the given prompt.
    
    Args:
        prompt: The text prompt to send to the LLM
        provider: The LLM provider to use ('openai', 'azure', 'anthropic', 'deepseek', 'gemini')
        model: The specific model to use (provider-dependent)
        temperature: Temperature setting for generation
        max_tokens: Maximum tokens to generate
        image_path: Optional path to an image file for multimodal models
        
    Returns:
        The LLM's response text
    """
    # Set default models for each provider
    default_models = {
        "openai": "gpt-4o",
        "anthropic": "claude-3-5-sonnet-20241022",
        "deepseek": "deepseek-chat",
        "gemini": "gemini-pro"
    }
    
    # Use the specified model or the default for the provider
    if model is None:
        model = default_models.get(provider, "")
    
    # Call the appropriate provider's API
    if provider == "openai":
        return query_openai(prompt, model, temperature, max_tokens, image_path)
    elif provider == "azure":
        return query_azure_openai(prompt, temperature, max_tokens, image_path)
    elif provider == "anthropic":
        return query_anthropic(prompt, model, temperature, max_tokens, image_path)
    elif provider == "deepseek":
        return query_deepseek(prompt, temperature, max_tokens)
    elif provider == "gemini":
        return query_gemini(prompt, temperature, max_tokens, image_path)
    else:
        return f"Error: Unknown provider '{provider}'"

def main():
    parser = argparse.ArgumentParser(description="LLM API utility for the Multi-Agent system")
    parser.add_argument("--prompt", required=True, help="The prompt to send to the LLM")
    parser.add_argument("--provider", choices=["openai", "azure", "anthropic", "deepseek", "gemini"], 
                        default="openai", help="LLM provider to use (default: openai)")
    parser.add_argument("--model", help="Specific model to use (provider-dependent)")
    parser.add_argument("--temperature", type=float, default=0.7, 
                        help="Temperature setting for generation (default: 0.7)")
    parser.add_argument("--max-tokens", type=int, default=4000, 
                        help="Maximum tokens to generate (default: 4000)")
    parser.add_argument("--image", dest="image_path", help="Path to an image file for multimodal models")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    response = query_llm(
        args.prompt,
        args.provider,
        args.model,
        args.temperature,
        args.max_tokens,
        args.image_path
    )
    
    print(response)

if __name__ == "__main__":
    main() 