#!/bin/bash

# Knowledge Engine Startup Script

echo "🚀 Initializing Knowledge Engine..."

# 1. Start Database (Docker)
echo "📦 Starting Database..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ Docker Failed. Is Docker running?"
    exit 1
fi

# 2. Start Backend
echo "🧠 Starting Backend (FastAPI)..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python Virtual Environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run in background
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "   -> Backend running on PID $BACKEND_PID (Port 8000)"
cd ..

# 3. Start Frontend
echo "🎨 Starting Frontend (Next.js)..."
cd frontend
# Run in background
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   -> Frontend running on PID $FRONTEND_PID (Port 3000)"
cd ..

echo "✅ Knowledge Engine Deployed!"
echo "👉 Open http://localhost:3000"
echo "   (Logs are being written to backend.log and frontend.log)"

# Trap Ctrl+C to kill background processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

wait
