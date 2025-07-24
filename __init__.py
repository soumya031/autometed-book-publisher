"""
Automated Book Publication Workflow Package
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "Automated book publication workflow with AI-driven content processing"

from .scraper import WebScraper
from .ai_agents import AIWriter, AIReviewer, AIEditor
from .db import ContentDatabase
from .main import BookPublicationWorkflow

__all__ = [
    "WebScraper",
    "AIWriter", 
    "AIReviewer",
    "AIEditor",
    "ContentDatabase",
    "BookPublicationWorkflow"
] 