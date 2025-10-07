# Audio Streaming System - GUI Applications

This folder contains graphical user interface (GUI) applications for the audio streaming system.

## 📁 Folder Structure

```
audioListner/
├── server_ui/              # Server GUI for Laptop 1 (Streaming)
│   ├── server_gui.py       # Main server GUI application
│   ├── start_server_gui.sh # Quick launcher script
│   └── README.md           # Server GUI documentation
│
└── client_ui/              # Client GUI for Laptop 2 (Listening)
    ├── client_gui.py       # Main client GUI application
    ├── start_client_gui.sh # Quick launcher script
    └── README.md           # Client GUI documentation
```

## 🎯 Overview

### Server UI (Laptop 1)
The server GUI runs on the laptop that has audio playing (e.g., Brave browser with music). It:
- Captures system audio in real-time
- Streams it over the network to connected clients
- Shows live audio levels and connected clients
- Provides a modern, user-friendly interface

### Client UI (Laptop 2)
The client GUI runs on the laptop where you want to hear the audio. It:
- Connects to the server on Laptop 1
- Receives and plays audio through speakers
- Shows connection status and audio levels
- Displays transfer statistics

## 🚀 Quick Start

### On Laptop 1 (Server):

1. Set up audio monitoring:
```bash
pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
```

2. Launch the server GUI:
```bash
cd server_ui
./start_server_gui.sh
```
Or:
```bash
cd server_ui
python3 server_gui.py
```

3. Click **"Start Server"** in the GUI
4. Note the IP address displayed (e.g., 192.168.1.100)
5. Share this IP with Laptop 2

### On Laptop 2 (Client):

1. Launch the client GUI:
```bash
cd client_ui
./start_client_gui.sh
```
Or:
```bash
cd client_ui
python3 client_gui.py
```

2. Enter the server IP address from Laptop 1
3. Click **"Connect"**
4. Audio will start playing!

## 🎨 Features

### Server GUI Features
- ✅ One-click start/stop
- ✅ Automatic IP address detection
- ✅ Real-time audio level visualization
- ✅ Connected clients counter
- ✅ Color-coded log messages
- ✅ Audio device information
- ✅ Professional modern design

### Client GUI Features
- ✅ Easy server connection
- ✅ Automatic audio configuration
- ✅ Real-time playback visualization
- ✅ Data transfer statistics
- ✅ Buffer status monitoring
- ✅ Color-coded log messages
- ✅ Professional modern design

## 📋 Prerequisites

Both GUIs require:
```bash
pip install sounddevice numpy
```

Tkinter (usually comes with Python, but if not):
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## 🎵 Audio Quality

- **Sample Rate**: 44100 Hz (CD quality)
- **Channels**: 2 (Stereo)
- **Bit Depth**: 32-bit float
- **Latency**: ~50-100ms
- **Protocol**: TCP/IP

## 🔧 Troubleshooting

### Server Issues

**"No suitable audio device found"**
- Run the audio monitoring setup command
- Check `pactl list short sources`

**Clients can't connect**
- Check firewall settings (allow port 9999)
- Verify both laptops are on the same network
- Make sure server is actually started

### Client Issues

**"Connection refused"**
- Ensure server is running on Laptop 1
- Verify IP address is correct
- Check network connectivity

**No audio playing**
- Check speaker/headphone connections
- Verify volume is not muted
- Check audio level indicator

**Audio stuttering**
- Check network stability
- Reduce other network traffic
- Check buffer status in GUI

## 🌐 Network Requirements

- **Both laptops must be on the same network**
- **Port 9999 must be open** (or configure firewall)
- **TCP connections** must be allowed
- **Stable network connection** recommended

To find your network information:
```bash
# Show IP address
hostname -I

# Test connectivity (from Laptop 2)
ping <laptop1_ip>

# Check port
nc -zv <laptop1_ip> 9999
```

## 📱 User Interface Guide

### Color Coding

Both GUIs use consistent color coding:
- **Blue** 🔵: Informational messages
- **Green** 🟢: Success messages
- **Orange** 🟠: Warning messages
- **Red** 🔴: Error messages

### Audio Level Bars

Visual audio level indicators:
- **Green**: Normal levels (0-50%)
- **Orange**: High levels (50-80%)
- **Red**: Very high levels (80-100%)

## 🎯 Comparison with CLI versions

| Feature | GUI Version | CLI Version |
|---------|------------|-------------|
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visual feedback | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Configuration | Click buttons | Command line args |
| Monitoring | Real-time graphs | Text output |
| Resource usage | Slightly higher | Lower |
| Remote use | GUI needed | SSH friendly |

**Use GUI version when:**
- You want easy point-and-click interface
- You need visual feedback
- Running on desktop with display

**Use CLI version when:**
- Running on headless server
- Using SSH/remote connection
- Automating with scripts

## 📝 Tips

1. **Server Setup**: Always set up audio monitoring before starting the server
2. **IP Address**: Server IP is shown in the GUI - note it down for clients
3. **Firewall**: Make sure port 9999 is allowed in firewall on both laptops
4. **Network**: Use wired connection for best stability
5. **Buffer**: Client automatically manages buffer to prevent dropouts

## 🆘 Support

For issues:
1. Check the logs in the GUI (color-coded)
2. Review the README in server_ui/ or client_ui/
3. Verify network connectivity
4. Check audio device configuration

## 📄 License

Part of the Audio Streaming project.
