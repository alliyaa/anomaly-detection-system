#!/bin/bash

# Setup script for Anomaly Detection System
# This script automates the setup process

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Anomaly Detection System - Setup Script              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q
echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data results models
echo "✅ Directories created"
echo ""

# Run a quick test
echo "🧪 Running quick validation test..."
python src/anomaly_detector.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ System validation passed"
else
    echo "⚠️  Validation encountered issues (check logs)"
fi
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE!                                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Run the pipeline: python src/anomaly_detector.py"
echo "  3. View results: ls results/"
echo "  4. Run demos: python demo.py"
echo ""
echo "For more information, see README.md or QUICKSTART.md"
echo ""
