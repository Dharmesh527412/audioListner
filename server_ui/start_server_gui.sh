#!/bin/bash
# Launcher script for Audio Streaming Server GUI

echo "🎵 Starting Audio Streaming Server GUI..."
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if virtual environment exists
if [ -d "$PROJECT_DIR/.venv" ]; then
    echo "Using virtual environment..."
    PYTHON="$PROJECT_DIR/.venv/bin/python"
else
    echo "Virtual environment not found, using system Python..."
    PYTHON="python3"
fi

# Check if Python is available
if ! command -v $PYTHON &> /dev/null && [ "$PYTHON" = "python3" ]; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
$PYTHON -c "import sounddevice, numpy, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies."
    echo "Please run: pip install sounddevice numpy"
    echo "And: sudo apt-get install python3-tk"
    exit 1
fi

echo ""
echo "📡 Make sure you have set up audio monitoring:"
echo "   pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor"
echo ""

# Run the server GUI
cd "$SCRIPT_DIR"
$PYTHON server_gui.py
