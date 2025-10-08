# 🎵 Audio Streaming - Ubuntu Desktop Applications

## ✅ Installation Complete!

Your audio streaming system is now installed as native Ubuntu applications!

## 📱 How to Access

### Method 1: Application Menu (Recommended)
1. **Press Super/Windows key** or click Activities
2. Type **"Audio Streaming"**
3. You'll see two apps:
   - 🎵 **Audio Streaming Server** (for Laptop 1)
   - 🎧 **Audio Streaming Client** (for Laptop 2)
4. Click to launch!

### Method 2: Terminal Launch
```bash
# Launch Server
gtk-launch audio-streaming-server

# Launch Client
gtk-launch audio-streaming-client
```

### Method 3: Desktop Shortcuts
You can drag the apps from the application menu to your desktop for quick access!

## 🎯 What Was Installed

### Desktop Files
- `~/.local/share/applications/audio-streaming-server.desktop`
- `~/.local/share/applications/audio-streaming-client.desktop`

### Custom Icons
- `/home/dharmesh.p/Trial/audioListner/server_ui/icon.svg` - Green server icon
- `/home/dharmesh.p/Trial/audioListner/client_ui/icon.svg` - Blue headphones icon

### Scripts
- `install_apps.sh` - Installation script
- `uninstall_apps.sh` - Uninstallation script

## 🚀 Usage

### On Laptop 1 (Server):

1. **Launch from Applications Menu**
   - Search: "Audio Streaming Server"
   - Or: `gtk-launch audio-streaming-server`

2. **Set up audio monitoring** (first time only):
   ```bash
   pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
   ```

3. **Start streaming**
   - Click "▶ Start Server"
   - Note the IP address shown
   - Share IP with Laptop 2

### On Laptop 2 (Client):

1. **Launch from Applications Menu**
   - Search: "Audio Streaming Client"
   - Or: `gtk-launch audio-streaming-client`

2. **Connect to server**
   - Enter server IP address
   - Click "🔌 Connect"
   - Enjoy the audio!

## 🎨 Application Icons

### Server Icon (Green)
- Broadcasting waves
- Server/transmitter symbol
- Green status indicator
- "SERVER" label

### Client Icon (Blue)
- Headphones
- Incoming audio arrow
- Green status indicator
- "CLIENT" label

## 🔧 Management

### To Reinstall:
```bash
cd /home/dharmesh.p/Trial/audioListner
./install_apps.sh
```

### To Uninstall:
```bash
cd /home/dharmesh.p/Trial/audioListner
./uninstall_apps.sh
```

### To Update Icons:
Edit the SVG files and reinstall:
- `server_ui/icon.svg`
- `client_ui/icon.svg`

## 📍 Finding the Apps

### In Application Menu:
- **Category**: AudioVideo → Audio
- **Search terms**: audio, streaming, server, client, broadcast, listen

### On Desktop:
1. Open application menu
2. Right-click on the app
3. Select "Add to Favorites" or drag to desktop

## 🎯 Features

### Desktop Integration:
- ✅ Native Ubuntu application
- ✅ Custom icons
- ✅ Searchable in application menu
- ✅ Can pin to dock
- ✅ Can add to desktop
- ✅ Can set as favorite
- ✅ Appears in "Show Applications"

### Application Properties:
- **Category**: AudioVideo, Audio, Network
- **Keywords**: audio, streaming, server, client, broadcast, listen, receiver
- **Startup**: GUI launches immediately (no terminal)

## 💡 Tips

### Pin to Dock:
1. Launch the application
2. Right-click icon in dock
3. Select "Add to Favorites"

### Create Desktop Shortcut:
1. Open application menu
2. Find "Audio Streaming Server" or "Client"
3. Drag icon to desktop

### Quick Launch:
Add to favorites or dock for one-click access!

## 🔄 Transferring to Laptop 2

To install on the second laptop:

### Method 1: Copy the whole folder
```bash
# On Laptop 1
scp -r /home/dharmesh.p/Trial/audioListner laptop2:~/

# On Laptop 2
cd ~/audioListner
./install_apps.sh
```

### Method 2: Copy just what's needed
```bash
# On Laptop 2, copy the entire project folder, then:
cd audioListner
./install_apps.sh
```

## 🖥️ Desktop Environment Compatibility

These apps work with:
- ✅ GNOME (Ubuntu default)
- ✅ KDE Plasma
- ✅ XFCE
- ✅ MATE
- ✅ Cinnamon
- ✅ Any freedesktop.org compliant DE

## 🎵 Audio Setup Reminder

### For Server (Laptop 1):
Before first use, set up audio monitoring:
```bash
pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
```

This only needs to be done once!

## 📱 Application Details

### Audio Streaming Server
- **Name**: Audio Streaming Server
- **Description**: Stream audio from this laptop to other devices
- **Icon**: Green with broadcast waves
- **Launch**: Opens server GUI immediately
- **Purpose**: Run on laptop with audio source

### Audio Streaming Client
- **Name**: Audio Streaming Client
- **Description**: Listen to audio streamed from another laptop
- **Icon**: Blue with headphones
- **Launch**: Opens client GUI immediately
- **Purpose**: Run on laptop where you want to hear audio

## 🔍 Troubleshooting

### App doesn't appear in menu:
```bash
# Update desktop database
update-desktop-database ~/.local/share/applications

# Or reinstall
./install_apps.sh
```

### Can't find app in search:
- Try searching: "audio", "streaming", "server", "client"
- Check in AudioVideo category
- Try logging out and back in

### Icon doesn't show:
- Icons are SVG files in each app folder
- Path is absolute, so moving the folder requires reinstall
- Reinstall: `./install_apps.sh`

### App won't launch:
- Check Python virtual environment exists: `.venv/`
- Check dependencies: `pip install sounddevice numpy`
- Check tkinter: `sudo apt-get install python3-tk`

## 📊 File Locations

```
/home/dharmesh.p/Trial/audioListner/
├── server_ui/
│   ├── server_gui.py                       # Server application
│   ├── icon.svg                            # Custom server icon
│   └── audio-streaming-server.desktop      # Desktop file template
├── client_ui/
│   ├── client_gui.py                       # Client application
│   ├── icon.svg                            # Custom client icon
│   └── audio-streaming-client.desktop      # Desktop file template
├── install_apps.sh                          # Install script
└── uninstall_apps.sh                        # Uninstall script

~/.local/share/applications/
├── audio-streaming-server.desktop           # Installed server launcher
└── audio-streaming-client.desktop           # Installed client launcher
```

## ✨ Advantages of Desktop Apps

**Before (CLI):**
- Had to open terminal
- Navigate to directory
- Remember command syntax
- Hard to find and launch

**Now (Desktop Apps):**
- ✅ Click from application menu
- ✅ No terminal needed
- ✅ One-click launch
- ✅ Easy to find
- ✅ Can pin to dock
- ✅ Professional appearance
- ✅ Easy to share/distribute

## 🎓 For Advanced Users

### Customize Desktop Files:
Edit installed files:
```bash
nano ~/.local/share/applications/audio-streaming-server.desktop
```

### Custom Keyboard Shortcuts:
In Ubuntu Settings → Keyboard → Custom Shortcuts:
- Command: `gtk-launch audio-streaming-server`
- Shortcut: Your choice (e.g., Ctrl+Alt+S)

### System-wide Installation:
Copy to system folder (requires sudo):
```bash
sudo cp server_ui/audio-streaming-server.desktop /usr/share/applications/
sudo cp client_ui/audio-streaming-client.desktop /usr/share/applications/
```

## 🎉 Summary

You can now launch your audio streaming apps like any other Ubuntu application:

1. **Press Super key**
2. **Type "Audio Streaming"**
3. **Click and go!**

No terminal, no commands, just point and click! 🎵🎧

---

**Enjoy your new desktop applications!** 🚀
