# Audio Streaming Setup

Stream audio from your Brave browser to another Ubuntu laptop on your network.

**🎤 IMPORTANT: This application captures ONLY system audio OUTPUT (browser audio). It does NOT capture or stream microphone input.**

## 📋 Requirements

Both laptops need:
- Python 3.x
- sounddevice and numpy packages

## 🚀 Quick Start Guide

### On the SOURCE laptop (with Brave browser playing music):

1. **Setup audio OUTPUT monitoring** (one time):
   ```bash
   pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
   ```
   *This captures only system audio OUTPUT (what your speakers play), NOT microphone input*

2. **Start the server**:
   ```bash
   /home/dharmesh.p/Trial/audioListner/.venv/bin/python audio_server.py
   ```

3. **Note the IP address** shown in the output (e.g., `192.168.1.100`)

### On the DESTINATION laptop (where you want to hear the music):

1. **Install required packages**:
   ```bash
   pip install sounddevice numpy
   ```

2. **Copy the client script** to the destination laptop:
   - Copy `audio_client.py` to the other laptop

3. **Run the client** (replace with your server's IP):
   ```bash
   python audio_client.py 192.168.1.100
   ```

4. **Play music** in Brave browser on the source laptop - you'll hear it on the destination laptop!

## 📝 Detailed Instructions

### Server Options

```bash
# Default (listen on all interfaces, port 9999)
python audio_server.py

# Custom port
python audio_server.py --port 8888

# Specific interface
python audio_server.py --host 192.168.1.100 --port 9999
```

### Client Options

```bash
# Connect to server
python audio_client.py <SERVER_IP>

# Custom port
python audio_client.py <SERVER_IP> --port 8888
```

## 🔧 Troubleshooting

### Can't connect to server?

1. **Check if server is running**:
   ```bash
   netstat -tulpn | grep 9999
   ```

2. **Check firewall** (on server laptop):
   ```bash
   sudo ufw allow 9999/tcp
   ```

3. **Find server IP address**:
   ```bash
   ip addr show | grep inet
   # or
   hostname -I
   ```

### No audio on client?

1. **Check volume** on destination laptop
2. **List audio devices**:
   ```bash
   python -c "import sounddevice; print(sounddevice.query_devices())"
   ```

### Server says "No suitable audio device found"?

This usually means the audio device detection needs to be configured:

1. **First, check if PulseAudio monitor exists**:
   ```bash
   pactl list sources short
   # Look for a line with ".monitor" in the name
   ```

2. **Set the monitor as default source**:
   ```bash
   pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
   # Replace with your actual monitor device name from step 1
   ```

3. **Verify it's set correctly**:
   ```bash
   pactl get-default-source
   # Should show the monitor device
   ```

4. **Test device detection**:
   ```bash
   python3 test_device_detection.py
   # Should show: ✅ SUCCESS: Found audio device!
   ```

**Note**: The application will use the `pulse` device which automatically uses PulseAudio's default source (the monitor you set above).

### No audio captured on server?

1. **Check PulseAudio is running**:
   ```bash
   pulseaudio --check && echo "PulseAudio is running" || echo "PulseAudio is not running"
   ```

2. **Verify default source is a monitor**:
   ```bash
   pactl get-default-source
   # Should show a device with ".monitor" in the name
   ```

3. **If needed, set correct monitor device**:
   ```bash
   pactl list sources short
   pactl set-default-source <YOUR_MONITOR_SOURCE>
   ```

## 🎯 How It Works

1. **Server** captures audio from the system's monitor device (what you hear in browser)
2. **Server** streams the audio data over TCP socket to connected clients
3. **Client** receives the audio data and plays it through speakers

## 📊 Display Information

Both scripts show real-time information:
- **Timestamp**: Current time
- **Level**: Audio volume level
- **Visual bar**: Graphical representation of volume
- **Clients** (server): Number of connected clients
- **Buffer** (client): Buffer queue size

## 🔐 Network Security

⚠️ **Note**: This streams audio over your local network without encryption. Only use on trusted networks!

To restrict to local network only:
```bash
python audio_server.py --host 192.168.1.100  # Use your local IP
```

## 🛑 Stopping the Application

The application automatically stops streaming when closed:

### Command-Line Version
- **Ctrl+C**: Cleanly stops streaming and releases all resources
- **Close Terminal**: Automatically stops streaming (no orphaned processes)
- **Kill Process**: Handles SIGTERM/SIGINT signals gracefully

### GUI Version
- **Click 'Stop' button**: Stops streaming and disconnects clients
- **Close Window (X)**: Automatically stops streaming first, then closes
- **Ctrl+C in Terminal**: Cleanly shuts down if launched from terminal

**✅ Guaranteed Cleanup**: All methods ensure:
- Audio streams are stopped
- Network connections are closed
- Ports are released for reuse
- No orphaned processes remain

## 💡 Tips

- **Low latency**: Keep both laptops on the same network
- **Multiple clients**: The server supports multiple clients simultaneously
- **Quality**: Uses 44.1kHz stereo (CD quality)
- **Buffer**: Client has a 50-frame buffer to handle network jitter

## 📁 Files

- `audio_server.py` - Run on laptop with Brave browser
- `audio_client.py` - Run on laptop where you want to hear audio
- `audioListner.py` - Original audio listener with recording features
- `listen_browser.py` - Simple local audio level monitor

---

**Created:** October 7, 2025
