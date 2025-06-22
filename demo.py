#!/usr/bin/env python3
"""
Demo script for Automated Book Publication Workflow
Shows how to use the system programmatically
"""

import asyncio
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

# Import our workflow
from app import BookPublicationWorkflow

console = Console()

def demo_workflow():
    """Demonstrate the complete workflow"""
    console.print(Panel.fit("📚 Automated Book Publication Workflow Demo", style="bold blue"))
    
    # Initialize the workflow
    console.print("\n[bold]Initializing workflow...[/bold]")
    workflow = BookPublicationWorkflow()
    
    if not workflow.ai_available:
        console.print("[yellow]⚠️  AI agents not available. Running in scraping-only mode.[/yellow]")
        console.print("To enable AI features, set your GOOGLE_API_KEY environment variable.")
    
    # Demo URL
    demo_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    
    console.print(f"\n[bold]Demo URL:[/bold] {demo_url}")
    console.print("[bold]Writing Style:[/bold] modern")
    console.print("[bold]Tone:[/bold] engaging")
    
    if Confirm.ask("\nWould you like to run the complete workflow?"):
        try:
            # Run the workflow
            result = asyncio.run(workflow.run_workflow(
                url=demo_url,
                style="modern",
                tone="engaging"
            ))
            
            if result:
                console.print(Panel.fit(
                    f"🎉 Demo completed successfully!\n\n"
                    f"Original ID: {result['original_id']}\n"
                    f"AI ID: {result.get('ai_id', 'N/A')}\n"
                    f"Final ID: {result['final_id']}",
                    style="bold green"
                ))
                
                # Show how to search and view history
                console.print("\n[bold]Next steps you can try:[/bold]")
                console.print("1. Search content: python -m app.main search 'your query'")
                console.print(f"2. View history: python -m app.main history {result['original_id']}")
                console.print("3. Run another workflow with different parameters")
                
            else:
                console.print("❌ Demo workflow was cancelled or failed")
                
        except Exception as e:
            console.print(f"❌ Error running demo: {e}")
            console.print("\nTroubleshooting:")
            console.print("1. Check your internet connection")
            console.print("2. Ensure all dependencies are installed")
            console.print("3. Check if the demo URL is accessible")
    else:
        console.print("Demo cancelled by user")

def demo_search():
    """Demonstrate content search functionality"""
    console.print(Panel.fit("🔍 Content Search Demo", style="bold green"))
    
    workflow = BookPublicationWorkflow()
    
    # Example search queries
    search_queries = [
        "morning",
        "chapter",
        "story",
        "adventure"
    ]
    
    for query in search_queries:
        console.print(f"\n[bold]Searching for:[/bold] {query}")
        workflow.search_published_content(query)
        
        if not Confirm.ask("Continue to next search?"):
            break

def demo_history():
    """Demonstrate content history functionality"""
    console.print(Panel.fit("📖 Content History Demo", style="bold yellow"))
    
    workflow = BookPublicationWorkflow()
    
    # This would typically be a real content ID from a previous run
    # For demo purposes, we'll show the interface
    console.print("To view content history, you need a content ID from a previous workflow run.")
    console.print("Example: python -m app.main history <content_id>")
    
    # Try to find some content to show history for
    results = workflow.db.search_content("", "original_content", n_results=1)
    if results:
        content_id = results[0]["id"]
        console.print(f"\nFound content with ID: {content_id}")
        if Confirm.ask("Show history for this content?"):
            workflow.show_content_history(content_id)
    else:
        console.print("No content found in database. Run a workflow first to see history.")

def main():
    """Main demo menu"""
    console.print("🚀 Welcome to the Automated Book Publication Workflow Demo!")
    
    while True:
        console.print("\n[bold]Available demos:[/bold]")
        console.print("1. Complete Workflow Demo")
        console.print("2. Content Search Demo")
        console.print("3. Content History Demo")
        console.print("4. Exit")
        
        choice = input("\nSelect a demo (1-4): ").strip()
        
        if choice == "1":
            demo_workflow()
        elif choice == "2":
            demo_search()
        elif choice == "3":
            demo_history()
        elif choice == "4":
            console.print("👋 Thanks for trying the demo!")
            break
        else:
            console.print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()