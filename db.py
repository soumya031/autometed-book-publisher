"""
Database Module for Automated Book Publication Workflow
Handles content versioning and storage using ChromaDB
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import chromadb
from chromadb.config import Settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentDatabase:
    """Database manager for content versioning and storage"""
    
    def __init__(self, db_path: str = "chroma_db"):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Create collections for different content types
        self.original_content = self.client.get_or_create_collection("original_content")
        self.ai_generated = self.client.get_or_create_collection("ai_generated")
        self.reviews = self.client.get_or_create_collection("reviews")
        self.final_versions = self.client.get_or_create_collection("final_versions")
        
    def store_original_content(self, content_data: Dict[str, Any]) -> str:
        """
        Store original scraped content
        
        Args:
            content_data: Dictionary containing content and metadata
            
        Returns:
            Content ID
        """
        content_id = str(uuid.uuid4())
        
        # Store the full content data as metadata
        metadata = {
            "url": content_data.get("url", ""),
            "title": content_data.get("title", ""),
            "screenshot_path": content_data.get("screenshot_path", ""),
            "timestamp": datetime.now().isoformat(),
            "content_type": "original",
            "full_data": json.dumps(content_data)
        }
        
        # Store the text content as the document
        text_content = content_data.get("text_content", "")
        
        self.original_content.add(
            documents=[text_content],
            metadatas=[metadata],
            ids=[content_id]
        )
        
        logger.info(f"Stored original content with ID: {content_id}")
        return content_id
    
    def store_ai_generated_content(self, original_id: str, content: str, 
                                 style: str, tone: str, version: int = 1) -> str:
        """
        Store AI-generated content
        
        Args:
            original_id: ID of the original content
            content: AI-generated content
            style: Writing style used
            tone: Tone used
            version: Version number
            
        Returns:
            Generated content ID
        """
        content_id = str(uuid.uuid4())
        
        metadata = {
            "original_id": original_id,
            "style": style,
            "tone": tone,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "content_type": "ai_generated"
        }
        
        self.ai_generated.add(
            documents=[content],
            metadatas=[metadata],
            ids=[content_id]
        )
        
        logger.info(f"Stored AI-generated content with ID: {content_id}")
        return content_id
    
    def store_review(self, content_id: str, review_data: Dict[str, Any]) -> str:
        """
        Store review feedback
        
        Args:
            content_id: ID of the content being reviewed
            review_data: Review feedback and scores
            
        Returns:
            Review ID
        """
        review_id = str(uuid.uuid4())
        
        metadata = {
            "content_id": content_id,
            "overall_score": review_data.get("overall_score", 0),
            "grammar_score": review_data.get("grammar_score", 0),
            "style_score": review_data.get("style_score", 0),
            "engagement_score": review_data.get("engagement_score", 0),
            "timestamp": datetime.now().isoformat(),
            "content_type": "review",
            "full_review": json.dumps(review_data)
        }
        
        # Create a document from the review summary
        review_doc = review_data.get("summary", "Review completed")
        
        self.reviews.add(
            documents=[review_doc],
            metadatas=[metadata],
            ids=[review_id]
        )
        
        logger.info(f"Stored review with ID: {review_id}")
        return review_id
    
    def store_final_version(self, content_id: str, final_content: str, 
                          requirements: Optional[Dict[str, Any]] = None) -> str:
        """
        Store final approved version
        
        Args:
            content_id: ID of the content being finalized
            final_content: Final approved content
            requirements: Publication requirements (optional)
            
        Returns:
            Final version ID
        """
        final_id = str(uuid.uuid4())
        
        metadata = {
            "content_id": content_id,
            "requirements": json.dumps(requirements) if requirements else "",
            "timestamp": datetime.now().isoformat(),
            "content_type": "final_version",
            "status": "published"
        }
        
        self.final_versions.add(
            documents=[final_content],
            metadatas=[metadata],
            ids=[final_id]
        )
        
        logger.info(f"Stored final version with ID: {final_id}")
        return final_id
    
    def get_content_by_id(self, content_id: str, collection_name: str = "original_content") -> Optional[Dict[str, Any]]:
        """
        Retrieve content by ID
        
        Args:
            content_id: Content ID
            collection_name: Name of the collection to search
            
        Returns:
            Content data or None if not found
        """
        collection = getattr(self, collection_name, None)
        if not collection:
            logger.error(f"Collection {collection_name} not found")
            return None
        
        try:
            result = collection.get(ids=[content_id])
            if result['ids']:
                return {
                    "id": result['ids'][0],
                    "content": result['documents'][0],
                    "metadata": result['metadatas'][0]
                }
        except Exception as e:
            logger.error(f"Error retrieving content: {e}")
        
        return None
    
    def search_content(self, query: str, collection_name: str = "original_content", 
                      n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search content using semantic search
        
        Args:
            query: Search query
            collection_name: Name of the collection to search
            n_results: Number of results to return
            
        Returns:
            List of matching content
        """
        collection = getattr(self, collection_name, None)
        if not collection:
            logger.error(f"Collection {collection_name} not found")
            return []
        
        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            matches = []
            for i in range(len(results['ids'][0])):
                matches.append({
                    "id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
            
            return matches
        except Exception as e:
            logger.error(f"Error searching content: {e}")
            return []
    
    def get_content_history(self, original_id: str) -> Dict[str, Any]:  # type: ignore
        """
        Get complete history of content processing
        
        Args:
            original_id: ID of the original content
            
        Returns:
            Dictionary containing all versions and reviews
        """
        history = {
            "original": None,
            "ai_versions": [],
            "reviews": [],
            "final_version": None
        }
        
        # Get original content
        original = self.get_content_by_id(original_id, "original_content")
        if original:
            history["original"] = original
        
        # Get AI-generated versions
        try:
            ai_results = self.ai_generated.get(
                where={"original_id": original_id}
            )
            if ai_results and ai_results['ids']:
                ai_results = ai_results  # type: ignore
                for i in range(len(ai_results['ids'])):
                    history["ai_versions"].append({
                        "id": ai_results['ids'][i],  # type: ignore
                        "content": ai_results['documents'][i],  # type: ignore
                        "metadata": ai_results['metadatas'][i]  # type: ignore
                    })
        except Exception as e:
            logger.error(f"Error retrieving AI versions: {e}")
        
        # Get reviews
        try:
            review_results = self.reviews.get(
                where={"content_id": original_id}
            )
            if review_results and review_results['ids']:
                review_results = review_results  # type: ignore
                for i in range(len(review_results['ids'])):
                    history["reviews"].append({
                        "id": review_results['ids'][i],  # type: ignore
                        "content": review_results['documents'][i],  # type: ignore
                        "metadata": review_results['metadatas'][i]  # type: ignore
                    })
        except Exception as e:
            logger.error(f"Error retrieving reviews: {e}")
        
        # Get final version
        try:
            final_results = self.final_versions.get(
                where={"content_id": original_id}
            )
            if final_results and final_results['ids']:
                final_results = final_results  # type: ignore
                history["final_version"] = {
                    "id": final_results['ids'][0],  # type: ignore
                    "content": final_results['documents'][0],  # type: ignore
                    "metadata": final_results['metadatas'][0]  # type: ignore
                }
        except Exception as e:
            logger.error(f"Error retrieving final version: {e}")
        
        return history
    
    def delete_content(self, content_id: str, collection_name: str = "original_content") -> bool:
        """
        Delete content by ID
        
        Args:
            content_id: Content ID to delete
            collection_name: Name of the collection
            
        Returns:
            True if successful, False otherwise
        """
        collection = getattr(self, collection_name, None)
        if not collection:
            logger.error(f"Collection {collection_name} not found")
            return False
        
        try:
            collection.delete(ids=[content_id])
            logger.info(f"Deleted content with ID: {content_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting content: {e}")
            return False


def main():
    """Test the database functionality"""
    db = ContentDatabase()
    
    # Test storing original content
    test_content = {
        "url": "https://example.com",
        "title": "Test Chapter",
        "text_content": "This is a test chapter content.",
        "screenshot_path": "test.png"
    }
    
    original_id = db.store_original_content(test_content)
    print(f"Stored original content with ID: {original_id}")
    
    # Test storing AI-generated content
    ai_content = "This is an AI-generated version of the test chapter."
    ai_id = db.store_ai_generated_content(original_id, ai_content, "modern", "engaging")
    print(f"Stored AI content with ID: {ai_id}")
    
    # Test storing review
    review_data = {
        "overall_score": 8,
        "strengths": ["Good flow", "Clear writing"],
        "weaknesses": ["Could use more detail"],
        "suggestions": ["Add more descriptive language"],
        "grammar_score": 9,
        "style_score": 8,
        "engagement_score": 7,
        "summary": "Overall good content with room for improvement"
    }
    review_id = db.store_review(ai_id, review_data)
    print(f"Stored review with ID: {review_id}")
    
    # Test retrieving content
    retrieved = db.get_content_by_id(original_id)
    if retrieved:
        print(f"Retrieved content: {retrieved['content'][:50]}...")
    else:
        print("No content retrieved")
    
    # Test search
    search_results = db.search_content("test chapter")
    print(f"Search results: {len(search_results)} found")
    
    # Test getting history
    history = db.get_content_history(original_id)
    print(f"Content history: {len(history['ai_versions'])} AI versions, {len(history['reviews'])} reviews")


if __name__ == "__main__":
    main() 