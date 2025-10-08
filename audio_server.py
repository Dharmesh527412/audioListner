#!/usr/bin/env python3
"""
Audio Streaming Server
Captures audio from browser and streams it over the network to clients.
Run this on the laptop that has the Brave browser playing music.
"""

import sounddevice as sd
import numpy as np
import socket
import struct
import threading
import sys
import signal
import atexit
from datetime import datetime


class AudioStreamServer:
    def __init__(self, host='0.0.0.0', port=9999):
        """
        Initialize audio streaming server
        
        Args:
            host: IP address to bind to (0.0.0.0 = all interfaces)
            port: Port to listen on
        """
        self.host = host
        self.port = port
        self.samplerate = 44100
        self.channels = 2
        self.blocksize = 2048
        self.clients = []
        self.running = False
        self.server_socket = None
        self.stream = None
        
        # Register cleanup handlers
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle termination signals"""
        print("\n\n" + "-" * 70)
        print("✓ Received shutdown signal, stopping server...")
        self.running = False
        sys.exit(0)
    
    def cleanup(self):
        """Cleanup function called on exit"""
        if self.running:
            self.running = False
            
            # Stop audio stream
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except:
                    pass
            
            # Close all client connections
            for client in self.clients[:]:
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
            
            # Close server socket
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
    
    def get_monitor_device(self):
        """Find the best audio input device for capturing system audio (OUTPUT monitor only, NOT microphone)"""
        devices = sd.query_devices()
        
        # Look for explicit monitor devices (these capture system OUTPUT, not microphone input)
        # Exclude any microphone or input devices
        for i, device in enumerate(devices):
            name = device['name'].lower()
            # Only accept monitor devices, explicitly exclude microphone/input devices
            if 'monitor' in name and device['max_input_channels'] > 0:
                # Exclude microphone-related devices
                if any(keyword in name for keyword in ['mic', 'microphone', 'input', 'capture']):
                    continue
                return i, device['name']
        
        # Fall back to PulseAudio via 'pulse' or 'default' device
        # When PulseAudio default source is set to a monitor, these will capture it
        for i, device in enumerate(devices):
            name = device['name'].lower()
            # Use 'pulse' device which will use PulseAudio's default source (the monitor)
            if name == 'pulse' and device['max_input_channels'] > 0:
                return i, device['name']
        
        # Try 'default' as another fallback (which also uses PulseAudio)
        for i, device in enumerate(devices):
            name = device['name'].lower()
            if name == 'default' and device['max_input_channels'] > 0:
                return i, device['name']
        
        return None, None
    
    def get_local_ip(self):
        """Get the local IP address of this machine"""
        try:
            # Create a socket to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def accept_clients(self):
        """Accept incoming client connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1.0)  # Timeout to check running flag
        
        print(f"🌐 Server listening on {self.host}:{self.port}")
        print(f"📡 Clients should connect to: {self.get_local_ip()}:{self.port}\n")
        
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"✓ New client connected: {address[0]}:{address[1]}")
                
                # Send audio configuration to client
                config_data = struct.pack('III', self.samplerate, self.channels, self.blocksize)
                client_socket.sendall(config_data)
                
                self.clients.append(client_socket)
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"❌ Error accepting client: {e}")
    
    def audio_callback(self, indata, frames, time_info, status):
        """Callback function to capture and stream audio"""
        if status:
            print(f"⚠️  Audio status: {status}")
        
        # Calculate volume for display
        volume_norm = np.linalg.norm(indata) * 10
        
        # Convert to bytes
        audio_bytes = indata.tobytes()
        
        # Send to all connected clients
        disconnected_clients = []
        for client in self.clients:
            try:
                # Send size of data first, then the data
                size = struct.pack('I', len(audio_bytes))
                client.sendall(size + audio_bytes)
            except Exception as e:
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            if client in self.clients:
                self.clients.remove(client)
                print(f"❌ Client disconnected")
        
        # Display status
        client_count = len(self.clients)
        bar_length = int(min(volume_norm, 30))
        bar = '█' * bar_length
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\r[{timestamp}] 🔊 Level: {volume_norm:6.1f} | Clients: {client_count} | {bar:<30}|", 
              end='', flush=True)
    
    def start_streaming(self):
        """Start the audio streaming server"""
        print("=" * 70)
        print("🎵  AUDIO STREAMING SERVER")
        print("=" * 70)
        print("\nCaptures audio OUTPUT from Brave browser and streams it over the network")
        print("🎤 MICROPHONE INPUT IS NOT CAPTURED - Only system audio output\n")
        
        # Get the monitor device
        device_idx, device_name = self.get_monitor_device()
        
        if device_idx is None:
            print("❌ Could not find a suitable audio OUTPUT monitor device!")
            print("\nThis application captures ONLY system audio output (browser audio).")
            print("It does NOT capture microphone input.")
            print("\nRun this command first to set up OUTPUT monitoring:")
            print("  pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor")
            sys.exit(1)
        
        print(f"✓ Audio device: {device_name}")
        print(f"  Device index: {device_idx}")
        print(f"  Sample rate: {self.samplerate} Hz")
        print(f"  Channels: {self.channels} (Stereo)")
        print(f"  Block size: {self.blocksize} frames\n")
        
        self.running = True
        
        # Start client acceptance thread
        accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
        accept_thread.start()
        
        print("-" * 70)
        print("🛑 Press Ctrl+C to stop streaming")
        print("💡 Streaming will automatically stop when you close the terminal\n")
        
        try:
            # Open audio input stream
            self.stream = sd.InputStream(
                device=device_idx,
                channels=self.channels,
                samplerate=self.samplerate,
                callback=self.audio_callback,
                blocksize=self.blocksize,
                dtype='float32'
            )
            self.stream.start()
            
            # Keep running until interrupted
            while self.running:
                sd.sleep(100)
        
        except KeyboardInterrupt:
            print("\n\n" + "-" * 70)
            print("✓ Stopping server...")
        
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
        
        finally:
            self.running = False
            
            # Stop audio stream
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except:
                    pass
            
            # Close all client connections
            for client in self.clients[:]:
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
            
            # Close server socket
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
            
            print("✓ Server stopped")
            print("=" * 70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Audio Streaming Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=9999, help='Port to listen on (default: 9999)')
    
    args = parser.parse_args()
    
    server = AudioStreamServer(host=args.host, port=args.port)
    server.start_streaming()


if __name__ == "__main__":
    main()
