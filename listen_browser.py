#!/usr/bin/env python3
"""
Simple Browser Audio Listener
Listens to audio from your Brave browser (or any system audio) and displays levels in real-time.
"""

import sounddevice as sd
import numpy as np
from datetime import datetime
import sys


def get_monitor_device():
    """
    Find the best audio input device for capturing system audio
    """
    devices = sd.query_devices()
    
    # Look for explicit monitor devices
    for i, device in enumerate(devices):
        name = device['name'].lower()
        if 'monitor' in name and device['max_input_channels'] > 0:
            return i, device['name']
    
    # Fall back to PulseAudio
    for i, device in enumerate(devices):
        if device['name'] in ['pulse', 'default'] and device['max_input_channels'] > 0:
            return i, device['name']
    
    return None, None


def listen_to_audio():
    """
    Main function to listen to browser audio and display levels
    """
    print("=" * 70)
    print("🎵  BROWSER AUDIO LISTENER")
    print("=" * 70)
    print("\nThis will capture and display audio levels from your Brave browser")
    print("(and any other system audio playing)\n")
    
    # Get the monitor device
    device_idx, device_name = get_monitor_device()
    
    if device_idx is None:
        print("❌ Could not find a suitable audio capture device!")
        print("\nAvailable devices:")
        print(sd.query_devices())
        sys.exit(1)
    
    print(f"✓ Using audio device: {device_name}")
    print(f"  Device index: {device_idx}")
    print(f"  Sample rate: 44100 Hz")
    print(f"  Channels: Stereo (2)\n")
    
    print("📊 Audio Level Monitoring Active")
    print("-" * 70)
    print("💡 Play some music in your Brave browser to see the levels!")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Audio callback function
    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"⚠️  Status: {status}")
        
        # Calculate volume (RMS - Root Mean Square)
        volume_norm = np.linalg.norm(indata) * 10
        
        # Calculate peak level
        peak = np.abs(indata).max()
        
        # Calculate left and right channel levels
        left_level = np.abs(indata[:, 0]).mean() if indata.shape[1] > 0 else 0
        right_level = np.abs(indata[:, 1]).mean() if indata.shape[1] > 1 else 0
        
        # Create visual bar (0-50 characters)
        bar_length = int(min(volume_norm, 50))
        bar = '█' * bar_length
        
        # Format output with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding based on volume
        if volume_norm > 30:
            status_icon = "🔊"  # Loud
        elif volume_norm > 10:
            status_icon = "🔉"  # Medium
        elif volume_norm > 0.5:
            status_icon = "🔈"  # Quiet
        else:
            status_icon = "🔇"  # Silent
        
        print(f"\r[{timestamp}] {status_icon} Level: {volume_norm:6.1f} | Peak: {peak:.3f} | L:{left_level:.3f} R:{right_level:.3f} |{bar:<50}|", 
              end='', flush=True)
    
    try:
        # Open audio input stream
        with sd.InputStream(
            device=device_idx,
            channels=2,  # Stereo
            samplerate=44100,
            callback=audio_callback,
            blocksize=2048
        ):
            # Keep running until interrupted
            while True:
                sd.sleep(100)  # Sleep for 100ms
    
    except KeyboardInterrupt:
        print("\n\n" + "-" * 70)
        print("✓ Audio monitoring stopped")
        print("=" * 70)
    
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure PulseAudio is running: pulseaudio --check")
        print("   2. Set monitor as default source:")
        print("      pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor")
        print("   3. List audio sources: pactl list sources short")
        sys.exit(1)


if __name__ == "__main__":
    listen_to_audio()
