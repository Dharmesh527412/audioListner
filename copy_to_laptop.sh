#!/bin/bash
# Copy necessary files to another laptop for audio streaming client

echo "═══════════════════════════════════════════════════════════════"
echo "  Transfer Audio Client to Another Laptop"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if IP is provided
if [ -z "$1" ]; then
    echo "📋 This script will help you copy the audio client to another laptop"
    echo ""
    echo "Method 1 - SCP (Secure Copy over network):"
    echo "  ./copy_to_laptop.sh <username>@<laptop-ip>"
    echo "  Example: ./copy_to_laptop.sh john@192.168.1.105"
    echo ""
    echo "Method 2 - Create a portable folder:"
    echo "  ./copy_to_laptop.sh portable"
    echo "  (This creates a folder you can copy via USB/network share)"
    echo ""
    exit 1
fi

if [ "$1" == "portable" ]; then
    # Create portable folder
    echo "📦 Creating portable client folder..."
    mkdir -p audio_streaming_client
    cp audio_client.py audio_streaming_client/
    cp start_client.sh audio_streaming_client/
    cp QUICK_START.txt audio_streaming_client/
    
    # Create a simple README
    cat > audio_streaming_client/HOW_TO_USE.txt << 'EOF'
AUDIO STREAMING CLIENT SETUP
=============================

1. Make the script executable:
   chmod +x start_client.sh

2. Install dependencies (first time only):
   pip3 install sounddevice numpy

3. Run the client with your server's IP:
   ./start_client.sh <SERVER_IP>
   
   Example:
   ./start_client.sh 192.168.1.100

4. Play music on the server laptop and enjoy!

Press Ctrl+C to stop.
EOF
    
    echo "✅ Done! Portable folder created: audio_streaming_client/"
    echo ""
    echo "📁 Contents:"
    ls -lh audio_streaming_client/
    echo ""
    echo "💡 Next steps:"
    echo "   1. Copy the 'audio_streaming_client' folder to the other laptop"
    echo "   2. Use USB drive, network share, or any transfer method"
    echo "   3. Follow instructions in HOW_TO_USE.txt"
    echo ""
else
    # SCP to remote laptop
    REMOTE=$1
    echo "📡 Copying files to $REMOTE..."
    echo ""
    
    # Create remote directory
    ssh $REMOTE "mkdir -p ~/audio_streaming_client" || {
        echo "❌ Could not connect to remote laptop"
        echo "   Make sure SSH is enabled and you have access"
        exit 1
    }
    
    # Copy files
    scp audio_client.py start_client.sh QUICK_START.txt $REMOTE:~/audio_streaming_client/ || {
        echo "❌ File transfer failed"
        exit 1
    }
    
    # Make script executable
    ssh $REMOTE "chmod +x ~/audio_streaming_client/start_client.sh"
    
    echo ""
    echo "✅ Files copied successfully to $REMOTE:~/audio_streaming_client/"
    echo ""
    echo "📋 Next steps on the remote laptop:"
    echo "   cd ~/audio_streaming_client"
    echo "   ./start_client.sh $(hostname -I | awk '{print $1}')"
    echo ""
    echo "Or connect via SSH and run:"
    echo "   ssh $REMOTE"
    echo "   cd ~/audio_streaming_client"
    echo "   ./start_client.sh $(hostname -I | awk '{print $1}')"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════════"
