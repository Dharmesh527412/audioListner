#!/bin/bash
# Quick start script for audio streaming client

if [ -z "$1" ]; then
    echo "❌ Error: Server IP address required"
    echo ""
    echo "Usage: ./start_client.sh <SERVER_IP>"
    echo "Example: ./start_client.sh 192.168.1.100"
    echo ""
    exit 1
fi

SERVER_IP=$1

echo "🎵 Starting Audio Streaming Client..."
echo "📡 Connecting to server: $SERVER_IP"
echo ""

# Check if packages are installed
python3 -c "import sounddevice, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Required packages not found. Installing..."
    pip3 install --user sounddevice numpy
    echo ""
fi

# Start the client
python3 audio_client.py $SERVER_IP
