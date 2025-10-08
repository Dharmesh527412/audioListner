#!/bin/bash
# Quick setup script for new laptop installation

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║    🎵 Audio Streaming Apps - Quick Setup for New Laptop 🎧    ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python version
echo "1️⃣  Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Please install: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   ✅ Python $PYTHON_VERSION found"

# Check for required system packages
echo ""
echo "2️⃣  Checking system dependencies..."

# Check for tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "   ⚠️  python3-tk not found"
    echo "   Installing python3-tk..."
    sudo apt-get install -y python3-tk
fi

# Check for portaudio
if ! dpkg -l | grep -q portaudio19-dev; then
    echo "   ⚠️  portaudio19-dev not found"
    echo "   Installing portaudio19-dev..."
    sudo apt-get install -y portaudio19-dev
fi

echo "   ✅ System dependencies ready"

# Create virtual environment
echo ""
echo "3️⃣  Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    echo "   Creating .venv..."
    python3 -m venv .venv
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "4️⃣  Installing Python packages..."
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip --quiet

# Install required packages
echo "   Installing sounddevice..."
pip install sounddevice --quiet

echo "   Installing numpy..."
pip install numpy --quiet

echo "   ✅ Python packages installed"

# Verify installations
echo ""
echo "5️⃣  Verifying installation..."
if python -c "import sounddevice, numpy" 2>/dev/null; then
    echo "   ✅ All Python packages working"
else
    echo "   ❌ Package verification failed"
    exit 1
fi

# Install desktop applications
echo ""
echo "6️⃣  Installing desktop applications..."
./install_apps.sh

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║                   ✅ SETUP COMPLETE! ✅                         ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📱 Your audio streaming apps are now installed!"
echo ""
echo "🔍 To launch, press Super key and search for:"
echo "   • Audio Streaming Server (for Laptop 1)"
echo "   • Audio Streaming Client (for Laptop 2)"
echo ""
echo "💡 Pro tip: Pin the apps to your dock for quick access!"
echo ""
echo "📚 For usage instructions, see:"
echo "   - DESKTOP_APPS_GUIDE.md"
echo "   - QUICK_START_APPS.md"
echo ""
echo "🎉 Enjoy your audio streaming system!"
