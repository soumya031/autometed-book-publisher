"""
Web Scraper Module for Automated Book Publication Workflow
Handles content extraction and screenshot capture using Playwright
"""

import asyncio
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraper for extracting content and taking screenshots"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.screenshots_dir = self.output_dir / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        
    async def scrape_content(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from the given URL and take screenshots
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing scraped content and metadata
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                logger.info(f"Navigating to {url}")
                await page.goto(url, wait_until="networkidle")
                
                # Take screenshot
                screenshot_path = self.screenshots_dir / f"{self._get_filename_from_url(url)}.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"Screenshot saved to {screenshot_path}")
                
                # Extract content
                content = await self._extract_content(page)
                
                await browser.close()
                
                return {
                    "url": url,
                    "title": content.get("title", ""),
                    "text_content": content.get("text_content", ""),
                    "screenshot_path": str(screenshot_path),
                    "metadata": content.get("metadata", {})
                }
                
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                await browser.close()
                raise
    
    async def _extract_content(self, page: Page) -> Dict[str, Any]:
        """Extract content from the page"""
        # Get page title
        title = await page.title()
        
        # Get main content
        content_element = await page.query_selector("main, .mw-parser-output, #content")
        if not content_element:
            content_element = page
        
        # Extract text content
        text_content = await content_element.inner_text()
        
        # Get HTML for additional processing
        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract metadata
        metadata = {
            "headings": [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
            "links": [a.get('href') for a in soup.find_all('a', href=True) if a.get('href')],
            "images": [img.get('src') for img in soup.find_all('img', src=True) if img.get('src')]
        }
        
        return {
            "title": title,
            "text_content": text_content,
            "metadata": metadata
        }
    
    def _get_filename_from_url(self, url: str) -> str:
        """Generate a filename from URL"""
        # Remove protocol and domain, replace special chars
        filename = re.sub(r'https?://[^/]+/', '', url)
        filename = re.sub(r'[^\w\-_.]', '_', filename)
        return filename or "scraped_content"


async def main():
    """Test the scraper"""
    scraper = WebScraper()
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    
    try:
        result = await scraper.scrape_content(url)
        print(f"Scraped content from {url}")
        print(f"Title: {result['title']}")
        print(f"Content length: {len(result['text_content'])} characters")
        print(f"Screenshot saved to: {result['screenshot_path']}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(main())