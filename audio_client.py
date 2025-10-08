#!/usr/bin/env python3
"""
Audio Streaming Client
Receives audio stream from server and plays it on the local speakers.
Run this on the laptop where you want to hear the music.
"""

import sounddevice as sd
import numpy as np
import socket
import struct
import sys
import signal
import atexit
from datetime import datetime
import queue
import threading


class AudioStreamClient:
    def __init__(self, server_ip, server_port=9999):
        """
        Initialize audio streaming client
        
        Args:
            server_ip: IP address of the streaming server
            server_port: Port of the streaming server
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.running = False
        self.audio_queue = queue.Queue(maxsize=50)
        self.stream = None
        
        # These will be received from server
        self.samplerate = None
        self.channels = None
        self.blocksize = None
        
        # Register cleanup handlers
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle termination signals"""
        print("\n\n" + "-" * 70)
        print("✓ Received shutdown signal, stopping client...")
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
            
            # Close socket
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
    
    def connect_to_server(self):
        """Connect to the audio streaming server"""
        print("=" * 70)
        print("🎵  AUDIO STREAMING CLIENT")
        print("=" * 70)
        print(f"\n📡 Connecting to server {self.server_ip}:{self.server_port}...")
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            print("✓ Connected to server!\n")
            
            # Receive audio configuration
            config_data = self.socket.recv(12)
            self.samplerate, self.channels, self.blocksize = struct.unpack('III', config_data)
            
            print(f"✓ Audio configuration received:")
            print(f"  Sample rate: {self.samplerate} Hz")
            print(f"  Channels: {self.channels} (Stereo)")
            print(f"  Block size: {self.blocksize} frames\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\n💡 Make sure:")
            print("   1. The server is running on the other laptop")
            print("   2. You're using the correct IP address")
            print("   3. Firewall allows port 9999")
            return False
    
    def receive_audio(self):
        """Receive audio data from server and put it in queue"""
        while self.running:
            try:
                # Receive size of incoming data
                size_data = self.socket.recv(4)
                if not size_data:
                    print("\n❌ Server disconnected")
                    self.running = False
                    break
                
                size = struct.unpack('I', size_data)[0]
                
                # Receive the actual audio data
                audio_data = b''
                while len(audio_data) < size:
                    chunk = self.socket.recv(size - len(audio_data))
                    if not chunk:
                        break
                    audio_data += chunk
                
                # Convert bytes to numpy array
                audio_array = np.frombuffer(audio_data, dtype='float32').reshape(-1, self.channels)
                
                # Add to queue (drop if full to avoid latency buildup)
                try:
                    self.audio_queue.put_nowait(audio_array)
                except queue.Full:
                    # Drop oldest frame if queue is full
                    try:
                        self.audio_queue.get_nowait()
                        self.audio_queue.put_nowait(audio_array)
                    except:
                        pass
                        
            except Exception as e:
                if self.running:
                    print(f"\n❌ Error receiving audio: {e}")
                break
    
    def audio_callback(self, outdata, frames, time_info, status):
        """Callback function to play received audio"""
        if status:
            print(f"⚠️  Playback status: {status}")
        
        try:
            # Get audio from queue
            data = self.audio_queue.get_nowait()
            
            # If data size doesn't match, pad or truncate
            if len(data) < frames:
                # Pad with zeros
                data = np.pad(data, ((0, frames - len(data)), (0, 0)), mode='constant')
            elif len(data) > frames:
                # Truncate
                data = data[:frames]
            
            outdata[:] = data
            
            # Display status
            volume = np.linalg.norm(data) * 10
            queue_size = self.audio_queue.qsize()
            bar_length = int(min(volume, 30))
            bar = '█' * bar_length
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\r[{timestamp}] 🔊 Level: {volume:6.1f} | Buffer: {queue_size:2d} | {bar:<30}|", 
                  end='', flush=True)
            
        except queue.Empty:
            # No data available, output silence
            outdata.fill(0)
    
    def start_playback(self):
        """Start receiving and playing audio"""
        if not self.connect_to_server():
            return
        
        self.running = True
        
        # Start receiving thread
        receive_thread = threading.Thread(target=self.receive_audio, daemon=True)
        receive_thread.start()
        
        print("-" * 70)
        print("🎧 Playing audio from server...")
        print("🛑 Press Ctrl+C to stop")
        print("💡 Playback will automatically stop when you close the terminal\n")
        
        try:
            # Open audio output stream
            self.stream = sd.OutputStream(
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
            print("✓ Stopping playback...")
        
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
            
            # Close socket
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
            
            print("✓ Client stopped")
            print("=" * 70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Audio Streaming Client - Play audio from server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audio_client.py 192.168.1.100
  python audio_client.py 192.168.1.100 --port 9999
        """
    )
    parser.add_argument('server_ip', help='IP address of the streaming server')
    parser.add_argument('--port', type=int, default=9999, help='Server port (default: 9999)')
    
    args = parser.parse_args()
    
    client = AudioStreamClient(server_ip=args.server_ip, server_port=args.port)
    client.start_playback()


if __name__ == "__main__":
    main()
