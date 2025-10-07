# Audio Streaming Client GUI - Laptop 2

Modern graphical user interface for the audio streaming client (listener).

## Features

- 🎧 Real-time audio playback from server
- 🔌 Easy connection management
- 📊 Live audio level visualization
- 📈 Data transfer statistics
- 🔊 Buffer status monitoring
- 📝 Real-time client log with colored output
- 🎨 Modern, user-friendly interface

## Prerequisites

Make sure you have the following installed:
```bash
pip install sounddevice numpy tkinter
```

## Usage

1. Get the server IP address from Laptop 1 (the one running the server)

2. Run the client GUI:
```bash
python client_gui.py
```

3. Enter connection details:
   - **Server IP Address**: The IP shown on the server (e.g., 192.168.1.100)
   - **Port**: Usually 9999 (match with server)

4. Click **"Connect"** to start receiving audio

5. The client will:
   - Connect to the server
   - Receive audio configuration automatically
   - Start playing audio through your speakers
   - Display real-time audio levels
   - Show transfer statistics

6. Click **"Disconnect"** when done

## Interface Guide

### Connection Settings Panel
- **Server IP Address**: Enter the IP of Laptop 1
- **Port**: Network port (default: 9999)

### Client Information Panel
- **Status**: Connection state (Connected/Disconnected)
- **Audio Config**: Sample rate, channels, block size
- **Data Received**: Total megabytes and frames received
- **Output Device**: Audio output device being used

### Audio Level Panel
- Visual bar showing real-time playback volume
- Green: Normal levels (0-50%)
- Orange: High levels (50-80%)
- Red: Very high levels (80-100%)
- **Buffer Status**: Queue fill level (0-50 frames)

### Control Buttons
- **Connect**: Connect to server and start playback
- **Disconnect**: Stop playback and close connection

### Client Log
- Timestamped log of all events
- Color-coded messages:
  - Blue: Information
  - Green: Success
  - Orange: Warnings
  - Red: Errors

## Audio Quality

The client automatically receives the audio configuration from the server:
- Sample Rate: 44100 Hz (CD quality)
- Channels: 2 (Stereo)
- Block Size: 2048 frames
- Latency: ~50-100ms depending on network

## Buffer Management

The client uses a 50-frame buffer to:
- Handle network jitter
- Prevent audio dropouts
- Maintain smooth playback

If the buffer fills up, old frames are dropped to prevent latency buildup.

## Troubleshooting

**Connection refused:**
- Make sure the server is running on Laptop 1
- Verify you're using the correct IP address
- Check that both laptops are on the same network

**Connection timeout:**
- Check network connectivity
- Verify firewall settings on both laptops
- Make sure port 9999 is not blocked

**No audio playback:**
- Check your speaker/headphone connections
- Verify audio output is not muted
- Check the audio level indicator for activity

**Audio stuttering:**
- Check network stability
- Look at the buffer status (should stay between 10-40 frames)
- Reduce network traffic if possible

**Audio lag:**
- This is normal (50-100ms)
- Reduce buffer size in code if needed (advanced)
- Check network latency

## Network Information

- Default Port: 9999
- Protocol: TCP
- Received Format: 44100 Hz, Stereo (2 channels)
- Buffer Size: 50 frames maximum
- Typical Latency: 50-100ms

## Advanced Usage

To find the server IP from Laptop 1:
```bash
# On Laptop 1
hostname -I
# or
ip addr show
```

To test network connectivity:
```bash
# From Laptop 2
ping <server_ip>
```

To check if port is open:
```bash
# From Laptop 2
nc -zv <server_ip> 9999
```
