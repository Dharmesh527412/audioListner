#!/bin/bash
# Installation script for Audio Streaming Apps

echo "🎵 Installing Audio Streaming Applications..."
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create .local/share/applications if it doesn't exist
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

# Copy desktop files
echo "📋 Installing desktop entries..."

# Server
cp "$SCRIPT_DIR/server_ui/audio-streaming-server.desktop" "$APPS_DIR/"
chmod +x "$APPS_DIR/audio-streaming-server.desktop"
echo "✓ Server app installed"

# Client
cp "$SCRIPT_DIR/client_ui/audio-streaming-client.desktop" "$APPS_DIR/"
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
echo "You can now find these apps in your application menu:"
echo "  • 🎵 Audio Streaming Server - Stream audio to other devices"
echo "  • 🎧 Audio Streaming Client - Listen to streamed audio"
echo ""
echo "You can also launch them from the terminal:"
echo "  gtk-launch audio-streaming-server"
echo "  gtk-launch audio-streaming-client"
echo ""
echo "To uninstall, run: ./uninstall_apps.sh"
