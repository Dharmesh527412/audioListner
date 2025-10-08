#!/usr/bin/env python3
"""
Audio Streaming Server GUI
Modern UI for streaming audio from Laptop 1 to clients.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sounddevice as sd
import numpy as np
import socket
import struct
import threading
import sys
from datetime import datetime
import queue


class AudioStreamServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Streaming Server - Laptop 1")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Audio parameters
        self.host = '0.0.0.0'
        self.port = 9999
        self.samplerate = 44100
        self.channels = 2
        self.blocksize = 2048
        self.clients = []
        self.running = False
        self.server_socket = None
        self.stream = None
        
        # UI update queue
        self.log_queue = queue.Queue()
        
        self.setup_ui()
        self.update_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🎵 Audio Streaming Server",
            font=('Helvetica', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(15, 2))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Streams system audio OUTPUT only - No microphone input",
            font=('Helvetica', 9),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Server Info Section
        info_frame = tk.LabelFrame(main_frame, text="Server Information", font=('Helvetica', 10, 'bold'), bg='#ecf0f1')
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_content = tk.Frame(info_frame, bg='#ecf0f1')
        info_content.pack(padx=10, pady=10, fill=tk.X)
        
        # IP Address
        self.ip_label = tk.Label(
            info_content,
            text=f"Server IP: {self.get_local_ip()}",
            font=('Courier', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.ip_label.pack(anchor='w', pady=2)
        
        # Port
        self.port_label = tk.Label(
            info_content,
            text=f"Port: {self.port}",
            font=('Courier', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.port_label.pack(anchor='w', pady=2)
        
        # Status
        self.status_label = tk.Label(
            info_content,
            text="Status: ⚫ Stopped",
            font=('Helvetica', 11, 'bold'),
            bg='#ecf0f1',
            fg='#e74c3c'
        )
        self.status_label.pack(anchor='w', pady=2)
        
        # Connected Clients
        self.clients_label = tk.Label(
            info_content,
            text="Connected Clients: 0",
            font=('Helvetica', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.clients_label.pack(anchor='w', pady=2)
        
        # Audio Device
        self.device_label = tk.Label(
            info_content,
            text="Audio Device: Not selected",
            font=('Helvetica', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.device_label.pack(anchor='w', pady=2)
        
        # Control Buttons Frame
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ Start Server",
            command=self.start_server,
            font=('Helvetica', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            cursor='hand2',
            relief=tk.RAISED,
            bd=3,
            width=15,
            height=2
        )
        self.start_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⬛ Stop Server",
            command=self.stop_server,
            font=('Helvetica', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            cursor='hand2',
            relief=tk.RAISED,
            bd=3,
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Audio Level Frame
        level_frame = tk.LabelFrame(main_frame, text="Audio Level", font=('Helvetica', 10, 'bold'), bg='#ecf0f1')
        level_frame.pack(fill=tk.X, pady=(0, 10))
        
        level_content = tk.Frame(level_frame, bg='#ecf0f1')
        level_content.pack(padx=10, pady=10, fill=tk.X)
        
        self.level_canvas = tk.Canvas(level_content, height=30, bg='#34495e', highlightthickness=0)
        self.level_canvas.pack(fill=tk.X, pady=5)
        
        self.level_text = tk.Label(
            level_content,
            text="Volume: 0%",
            font=('Courier', 10),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.level_text.pack()
        
        # Log Frame
        log_frame = tk.LabelFrame(main_frame, text="Server Log", font=('Helvetica', 10, 'bold'), bg='#ecf0f1')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white',
            state=tk.DISABLED
        )
        self.log_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.log_text.tag_config('info', foreground='#3498db')
        self.log_text.tag_config('success', foreground='#2ecc71')
        self.log_text.tag_config('warning', foreground='#f39c12')
        self.log_text.tag_config('error', foreground='#e74c3c')
        
        self.log("Welcome to Audio Streaming Server!", 'info')
        self.log("Click 'Start Server' to begin streaming audio.", 'info')
    
    def get_local_ip(self):
        """Get the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def log(self, message, tag='info'):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put((f"[{timestamp}] {message}", tag))
    
    def update_log(self):
        """Update log from queue"""
        try:
            while True:
                message, tag = self.log_queue.get_nowait()
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, message + '\n', tag)
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)
        except queue.Empty:
            pass
    
    def update_ui(self):
        """Periodic UI update"""
        self.update_log()
        self.root.after(100, self.update_ui)
    
    def get_monitor_device(self):
        """Find the best audio OUTPUT monitor device (NOT microphone)"""
        devices = sd.query_devices()
        
        # Look for monitor devices (these capture system OUTPUT, not microphone input)
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
    
    def accept_clients(self):
        """Accept incoming client connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.log(f"New client connected: {address[0]}:{address[1]}", 'success')
                
                # Send audio configuration
                config_data = struct.pack('III', self.samplerate, self.channels, self.blocksize)
                client_socket.sendall(config_data)
                
                self.clients.append(client_socket)
                self.root.after(0, self.update_client_count)
            except socket.timeout:
                continue
            except OSError:
                # Socket was closed, exit gracefully
                break
            except Exception as e:
                if self.running:
                    self.log(f"Error accepting client: {e}", 'error')
                break
    
    def update_client_count(self):
        """Update connected clients count"""
        self.clients_label.config(text=f"Connected Clients: {len(self.clients)}")
    
    def audio_callback(self, indata, frames, time_info, status):
        """Audio capture callback"""
        if not self.running:
            # Stop processing if server is stopped
            raise sd.CallbackStop()
        
        if status:
            self.log(f"Audio status: {status}", 'warning')
        
        # Calculate volume
        volume_norm = np.linalg.norm(indata) * 10
        volume_percent = min(int(volume_norm), 100)
        
        # Update level display
        self.root.after(0, self.update_level, volume_percent)
        
        # Convert to bytes
        audio_bytes = indata.tobytes()
        size = len(audio_bytes)
        
        # Send to all clients
        disconnected = []
        for client in self.clients:
            try:
                client.sendall(struct.pack('I', size))
                client.sendall(audio_bytes)
            except:
                disconnected.append(client)
        
        # Remove disconnected clients
        for client in disconnected:
            if client in self.clients:
                self.clients.remove(client)
                try:
                    client.close()
                except:
                    pass
            self.root.after(0, self.update_client_count)
            self.log("Client disconnected", 'warning')
    
    def update_level(self, volume_percent):
        """Update volume level visualization"""
        self.level_text.config(text=f"Volume: {volume_percent}%")
        
        # Draw level bar
        canvas_width = self.level_canvas.winfo_width()
        canvas_height = self.level_canvas.winfo_height()
        
        if canvas_width > 1:
            self.level_canvas.delete("all")
            
            # Background
            self.level_canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill='#34495e', outline='')
            
            # Level bar with color gradient
            bar_width = (volume_percent / 100) * canvas_width
            if volume_percent > 80:
                color = '#e74c3c'  # Red
            elif volume_percent > 50:
                color = '#f39c12'  # Orange
            else:
                color = '#2ecc71'  # Green
            
            self.level_canvas.create_rectangle(0, 0, bar_width, canvas_height, fill=color, outline='')
    
    def start_server(self):
        """Start the audio streaming server"""
        try:
            # Find audio OUTPUT monitor device (NOT microphone)
            device_idx, device_name = self.get_monitor_device()
            if device_idx is None:
                self.log("Error: No suitable audio OUTPUT monitor device found!", 'error')
                self.log("This captures ONLY system audio output, NOT microphone.", 'error')
                self.log("Run: pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor", 'error')
                return
            
            self.log(f"Using audio OUTPUT device: {device_name}", 'success')
            self.log("Streaming system audio OUTPUT only - microphone NOT captured", 'info')
            self.device_label.config(text=f"Audio Device: {device_name}")
            
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)
            
            self.running = True
            
            # Start client acceptor thread
            accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
            accept_thread.start()
            
            # Start audio stream
            self.stream = sd.InputStream(
                device=device_idx,
                samplerate=self.samplerate,
                channels=self.channels,
                blocksize=self.blocksize,
                callback=self.audio_callback
            )
            self.stream.start()
            
            # Update UI
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: 🟢 Running", fg='#27ae60')
            
            self.log("Server started successfully!", 'success')
            self.log(f"Listening on {self.get_local_ip()}:{self.port}", 'success')
            self.log("Waiting for clients to connect...", 'info')
            
        except Exception as e:
            self.log(f"Error starting server: {e}", 'error')
            self.running = False
    
    def stop_server(self):
        """Stop the audio streaming server"""
        try:
            self.log("Stopping server...", 'info')
            self.running = False
            
            # Stop audio stream first
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except:
                    pass
                finally:
                    self.stream = None
            
            # Close all client connections
            clients_copy = self.clients.copy()
            for client in clients_copy:
                try:
                    client.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
            
            # Close server socket
            if self.server_socket:
                try:
                    self.server_socket.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                try:
                    self.server_socket.close()
                except:
                    pass
                finally:
                    self.server_socket = None
            
            # Give threads time to finish
            import time
            time.sleep(0.5)
            
            # Update UI
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: ⚫ Stopped", fg='#e74c3c')
            self.update_client_count()
            self.device_label.config(text="Audio Device: Not selected")
            
            # Clear level display
            self.level_canvas.delete("all")
            self.level_text.config(text="Volume: 0%")
            
            self.log("Server stopped.", 'warning')
            
        except Exception as e:
            self.log(f"Error stopping server: {e}", 'error')


def main():
    root = tk.Tk()
    app = AudioStreamServerGUI(root)
    
    # Handle window close
    def on_closing():
        if app.running:
            app.log("Closing application...", 'info')
            app.stop_server()
            # Give time for cleanup
            root.after(100, root.destroy)
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        if app.running:
            app.stop_server()


if __name__ == "__main__":
    main()
