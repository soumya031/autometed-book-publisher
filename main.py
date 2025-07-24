"""
Main Workflow Orchestrator for Automated Book Publication Workflow
Coordinates scraping, AI processing, human review, and content storage
"""

import asyncio
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from dotenv import load_dotenv

# Import our modules
from .scraper import WebScraper
from .ai_agents import AIWriter, AIReviewer, AIEditor
from .db import ContentDatabase

load_dotenv()
console = Console()


class BookPublicationWorkflow:
    """Main workflow orchestrator for the book publication system"""
    
    def __init__(self):
        self.scraper = WebScraper()
        self.db = ContentDatabase()
        
        # Initialize AI agents (will fail gracefully if API key not set)
        try:
            self.writer = AIWriter()
            self.reviewer = AIReviewer()
            self.editor = AIEditor()
            self.ai_available = True
        except Exception as e:
            console.print(f"[yellow]Warning: AI agents not available: {e}[/yellow]")
            self.ai_available = False
    
    async def run_workflow(self, url: str, style: str = "modern", tone: str = "engaging"):
        """
        Run the complete publication workflow
        
        Args:
            url: URL to scrape
            style: Writing style for AI generation
            tone: Tone for AI generation
        """
        console.print(Panel.fit("🚀 Starting Book Publication Workflow", style="bold blue"))
        
        # Step 1: Scrape content
        console.print("\n[bold]Step 1: Scraping Content[/bold]")
        try:
            content_data = await self.scraper.scrape_content(url)
            console.print(f"✅ Successfully scraped content from {url}")
            console.print(f"📄 Title: {content_data['title']}")
            console.print(f"📊 Content length: {len(content_data['text_content'])} characters")
            console.print(f"📸 Screenshot saved to: {content_data['screenshot_path']}")
            
            # Store original content
            original_id = self.db.store_original_content(content_data)
            console.print(f"💾 Original content stored with ID: {original_id}")
            
        except Exception as e:
            console.print(f"❌ Error scraping content: {e}")
            return None
        
        # Step 2: AI Content Generation
        if self.ai_available:
            console.print("\n[bold]Step 2: AI Content Generation[/bold]")
            try:
                ai_content = self.writer.spin_chapter(
                    content_data['text_content'], 
                    style=style, 
                    tone=tone
                )
                console.print("✅ AI content generation completed")
                
                # Store AI-generated content
                ai_id = self.db.store_ai_generated_content(
                    original_id, ai_content, style, tone
                )
                console.print(f"💾 AI content stored with ID: {ai_id}")
                
                # Show AI content preview
                self._show_content_preview("AI-Generated Content", ai_content)
                
            except Exception as e:
                console.print(f"❌ Error in AI content generation: {e}")
                ai_content = content_data['text_content']
                ai_id = None
        else:
            ai_content = content_data['text_content']
            ai_id = None
            console.print("[yellow]⚠️  Skipping AI generation (AI not available)[/yellow]")
        
        # Step 3: Human Review and Iteration
        console.print("\n[bold]Step 3: Human Review and Iteration[/bold]")
        final_content = await self._human_review_loop(
            original_content=content_data['text_content'],
            ai_content=ai_content,
            original_id=original_id,
            ai_id=ai_id,
            style=style,
            tone=tone
        )
        
        if not final_content:
            console.print("❌ Workflow cancelled by user")
            return None
        
        # Step 4: Final Review and Publication
        console.print("\n[bold]Step 4: Final Review and Publication[/bold]")
        
        if self.ai_available:
            try:
                # AI final review
                review = self.reviewer.review_content(final_content, content_data['text_content'])
                console.print("✅ AI final review completed")
                
                # Store review
                if ai_id:
                    review_id = self.db.store_review(ai_id, review)
                    console.print(f"💾 Review stored with ID: {review_id}")
                
                # Show review summary
                self._show_review_summary(review)
                
                # AI finalization
                requirements = {
                    "style": style,
                    "tone": tone,
                    "publication_format": "standard"
                }
                finalized_content = self.editor.finalize_content(final_content, requirements)
                console.print("✅ AI finalization completed")
                
            except Exception as e:
                console.print(f"❌ Error in AI finalization: {e}")
                finalized_content = final_content
        else:
            finalized_content = final_content
            console.print("[yellow]⚠️  Skipping AI finalization (AI not available)[/yellow]")
        
        # Step 5: Store Final Version
        console.print("\n[bold]Step 5: Storing Final Version[/bold]")
        try:
            final_id = self.db.store_final_version(
                original_id, 
                finalized_content,
                {"style": style, "tone": tone}
            )
            console.print(f"✅ Final version stored with ID: {final_id}")
            
            # Show final content preview
            self._show_content_preview("Final Published Content", finalized_content)
            
        except Exception as e:
            console.print(f"❌ Error storing final version: {e}")
        
        console.print(Panel.fit("🎉 Workflow Completed Successfully!", style="bold green"))
        return {
            "original_id": original_id,
            "ai_id": ai_id,
            "final_id": final_id,
            "final_content": finalized_content
        }
    
    async def _human_review_loop(self, original_content: str, ai_content: str, 
                               original_id: str, ai_id: Optional[str], 
                               style: str, tone: str) -> Optional[str]:
        """Handle human review and iteration loop"""
        current_content = ai_content
        iteration = 1
        max_iterations = 5
        
        while iteration <= max_iterations:
            console.print(f"\n[bold]Iteration {iteration}/{max_iterations}[/bold]")
            
            # Show current content
            self._show_content_preview(f"Current Content (Iteration {iteration})", current_content)
            
            # Ask for human input
            action = Prompt.ask(
                "What would you like to do?",
                choices=["approve", "edit", "regenerate", "review", "cancel"],
                default="review"
            )
            
            if action == "approve":
                console.print("✅ Content approved by human reviewer")
                return current_content
            
            elif action == "cancel":
                if Confirm.ask("Are you sure you want to cancel the workflow?"):
                    return None
            
            elif action == "edit":
                console.print("\n[bold]Manual Editing Mode[/bold]")
                console.print("Please edit the content. Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done.")
                
                # For simplicity, we'll use a simple input method
                # In a real implementation, you might want to open an external editor
                edited_content = Prompt.ask("Enter your edited content (or press Enter to keep current)")
                if edited_content.strip():
                    current_content = edited_content
                    console.print("✅ Content updated with manual edits")
                else:
                    console.print("ℹ️  No changes made")
            
            elif action == "regenerate":
                if not self.ai_available:
                    console.print("❌ AI not available for regeneration")
                    continue
                
                console.print("🔄 Regenerating content with AI...")
                try:
                    current_content = self.writer.spin_chapter(
                        original_content, style=style, tone=tone
                    )
                    
                    # Store new AI version
                    if ai_id:
                        new_ai_id = self.db.store_ai_generated_content(
                            original_id, current_content, style, tone, version=iteration
                        )
                        console.print(f"💾 New AI version stored with ID: {new_ai_id}")
                    
                    console.print("✅ Content regenerated")
                    
                except Exception as e:
                    console.print(f"❌ Error regenerating content: {e}")
            
            elif action == "review":
                if self.ai_available:
                    console.print("🤖 Getting AI review...")
                    try:
                        review = self.reviewer.review_content(current_content, original_content)
                        self._show_review_summary(review)
                        
                        # Ask if user wants to apply AI suggestions
                        if Confirm.ask("Would you like to apply AI improvement suggestions?"):
                            improved_content = self.reviewer.suggest_improvements(current_content, review)
                            current_content = improved_content
                            console.print("✅ Applied AI improvements")
                    
                    except Exception as e:
                        console.print(f"❌ Error getting AI review: {e}")
                else:
                    console.print("⚠️  AI review not available")
            
            iteration += 1
        
        console.print("⚠️  Maximum iterations reached. Using current content.")
        return current_content
    
    def _show_content_preview(self, title: str, content: str, max_length: int = 500):
        """Display a preview of content"""
        preview = content[:max_length]
        if len(content) > max_length:
            preview += "..."
        
        console.print(Panel(
            preview,
            title=title,
            border_style="blue"
        ))
    
    def _show_review_summary(self, review: Dict[str, Any]):
        """Display review summary"""
        table = Table(title="AI Review Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Score", style="magenta")
        table.add_column("Details", style="green")
        
        table.add_row("Overall Score", str(review.get("overall_score", "N/A")), "")
        table.add_row("Grammar Score", str(review.get("grammar_score", "N/A")), "")
        table.add_row("Style Score", str(review.get("style_score", "N/A")), "")
        table.add_row("Engagement Score", str(review.get("engagement_score", "N/A")), "")
        
        console.print(table)
        
        if review.get("summary"):
            console.print(Panel(review["summary"], title="Review Summary", border_style="yellow"))
        
        if review.get("suggestions"):
            console.print("\n[bold]Suggestions:[/bold]")
            for suggestion in review["suggestions"]:
                console.print(f"• {suggestion}")
    
    def search_published_content(self, query: str):
        """Search through published content"""
        console.print(f"\n[bold]Searching for: {query}[/bold]")
        
        results = self.db.search_content(query, "final_versions", n_results=10)
        
        if not results:
            console.print("No results found.")
            return
        
        table = Table(title="Search Results")
        table.add_column("ID", style="cyan")
        table.add_column("Content Preview", style="green")
        table.add_column("Timestamp", style="yellow")
        
        for result in results:
            preview = result["content"][:100] + "..." if len(result["content"]) > 100 else result["content"]
            timestamp = result["metadata"].get("timestamp", "Unknown")
            table.add_row(result["id"], preview, timestamp)
        
        console.print(table)
    
    def show_content_history(self, content_id: str):
        """Show complete history of content processing"""
        console.print(f"\n[bold]Content History for ID: {content_id}[/bold]")
        
        history = self.db.get_content_history(content_id)
        
        if not history["original"]:
            console.print("❌ Content not found")
            return
        
        # Show original content
        if history["original"]:
            console.print(Panel(
                f"Original Content\n\n{history['original']['content'][:300]}...",
                title="Original Content",
                border_style="blue"
            ))
        
        # Show AI versions
        if history["ai_versions"]:
            console.print(f"\n[bold]AI Versions ({len(history['ai_versions'])})[/bold]")
            for i, version in enumerate(history["ai_versions"], 1):
                console.print(Panel(
                    f"Version {i}\nStyle: {version['metadata'].get('style', 'N/A')}\nTone: {version['metadata'].get('tone', 'N/A')}\n\n{version['content'][:200]}...",
                    title=f"AI Version {i}",
                    border_style="green"
                ))
        
        # Show reviews
        if history["reviews"]:
            console.print(f"\n[bold]Reviews ({len(history['reviews'])})[/bold]")
            for i, review in enumerate(history["reviews"], 1):
                console.print(Panel(
                    f"Review {i}\nScore: {review['metadata'].get('overall_score', 'N/A')}\n\n{review['content']}",
                    title=f"Review {i}",
                    border_style="yellow"
                ))
        
        # Show final version
        if history["final_version"]:
            console.print(Panel(
                f"Final Published Version\n\n{history['final_version']['content'][:300]}...",
                title="Final Version",
                border_style="red"
            ))


@click.group()
def cli():
    """Automated Book Publication Workflow CLI"""
    pass


@cli.command()
@click.option('--url', default='https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1', 
              help='URL to scrape')
@click.option('--style', default='modern', help='Writing style for AI generation')
@click.option('--tone', default='engaging', help='Tone for AI generation')
def publish(url, style, tone):
    """Run the complete publication workflow"""
    workflow = BookPublicationWorkflow()
    asyncio.run(workflow.run_workflow(url, style, tone))


@cli.command()
@click.argument('query')
def search(query):
    """Search published content"""
    workflow = BookPublicationWorkflow()
    workflow.search_published_content(query)


@cli.command()
@click.argument('content_id')
def history(content_id):
    """Show content processing history"""
    workflow = BookPublicationWorkflow()
    workflow.show_content_history(content_id)


@cli.command()
def test():
    """Test the system components"""
    console.print("[bold]Testing System Components[/bold]")
    
    # Test database
    console.print("\n[bold]Testing Database...[/bold]")
    try:
        db = ContentDatabase()
        console.print("✅ Database connection successful")
    except Exception as e:
        console.print(f"❌ Database error: {e}")
    
    # Test AI agents
    console.print("\n[bold]Testing AI Agents...[/bold]")
    try:
        workflow = BookPublicationWorkflow()
        if workflow.ai_available:
            console.print("✅ AI agents available")
        else:
            console.print("⚠️  AI agents not available (check API key)")
    except Exception as e:
        console.print(f"❌ AI agents error: {e}")


if __name__ == "__main__":
    cli() 