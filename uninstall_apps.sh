#!/bin/bash
# Uninstallation script for Audio Streaming Apps

echo "🗑️  Uninstalling Audio Streaming Applications..."
echo ""

APPS_DIR="$HOME/.local/share/applications"

# Remove desktop files
if [ -f "$APPS_DIR/audio-streaming-server.desktop" ]; then
    rm "$APPS_DIR/audio-streaming-server.desktop"
    echo "✓ Server app removed"
fi

if [ -f "$APPS_DIR/audio-streaming-client.desktop" ]; then
    rm "$APPS_DIR/audio-streaming-client.desktop"
    echo "✓ Client app removed"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$APPS_DIR"
    echo "✓ Desktop database updated"
fi

echo ""
echo "✅ Uninstallation complete!"
echo ""
echo "To reinstall, run: ./install_apps.sh"
