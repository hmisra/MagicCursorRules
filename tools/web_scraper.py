#!/usr/bin/env python3
"""
web_scraper.py - A utility for scraping web content.
This script helps the Multi-Agent system access information from the web.
"""

import sys
import argparse
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("web_scraper")

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Fetch content from a URL using aiohttp."""
    try:
        logger.debug(f"Fetching {url}")
        async with session.get(url, timeout=30) as response:
            if response.status != 200:
                return {
                    "url": url,
                    "success": False,
                    "status": response.status,
                    "error": f"HTTP error: {response.status}",
                    "content": None
                }
            
            content = await response.text()
            logger.debug(f"Successfully fetched {url} ({len(content)} bytes)")
            return {
                "url": url,
                "success": True,
                "status": response.status,
                "content": content
            }
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return {
            "url": url,
            "success": False,
            "error": str(e),
            "content": None
        }

def extract_main_content(html_content: str) -> str:
    """Extract main content from HTML using BeautifulSoup."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove scripts, styles, and other non-content elements
        for element in soup(['script', 'style', 'nav', 'footer', 'iframe']):
            element.decompose()
        
        # Try to find main content area
        main_content = None
        for container in ['main', 'article', '[role="main"]', '#content', '.content', '#main', '.main']:
            content = soup.select(container)
            if content:
                main_content = content[0]
                break
        
        # Fall back to body if no main content found
        if not main_content:
            main_content = soup.body
        
        # If still nothing found, use the whole soup
        if not main_content:
            main_content = soup
        
        # Get text with preserved paragraph structure
        text = ""
        for p in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
            text += p.get_text().strip() + "\n\n"
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting content: {e}")
        return "Error extracting content"

async def scrape_urls(urls: List[str], max_concurrent: int = 5) -> List[Dict[str, Any]]:
    """Scrape multiple URLs concurrently."""
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # Process results to extract main content
        for result in results:
            if result["success"]:
                result["extracted_content"] = extract_main_content(result["content"])
                # Remove the raw HTML to save space
                del result["content"]
        
        return results

def main():
    parser = argparse.ArgumentParser(description="Web scraper utility for the Multi-Agent system")
    parser.add_argument("urls", nargs="+", help="URLs to scrape")
    parser.add_argument("--max-concurrent", type=int, default=5, 
                        help="Maximum number of concurrent requests (default: 5)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    results = asyncio.run(scrape_urls(args.urls, args.max_concurrent))
    
    # Print results
    for result in results:
        print(f"URL: {result['url']}")
        print(f"Status: {'Success' if result['success'] else 'Failed'}")
        
        if not result['success']:
            print(f"Error: {result.get('error', 'Unknown error')}")
            print()
            continue
        
        print("\nContent:")
        print("-" * 80)
        print(result.get('extracted_content', ''))
        print("-" * 80)
        print("\n")

if __name__ == "__main__":
    main() 