#!/usr/bin/env python3
"""
Audio Streaming Client GUI
Modern UI for receiving audio stream on Laptop 2.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sounddevice as sd
import numpy as np
import socket
import struct
import sys
from datetime import datetime
import queue
import threading


class AudioStreamClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Streaming Client - Laptop 2")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        # Client parameters
        self.server_ip = ""
        self.server_port = 9999
        self.socket = None
        self.running = False
        self.audio_queue = queue.Queue(maxsize=50)
        self.stream = None
        
        # Audio config (received from server)
        self.samplerate = None
        self.channels = None
        self.blocksize = None
        
        # UI update queue
        self.log_queue = queue.Queue()
        
        # Statistics
        self.bytes_received = 0
        self.frames_received = 0
        
        self.setup_ui()
        self.update_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#16a085', height=80)
        header_frame.pack(fill=tk.X, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🎧 Audio Streaming Client",
            font=('Helvetica', 20, 'bold'),
            bg='#16a085',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Connection Settings Frame
        settings_frame = tk.LabelFrame(main_frame, text="Connection Settings", font=('Helvetica', 10, 'bold'), bg='#ecf0f1')
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        settings_content = tk.Frame(settings_frame, bg='#ecf0f1')
        settings_content.pack(padx=10, pady=10, fill=tk.X)
        
        # Server IP input
        ip_frame = tk.Frame(settings_content, bg='#ecf0f1')
        ip_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            ip_frame,
            text="Server IP Address:",
            font=('Helvetica', 10),
            bg='#ecf0f1',
            fg='#2c3e50',
            width=18,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.ip_entry = tk.Entry(
            ip_frame,
            font=('Courier', 11),
            width=25,
            relief=tk.SOLID,
            bd=1
        )
        self.ip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ip_entry.insert(0, "192.168.1.100")  # Default placeholder
        
        # Port input
        port_frame = tk.Frame(settings_content, bg='#ecf0f1')
        port_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            port_frame,
            text="Port:",
            font=('Helvetica', 10),
            bg='#ecf0f1',
            fg='#2c3e50',
            width=18,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.port_entry = tk.Entry(
            port_frame,
            font=('Courier', 11),
            width=10,
            relief=tk.SOLID,
            bd=1
        )
        self.port_entry.pack(side=tk.LEFT)
        self.port_entry.insert(0, "9999")
        
        # Client Info Section
        info_frame = tk.LabelFrame(main_frame, text="Client Information", font=('Helvetica', 10, 'bold'), bg='#ecf0f1')
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_content = tk.Frame(info_frame, bg='#ecf0f1')
        info_content.pack(padx=10, pady=10, fill=tk.X)
        
        # Status
        self.status_label = tk.Label(
            info_content,
            text="Status: ⚫ Disconnected",
            font=('Helvetica', 11, 'bold'),
            bg='#ecf0f1',
            fg='#e74c3c'
        )
        self.status_label.pack(anchor='w', pady=2)
        
        # Audio Config
        self.config_label = tk.Label(
            info_content,
            text="Audio Config: Not received",
            font=('Helvetica', 10),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.config_label.pack(anchor='w', pady=2)
        
        # Statistics
        self.stats_label = tk.Label(
            info_content,
            text="Data Received: 0 MB | Frames: 0",
            font=('Helvetica', 10),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.stats_label.pack(anchor='w', pady=2)
        
        # Output Device
        self.output_label = tk.Label(
            info_content,
            text="Output Device: Default",
            font=('Helvetica', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.output_label.pack(anchor='w', pady=2)
        
        # Control Buttons Frame
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.connect_button = tk.Button(
            button_frame,
            text="🔌 Connect",
            command=self.connect_to_server,
            font=('Helvetica', 12, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            cursor='hand2',
            relief=tk.RAISED,
            bd=3,
            width=15,
            height=2
        )
        self.connect_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.disconnect_button = tk.Button(
            button_frame,
            text="🔌 Disconnect",
            command=self.disconnect_from_server,
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
        self.disconnect_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Audio Level Frame
        level_frame = tk.LabelFrame(main_frame, text="Playback Level", font=('Helvetica', 10, 'bold'), bg='#ecf0f1')
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
        
        # Queue Status
        self.queue_label = tk.Label(
            level_content,
            text="Buffer: 0 / 50 frames",
            font=('Courier', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.queue_label.pack(pady=(5, 0))
        
        # Log Frame
        log_frame = tk.LabelFrame(main_frame, text="Client Log", font=('Helvetica', 10, 'bold'), bg='#ecf0f1')
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
        
        # Configure text tags
        self.log_text.tag_config('info', foreground='#3498db')
        self.log_text.tag_config('success', foreground='#2ecc71')
        self.log_text.tag_config('warning', foreground='#f39c12')
        self.log_text.tag_config('error', foreground='#e74c3c')
        
        self.log("Welcome to Audio Streaming Client!", 'info')
        self.log("Enter server IP address and click 'Connect' to start.", 'info')
    
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
        
        # Update statistics
        if self.running:
            mb_received = self.bytes_received / (1024 * 1024)
            self.stats_label.config(text=f"Data Received: {mb_received:.2f} MB | Frames: {self.frames_received}")
            
            # Update queue status
            queue_size = self.audio_queue.qsize()
            self.queue_label.config(text=f"Buffer: {queue_size} / 50 frames")
        
        self.root.after(100, self.update_ui)
    
    def connect_to_server(self):
        """Connect to the audio streaming server"""
        # Get IP and port
        self.server_ip = self.ip_entry.get().strip()
        try:
            self.server_port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")
            return
        
        if not self.server_ip:
            messagebox.showerror("Error", "Please enter server IP address!")
            return
        
        self.log(f"Connecting to {self.server_ip}:{self.server_port}...", 'info')
        
        # Start connection in thread
        connect_thread = threading.Thread(target=self._connect_thread, daemon=True)
        connect_thread.start()
    
    def _connect_thread(self):
        """Connection thread"""
        try:
            # Connect to server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10.0)
            self.socket.connect((self.server_ip, self.server_port))
            
            self.log("Connected to server!", 'success')
            
            # Receive audio configuration
            config_data = self.socket.recv(12)
            self.samplerate, self.channels, self.blocksize = struct.unpack('III', config_data)
            
            self.log(f"Audio config: {self.samplerate}Hz, {self.channels} channels, block size: {self.blocksize}", 'success')
            self.root.after(0, self.update_config_display)
            
            # Update UI
            self.root.after(0, self.on_connected)
            
            self.running = True
            
            # Start audio playback
            self.start_playback()
            
            # Start receiving audio
            self.receive_audio()
            
        except socket.timeout:
            self.log("Connection timeout! Check if server is running.", 'error')
            self.root.after(0, self.on_connection_failed)
        except ConnectionRefusedError:
            self.log("Connection refused! Make sure server is running.", 'error')
            self.root.after(0, self.on_connection_failed)
        except Exception as e:
            self.log(f"Connection error: {e}", 'error')
            self.root.after(0, self.on_connection_failed)
    
    def update_config_display(self):
        """Update audio config display"""
        self.config_label.config(
            text=f"Audio Config: {self.samplerate}Hz, {self.channels}ch, {self.blocksize} frames"
        )
    
    def on_connected(self):
        """UI updates when connected"""
        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: 🟢 Connected", fg='#27ae60')
        self.ip_entry.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.DISABLED)
    
    def on_connection_failed(self):
        """UI updates when connection fails"""
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def start_playback(self):
        """Start audio playback stream"""
        try:
            self.stream = sd.OutputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                blocksize=self.blocksize,
                callback=self.playback_callback
            )
            self.stream.start()
            self.log("Audio playback started", 'success')
        except Exception as e:
            self.log(f"Error starting playback: {e}", 'error')
    
    def playback_callback(self, outdata, frames, time_info, status):
        """Audio playback callback"""
        if not self.running:
            # Stop processing if disconnected
            raise sd.CallbackStop()
        
        if status:
            self.log(f"Playback status: {status}", 'warning')
        
        try:
            # Get audio from queue
            audio_data = self.audio_queue.get_nowait()
            
            # Calculate volume
            volume_norm = np.linalg.norm(audio_data) * 10
            volume_percent = min(int(volume_norm), 100)
            self.root.after(0, self.update_level, volume_percent)
            
            outdata[:] = audio_data
        except queue.Empty:
            # No audio data available, output silence
            outdata.fill(0)
    
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
    
    def receive_audio(self):
        """Receive audio data from server"""
        # Set socket timeout to allow checking running flag
        if self.socket:
            self.socket.settimeout(1.0)
        
        while self.running:
            try:
                # Receive size
                size_data = self.socket.recv(4)
                if not size_data:
                    self.log("Server disconnected", 'error')
                    self.running = False
                    break
                
                size = struct.unpack('I', size_data)[0]
                
                # Receive audio data
                audio_data = b''
                while len(audio_data) < size and self.running:
                    try:
                        chunk = self.socket.recv(min(4096, size - len(audio_data)))
                        if not chunk:
                            break
                        audio_data += chunk
                    except socket.timeout:
                        if not self.running:
                            break
                        continue
                
                if not self.running or len(audio_data) < size:
                    break
                
                # Convert to numpy array
                audio_array = np.frombuffer(audio_data, dtype='float32').reshape(-1, self.channels)
                
                # Add to queue
                try:
                    self.audio_queue.put_nowait(audio_array)
                except queue.Full:
                    # Drop oldest frame
                    try:
                        self.audio_queue.get_nowait()
                        self.audio_queue.put_nowait(audio_array)
                    except:
                        pass
                
                # Update statistics
                self.bytes_received += size
                self.frames_received += 1
                
            except socket.timeout:
                # Check if still running
                if not self.running:
                    break
                continue
            except OSError:
                # Socket closed
                break
            except Exception as e:
                if self.running:
                    self.log(f"Receive error: {e}", 'error')
                break
        
        # Connection ended
        self.root.after(0, self.on_disconnected)
    
    def disconnect_from_server(self):
        """Disconnect from server"""
        self.log("Disconnecting from server...", 'info')
        self.running = False
        
        # Stop playback first
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except:
                pass
            finally:
                self.stream = None
        
        # Close socket
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.socket.close()
            except:
                pass
            finally:
                self.socket = None
        
        # Clear queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                break
        
        # Give threads time to finish
        import time
        time.sleep(0.3)
        
        self.on_disconnected()
    
    def on_disconnected(self):
        """UI updates when disconnected"""
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: ⚫ Disconnected", fg='#e74c3c')
        self.ip_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        
        # Clear level display
        self.level_canvas.delete("all")
        self.level_text.config(text="Volume: 0%")
        self.queue_label.config(text="Buffer: 0 / 50 frames")
        
        self.log("Disconnected from server", 'warning')


def main():
    root = tk.Tk()
    app = AudioStreamClientGUI(root)
    
    # Handle window close
    def on_closing():
        if app.running:
            app.log("Closing application...", 'info')
            app.disconnect_from_server()
            # Give time for cleanup
            root.after(100, root.destroy)
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        if app.running:
            app.disconnect_from_server()


if __name__ == "__main__":
    main()
