"""
Flask Web Server for AI Book Publication Workflow Frontend
Provides API endpoints and serves the web interface
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from .main import BookPublicationWorkflow
from .scraper import WebScraper
from .db import ContentDatabase
from .ai_agents import AIWriter, AIReviewer, AIEditor

load_dotenv()

app = Flask(__name__, 
            static_folder='../frontend',
            template_folder='../frontend')
CORS(app)

# Initialize workflow components
workflow = None
scraper = None
db = None
writer = None
reviewer = None
editor = None

def initialize_components():
    """Initialize all workflow components"""
    global workflow, scraper, db, writer, reviewer, editor
    
    try:
        scraper = WebScraper()
        db = ContentDatabase()
        
        # Initialize AI agents (will fail gracefully if API key not set)
        try:
            writer = AIWriter()
            reviewer = AIReviewer()
            editor = AIEditor()
            ai_available = True
        except Exception as e:
            print(f"Warning: AI agents not available: {e}")
            ai_available = False
        
        workflow = BookPublicationWorkflow()
        return True
    except Exception as e:
        print(f"Error initializing components: {e}")
        return False

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('../frontend', filename)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    try:
        db_status = db is not None
        ai_status = writer is not None and reviewer is not None and editor is not None
        
        return jsonify({
            'database': db_status,
            'ai': ai_status,
            'status': 'ok'
        })
    except Exception as e:
        return jsonify({
            'database': False,
            'ai': False,
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/test', methods=['POST'])
def test_system():
    """Test system components"""
    try:
        # Test database
        db_status = False
        if db:
            try:
                # Try to create a test collection
                test_content = {
                    "url": "test.com",
                    "title": "Test",
                    "text_content": "Test content",
                    "screenshot_path": "test.png"
                }
                test_id = db.store_original_content(test_content)
                db.delete_content(test_id)
                db_status = True
            except Exception as e:
                print(f"Database test failed: {e}")
        
        # Test AI
        ai_status = False
        if writer and reviewer and editor:
            try:
                # Simple test without making actual API calls
                ai_status = True
            except Exception as e:
                print(f"AI test failed: {e}")
        
        return jsonify({
            'database': db_status,
            'ai': ai_status,
            'status': 'ok'
        })
    except Exception as e:
        return jsonify({
            'database': False,
            'ai': False,
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/scrape', methods=['POST'])
def scrape_content():
    """Scrape content from URL"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not scraper or not db:
            return jsonify({'error': 'Scraper or database not available'}), 500
        
        # Run scraping in async context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(scraper.scrape_content(url))
            
            # Store in database
            content_id = db.store_original_content(result)
            
            return jsonify({
                'id': content_id,
                'title': result['title'],
                'text_content': result['text_content'],
                'screenshot_path': result['screenshot_path'],
                'status': 'success'
            })
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate AI content"""
    try:
        data = request.get_json()
        content = data.get('content')
        style = data.get('style', 'modern')
        tone = data.get('tone', 'engaging')
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        if not writer:
            return jsonify({'error': 'AI Writer not available'}), 500
        
        # Generate AI content
        ai_content = writer.spin_chapter(content, style=style, tone=tone)
        
        return jsonify({
            'content': ai_content,
            'style': style,
            'tone': tone,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/publish', methods=['POST'])
def publish_content():
    """Publish final content"""
    try:
        data = request.get_json()
        content = data.get('content')
        original_id = data.get('original_id')
        
        if not content or not original_id:
            return jsonify({'error': 'Content and original_id are required'}), 400
        
        if not db:
            return jsonify({'error': 'Database not available'}), 500
        
        # Store final version
        final_id = db.store_final_version(original_id, content)
        
        return jsonify({
            'final_id': final_id,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_content():
    """Search published content"""
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not db:
            return jsonify({'error': 'Database not available'}), 500
        
        # Search content
        results = db.search_content(query, "final_versions", n_results=10)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET', 'POST'])
def get_history():
    """Get workflow history"""
    try:
        if not db:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get content from all collections
        history = []
        
        # Get original content
        try:
            original_results = db.original_content.get()
            if original_results and 'ids' in original_results:
                for i, content_id in enumerate(original_results['ids']):
                    metadata = original_results['metadatas'][i] if original_results['metadatas'] else {}
                    content = original_results['documents'][i] if original_results['documents'] else ""
                    
                    # Parse full data if available
                    full_data = {}
                    if 'full_data' in metadata and metadata['full_data']:
                        try:
                            full_data = json.loads(str(metadata['full_data']))
                        except:
                            pass
                    
                    history.append({
                        'id': content_id,
                        'title': metadata.get('title', full_data.get('title', 'Untitled')),
                        'description': content[:100] + '...' if content else 'No description',
                        'status': 'completed',
                        'timestamp': metadata.get('timestamp', ''),
                        'input': {
                            'url': metadata.get('url', full_data.get('url', '')),
                            'topic': full_data.get('topic', '')
                        },
                        'results': {
                            'scraped_content': content,
                            'ai_content': full_data.get('ai_content', ''),
                            'review': full_data.get('review', '')
                        },
                        'duration': 'N/A',
                        'steps': []
                    })
        except Exception as e:
            print(f"Error getting original content: {e}")
        
        # Get AI generated content
        try:
            ai_results = db.ai_generated.get()
            if ai_results and 'ids' in ai_results:
                for i, content_id in enumerate(ai_results['ids']):
                    metadata = ai_results['metadatas'][i] if ai_results['metadatas'] else {}
                    content = ai_results['documents'][i] if ai_results['documents'] else ""
                    
                    history.append({
                        'id': content_id,
                        'title': f"AI Generated - {metadata.get('style', 'Unknown')} Style",
                        'description': content[:100] + '...' if content else 'No description',
                        'status': 'completed',
                        'timestamp': metadata.get('timestamp', ''),
                        'input': {
                            'url': '',
                            'topic': ''
                        },
                        'results': {
                            'scraped_content': '',
                            'ai_content': content,
                            'review': ''
                        },
                        'duration': 'N/A',
                        'steps': []
                    })
        except Exception as e:
            print(f"Error getting AI content: {e}")
        
        return jsonify({
            'history': history,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<content_id>', methods=['DELETE'])
def delete_history_item(content_id):
    """Delete a specific history item"""
    try:
        if not db:
            return jsonify({'error': 'Database not available'}), 500
        
        # Try to delete from all collections
        success = False
        for collection_name in ['original_content', 'ai_generated', 'reviews', 'final_versions']:
            try:
                if db.delete_content(content_id, collection_name):
                    success = True
                    break
            except:
                continue
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Content not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear all history"""
    try:
        if not db:
            return jsonify({'error': 'Database not available'}), 500
        
        # Clear all collections
        for collection_name in ['original_content', 'ai_generated', 'reviews', 'final_versions']:
            try:
                collection = getattr(db, collection_name, None)
                if collection:
                    # Get all IDs and delete them
                    results = collection.get()
                    if results['ids']:
                        collection.delete(ids=results['ids'])
            except Exception as e:
                print(f"Error clearing {collection_name}: {e}")
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET', 'PUT', 'POST'])
def manage_settings():
    """Get or update settings"""
    try:
        if request.method == 'GET':
            # Return current settings
            settings = {
                'apiKey': os.getenv('GOOGLE_API_KEY', ''),
                'maxTokens': 1000,
                'temperature': 0.7,
                'model': 'gemini-pro',
                'databasePath': './chroma_db',
                'enableLogging': True,
                'autoSave': True
            }
            return jsonify({'settings': settings, 'status': 'success'})
        
        elif request.method in ['PUT', 'POST']:
            # Update settings
            data = request.get_json()
            
            # Update environment variables if API key is provided
            if 'apiKey' in data and data['apiKey']:
                os.environ['GOOGLE_API_KEY'] = data['apiKey']
                
                # Update .env file
                env_path = Path('.env')
                if env_path.exists():
                    with open(env_path, 'r') as f:
                        lines = f.readlines()
                    
                    # Update or add GOOGLE_API_KEY
                    api_key_found = False
                    for i, line in enumerate(lines):
                        if line.startswith('GOOGLE_API_KEY='):
                            lines[i] = f"GOOGLE_API_KEY={data['apiKey']}\n"
                            api_key_found = True
                            break
                    
                    if not api_key_found:
                        lines.append(f"GOOGLE_API_KEY={data['apiKey']}\n")
                    
                    with open(env_path, 'w') as f:
                        f.writelines(lines)
                else:
                    # Create .env file
                    with open(env_path, 'w') as f:
                        f.write(f"GOOGLE_API_KEY={data['apiKey']}\n")
            
            return jsonify({'settings': data, 'status': 'success'})
        
        # Default response for unsupported methods
        return jsonify({'error': 'Method not allowed'}), 405
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings/test-connection', methods=['POST'])
def test_connection():
    """Test database connection"""
    try:
        if not db:
            return jsonify({
                'connected': False,
                'message': 'Database not initialized'
            }), 500
        
        # Test database connection
        try:
            # Try to create a test collection
            test_content = {
                "url": "test.com",
                "title": "Test",
                "text_content": "Test content",
                "screenshot_path": "test.png"
            }
            test_id = db.store_original_content(test_content)
            db.delete_content(test_id)
            
            return jsonify({
                'connected': True,
                'message': 'Database connection successful'
            })
        except Exception as e:
            return jsonify({
                'connected': False,
                'message': f'Database connection failed: {str(e)}'
            })
        
    except Exception as e:
        return jsonify({
            'connected': False,
            'message': f'Connection test failed: {str(e)}'
        }), 500

@app.route('/api/workflow', methods=['POST'])
def run_workflow():
    """Run the complete publication workflow"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        topic = data.get('topic', '')
        
        if not url and not topic:
            return jsonify({'error': 'Either URL or topic is required'}), 400
        
        if not workflow or not scraper or not db:
            return jsonify({'error': 'Workflow components not available'}), 500
        
        # Run workflow using the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            if url:
                result = loop.run_until_complete(workflow.run_workflow(url))
            else:
                # For topic-based generation, we'll need to implement this
                result = {'error': 'Topic-based generation not yet implemented'}
            
            return jsonify(result)
        finally:
            loop.close()
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Run the Flask development server"""
    print("Initializing AI Book Publication Workflow Web Server...")
    
    if not initialize_components():
        print("Warning: Some components failed to initialize")
    
    print("Starting web server on http://localhost:5000")
    print("Open your browser and navigate to http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 