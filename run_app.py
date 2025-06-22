#!/usr/bin/env python3
"""
Comprehensive Launcher for AI Book Publication Workflow
Handles setup, dependencies, and launches the application
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    AI Book Publication Workflow              ║
║                                                              ║
║  🚀 Automated content creation with AI-powered writing      ║
║  📚 Web scraping, content spinning, and human review        ║
║  🎯 Complete workflow from URL to published content         ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        
        # Install Playwright browsers
        print("🌐 Installing Playwright browsers...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("✅ Playwright browsers installed")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def check_environment():
    """Check and setup environment"""
    print("\n🔧 Checking environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  No .env file found. Creating template...")
        with open(env_file, "w") as f:
            f.write("# Google Generative AI API Key\n")
            f.write("# Get your API key from: https://makersuite.google.com/app/apikey\n")
            f.write("GOOGLE_API_KEY=your_api_key_here\n")
        print("✅ Created .env template")
        print("📝 Please edit .env file and add your Google API key")
    else:
        print("✅ .env file found")
    
    # Create output directories
    Path("output/screenshots").mkdir(parents=True, exist_ok=True)
    print("✅ Output directories created")

def test_installation():
    """Test if everything is working"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import chromadb
        print("✅ ChromaDB imported successfully")
        
        import playwright
        print("✅ Playwright imported successfully")
        
        # Test database
        from app.db import ContentDatabase
        db = ContentDatabase()
        print("✅ Database connection successful")
        
        # Test scraper
        from app.scraper import WebScraper
        scraper = WebScraper()
        print("✅ Web scraper initialized successfully")
        
        print("✅ All components working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def show_menu():
    """Show main menu"""
    menu = """
╔══════════════════════════════════════════════════════════════╗
║                        MAIN MENU                            ║
╠══════════════════════════════════════════════════════════════╣
║  1. 🌐 Launch Web Interface (Recommended)                   ║
║  2. 🖥️  Run CLI Workflow                                     ║
║  3. 🧪 Run Tests                                             ║
║  4. 📊 View System Status                                   ║
║  5. 🔧 Setup & Configuration                                ║
║  6. 📚 View Documentation                                   ║
║  7. 🚪 Exit                                                 ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(menu)

def launch_web_interface():
    """Launch the web interface"""
    print("\n🌐 Launching Web Interface...")
    print("📱 Opening browser to http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        # Open browser
        if platform.system() == "Windows":
            os.system("start http://localhost:5000")
        elif platform.system() == "Darwin":  # macOS
            os.system("open http://localhost:5000")
        else:  # Linux
            os.system("xdg-open http://localhost:5000")
        
        # Start web server
        from app.web_server import main
        main()
        
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped")
    except Exception as e:
        print(f"❌ Error launching web interface: {e}")

def run_cli_workflow():
    """Run CLI workflow"""
    print("\n🖥️  Running CLI Workflow...")
    
    try:
        # Run the main CLI
        from app.main import cli
        cli()
    except Exception as e:
        print(f"❌ Error running CLI workflow: {e}")

def run_tests():
    """Run all tests"""
    print("\n🧪 Running Tests...")
    
    tests = [
        ("Database Test", "python app/db.py"),
        ("Scraper Test", "python app/scraper.py"),
        ("Installation Test", "python test_installation.py"),
        ("Demo Test", "python demo.py")
    ]
    
    for test_name, command in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")

def show_system_status():
    """Show system status"""
    print("\n📊 System Status:")
    
    # Check Python
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Check OS
    print(f"💻 OS: {platform.system()} {platform.release()}")
    
    # Check dependencies
    try:
        import chromadb
        print("✅ ChromaDB: Installed")
    except ImportError:
        print("❌ ChromaDB: Not installed")
    
    try:
        import playwright
        print("✅ Playwright: Installed")
    except ImportError:
        print("❌ Playwright: Not installed")
    
    try:
        import google.generativeai
        print("✅ Google Generative AI: Installed")
    except ImportError:
        print("❌ Google Generative AI: Not installed")
    
    # Check files
    files_to_check = [
        (".env", "Environment Configuration"),
        ("requirements.txt", "Dependencies List"),
        ("app/main.py", "Main Application"),
        ("frontend/index.html", "Web Interface")
    ]
    
    for file_path, description in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {description}: Found")
        else:
            print(f"❌ {description}: Missing")

def show_documentation():
    """Show documentation"""
    print("\n📚 Documentation:")
    print("📖 README.md - Complete project documentation")
    print("🌐 Web Interface - http://localhost:5000 (when running)")
    print("🔗 Google API Setup - https://makersuite.google.com/app/apikey")
    print("📧 Support - Check README.md for troubleshooting")

def setup_configuration():
    """Setup and configuration"""
    print("\n🔧 Setup & Configuration:")
    
    # Check API key
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
            if "your_api_key_here" in content:
                print("⚠️  Please set your Google API key in .env file")
                print("🔗 Get API key from: https://makersuite.google.com/app/apikey")
            else:
                print("✅ API key configured")
    
    # Install dependencies if needed
    response = input("\n📦 Install/Update dependencies? (y/n): ").lower()
    if response == 'y':
        install_dependencies()
    
    # Test installation
    response = input("\n🧪 Run installation test? (y/n): ").lower()
    if response == 'y':
        test_installation()

def main():
    """Main launcher function"""
    print_banner()
    check_python_version()
    
    # Check if this is first run
    if not Path(".env").exists():
        print("\n🎉 Welcome! This appears to be your first run.")
        print("Let's set up your environment...")
        install_dependencies()
        check_environment()
        
        if not test_installation():
            print("❌ Setup failed. Please check the errors above.")
            sys.exit(1)
        
        print("\n🎉 Setup complete! You can now use the application.")
    
    while True:
        show_menu()
        choice = input("\nSelect an option (1-7): ").strip()
        
        if choice == '1':
            launch_web_interface()
        elif choice == '2':
            run_cli_workflow()
        elif choice == '3':
            run_tests()
        elif choice == '4':
            show_system_status()
        elif choice == '5':
            setup_configuration()
        elif choice == '6':
            show_documentation()
        elif choice == '7':
            print("\n👋 Thank you for using AI Book Publication Workflow!")
            break
        else:
            print("❌ Invalid choice. Please select 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 