#!/bin/bash
# Quick start script for audio streaming server

echo "🎵 Starting Audio Streaming Server..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
    .venv/bin/pip install sounddevice numpy
fi

# Set the audio source to monitor (capture system audio)
echo "🔧 Configuring PulseAudio to capture system audio..."
pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor

echo ""
echo "✓ Configuration complete!"
echo ""

# Start the server
.venv/bin/python audio_server.py
