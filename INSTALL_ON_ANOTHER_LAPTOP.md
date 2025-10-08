# 📦 Installing Audio Streaming Apps on Another Laptop

## 🎯 Complete Installation Guide for Laptop 2

This guide shows you how to install the audio streaming applications on a second laptop (or any new system).

---

## 📋 Prerequisites

Before installing, make sure you have:

### 1. Python 3 and pip
```bash
python3 --version  # Should be 3.8 or higher
pip3 --version
```

### 2. Required System Packages
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-venv python3-tk portaudio19-dev

# Fedora
sudo dnf install python3-tkinter portaudio-devel
```

---

## 🚀 Installation Steps

### Step 1: Transfer Project to Laptop 2

Choose one method:

#### Method A: Using SCP (Secure Copy)
```bash
# On Laptop 1
cd /home/dharmesh.p/Trial
tar -czf audioListner.tar.gz audioListner/
scp audioListner.tar.gz user@laptop2-ip:~/

# On Laptop 2
cd ~
tar -xzf audioListner.tar.gz
cd audioListner
```

#### Method B: Using Git
```bash
# On Laptop 1 (if you have git repo)
cd /home/dharmesh.p/Trial/audioListner
git add .
git commit -m "Audio streaming apps"
git push

# On Laptop 2
git clone <your-repo-url>
cd audioListner
```

#### Method C: Using USB Drive
```bash
# Copy entire audioListner folder to USB
# Copy from USB to Laptop 2 home directory
cd ~/audioListner
```

### Step 2: Create Virtual Environment
```bash
cd ~/audioListner  # or wherever you copied it

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Verify activation
which python  # Should show path to .venv/bin/python
```

### Step 3: Install Python Dependencies
```bash
# Make sure virtual environment is activated
pip install --upgrade pip

# Install required packages
pip install sounddevice numpy

# Verify installation
pip list | grep -E "sounddevice|numpy"
```

### Step 4: Install Desktop Applications
```bash
# Make install script executable
chmod +x install_apps.sh

# Run installation
./install_apps.sh
```

You should see:
```
🎵 Installing Audio Streaming Applications...

📋 Installing desktop entries...
✓ Server app installed
✓ Client app installed
✓ Desktop database updated

✅ Installation complete!
```

### Step 5: Verify Installation
```bash
# Check desktop files exist
ls -la ~/.local/share/applications/audio-streaming-*

# Test launch
gio launch ~/.local/share/applications/audio-streaming-client.desktop
```

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Virtual environment exists: `ls -la .venv/`
- [ ] Python packages installed: `pip list`
- [ ] Desktop files created: `ls ~/.local/share/applications/audio-streaming-*`
- [ ] Apps appear in menu: Search "Audio Streaming"
- [ ] Server GUI launches (if Laptop 1)
- [ ] Client GUI launches (if Laptop 2)

---

## 🔧 Troubleshooting

### Problem: "No such file or directory" error
**Solution:** Make sure you're in the audioListner directory
```bash
cd ~/audioListner  # or your installation path
pwd  # Verify you're in the right place
```

### Problem: "python3-venv not found"
**Solution:** Install it
```bash
sudo apt-get install python3-venv
```

### Problem: "No module named 'sounddevice'"
**Solution:** Activate venv and install packages
```bash
source .venv/bin/activate
pip install sounddevice numpy
```

### Problem: Apps don't appear in menu
**Solution:** Update desktop database and log out/in
```bash
update-desktop-database ~/.local/share/applications
# Then log out and log back in
```

### Problem: "gtk-launch: no such application"
**Solution:** Use full path with gio
```bash
gio launch ~/.local/share/applications/audio-streaming-server.desktop
```

### Problem: Permission denied
**Solution:** Make scripts executable
```bash
chmod +x install_apps.sh
chmod +x server_ui/start_server_gui.sh
chmod +x client_ui/start_client_gui.sh
```

---

## 📱 Quick Setup for Different Scenarios

### Scenario 1: Both Laptops (Server + Client)
```bash
# Do full installation on both laptops
# Install all dependencies
# Run install_apps.sh on both
```

### Scenario 2: Only Client (Laptop 2)
```bash
# Full installation needed
# You need all files and dependencies
# Client GUI requires same setup as server
```

### Scenario 3: Multiple Clients
```bash
# Install on each client laptop
# All clients can connect to one server
```

---

## 🎯 What Gets Installed

### Files Installed:
```
~/.local/share/applications/
├── audio-streaming-server.desktop
└── audio-streaming-client.desktop
```

### Project Structure Needed:
```
~/audioListner/                          (or your path)
├── .venv/                               (virtual environment)
│   └── bin/python                       (Python interpreter)
├── server_ui/
│   ├── server_gui.py                    (Server application)
│   └── icon.svg                         (Server icon)
├── client_ui/
│   ├── client_gui.py                    (Client application)
│   └── icon.svg                         (Client icon)
└── install_apps.sh                      (Installation script)
```

---

## 🔄 Updating After Changes

If you make changes to the code:

```bash
# On the laptop with changes
cd ~/audioListner
./install_apps.sh  # Reinstall desktop entries

# Or transfer updated files to other laptop
scp -r ~/audioListner user@laptop2:~/
```

---

## 🎓 Installation Script Details

The `install_apps.sh` script automatically:

1. ✅ Detects the current installation directory
2. ✅ Creates desktop files with correct paths
3. ✅ Installs to `~/.local/share/applications/`
4. ✅ Updates desktop database
5. ✅ Makes desktop files executable
6. ✅ Works on any system, any username, any path

**Key Feature:** The script uses dynamic paths, so it works regardless of:
- Username (doesn't have to be dharmesh.p)
- Installation location (doesn't have to be /home/dharmesh.p/Trial/)
- System configuration

---

## 💡 Pro Tips

### Tip 1: Use the Same Virtual Environment
```bash
# Copy entire .venv folder with project
# Faster than reinstalling packages
```

### Tip 2: Verify Python Path
```bash
# Check what Python the desktop file uses
cat ~/.local/share/applications/audio-streaming-server.desktop | grep Exec
```

### Tip 3: Test Before Installing
```bash
# Test GUIs directly before installing
source .venv/bin/activate
cd server_ui
python server_gui.py  # Should launch GUI
```

### Tip 4: Batch Installation
```bash
# Create a setup script for quick setup on new systems
cat > setup.sh << 'EOF'
#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install sounddevice numpy
./install_apps.sh
EOF
chmod +x setup.sh
./setup.sh
```

---

## 📊 Installation Comparison

| Method | Pros | Cons |
|--------|------|------|
| SCP | Fast, direct | Requires network |
| Git | Version control | Requires repo |
| USB | No network needed | Manual transfer |
| Shared folder | Easy sync | Requires network setup |

---

## 🎉 After Installation

Once installed on Laptop 2:

### As Client:
1. Search: "Audio Streaming Client"
2. Click to launch
3. Enter Laptop 1's IP address
4. Click "Connect"
5. Enjoy audio! 🎧

### As Server (if needed):
1. Search: "Audio Streaming Server"
2. Click to launch
3. Set up audio monitoring
4. Click "Start Server"
5. Share your IP with clients

---

## 📝 Installation Summary

**What You Need:**
- Python 3.8+ with venv
- python3-tk (for GUI)
- portaudio (for audio)
- sounddevice and numpy (Python packages)

**What You Do:**
1. Copy audioListner folder to Laptop 2
2. Create virtual environment: `python3 -m venv .venv`
3. Activate venv: `source .venv/bin/activate`
4. Install packages: `pip install sounddevice numpy`
5. Install apps: `./install_apps.sh`

**What You Get:**
- Desktop applications in menu
- Server GUI (for streaming)
- Client GUI (for listening)
- Icons and proper integration

---

## ✅ Success Indicators

You know installation worked when:

✅ No errors during install_apps.sh
✅ Desktop files exist in ~/.local/share/applications/
✅ Apps appear when searching "Audio Streaming"
✅ Apps launch without errors
✅ Python packages are installed
✅ Virtual environment is activated

---

**🎊 You're all set! Enjoy your audio streaming system on multiple laptops!**

For any issues, check the troubleshooting section or the error messages carefully.
