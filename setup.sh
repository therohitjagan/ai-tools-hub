#!/bin/bash

echo "🤖 Setting up AI Tools Hub..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p app/static/uploads
mkdir -p model_cache
mkdir -p logs

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

echo "✅ Setup complete! Run 'python run.py' to start the application."