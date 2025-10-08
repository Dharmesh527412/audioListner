#!/usr/bin/env python3
"""
Test script to verify audio device detection works
"""
import sys
sys.path.insert(0, '/home/dharmesh.p/Trial/audioListner')

from audio_server import AudioStreamServer

print("Testing audio device detection...")
print("=" * 60)

server = AudioStreamServer()
device_idx, device_name = server.get_monitor_device()

if device_idx is not None:
    print(f"✅ SUCCESS: Found audio device!")
    print(f"   Device Index: {device_idx}")
    print(f"   Device Name: {device_name}")
    print()
    print("The server should now start successfully.")
    print("You can now use:")
    print("  - python audio_server.py")
    print("  - python server_ui/server_gui.py")
else:
    print("❌ FAILED: No suitable audio device found")
    print()
    print("Please run:")
    print("  pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor")

print("=" * 60)
