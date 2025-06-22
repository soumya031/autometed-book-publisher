#!/bin/bash

# AI Book Publication Workflow - Quick Start Script
# This script provides easy deployment options

set -e

echo "🚀 AI Book Publication Workflow - Quick Start"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        echo "✅ Python $python_version found"
        return 0
    elif command_exists python; then
        python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        echo "✅ Python $python_version found"
        return 0
    else
        echo "❌ Python not found. Please install Python 3.8 or higher."
        return 1
    fi
}

# Function to check Docker
check_docker() {
    if command_exists docker; then
        echo "✅ Docker found"
        return 0
    else
        echo "❌ Docker not found"
        return 1
    fi
}

# Function to run with Python
run_python() {
    echo "🐍 Running with Python..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    # Install Playwright browsers
    echo "🌐 Installing Playwright browsers..."
    playwright install
    
    # Run the application
    echo "🚀 Starting application..."
    python run_app.py
}

# Function to run with Docker
run_docker() {
    echo "🐳 Running with Docker..."
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo "⚠️  Creating .env template..."
        cat > .env << EOF
# Google Generative AI API Key
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_api_key_here
EOF
        echo "📝 Please edit .env file and add your Google API key"
        echo "🔗 Get API key from: https://makersuite.google.com/app/apikey"
        read -p "Press Enter after setting your API key..."
    fi
    
    # Build and run with docker-compose
    echo "🔨 Building Docker image..."
    docker-compose build
    
    echo "🚀 Starting services..."
    docker-compose up -d
    
    echo "✅ Application is running!"
    echo "🌐 Web Interface: http://localhost:5000"
    echo "📊 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
}

# Function to run with Docker Compose (production)
run_docker_production() {
    echo "🏭 Running with Docker Compose (Production)..."
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo "❌ .env file not found. Please create it first."
        exit 1
    fi
    
    # Build and run with production profile
    echo "🔨 Building Docker image..."
    docker-compose --profile production build
    
    echo "🚀 Starting production services..."
    docker-compose --profile production up -d
    
    echo "✅ Production deployment complete!"
    echo "🌐 Web Interface: http://localhost"
    echo "📊 To view logs: docker-compose --profile production logs -f"
    echo "🛑 To stop: docker-compose --profile production down"
}

# Main menu
show_menu() {
    echo ""
    echo "Choose deployment method:"
    echo "1. 🐍 Python (Local development)"
    echo "2. 🐳 Docker (Development)"
    echo "3. 🏭 Docker Compose (Production)"
    echo "4. 📊 Check System Status"
    echo "5. 🧹 Clean Up"
    echo "6. 🚪 Exit"
    echo ""
}

# Check system status
check_status() {
    echo "📊 System Status Check"
    echo "====================="
    
    # Check Python
    if check_python; then
        echo "   Python: ✅ Available"
    else
        echo "   Python: ❌ Not available"
    fi
    
    # Check Docker
    if check_docker; then
        echo "   Docker: ✅ Available"
    else
        echo "   Docker: ❌ Not available"
    fi
    
    # Check files
    if [ -f "requirements.txt" ]; then
        echo "   Requirements: ✅ Found"
    else
        echo "   Requirements: ❌ Missing"
    fi
    
    if [ -f "Dockerfile" ]; then
        echo "   Dockerfile: ✅ Found"
    else
        echo "   Dockerfile: ❌ Missing"
    fi
    
    if [ -f ".env" ]; then
        echo "   Environment: ✅ Configured"
    else
        echo "   Environment: ⚠️  Not configured"
    fi
    
    echo ""
}

# Clean up function
cleanup() {
    echo "🧹 Cleaning up..."
    
    # Stop Docker containers
    if command_exists docker-compose; then
        echo "🛑 Stopping Docker containers..."
        docker-compose down 2>/dev/null || true
        docker-compose --profile production down 2>/dev/null || true
    fi
    
    # Remove Python cache
    echo "🗑️  Removing Python cache..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove virtual environment
    if [ -d "venv" ]; then
        echo "🗑️  Removing virtual environment..."
        rm -rf venv
    fi
    
    echo "✅ Cleanup complete!"
}

# Main script
main() {
    # Check if we're in the right directory
    if [ ! -f "run_app.py" ]; then
        echo "❌ Error: run_app.py not found. Please run this script from the project root directory."
        exit 1
    fi
    
    while true; do
        show_menu
        read -p "Select option (1-6): " choice
        
        case $choice in
            1)
                if check_python; then
                    run_python
                else
                    echo "❌ Python is required for this option."
                fi
                ;;
            2)
                if check_docker; then
                    run_docker
                else
                    echo "❌ Docker is required for this option."
                fi
                ;;
            3)
                if check_docker; then
                    run_docker_production
                else
                    echo "❌ Docker is required for this option."
                fi
                ;;
            4)
                check_status
                ;;
            5)
                cleanup
                ;;
            6)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid option. Please select 1-6."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main 