#!/bin/bash

# Ubuntu Launch Script for Plotter AppImage
# This script helps launch the AppImage on Ubuntu systems with fallback options

echo "Starting Plotter AppImage..."

# Check if the AppImage exists
if [ ! -f "plotter-linux-*.AppImage" ]; then
    echo "Error: AppImage file not found!"
    echo "Please make sure you have downloaded the plotter-linux-*.AppImage file"
    exit 1
fi

# Find the AppImage file
APPIMAGE_FILE=$(ls plotter-linux-*.AppImage 2>/dev/null | head -n 1)

if [ -z "$APPIMAGE_FILE" ]; then
    echo "Error: No AppImage file found!"
    exit 1
fi

echo "Found AppImage: $APPIMAGE_FILE"

# Make it executable
chmod +x "$APPIMAGE_FILE"

# Try to launch the AppImage directly first
echo "Attempting to launch AppImage directly..."
if ./"$APPIMAGE_FILE" 2>/dev/null; then
    echo "AppImage launched successfully!"
    exit 0
fi

# If direct launch fails, try extraction method
echo "Direct launch failed. Trying extraction method..."
echo "Extracting AppImage contents..."

# Extract the AppImage
if ./"$APPIMAGE_FILE" --appimage-extract 2>/dev/null; then
    echo "Extraction successful. Launching extracted executable..."
    
    # Find the extracted executable
    if [ -f "squashfs-root/usr/bin/plotter" ]; then
        chmod +x squashfs-root/usr/bin/plotter
        ./squashfs-root/usr/bin/plotter
        echo "Plotter has closed."
    else
        echo "Error: Could not find extracted executable"
        exit 1
    fi
else
    echo "Error: Both direct launch and extraction failed"
    echo "Please check that you have FUSE installed: sudo apt install fuse libfuse2"
    exit 1
fi
