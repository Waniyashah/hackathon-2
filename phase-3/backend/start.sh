#!/bin/bash
# Startup script for Todo AI Chatbot Backend

echo "🚀 Starting Todo AI Chatbot Backend..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "⚠️  Warning: .env file not found in project root!"
    echo "Please create a .env file with your GEMINI_API_KEY"
    exit 1
fi

# Run database migrations
echo "🗄️  Running database migrations..."
cd backend
alembic upgrade head
cd ..

# Start the server
echo "✅ Starting FastAPI server..."
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
