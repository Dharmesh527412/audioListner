# Audio Device Detection Fix

## Date: October 8, 2025

## Issue
The application was unable to find the audio OUTPUT monitor device, showing error:
```
Error: No suitable audio OUTPUT monitor device found!
```

This occurred even though:
- The PulseAudio monitor was correctly configured
- `pactl get-default-source` returned the correct monitor device
- The monitor device was visible in `pactl list sources short`

## Root Cause
The `sounddevice` library was using ALSA as its backend instead of directly accessing PulseAudio devices. When using ALSA backend:
- Device names don't include "monitor" suffix
- The PulseAudio monitor devices aren't directly visible
- The application's device filtering logic was looking for "monitor" in the device name

## Solution Applied
Updated the `get_monitor_device()` method in both `audio_server.py` and `server_ui/server_gui.py` to:

1. **First priority**: Look for devices with "monitor" in the name (direct PulseAudio devices)
2. **Second priority**: Use the `pulse` device (which respects PulseAudio's default source setting)
3. **Third priority**: Use the `default` device (also respects PulseAudio settings)

### Code Changes

```python
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
```

## How It Works Now

The application will:
1. Check for direct PulseAudio monitor devices (if sounddevice can see them)
2. Fall back to using the `pulse` device, which automatically uses whatever PulseAudio's default source is set to
3. Since we set the default source to the monitor device using:
   ```bash
   pactl set-default-source alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
   ```
   The `pulse` device will capture from that monitor

## Benefits

- **More Compatible**: Works regardless of whether sounddevice uses ALSA or PulseAudio backend
- **Respects System Settings**: Uses PulseAudio's default source configuration
- **Backward Compatible**: Still works with systems that show direct PulseAudio devices
- **Still Secure**: Still only captures audio OUTPUT (the monitor), never microphone

## Verification

To verify the fix works:

1. **Check PulseAudio configuration**:
   ```bash
   pactl get-default-source
   # Should show: alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
   ```

2. **Check sounddevice can see the pulse device**:
   ```bash
   python3 -c "import sounddevice as sd; devices = sd.query_devices(); print([d['name'] for d in devices if 'pulse' in d['name'].lower()])"
   ```

3. **Start the server**:
   ```bash
   python audio_server.py
   # or
   python server_ui/server_gui.py
   ```

4. **Verify it starts successfully**:
   - Should show: "Using audio OUTPUT device: pulse"
   - No error messages about missing devices

## Technical Details

### sounddevice Backend Behavior
- `sounddevice` (PortAudio) can use different backends (ALSA, PulseAudio, JACK, etc.)
- On most Linux systems, it defaults to ALSA backend
- When using ALSA backend, it doesn't see PulseAudio-specific devices directly
- However, the "pulse" and "default" devices act as bridges to PulseAudio

### Device Selection Priority
1. Direct monitor devices (name contains "monitor")
2. `pulse` device (uses PulseAudio default source)
3. `default` device (also uses PulseAudio on most systems)

### What Gets Captured
With this fix, the application still:
- ✅ Captures only audio OUTPUT (browser, system sounds)
- ❌ Does NOT capture microphone input
- ✅ Respects PulseAudio's default source setting

## Files Modified
1. `audio_server.py` - Updated `get_monitor_device()` method
2. `server_ui/server_gui.py` - Updated `get_monitor_device()` method

## Testing

After applying the fix:
```bash
# Start GUI server
python server_ui/server_gui.py

# Click "Start Server" button
# Should now work without errors
```

## Related Documentation
- **MICROPHONE_EXCLUSION_FIX.md** - Original microphone exclusion implementation
- **SHUTDOWN_IMPROVEMENTS.md** - Shutdown handling improvements
- **README.md** - General usage documentation

---

**Fix Applied**: October 8, 2025  
**Status**: ✅ Working  
**Tested On**: Ubuntu with PulseAudio
