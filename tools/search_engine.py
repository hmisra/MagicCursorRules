#!/usr/bin/env python3
"""
search_engine.py - A utility for performing web searches.
This script helps the Multi-Agent system find relevant information on the web.
"""

import os
import sys
import json
import argparse
import requests
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("search_engine")

# Search API configurations
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_CX = os.environ.get("GOOGLE_CX", "")

def search_serpapi(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a web search using SerpAPI.
    
    Args:
        query: The search query
        num_results: Number of results to return
        
    Returns:
        List of dictionaries with search results
    """
    if not SERPAPI_KEY:
        logger.error("SERPAPI_KEY environment variable not set")
        return [{"error": "SERPAPI_KEY environment variable not set"}]
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "num": num_results
        }
        
        logger.debug(f"Searching SerpAPI for: {query}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        organic_results = data.get("organic_results", [])
        
        results = []
        for result in organic_results[:num_results]:
            results.append({
                "title": result.get("title", ""),
                "url": result.get("link", ""),
                "snippet": result.get("snippet", "")
            })
        
        return results
    except Exception as e:
        logger.error(f"Error searching with SerpAPI: {str(e)}")
        return [{"error": f"Search failed: {str(e)}"}]

def search_google_custom_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a web search using Google Custom Search API.
    
    Args:
        query: The search query
        num_results: Number of results to return
        
    Returns:
        List of dictionaries with search results
    """
    if not GOOGLE_API_KEY or not GOOGLE_CX:
        logger.error("GOOGLE_API_KEY or GOOGLE_CX environment variable not set")
        return [{"error": "Google Search API credentials not set"}]
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "num": min(num_results, 10)  # Google API max is 10
        }
        
        logger.debug(f"Searching Google Custom Search for: {query}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        
        results = []
        for item in items[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        
        return results
    except Exception as e:
        logger.error(f"Error searching with Google Custom Search: {str(e)}")
        return [{"error": f"Search failed: {str(e)}"}]

def search_duckduckgo_lite(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a web search using DuckDuckGo Lite (HTML scraping as fallback).
    
    Args:
        query: The search query
        num_results: Number of results to return
        
    Returns:
        List of dictionaries with search results
    """
    try:
        encoded_query = quote_plus(query)
        url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
        
        logger.debug(f"Searching DuckDuckGo Lite for: {query}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        for i, tr in enumerate(soup.find_all("tr", class_=["result-link", "result-snippet"])):
            if i >= num_results * 2:
                break
            
            # Every other row is a link/title or snippet
            if i % 2 == 0:  # Link row
                a_tag = tr.find("a")
                if a_tag:
                    title = a_tag.get_text().strip()
                    href = a_tag.get("href", "")
                    results.append({"title": title, "url": href, "snippet": ""})
            else:  # Snippet row
                if results:  # Make sure there's a result to add the snippet to
                    results[-1]["snippet"] = tr.get_text().strip()
        
        return results[:num_results]
    except Exception as e:
        logger.error(f"Error searching with DuckDuckGo Lite: {str(e)}")
        return [{"error": f"Search failed: {str(e)}"}]

def perform_search(query: str, num_results: int = 5, engine: str = "auto") -> List[Dict[str, str]]:
    """
    Perform a web search using available search engines.
    
    Args:
        query: The search query
        num_results: Number of results to return
        engine: Search engine to use ('serpapi', 'google', 'ddg', or 'auto')
        
    Returns:
        List of dictionaries with search results
    """
    # If engine is auto, try engines in order of preference
    if engine == "auto":
        if SERPAPI_KEY:
            engine = "serpapi"
        elif GOOGLE_API_KEY and GOOGLE_CX:
            engine = "google"
        else:
            engine = "ddg"
    
    # Perform search with selected engine
    if engine == "serpapi":
        return search_serpapi(query, num_results)
    elif engine == "google":
        return search_google_custom_search(query, num_results)
    elif engine == "ddg":
        return search_duckduckgo_lite(query, num_results)
    else:
        return [{"error": f"Unknown search engine: {engine}"}]

def main():
    parser = argparse.ArgumentParser(description="Search engine utility for the Multi-Agent system")
    parser.add_argument("query", help="The search query")
    parser.add_argument("--num-results", "-n", type=int, default=5, 
                        help="Number of results to return (default: 5)")
    parser.add_argument("--engine", "-e", choices=["auto", "serpapi", "google", "ddg"], 
                        default="auto", help="Search engine to use (default: auto)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    results = perform_search(args.query, args.num_results, args.engine)
    
    # Print results
    for result in results:
        if "error" in result:
            print(f"Error: {result['error']}")
            continue
            
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Snippet: {result['snippet']}")
        print()

if __name__ == "__main__":
    main() 