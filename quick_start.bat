@echo off
setlocal enabledelayedexpansion

REM AI Book Publication Workflow - Quick Start Script for Windows
REM This script provides easy deployment options

echo.
echo 🚀 AI Book Publication Workflow - Quick Start
echo ==============================================
echo.

REM Function to check if command exists
:check_command
set "command=%~1"
where %command% >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ %command% found
    exit /b 0
) else (
    echo ❌ %command% not found
    exit /b 1
)

REM Function to check Python
:check_python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "python_version=%%i"
    echo ✅ Python !python_version! found
    exit /b 0
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        for /f "tokens=2" %%i in ('python3 --version 2^>^&1') do set "python_version=%%i"
        echo ✅ Python !python_version! found
        exit /b 0
    ) else (
        echo ❌ Python not found. Please install Python 3.8 or higher.
        exit /b 1
    )
)

REM Function to check Docker
:check_docker
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker found
    exit /b 0
) else (
    echo ❌ Docker not found
    exit /b 1
)

REM Function to run with Python
:run_python
echo 🐍 Running with Python...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Install Playwright browsers
echo 🌐 Installing Playwright browsers...
playwright install

REM Run the application
echo 🚀 Starting application...
python run_app.py
goto :eof

REM Function to run with Docker
:run_docker
echo 🐳 Running with Docker...
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Creating .env template...
    (
        echo # Google Generative AI API Key
        echo # Get your API key from: https://makersuite.google.com/app/apikey
        echo GOOGLE_API_KEY=your_api_key_here
    ) > .env
    echo 📝 Please edit .env file and add your Google API key
    echo 🔗 Get API key from: https://makersuite.google.com/app/apikey
    pause
)

REM Build and run with docker-compose
echo 🔨 Building Docker image...
docker-compose build

echo 🚀 Starting services...
docker-compose up -d

echo ✅ Application is running!
echo 🌐 Web Interface: http://localhost:5000
echo 📊 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
goto :eof

REM Function to run with Docker Compose (production)
:run_docker_production
echo 🏭 Running with Docker Compose (Production)...
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found. Please create it first.
    pause
    exit /b 1
)

REM Build and run with production profile
echo 🔨 Building Docker image...
docker-compose --profile production build

echo 🚀 Starting production services...
docker-compose --profile production up -d

echo ✅ Production deployment complete!
echo 🌐 Web Interface: http://localhost
echo 📊 To view logs: docker-compose --profile production logs -f
echo 🛑 To stop: docker-compose --profile production down
goto :eof

REM Function to check system status
:check_status
echo 📊 System Status Check
echo =====================
echo.

REM Check Python
call :check_python
if %errorlevel% equ 0 (
    echo    Python: ✅ Available
) else (
    echo    Python: ❌ Not available
)

REM Check Docker
call :check_docker
if %errorlevel% equ 0 (
    echo    Docker: ✅ Available
) else (
    echo    Docker: ❌ Not available
)

REM Check files
if exist "requirements.txt" (
    echo    Requirements: ✅ Found
) else (
    echo    Requirements: ❌ Missing
)

if exist "Dockerfile" (
    echo    Dockerfile: ✅ Found
) else (
    echo    Dockerfile: ❌ Missing
)

if exist ".env" (
    echo    Environment: ✅ Configured
) else (
    echo    Environment: ⚠️  Not configured
)

echo.
goto :eof

REM Function to clean up
:cleanup
echo 🧹 Cleaning up...
echo.

REM Stop Docker containers
docker-compose down >nul 2>&1
docker-compose --profile production down >nul 2>&1

REM Remove Python cache
echo 🗑️  Removing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" >nul 2>&1
del /s *.pyc >nul 2>&1

REM Remove virtual environment
if exist "venv" (
    echo 🗑️  Removing virtual environment...
    rd /s /q venv >nul 2>&1
)

echo ✅ Cleanup complete!
goto :eof

REM Main menu
:show_menu
echo.
echo Choose deployment method:
echo 1. 🐍 Python (Local development)
echo 2. 🐳 Docker (Development)
echo 3. 🏭 Docker Compose (Production)
echo 4. 📊 Check System Status
echo 5. 🧹 Clean Up
echo 6. 🚪 Exit
echo.

REM Main script
:main
REM Check if we're in the right directory
if not exist "run_app.py" (
    echo ❌ Error: run_app.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

:menu_loop
call :show_menu
set /p choice="Select option (1-6): "

if "%choice%"=="1" (
    call :check_python
    if %errorlevel% equ 0 (
        call :run_python
    ) else (
        echo ❌ Python is required for this option.
    )
) else if "%choice%"=="2" (
    call :check_docker
    if %errorlevel% equ 0 (
        call :run_docker
    ) else (
        echo ❌ Docker is required for this option.
    )
) else if "%choice%"=="3" (
    call :check_docker
    if %errorlevel% equ 0 (
        call :run_docker_production
    ) else (
        echo ❌ Docker is required for this option.
    )
) else if "%choice%"=="4" (
    call :check_status
) else if "%choice%"=="5" (
    call :cleanup
) else if "%choice%"=="6" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid option. Please select 1-6.
)

echo.
pause
goto :menu_loop 