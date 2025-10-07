import sounddevice as sd
import numpy as np
import wave
import sys
from datetime import datetime
import time

class BrowserAudioListener:
    def __init__(self, output_file="system_audio.wav", duration=10):
        """
        Initialize the audio listener for browser audio
        
        Args:
            output_file: Name of the output WAV file
            duration: Recording duration in seconds
        """
        self.output_file = output_file
        self.duration = duration
        self.samplerate = 44100
        self.channels = 2
        self.frames = []
        
    def list_audio_devices(self):
        """List all available audio devices"""
        print("\n=== Available Audio Devices ===")
        devices = sd.query_devices()
        
        for i, device in enumerate(devices):
            print(f"\nDevice {i}: {device['name']}")
            print(f"  Max Input Channels: {device['max_input_channels']}")
            print(f"  Max Output Channels: {device['max_output_channels']}")
            print(f"  Default Sample Rate: {device['default_samplerate']}")
            print(f"  Host API: {sd.query_hostapis(device['hostapi'])['name']}")
        
        print("\n=== PulseAudio Monitor Devices (for system audio) ===")
        for i, device in enumerate(devices):
            if 'monitor' in device['name'].lower():
                print(f"Device {i}: {device['name']} ⭐ (Use this for system audio)")
    
    def get_monitor_device(self):
        """
        Find PulseAudio monitor device for system audio capture
        Returns device index or None
        """
        devices = sd.query_devices()
        
        # Look for monitor devices (these capture system audio output)
        for i, device in enumerate(devices):
            name = device['name'].lower()
            if 'monitor' in name and device['max_input_channels'] > 0:
                return i
        
        # If no explicit monitor device found, try PulseAudio default
        # Device 6 or 7 is usually 'pulse' or 'default' which can capture from monitor
        for i, device in enumerate(devices):
            if device['name'] in ['pulse', 'default'] and device['max_input_channels'] > 0:
                print(f"  Using PulseAudio device: {device['name']}")
                return i
        
        return None
    
    def record_audio(self, device_index=None):
        """
        Record system audio
        
        Args:
            device_index: Specific device index to use (None = auto-detect monitor)
        """
        if device_index is None:
            device_index = self.get_monitor_device()
            if device_index is None:
                print("\nWarning: No monitor device found.")
                print("On Ubuntu/Linux with PulseAudio:")
                print("  Monitor devices should be available by default")
                print("  Look for devices with 'monitor' in the name")
                print("\nUsing default input device instead...")
        
        if device_index is not None:
            device_info = sd.query_devices(device_index)
            print(f"\nRecording from: {device_info['name']}")
            print(f"Device index: {device_index}")
        else:
            print("\nRecording from default input device")
        
        try:
            print(f"\nRecording for {self.duration} seconds...")
            print("Play audio on your system now - it will be captured.")
            print("Press Ctrl+C to stop early\n")
            
            # Record audio
            recording = sd.rec(
                int(self.duration * self.samplerate),
                samplerate=self.samplerate,
                channels=self.channels,
                device=device_index,
                dtype='int16'
            )
            
            # Show progress
            for i in range(self.duration):
                sd.sleep(1000)  # Sleep 1 second
                progress = (i + 1) / self.duration * 100
                print(f"\rProgress: {progress:.0f}%", end='')
            
            sd.wait()  # Wait until recording is finished
            print("\n\nRecording complete!")
            
            self.frames = recording
            self.save_audio()
            
        except KeyboardInterrupt:
            print("\n\nRecording stopped by user.")
            sd.stop()
        except Exception as e:
            print(f"\nError recording audio: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure PulseAudio is running: pulseaudio --check")
            print("2. List devices with: pactl list sources short")
            print("3. Try a different device index")
    
    def save_audio(self):
        """Save recorded audio to WAV file"""
        with wave.open(self.output_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.samplerate)
            wf.writeframes(self.frames.tobytes())
        
        print(f"Audio saved to: {self.output_file}")
        
        # Show file info
        import os
        size = os.path.getsize(self.output_file) / 1024 / 1024
        print(f"File size: {size:.2f} MB")
    
    def monitor_audio_levels(self, device_index=None, duration=30):
        """
        Monitor audio levels in real-time without saving
        
        Args:
            device_index: Specific device index to use
            duration: Monitoring duration in seconds
        """
        if device_index is None:
            device_index = self.get_monitor_device()
        
        if device_index is not None:
            device_info = sd.query_devices(device_index)
            print(f"\nMonitoring: {device_info['name']}")
        
        print(f"\nMonitoring audio levels for {duration} seconds...")
        print("Press Ctrl+C to stop\n")
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            
            volume = np.linalg.norm(indata) * 10
            bar_length = int(volume)
            bar = '█' * min(bar_length, 50)
            print(f"\rVolume: {volume:6.1f} |{bar:<50}|", end='')
        
        try:
            with sd.InputStream(
                device=device_index,
                channels=self.channels,
                samplerate=self.samplerate,
                callback=callback
            ):
                sd.sleep(duration * 1000)
            
            print("\n\nMonitoring stopped.")
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user.")
        except Exception as e:
            print(f"\nError monitoring audio: {e}")
    
    def stream_audio_callback(self, device_index=None):
        """
        Stream audio with a custom callback function
        Useful for real-time audio processing
        
        Args:
            device_index: Specific device index to use
        """
        if device_index is None:
            device_index = self.get_monitor_device()
        
        print("\nStreaming audio with callback (Press Ctrl+C to stop)...")
        print("This demonstrates real-time audio processing\n")
        
        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            
            # Example: Detect loud sounds
            volume = np.abs(indata).mean()
            if volume > 0.1:  # Threshold
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{timestamp}] Audio detected! Volume: {volume:.3f}")
        
        try:
            with sd.InputStream(
                device=device_index,
                channels=self.channels,
                samplerate=self.samplerate,
                callback=audio_callback
            ):
                print("Listening... (play some audio)")
                while True:
                    sd.sleep(100)
        except KeyboardInterrupt:
            print("\n\nStreaming stopped.")
        except Exception as e:
            print(f"\nError: {e}")


def listen_to_browser_audio():
    """
    Simple function to listen to browser audio and display levels
    Perfect for monitoring Brave browser audio playback
    """
    print("=== Browser Audio Listener ===")
    print("This will capture audio from your Brave browser (and other system audio)\n")
    
    listener = BrowserAudioListener()
    
    # Find the monitor device
    monitor_device = listener.get_monitor_device()
    
    if monitor_device is None:
        print("⚠️  No PulseAudio monitor device found!")
        print("\nShowing all available devices:")
        listener.list_audio_devices()
        print("\n💡 Tip: Look for a device with 'monitor' in its name")
        
        try:
            device_choice = input("\nEnter device index to use (or press Enter to use default): ").strip()
            monitor_device = int(device_choice) if device_choice else None
        except ValueError:
            monitor_device = None
    else:
        device_info = sd.query_devices(monitor_device)
        print(f"✓ Auto-detected monitor device: {device_info['name']}")
        print(f"  Device index: {monitor_device}\n")
    
    # Start listening
    print("🎵 Starting audio level monitoring...")
    print("   Play music in your Brave browser now!")
    print("   Press Ctrl+C to stop\n")
    print("-" * 60)
    
    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"⚠️  {status}")
        
        # Calculate volume (RMS - Root Mean Square)
        volume_norm = np.linalg.norm(indata) * 10
        
        # Calculate peak level
        peak = np.abs(indata).max()
        
        # Create visual bar
        bar_length = int(volume_norm)
        bar = '█' * min(bar_length, 50)
        
        # Format output
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\r[{timestamp}] Level: {volume_norm:6.1f} Peak: {peak:.3f} |{bar:<50}|", end='', flush=True)
    
    try:
        with sd.InputStream(
            device=monitor_device,
            channels=listener.channels,
            samplerate=listener.samplerate,
            callback=audio_callback
        ):
            # Keep running until interrupted
            while True:
                sd.sleep(100)
    
    except KeyboardInterrupt:
        print("\n\n" + "-" * 60)
        print("✓ Monitoring stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure PulseAudio is running: pulseaudio --check")
        print("   2. List audio sources: pactl list sources short")
        print("   3. Try running with a different device index")


def main():
    print("=== Brave Browser Audio Listener ===\n")
    
    listener = BrowserAudioListener(duration=10)
    
    print("Options:")
    print("1. Listen to browser audio (real-time levels) ⭐ RECOMMENDED")
    print("2. List all audio devices")
    print("3. Record system audio (10 seconds)")
    print("4. Monitor audio levels (30 seconds)")
    print("5. Stream with callback (real-time processing)")
    
    try:
        choice = input("\nEnter choice (1-5, or press Enter for option 1): ").strip()
        
        if choice == '' or choice == '1':
            listen_to_browser_audio()
        elif choice == '2':
            listener.list_audio_devices()
        elif choice == '3':
            monitor_idx = listener.get_monitor_device()
            listener.record_audio(device_index=monitor_idx)
        elif choice == '4':
            monitor_idx = listener.get_monitor_device()
            listener.monitor_audio_levels(device_index=monitor_idx)
        elif choice == '5':
            monitor_idx = listener.get_monitor_device()
            listener.stream_audio_callback(device_index=monitor_idx)
        else:
            print("Invalid choice")
    except KeyboardInterrupt:
        print("\n\n✓ Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
