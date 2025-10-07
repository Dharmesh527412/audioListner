# Audio Streaming Server GUI - Laptop 1

Modern graphical user interface for the audio streaming server.

## Features

- 🎵 Real-time audio capture from system audio
- 🌐 Network streaming to multiple clients
- 📊 Live audio level visualization
- 📝 Real-time server log with colored output
- 👥 Connected clients counter
- 🎨 Modern, user-friendly interface

## Prerequisites

Make sure you have the following installed:
```bash
pip install sounddevice numpy tkinter
```

## Setup Audio Monitoring

Before running the server, set up audio monitoring:

```bash
# Find your audio output device
pactl list short sinks

# Set it as monitor (replace with your device name)
pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
```

## Usage

1. Run the server GUI:
```bash
python server_gui.py
```

2. The interface will show:
   - Your server IP address (share this with clients)
   - Server port (default: 9999)
   - Current status

3. Click **"Start Server"** to begin streaming

4. The server will:
   - Start capturing system audio
   - Listen for client connections
   - Display audio levels in real-time
   - Show connected clients count
   - Log all activities

5. Share your IP address with clients so they can connect

6. Click **"Stop Server"** when done

## Interface Guide

### Server Information Panel
- **Server IP**: Your local IP address (share with clients)
- **Port**: Network port for connections
- **Status**: Current server state (Running/Stopped)
- **Connected Clients**: Number of active connections
- **Audio Device**: Current capture device

### Audio Level Panel
- Visual bar showing real-time audio volume
- Green: Normal levels (0-50%)
- Orange: High levels (50-80%)
- Red: Very high levels (80-100%)

### Control Buttons
- **Start Server**: Begin audio streaming
- **Stop Server**: Stop streaming and disconnect all clients

### Server Log
- Timestamped log of all events
- Color-coded messages:
  - Blue: Information
  - Green: Success
  - Orange: Warnings
  - Red: Errors

## Troubleshooting

**No audio device found:**
- Run the audio monitoring setup commands
- Check `pactl list short sources` to see available sources

**Clients can't connect:**
- Check if firewall is blocking port 9999
- Make sure you're on the same network
- Verify the IP address is correct

**No audio streaming:**
- Make sure audio is playing in your browser/application
- Check the audio level indicator
- Verify audio monitoring is set up correctly

## Network Information

- Default Port: 9999
- Protocol: TCP
- Audio Format: 44100 Hz, Stereo (2 channels)
- Block Size: 2048 frames
