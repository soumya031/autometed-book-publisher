# AI-Powered Automated Book Publication Workflow

A comprehensive system for automated book publication featuring web scraping, AI-driven content generation, human-in-the-loop review, and a modern web interface.

---

## 📋 Quick Command Reference

| Task                        | Windows Command(s)                                 | Linux/macOS Command(s)                  |
|-----------------------------|---------------------------------------------------|-----------------------------------------|
| Install Python deps         | `pip install -r requirements.txt`                  | `pip install -r requirements.txt`       |
| Install Node deps           | `cd frontend && npm install`                       | `cd frontend && npm install`            |
| Start backend               | `python run_web_server.py`                         | `python run_web_server.py`              |
| Start frontend              | `cd frontend && npm start`                         | `cd frontend && npm start`              |
| Run all-in-one launcher     | `python run_app.py`                                | `./run_app.py`                          |
| Test API                    | `python test_api.py`                               | `python test_api.py`                    |
| Stop backend/frontend       | `Ctrl+C` in terminal or see stop section below     | `Ctrl+C` in terminal or see stop section|

---

## 🚀 Step-by-Step Setup & Run Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/soumya031/autometed-book-publisher
cd autometed-book-publisher
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Node.js (React) Dependencies
```bash
cd frontend
npm install
cd ..
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 5. Start the Backend Server
```bash
python run_web_server.py
```

### 6. Start the React Frontend (in a new terminal)
```bash
cd frontend
npm start
```

### 7. Open the Web Interface
- Go to [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🛠️ All-in-One Launcher (Recommended)
```bash
# Windows
python run_app.py

# Linux/macOS
./run_app.py
```
This script will guide you through setup and let you choose to run the backend, frontend, tests, or status checks.

---

## 🧪 Testing & Diagnostics

### Test API Endpoints
```bash
python test_api.py
```

### Test System Installation
```bash
python test_installation.py
```

### Test Scraper
```bash
python test_scraper.py
```

---

## 🐳 Docker Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

### Manual Docker Build
```bash
docker build -t ai-book-publication .
docker run -p 5000:5000 -p 3000:3000 ai-book-publication
```

---

## 🧰 Useful Monitoring & Stop Commands

### Check Running Processes
```bash
# Python backend
# Windows:
tasklist | findstr python
# Linux/macOS:
ps aux | grep python

# Node frontend
# Windows:
tasklist | findstr node
# Linux/macOS:
ps aux | grep node

# Check ports
# Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :5000
# Linux/macOS:
netstat -tulpn | grep :3000
netstat -tulpn | grep :5000
```

### Stop Servers
```bash
# Stop backend/frontend: Ctrl+C in their terminal
# Or kill process:
# Windows:
taskkill /F /IM python.exe
taskkill /F /IM node.exe
# Linux/macOS:
pkill -f python
pkill -f node

# Stop Docker containers
docker-compose down
docker stop $(docker ps -q)
```

---

## 🎯 CLI Workflow Commands

```bash
# Run complete publication workflow
python -m app.main publish --url "https://example.com" --style modern --tone engaging

# Search content
python -m app.main search "your search query"

# View content history
python -m app.main history content_id

# Test system components
python -m app.main test
```

---

## 🌐 API Endpoints

- `GET /api/status` — System status
- `GET /api/settings` — Get settings
- `PUT /api/settings` — Update settings
- `GET /api/history` — Workflow history
- `POST /api/search` — Semantic search
- `POST /api/workflow` — Run workflow
- `POST /api/scrape` — Scrape content
- `POST /api/generate` — Generate AI content

---

## 📁 Project Structure

```
project ai/
├── app/                    # Core Python modules
│   ├── ai_agents.py       # AI content generation
│   ├── db.py              # ChromaDB database management
│   ├── main.py            # Workflow orchestrator
│   ├── scraper.py         # Web scraping with Playwright
│   └── web_server.py      # Flask API server
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── pages/         # Page components
│   │   └── App.js         # Main app component
│   └── public/            # Static assets
├── chroma_db/             # ChromaDB storage
├── output/                # Generated content and screenshots
└── requirements.txt       # Python dependencies
```

---

## 🔧 Configuration & Troubleshooting

- Ensure `GOOGLE_API_KEY` is set in `.env` for AI features
- Restart servers after changing `.env`
- If ports are in use, kill the process or change the port
- For frontend issues, ensure all npm packages are installed
- For backend issues, check Python dependencies and logs

---

## 🙏 Acknowledgments

- **Google Gemini** for AI content generation
- **ChromaDB** for vector storage
- **Playwright** for web scraping
- **React** and **Tailwind CSS** for the frontend
- **Flask** for the backend API

---

**Note:** This system requires a Google Gemini API key for AI features. The API key should be kept secure and not committed to version control.
