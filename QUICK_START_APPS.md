# 🎵 Audio Streaming Apps - Quick Reference

## ✅ INSTALLATION COMPLETE!

Your audio streaming system is now installed as Ubuntu desktop applications!

---

## 🚀 HOW TO LAUNCH

### 🔍 Method 1: Search in Applications (EASIEST)

1. Press **Super/Windows key** (or click Activities)
2. Type: **"Audio Streaming"**
3. Click on:
   - **🎵 Audio Streaming Server** (Laptop 1)
   - **🎧 Audio Streaming Client** (Laptop 2)

### ⌨️ Method 2: Command Line

```bash
# Launch Server GUI
gio launch ~/.local/share/applications/audio-streaming-server.desktop

# Launch Client GUI
gio launch ~/.local/share/applications/audio-streaming-client.desktop
```

### 📍 Method 3: Pin to Dock

1. Search for the app in Activities
2. Right-click on the icon
3. Select "Add to Favorites"
4. Now it's in your dock!

---

## 📋 INSTALLED FILES

### Desktop Launchers
- `~/.local/share/applications/audio-streaming-server.desktop`
- `~/.local/share/applications/audio-streaming-client.desktop`

### Application Files
- **Server**: `/home/dharmesh.p/Trial/audioListner/server_ui/server_gui.py`
- **Client**: `/home/dharmesh.p/Trial/audioListner/client_ui/client_gui.py`

### Custom Icons
- **Server**: `/home/dharmesh.p/Trial/audioListner/server_ui/icon.svg` (Green)
- **Client**: `/home/dharmesh.p/Trial/audioListner/client_ui/icon.svg` (Blue)

---

## 🎯 QUICK START

### Laptop 1 (Server) - 3 Steps:

1. **Search** → "Audio Streaming Server" → Click
2. **Click** → "▶ Start Server" button
3. **Share** → IP address with Laptop 2

### Laptop 2 (Client) - 3 Steps:

1. **Search** → "Audio Streaming Client" → Click
2. **Enter** → Server IP address
3. **Click** → "🔌 Connect" button

---

## 🔧 MANAGEMENT

### Reinstall Apps
```bash
cd /home/dharmesh.p/Trial/audioListner
./install_apps.sh
```

### Uninstall Apps
```bash
cd /home/dharmesh.p/Trial/audioListner
./uninstall_apps.sh
```

### Update Desktop Database (if apps don't show)
```bash
update-desktop-database ~/.local/share/applications
```

---

## 🎨 APP ICONS

| App | Icon | Color |
|-----|------|-------|
| Server | Broadcasting waves + transmitter | Green |
| Client | Headphones + incoming audio | Blue |

---

## 💡 TIPS

### Pin to Dock for Quick Access
1. Launch the app
2. Right-click dock icon
3. "Add to Favorites"

### Create Desktop Shortcut
1. Open Activities
2. Find the app
3. Drag to desktop

### Add Keyboard Shortcut
Settings → Keyboard → Custom Shortcuts:
- Command: `gio launch ~/.local/share/applications/audio-streaming-server.desktop`
- Shortcut: Your choice (e.g., **Ctrl+Alt+A**)

---

## 🔍 FINDING THE APPS

### Where to Look:
- Activities → Search "Audio"
- Activities → Search "Streaming"
- Applications → AudioVideo section
- Show All Applications grid

### Search Keywords:
- audio
- streaming
- server
- client
- broadcast
- listen

---

## 📱 TRANSFERRING TO LAPTOP 2

### Copy entire project:
```bash
# On Laptop 1
scp -r /home/dharmesh.p/Trial/audioListner user@laptop2:~/

# On Laptop 2
cd ~/audioListner
./install_apps.sh
```

---

## ✨ WHAT YOU GET

### Before:
❌ Terminal commands
❌ Navigate to folders
❌ Remember Python paths
❌ Type complex commands

### Now:
✅ Click from menu
✅ No terminal needed
✅ One-click launch
✅ Professional apps
✅ Pin to dock
✅ Desktop shortcuts

---

## 🎵 READY TO USE!

### On Laptop 1:
1. Press **Super** key
2. Type **"Server"**
3. Click and stream! 🎵

### On Laptop 2:
1. Press **Super** key
2. Type **"Client"**
3. Click and listen! 🎧

---

## 📞 QUICK LAUNCH COMMANDS

```bash
# Server
gio launch ~/.local/share/applications/audio-streaming-server.desktop

# Client
gio launch ~/.local/share/applications/audio-streaming-client.desktop
```

---

**🎉 Enjoy your professional audio streaming applications!**

*No more terminal commands - just click and go!* 🚀
