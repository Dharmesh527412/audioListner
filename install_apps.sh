#!/bin/bash
# Installation script for Audio Streaming Apps

echo "🎵 Installing Audio Streaming Applications..."
echo ""

# Get the script directory (absolute path)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create .local/share/applications if it doesn't exist
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "⚠️  Warning: Virtual environment not found at $SCRIPT_DIR/.venv"
    echo "   Please create it first or apps may not work."
    echo ""
fi

# Copy desktop files and update paths
echo "📋 Installing desktop entries..."

# Server - Generate desktop file with current paths
cat > "$APPS_DIR/audio-streaming-server.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Audio Streaming Server
Comment=Stream audio from this laptop to other devices
Exec=$SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/server_ui/server_gui.py
Path=$SCRIPT_DIR/server_ui
Icon=$SCRIPT_DIR/server_ui/icon.svg
Terminal=false
Categories=AudioVideo;Audio;Network;
Keywords=audio;streaming;server;broadcast;
StartupNotify=true
StartupWMClass=server_gui
EOF
chmod +x "$APPS_DIR/audio-streaming-server.desktop"
echo "✓ Server app installed"

# Client - Generate desktop file with current paths
cat > "$APPS_DIR/audio-streaming-client.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Audio Streaming Client
Comment=Listen to audio streamed from another laptop
Exec=$SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/client_ui/client_gui.py
Path=$SCRIPT_DIR/client_ui
Icon=$SCRIPT_DIR/client_ui/icon.svg
Terminal=false
Categories=AudioVideo;Audio;Network;
Keywords=audio;streaming;client;listen;receiver;
StartupNotify=true
StartupWMClass=client_gui
EOF
chmod +x "$APPS_DIR/audio-streaming-client.desktop"
echo "✓ Client app installed"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$APPS_DIR"
    echo "✓ Desktop database updated"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Installation details:"
echo "  Project directory: $SCRIPT_DIR"
echo "  Desktop files: $APPS_DIR"
echo "  Python: $SCRIPT_DIR/.venv/bin/python"
echo ""
echo "You can now find these apps in your application menu:"
echo "  • 🎵 Audio Streaming Server - Stream audio to other devices"
echo "  • 🎧 Audio Streaming Client - Listen to streamed audio"
echo ""
echo "Search for: 'Audio Streaming' in your application menu"
echo ""
echo "You can also launch them from the terminal:"
echo "  gio launch $APPS_DIR/audio-streaming-server.desktop"
echo "  gio launch $APPS_DIR/audio-streaming-client.desktop"
echo ""
echo "To uninstall, run: ./uninstall_apps.sh"
echo ""
echo "💡 Note: If apps don't appear in menu, try:"
echo "   1. Log out and log back in"
echo "   2. Or run: update-desktop-database $APPS_DIR"
