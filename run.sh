#!/bin/bash

echo "========================================"
echo "GuardELNS - Network Security Dashboard"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create necessary directories
mkdir -p data/logs
mkdir -p data/database
mkdir -p data/models
echo ""

# Run the application
echo "Starting GuardELNS Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""
streamlit run app.py
