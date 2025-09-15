# Ubuntu Launch Guide for Plotter AppImage

## Quick Start

### Method 1: Direct Launch (Recommended)
```bash
# Download the AppImage file
wget https://github.com/Raghavendra-Pratap/Plotter/releases/latest/download/plotter-linux-*.AppImage

# Make it executable
chmod +x plotter-linux-*.AppImage

# Launch directly
./plotter-linux-*.AppImage
```

### Method 2: Using Launch Script
```bash
# Download the launch script
wget https://raw.githubusercontent.com/Raghavendra-Pratap/Plotter/develop/launch-ubuntu.sh

# Make it executable
chmod +x launch-ubuntu.sh

# Run the script
./launch-ubuntu.sh
```

## Troubleshooting

### Issue: "execv error: No such file or directory"

This error occurs when the AppImage's internal mounting mechanism fails. Here's how to fix it:

#### Solution 1: Manual Extraction (Always Works)
```bash
# Extract the AppImage contents
./plotter-linux-*.AppImage --appimage-extract

# Run the extracted executable
./squashfs-root/usr/bin/plotter
```

#### Solution 2: Install FUSE (For Direct Launch)
```bash
# Install FUSE libraries
sudo apt update
sudo apt install fuse libfuse2

# Try launching again
./plotter-linux-*.AppImage
```

#### Solution 3: Use Launch Script
The launch script automatically tries both methods:
```bash
./launch-ubuntu.sh
```

### Issue: "Permission denied"

```bash
# Make the AppImage executable
chmod +x plotter-linux-*.AppImage

# Or make the launch script executable
chmod +x launch-ubuntu.sh
```

### Issue: "AppImage not found"

Make sure you're in the correct directory and the file exists:
```bash
# List files to see the exact name
ls -la plotter-linux-*

# Download if missing
wget https://github.com/Raghavendra-Pratap/Plotter/releases/latest/download/plotter-linux-*.AppImage
```

## System Requirements

- **OS**: Ubuntu 18.04+ or compatible Linux distribution
- **Architecture**: x86_64 (64-bit)
- **Dependencies**: FUSE libraries (for direct launch)
- **Disk Space**: ~100MB for AppImage + extraction space

## Installation Dependencies

```bash
# Install FUSE (required for AppImage mounting)
sudo apt install fuse libfuse2

# Optional: Install additional GUI libraries
sudo apt install libgtk-3-0 libx11-6 libxext6 libxrender1 libxtst6
```

## File Structure

After extraction, the AppImage contains:
```
squashfs-root/
├── .DirIcon
├── plotter.desktop
├── plotter.png
└── usr/
    ├── bin/
    │   └── plotter          # Main executable
    └── share/
        ├── applications/
        │   └── plotter.desktop
        └── icons/
```

## Performance Tips

1. **First Launch**: May be slower due to extraction
2. **Subsequent Launches**: Faster with direct AppImage mounting
3. **Disk Space**: Keep ~200MB free for extraction
4. **Memory**: Requires ~500MB RAM for smooth operation

## Support

If you continue to have issues:

1. **Check System Logs**: `journalctl -f` while launching
2. **Verify Dependencies**: `ldd squashfs-root/usr/bin/plotter`
3. **Report Issues**: Create an issue on GitHub with system details

## Alternative Methods

If AppImage doesn't work, consider:

1. **Python Installation**: Install Python and run from source
2. **Docker**: Use containerized version
3. **Virtual Machine**: Run in VM with different OS

---

*This guide covers the most common AppImage issues and solutions.*
