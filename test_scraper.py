#!/usr/bin/env python3
"""
Simple test script for the web scraper
"""

import asyncio
from app.scraper import WebScraper

async def test_scraper():
    print("Testing web scraper...")
    scraper = WebScraper()
    
    try:
        result = await scraper.scrape_content('https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1')
        print(f"✅ Success! Scraped {len(result['text_content'])} characters")
        print(f"📄 Title: {result['title']}")
        print(f"📸 Screenshot saved to: {result['screenshot_path']}")
        print(f"📝 Content preview: {result['text_content'][:200]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_scraper())
    if success:
        print("\n🎉 Web scraper is working perfectly!")
    else:
        print("\n❌ Web scraper test failed.")