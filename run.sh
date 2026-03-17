#!/bin/bash

# AI Surveillance System - Quick Start Script

echo "🚀 Starting AI Surveillance System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/frames data/alerts data/reports

# Run the application
echo "✅ Starting application..."
python app.py
