# 🚀 Quick Start - Installing on Laptop 2

## One-Command Installation

For a new laptop, just run:

```bash
./quick_setup.sh
```

This will:
1. ✅ Check Python version
2. ✅ Install system dependencies
3. ✅ Create virtual environment
4. ✅ Install Python packages
5. ✅ Install desktop applications
6. ✅ Update application menu

---

## Manual Installation (Step by Step)

If you prefer to do it manually:

### Step 1: Transfer Files
Copy the entire `audioListner` folder to Laptop 2 (via USB, SCP, or network share)

### Step 2: Install System Packages
```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-tk portaudio19-dev
```

### Step 3: Create Virtual Environment
```bash
cd audioListner
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Python Packages
```bash
pip install --upgrade pip
pip install sounddevice numpy
```

### Step 5: Install Desktop Apps
```bash
./install_apps.sh
```

---

## What Gets Installed

### System Level:
- `~/.local/share/applications/audio-streaming-server.desktop`
- `~/.local/share/applications/audio-streaming-client.desktop`

### Project Directory:
- `.venv/` - Virtual environment with packages
- `server_ui/` - Server application
- `client_ui/` - Client application

---

## Launching the Apps

### From Application Menu:
1. Press **Super** key
2. Type: **"Audio Streaming"**
3. Click on the app you want

### From Terminal:
```bash
# Server
gio launch ~/.local/share/applications/audio-streaming-server.desktop

# Client
gio launch ~/.local/share/applications/audio-streaming-client.desktop
```

---

## Troubleshooting

### "gtk-launch: no such application"
**Cause:** The desktop files use the wrong paths  
**Solution:** Run `./install_apps.sh` again - it will detect your current path

### "No module named 'sounddevice'"
**Cause:** Virtual environment not activated or packages not installed  
**Solution:**
```bash
source .venv/bin/activate
pip install sounddevice numpy
```

### Apps don't appear in menu
**Cause:** Desktop database not updated  
**Solution:**
```bash
update-desktop-database ~/.local/share/applications
# Log out and log back in
```

### "Permission denied"
**Cause:** Scripts not executable  
**Solution:**
```bash
chmod +x quick_setup.sh install_apps.sh
```

---

## Verification

Check that everything is installed:

```bash
# Virtual environment exists
ls -la .venv/

# Python packages installed
source .venv/bin/activate
pip list | grep -E "sounddevice|numpy"

# Desktop files exist
ls -la ~/.local/share/applications/audio-streaming-*

# Apps appear in menu
# Press Super and search "Audio Streaming"
```

---

## Different Paths?

The installation script automatically detects where you installed the project.

**Examples that work:**
- `/home/user/audioListner/`
- `/opt/audioListner/`
- `/home/john/Projects/audioListner/`
- Any path you choose!

Just run `./install_apps.sh` and it will use the correct paths.

---

## Updating

If you update the code:

```bash
# Pull new changes or copy updated files
cd audioListner

# Reinstall desktop apps (updates paths if needed)
./install_apps.sh
```

---

## Uninstalling

```bash
./uninstall_apps.sh
```

This removes the desktop applications from your menu.

To completely remove:
```bash
./uninstall_apps.sh
cd ..
rm -rf audioListner/
```

---

## Summary

**Easiest way:**
```bash
./quick_setup.sh
```

**That's it!** Your apps are now installed and ready to use.

Search for "Audio Streaming" in your application menu! 🎉
