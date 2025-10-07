# 🎵 Audio Streaming GUI Applications - Complete Guide

## 📦 What Was Created

I've created two modern graphical user interface (GUI) applications for your audio streaming system, organized in separate folders:

### 1. **server_ui/** - Server GUI (Laptop 1)
   - `server_gui.py` - Main server application with GUI
   - `start_server_gui.sh` - Quick launcher script
   - `README.md` - Detailed documentation

### 2. **client_ui/** - Client GUI (Laptop 2)
   - `client_gui.py` - Main client application with GUI
   - `start_client_gui.sh` - Quick launcher script
   - `README.md` - Detailed documentation

### 3. **GUI_README.md** - Master documentation for both GUIs

## 🎨 Features Overview

### Server GUI (Laptop 1) Features:
✅ **One-Click Operation** - Start/Stop with single button click
✅ **Automatic IP Detection** - Shows your IP address automatically
✅ **Real-Time Audio Level** - Visual bar showing audio volume
✅ **Client Counter** - See how many clients are connected
✅ **Color-Coded Logging** - Easy-to-read log with color coding
✅ **Device Information** - Shows which audio device is being used
✅ **Modern Design** - Professional, clean interface

### Client GUI (Laptop 2) Features:
✅ **Easy Connection** - Simple IP entry and connect button
✅ **Auto Configuration** - Receives audio settings from server
✅ **Real-Time Visualization** - Live audio level display
✅ **Statistics** - Shows data received and frame count
✅ **Buffer Status** - Monitor audio buffer fill level
✅ **Color-Coded Logging** - Easy-to-read log with color coding
✅ **Modern Design** - Professional, clean interface

## 🚀 Quick Start Guide

### Prerequisites (Both Laptops)

1. **Install Python tkinter** (already done on this laptop):
```bash
sudo apt-get install python3-tk
```

2. **Packages are already installed** in your `.venv`:
   - sounddevice ✓
   - numpy ✓

### Running Server GUI (Laptop 1)

1. **Set up audio monitoring** (one-time setup):
```bash
pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
```

2. **Launch the server GUI**:
```bash
cd server_ui
./start_server_gui.sh
```

Or directly:
```bash
cd server_ui
../.venv/bin/python server_gui.py
```

3. **In the GUI**:
   - Click **"▶ Start Server"**
   - Note the IP address shown (e.g., 192.168.1.100)
   - Share this IP with Laptop 2
   - Watch the audio levels in real-time
   - See connected clients count

4. **To stop**:
   - Click **"⬛ Stop Server"**
   - Or close the window

### Running Client GUI (Laptop 2)

1. **Get the server IP** from Laptop 1's GUI

2. **Launch the client GUI**:
```bash
cd client_ui
./start_client_gui.sh
```

Or directly:
```bash
cd client_ui
../.venv/bin/python client_gui.py
```

3. **In the GUI**:
   - Enter the server IP address
   - Keep port as 9999 (or match server)
   - Click **"🔌 Connect"**
   - Audio will start playing automatically
   - Watch the audio levels and statistics

4. **To disconnect**:
   - Click **"🔌 Disconnect"**
   - Or close the window

## 🎯 Interface Guide

### Server GUI Layout

```
┌─────────────────────────────────────────┐
│   🎵 Audio Streaming Server             │  <- Header
├─────────────────────────────────────────┤
│ Server Information                      │
│  Server IP: 192.168.1.100              │
│  Port: 9999                            │
│  Status: 🟢 Running                     │
│  Connected Clients: 2                  │
│  Audio Device: monitor                 │
├─────────────────────────────────────────┤
│  [▶ Start Server]  [⬛ Stop Server]     │  <- Controls
├─────────────────────────────────────────┤
│ Audio Level                            │
│  ████████████░░░░░░░░░░░░░░            │  <- Level bar
│  Volume: 45%                           │
├─────────────────────────────────────────┤
│ Server Log                             │
│  [12:34:56] Server started ✓           │
│  [12:35:01] Client connected ✓         │
│  [12:35:15] Streaming audio...         │
│                                        │
└─────────────────────────────────────────┘
```

### Client GUI Layout

```
┌─────────────────────────────────────────┐
│   🎧 Audio Streaming Client             │  <- Header
├─────────────────────────────────────────┤
│ Connection Settings                     │
│  Server IP: [192.168.1.100________]    │
│  Port:      [9999]                     │
├─────────────────────────────────────────┤
│ Client Information                      │
│  Status: 🟢 Connected                   │
│  Audio: 44100Hz, 2ch, 2048 frames      │
│  Data: 15.32 MB | Frames: 3254         │
│  Output: Default                       │
├─────────────────────────────────────────┤
│  [🔌 Connect]  [🔌 Disconnect]          │  <- Controls
├─────────────────────────────────────────┤
│ Playback Level                         │
│  ██████████████░░░░░░░░░░░░            │  <- Level bar
│  Volume: 52%                           │
│  Buffer: 25 / 50 frames                │
├─────────────────────────────────────────┤
│ Client Log                             │
│  [12:35:00] Connecting...              │
│  [12:35:01] Connected! ✓               │
│  [12:35:02] Audio playing...           │
│                                        │
└─────────────────────────────────────────┘
```

## 🎨 Color Coding

Both GUIs use consistent color schemes:

### Log Messages:
- 🔵 **Blue** - Information (general messages)
- 🟢 **Green** - Success (operations completed)
- 🟠 **Orange** - Warning (non-critical issues)
- 🔴 **Red** - Error (critical problems)

### Audio Level Bars:
- 🟢 **Green** (0-50%) - Normal audio levels
- 🟠 **Orange** (50-80%) - High audio levels
- 🔴 **Red** (80-100%) - Very high audio levels

## 📊 Features Comparison

| Feature | Server GUI | Client GUI |
|---------|-----------|-----------|
| Audio level visualization | ✓ | ✓ |
| Real-time logging | ✓ | ✓ |
| Statistics display | Client count | Data/frames |
| Network info | Shows server IP | Shows connection status |
| Buffer monitoring | - | ✓ |
| Auto configuration | - | ✓ (from server) |
| Device selection | Auto-detect | Default output |

## 🔧 Technical Details

### Audio Configuration:
- **Sample Rate**: 44100 Hz (CD quality)
- **Channels**: 2 (Stereo)
- **Block Size**: 2048 frames
- **Bit Depth**: 32-bit float
- **Latency**: ~50-100ms (network dependent)

### Network:
- **Protocol**: TCP/IP
- **Port**: 9999 (configurable)
- **Connection**: Point-to-multipoint (one server, multiple clients)

### Buffer Management:
- **Client Buffer**: 50 frames maximum
- **Overflow Handling**: Drop oldest frames
- **Purpose**: Handle network jitter, prevent dropouts

## ⚠️ Troubleshooting

### Common Issues and Solutions

#### Server GUI Issues:

**Problem**: "No suitable audio device found"
**Solution**: 
```bash
pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
```

**Problem**: Clients can't connect
**Solution**: 
- Check firewall: `sudo ufw allow 9999`
- Verify network: `ip addr show`
- Test connectivity: `ping <server_ip>`

**Problem**: No audio being captured
**Solution**:
- Make sure audio is actually playing
- Check the audio level indicator in GUI
- Verify audio device in GUI matches your setup

#### Client GUI Issues:

**Problem**: "Connection refused"
**Solution**:
- Ensure server is running and started
- Verify IP address is correct
- Check both laptops are on same network

**Problem**: "Connection timeout"
**Solution**:
- Check network connectivity
- Verify firewall settings
- Try pinging server: `ping <server_ip>`

**Problem**: No audio playback
**Solution**:
- Check speakers/headphones are connected
- Verify volume is not muted
- Look at audio level indicator in GUI
- Check buffer status

**Problem**: Audio stuttering/dropouts
**Solution**:
- Check network stability
- Look at buffer status (should be 10-40 frames)
- Reduce other network traffic
- Use wired connection instead of WiFi

## 💡 Tips for Best Experience

1. **Network**: Use wired Ethernet connection for best stability
2. **Audio**: Play music before starting server
3. **Firewall**: Allow port 9999 on both laptops
4. **Monitoring**: Keep an eye on the audio level bars
5. **Logs**: Check the color-coded logs if issues occur
6. **Buffer**: Client buffer should stay between 10-40 frames
7. **Distance**: Keep laptops on same network/subnet

## 🔄 Workflow Example

### Typical Usage Flow:

**On Laptop 1 (Server):**
1. Open Brave browser, start playing music
2. Run: `cd server_ui && ./start_server_gui.sh`
3. Click "Start Server"
4. Note the IP address (e.g., 192.168.1.100)
5. Watch audio levels to confirm capture
6. Wait for clients to connect

**On Laptop 2 (Client):**
1. Run: `cd client_ui && ./start_client_gui.sh`
2. Enter server IP: 192.168.1.100
3. Click "Connect"
4. Audio plays automatically!
5. Watch audio levels and statistics
6. When done, click "Disconnect"

**Cleanup:**
- Stop server on Laptop 1
- Both GUIs can be closed

## 📁 File Locations

All GUI files are in your main audioListner directory:

```
/home/dharmesh.p/Trial/audioListner/
├── server_ui/
│   ├── server_gui.py           <- Main server GUI
│   ├── start_server_gui.sh     <- Launcher
│   └── README.md               <- Server docs
├── client_ui/
│   ├── client_gui.py           <- Main client GUI
│   ├── start_client_gui.sh     <- Launcher
│   └── README.md               <- Client docs
└── GUI_README.md               <- Master guide
```

## 🆚 GUI vs CLI Versions

You still have your original CLI versions:
- `audio_server.py` - Command-line server
- `audio_client.py` - Command-line client

**When to use GUI:**
- Desktop usage with display
- Want visual feedback
- Prefer point-and-click
- Need to monitor levels visually

**When to use CLI:**
- Remote/SSH access
- Headless servers
- Scripting/automation
- Lower resource usage

## 🎓 Understanding the Code

Both GUIs are built with:
- **Tkinter**: Python's standard GUI library
- **Threading**: For non-blocking network operations
- **Queues**: For thread-safe logging and data transfer
- **Sounddevice**: For audio capture/playback
- **NumPy**: For audio data processing
- **Socket**: For network communication

The code is well-commented and easy to modify if needed!

## 🚀 Next Steps

You can now:
1. ✅ Run the server GUI on Laptop 1
2. ✅ Run the client GUI on Laptop 2
3. ✅ Stream audio with visual feedback
4. ✅ Monitor connection status
5. ✅ See real-time statistics

## 📝 Summary

**Created:**
- ✓ Modern server GUI with real-time monitoring
- ✓ Modern client GUI with easy connection
- ✓ Launcher scripts for both
- ✓ Comprehensive documentation
- ✓ Organized in separate folders

**Features:**
- ✓ One-click operation
- ✓ Visual audio level indicators
- ✓ Real-time logging with colors
- ✓ Statistics and monitoring
- ✓ Professional, clean design
- ✓ Easy to use for anyone

Enjoy your new audio streaming GUIs! 🎵🎧
