"""
AI Agents Module for Automated Book Publication Workflow
Handles AI writing, reviewing, and editing using Google's Generative AI
"""

import os
import json
from typing import Dict, Any, List, Optional
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIWriter:
    """AI Writer agent for content spinning and rewriting"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        configure(api_key=self.api_key)
        self.model = GenerativeModel('gemini-1.5-pro')
        
    def spin_chapter(self, original_content: str, style: str = "modern", tone: str = "engaging") -> str:
        """
        Spin/rewrite a chapter with AI
        
        Args:
            original_content: Original text content
            style: Writing style (modern, classic, poetic, etc.)
            tone: Tone of the writing (engaging, formal, casual, etc.)
            
        Returns:
            AI-generated rewritten content
        """
        prompt = f"""
        You are an AI writer tasked with rewriting a chapter from a book. 
        Please rewrite the following content in a {style} style with a {tone} tone.
        
        Original content:
        {original_content}
        
        Instructions:
        1. Maintain the core story and plot points
        2. Improve readability and flow
        3. Add engaging descriptions where appropriate
        4. Keep the same chapter structure
        5. Make the writing more {style} and {tone}
        
        Please provide the rewritten chapter:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error in AI writing: {e}")
            return original_content


class AIReviewer:
    """AI Reviewer agent for content review and feedback"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        configure(api_key=self.api_key)
        self.model = GenerativeModel('gemini-pro')
        
    def review_content(self, content: str, original_content: str = "") -> Dict[str, Any]:
        """
        Review content and provide feedback
        
        Args:
            content: Content to review
            original_content: Original content for comparison (optional)
            
        Returns:
            Dictionary containing review feedback and suggestions
        """
        prompt = f"""
        You are an AI reviewer tasked with reviewing a rewritten chapter. 
        Please provide a comprehensive review of the following content.
        
        Content to review:
        {content}
        
        {f"Original content for comparison:\n{original_content}" if original_content else ""}
        
        Please provide a review in the following JSON format:
        {{
            "overall_score": 1-10,
            "strengths": ["list", "of", "strengths"],
            "weaknesses": ["list", "of", "weaknesses"],
            "suggestions": ["list", "of", "improvement", "suggestions"],
            "grammar_score": 1-10,
            "style_score": 1-10,
            "engagement_score": 1-10,
            "summary": "brief summary of the review"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Try to parse JSON response
            try:
                review_data = json.loads(response.text)
                return review_data
            except json.JSONDecodeError:
                # If JSON parsing fails, return a structured response
                return {
                    "overall_score": 7,
                    "strengths": ["Content is readable"],
                    "weaknesses": ["Could not parse AI response properly"],
                    "suggestions": ["Review the content manually"],
                    "grammar_score": 7,
                    "style_score": 7,
                    "engagement_score": 7,
                    "summary": "AI review completed but response format was unexpected",
                    "raw_response": response.text
                }
        except Exception as e:
            logger.error(f"Error in AI review: {e}")
            return {
                "overall_score": 5,
                "strengths": [],
                "weaknesses": ["AI review failed"],
                "suggestions": ["Manual review required"],
                "grammar_score": 5,
                "style_score": 5,
                "engagement_score": 5,
                "summary": f"Review failed due to error: {e}"
            }
    
    def suggest_improvements(self, content: str, review_feedback: Dict[str, Any]) -> str:
        """
        Generate improvement suggestions based on review feedback
        
        Args:
            content: Original content
            review_feedback: Feedback from review
            
        Returns:
            Improved version of the content
        """
        prompt = f"""
        You are an AI editor. Based on the following review feedback, please improve the content.
        
        Original content:
        {content}
        
        Review feedback:
        {json.dumps(review_feedback, indent=2)}
        
        Please provide an improved version that addresses the weaknesses and incorporates the suggestions:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error in AI improvement: {e}")
            return content


class AIEditor:
    """AI Editor agent for final content refinement"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        configure(api_key=self.api_key)
        self.model = GenerativeModel('gemini-pro')
        
    def finalize_content(self, content: str, requirements: Optional[Dict[str, Any]] = None) -> str:
        """
        Finalize content for publication
        
        Args:
            content: Content to finalize
            requirements: Publication requirements (optional)
            
        Returns:
            Finalized content ready for publication
        """
        requirements = requirements or {}
        
        prompt = f"""
        You are an AI editor performing final review and preparation for publication.
        Please finalize the following content for publication.
        
        Content to finalize:
        {content}
        
        Publication requirements:
        {json.dumps(requirements, indent=2) if requirements else "Standard publication format"}
        
        Please provide the finalized content that is:
        1. Grammatically correct
        2. Well-formatted
        3. Ready for publication
        4. Consistent in style and tone
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error in AI finalization: {e}")
            return content


def main():
    """Test the AI agents"""
    # Note: This requires GOOGLE_API_KEY to be set
    try:
        writer = AIWriter()
        reviewer = AIReviewer()
        editor = AIEditor()
        
        test_content = "This is a test chapter content for the AI agents."
        
        print("Testing AI Writer...")
        spun_content = writer.spin_chapter(test_content, style="modern", tone="engaging")
        print(f"Spun content: {spun_content[:100]}...")
        
        print("\nTesting AI Reviewer...")
        review = reviewer.review_content(spun_content, test_content)
        print(f"Review: {review}")
        
        print("\nTesting AI Editor...")
        finalized = editor.finalize_content(spun_content)
        print(f"Finalized: {finalized[:100]}...")
        
    except Exception as e:
        print(f"Error testing AI agents: {e}")
        print("Make sure GOOGLE_API_KEY environment variable is set.")


if __name__ == "__main__":
    main() 