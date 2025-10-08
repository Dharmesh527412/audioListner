#!/bin/bash
# Test script to verify shutdown handling

echo "======================================"
echo "Audio Streaming Shutdown Test"
echo "======================================"
echo ""

# Function to check for orphaned processes
check_orphaned() {
    echo "Checking for orphaned audio processes..."
    ORPHANED=$(ps aux | grep -E "audio_server.py|audio_client.py" | grep -v grep | grep -v test_shutdown)
    if [ -z "$ORPHANED" ]; then
        echo "✅ No orphaned processes found"
        return 0
    else
        echo "❌ Found orphaned processes:"
        echo "$ORPHANED"
        return 1
    fi
}

# Function to check if port is free
check_port() {
    echo "Checking if port 9999 is free..."
    PORT_IN_USE=$(netstat -tulpn 2>/dev/null | grep :9999 | grep -v grep)
    if [ -z "$PORT_IN_USE" ]; then
        echo "✅ Port 9999 is free"
        return 0
    else
        echo "❌ Port 9999 is still in use:"
        echo "$PORT_IN_USE"
        return 1
    fi
}

echo "Test 1: Quick server start and stop (Ctrl+C)"
echo "--------------------------------------"
echo "Starting server for 3 seconds..."

# Get the Python interpreter path
PYTHON_PATH="/home/dharmesh.p/Trial/audioListner/.venv/bin/python"
if [ ! -f "$PYTHON_PATH" ]; then
    PYTHON_PATH="python3"
fi

# Start server in background
timeout 3s $PYTHON_PATH audio_server.py 2>&1 | head -20 &
SERVER_PID=$!

sleep 3
echo "Stopping server..."
kill -INT $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

sleep 1
check_orphaned
check_port
echo ""

echo "Test 2: Server termination with SIGTERM"
echo "--------------------------------------"
echo "Starting server..."

$PYTHON_PATH audio_server.py > /dev/null 2>&1 &
SERVER_PID=$!

sleep 2
echo "Sending SIGTERM signal..."
kill -TERM $SERVER_PID
wait $SERVER_PID 2>/dev/null

sleep 1
check_orphaned
check_port
echo ""

echo "======================================"
echo "Shutdown Test Complete"
echo "======================================"
echo ""
echo "Manual Tests Recommended:"
echo "1. Start server, press Ctrl+C - should see clean shutdown"
echo "2. Start server, close terminal - check no orphaned processes"
echo "3. Start GUI, click X button - should stop streaming first"
echo "4. Run: ps aux | grep audio - should show no processes"
echo "5. Run: netstat -tulpn | grep 9999 - should show port is free"
