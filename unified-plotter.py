import importlib
import os
import subprocess
import sys
from typing import Any, Dict, List

# Set matplotlib backend before importing matplotlib to prevent segmentation faults
os.environ["MPLBACKEND"] = "TkAgg"
# Performance optimizations
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"
os.environ["PYTHONUNBUFFERED"] = "1"

# Global variables (will be initialized when needed)
root = None
settings = None
annotations = []
confidences = []
file_path_holder = []


def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False
    return True


def check_and_install_dependencies(progress_callback=None):
    """Check and install required dependencies with progress updates"""
    required_packages = {
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "numpy": "numpy",
        "PIL": "Pillow",
        "requests": "requests",
        "psutil": "psutil",
    }

    total_packages = len(required_packages)
    checked_packages = 0
    missing_packages = []

    # Check which packages are missing
    for module_name, package_name in required_packages.items():
        try:
            importlib.import_module(module_name)
            print(f"✓ {module_name} is already installed")
            checked_packages += 1
            if progress_callback:
                progress_callback(
                    f"Checking dependencies... ({checked_packages}/{total_packages})",
                    int((checked_packages / total_packages) * 100),
                )
        except ImportError:
            print(f"✗ {module_name} is not installed")
            missing_packages.append((module_name, package_name))
            checked_packages += 1
            if progress_callback:
                progress_callback(
                    f"Checking dependencies... ({checked_packages}/{total_packages})",
                    int((checked_packages / total_packages) * 100),
                )

    # If no packages are missing, we're done
    if not missing_packages:
        if progress_callback:
            progress_callback("All dependencies are ready!", 100)
        return True

    # Install missing packages with progress updates
    if progress_callback:
        progress_callback("Installing missing packages...", 50)

    for i, (module_name, package_name) in enumerate(missing_packages):
        if progress_callback:
            progress_callback(
                f"Installing {package_name}... ({i+1}/{len(missing_packages)})",
                50 + int((i / len(missing_packages)) * 40),
            )

        print(f"Installing {package_name}...")
        if install_package(package_name):
            print(f"✓ {package_name} installed successfully")
        else:
            print(f"✗ Failed to install {package_name}")
            if progress_callback:
                progress_callback(
                    f"Failed to install {package_name}. Please install manually.", 0
                )
            return False

    # Final verification
    if progress_callback:
        progress_callback("Verifying installations...", 95)

    # Re-import matplotlib if it was installed
    if "matplotlib" in [pkg[1] for pkg in missing_packages if pkg[1] == "matplotlib"]:
        try:
            import matplotlib

            matplotlib.use("TkAgg")
            import matplotlib.patches as patches
            import matplotlib.pyplot as plt
            from matplotlib import gridspec
            from matplotlib import image as mpimg
            from matplotlib.transforms import Bbox
            from matplotlib.widgets import Button, RadioButtons, Slider

            print("✓ matplotlib re-imported successfully after installation")
        except Exception as e:
            print(f"✗ Failed to re-import matplotlib after installation: {e}")
            if progress_callback:
                progress_callback(
                    "Failed to re-import matplotlib after installation", 0
                )
            return False

    # Check tkinter (built-in on most systems)
    try:
        import tkinter

        print("✓ tkinter is available")
    except ImportError:
        print("✗ tkinter is not available. This may cause issues with file dialogs.")
        print("On some systems, you may need to install python3-tk package.")

    if progress_callback:
        progress_callback("All dependencies ready!", 100)

    return True


# Dependencies will be checked after loading screen is shown
# All imports will be done after dependency checking


def import_dependencies():
    """Import all required dependencies after they are installed"""
    global plt, patches, Button, RadioButtons, Slider, gridspec, Bbox, mpimg, np, pd, webbrowser, requests, Image, io

    try:
        # Import matplotlib with error handling
        import matplotlib

        matplotlib.use("TkAgg")  # Force TkAgg backend
        import matplotlib.patches as patches
        import matplotlib.pyplot as plt
        from matplotlib import gridspec
        from matplotlib import image as mpimg
        from matplotlib.transforms import Bbox
        from matplotlib.widgets import Button, RadioButtons, Slider

        print("✓ matplotlib imported successfully with TkAgg backend")
    except Exception as e:
        print(f"✗ Error importing matplotlib with TkAgg: {e}")
        print("Trying Qt5Agg backend...")
        try:
            import matplotlib

            matplotlib.use("Qt5Agg")  # Try Qt5Agg backend
            import matplotlib.patches as patches
            import matplotlib.pyplot as plt
            from matplotlib import gridspec
            from matplotlib import image as mpimg
            from matplotlib.transforms import Bbox
            from matplotlib.widgets import Button, RadioButtons, Slider

            print("✓ matplotlib imported with Qt5Agg backend")
        except Exception as e2:
            print(f"✗ Error importing matplotlib with Qt5Agg: {e2}")
            print("Trying Qt4Agg backend...")
            try:
                import matplotlib

                matplotlib.use("Qt4Agg")  # Try Qt4Agg backend
                import matplotlib.patches as patches
                import matplotlib.pyplot as plt
                from matplotlib import gridspec
                from matplotlib import image as mpimg
                from matplotlib.transforms import Bbox
                from matplotlib.widgets import Button, RadioButtons, Slider

                print("✓ matplotlib imported with Qt4Agg backend")
            except Exception as e3:
                print(f"✗ Error importing matplotlib with Qt4Agg: {e3}")
                print("Falling back to non-interactive Agg backend")
                import matplotlib

                matplotlib.use("Agg")  # Fallback to non-interactive backend
                import matplotlib.patches as patches
                import matplotlib.pyplot as plt
                from matplotlib import gridspec
                from matplotlib import image as mpimg
                from matplotlib.transforms import Bbox
                from matplotlib.widgets import Button, RadioButtons, Slider

                print("✓ matplotlib imported with Agg backend (non-interactive)")
                print("⚠ WARNING: Interactive plotting will not work with Agg backend")

    # Import other dependencies
    import io
    import webbrowser

    import numpy as np
    import pandas as pd
    import requests
    from PIL import Image

    print("✓ All dependencies imported successfully")
    return True


import io
import json
import logging
import shutil
import tempfile
import threading
import time
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox, ttk

# Import other dependencies at module level
import numpy as np
import pandas as pd
import requests
from PIL import Image


# --- NEW: Unified Screen Manager ---
class UnifiedScreenManager:
    """Manages all screen components (loading, welcome, progress, error) in one unified window"""

    def __init__(self):
        # Standard window dimensions for all components
        self.window_width = 800
        self.window_height = 600
        self.root = None
        self.main_container = None
        self.current_mode = None

        # Component references
        self.logo_frame = None
        self.content_frame = None
        self.button_frame = None
        self.progress_bar = None
        self.status_text = None
        self.progress_text = None
        self.spinner_canvas = None

        # Animation variables
        self.spinner_angle = 0
        self.progress_value = 0
        self.current_step = 0
        self.loading_steps = []

    def create_unified_window(self, title="Unified Plotter", show_title_bar=True):
        """Create the unified window with standard dimensions"""
        # Destroy existing window if it exists
        if self.root:
            try:
                self.root.destroy()
            except:
                pass  # Window already destroyed

        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(bg="#1a1a1a")

        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        # Ensure positive coordinates
        center_x = max(0, center_x)
        center_y = max(0, center_y)

        self.root.geometry(
            f"{self.window_width}x{self.window_height}+{center_x}+{center_y}"
        )

        # Configure window properties
        self.root.resizable(False, False)

        # Create main container
        self.main_container = tk.Frame(self.root, bg="#1a1a1a", padx=40, pady=40)
        self.main_container.pack(expand=True, fill="both")

        # Create logo section (always visible)
        self.create_logo_section()

        # Create content frame (dynamic content area)
        self.content_frame = tk.Frame(self.main_container, bg="#1a1a1a")
        self.content_frame.pack(expand=True, fill="both", pady=(20, 0))

        # Create button frame (for welcome screen)
        self.button_frame = tk.Frame(self.main_container, bg="#1a1a1a")
        self.button_frame.pack(side="bottom", fill="x", pady=(20, 0))

        # Force window to appear immediately
        self.root.update_idletasks()
        self.root.deiconify()

        # Apply overrideredirect after window is positioned (fixes macOS positioning issue)
        if not show_title_bar:
            self.root.overrideredirect(1)
            # Re-center after removing title bar
            self.root.geometry(
                f"{self.window_width}x{self.window_height}+{center_x}+{center_y}"
            )

    def create_logo_section(self):
        """Create the logo section that appears on all screens"""
        self.logo_frame = tk.Frame(self.main_container, bg="#1a1a1a")
        self.logo_frame.pack(pady=(0, 20))

        # Logo text
        logo_text = tk.Label(
            self.logo_frame,
            text="Unified Plotter",
            font=tkFont.Font(family="Helvetica", size=28, weight="bold"),
            bg="#1a1a1a",
            fg="#ffffff",
        )
        logo_text.pack()

        # Subtitle
        subtitle_text = tk.Label(
            self.logo_frame,
            text="Professional Bounding Box Visualization Tool",
            font=tkFont.Font(family="Helvetica", size=12),
            bg="#1a1a1a",
            fg="#888888",
        )
        subtitle_text.pack(pady=(5, 0))

    def clear_content(self):
        """Clear the content frame for new content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def restore_welcome_screen(self, select_callback, settings_callback):
        """Restore the welcome screen without destroying and recreating everything"""
        # Use the same approach as show_welcome_screen
        self.clear_content()
        self.current_mode = "welcome"

        # Restore logo section for welcome screen
        if self.logo_frame:
            self.logo_frame.pack(pady=(0, 20))

        # Description text
        description_text = (
            "Welcome to the professional bounding box visualization tool!\n\n"
            "This advanced tool helps you visualize and annotate bounding box data\n"
            "directly from your CSV files with enterprise-grade features.\n\n"
            "📋 Requirements:\n"
            "• CSV must include: image_id, x_min, x_max, y_min, y_max\n"
            "• Optional: label_* columns or image URL columns\n\n"
            "🚀 Click below to begin your professional workflow.\n"
            "⬇"
        )
        description_label = tk.Label(
            self.content_frame,
            text=description_text,
            font=tkFont.Font(family="Helvetica", size=11),
            justify=tk.CENTER,
            bg="#1a1a1a",
            fg="#cccccc",
            pady=15,
            wraplength=600,
        )
        description_label.pack()

        # Main action button
        select_button = tk.Button(
            self.content_frame,
            text="📁 Select CSV File",
            command=select_callback,
            font=tkFont.Font(family="Helvetica", size=13, weight="bold"),
            bg="#00ff88",
            fg="#1a1a1a",
            activebackground="#00cc6a",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            borderwidth=0,
            padx=40,
            pady=18,
            cursor="hand2",
        )
        select_button.pack(pady=(30, 0))

        # Bottom buttons
        settings_button = tk.Button(
            self.button_frame,
            text="⚙️ Settings",
            command=settings_callback,
            font=tkFont.Font(family="Helvetica", size=13, weight="bold"),
            bg="#333333",
            fg="#ffffff",
            activebackground="#555555",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        settings_button.pack(side="left", padx=(0, 10))

        exit_button = tk.Button(
            self.button_frame,
            text="❌ Exit",
            command=self.root.destroy,
            font=tkFont.Font(family="Helvetica", size=13, weight="bold"),
            bg="#666666",
            fg="#ffffff",
            activebackground="#888888",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        exit_button.pack(side="right", padx=(10, 0))

    def show_loading_screen(self):
        """Display loading screen with spinner and progress"""
        self.clear_content()
        self.current_mode = "loading"

        # Loading animation section
        animation_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        animation_frame.pack(pady=(20, 30))

        # Create loading spinner
        self.spinner_canvas = tk.Canvas(
            animation_frame, width=60, height=60, bg="#1a1a1a", highlightthickness=0
        )
        self.spinner_canvas.pack()

        # Progress bar
        progress_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        progress_frame.pack(fill="x", pady=(0, 20))

        self.progress_bar = tk.Canvas(
            progress_frame, height=8, bg="#333333", highlightthickness=0
        )
        self.progress_bar.pack(fill="x")

        # Progress text
        self.progress_text = tk.Label(
            self.content_frame,
            text="Initializing...",
            font=tkFont.Font(family="Helvetica", size=12),
            bg="#1a1a1a",
            fg="#ffffff",
        )
        self.progress_text.pack()

        # Status text
        self.status_text = tk.Label(
            self.content_frame,
            text="Loading dependencies and preparing interface...",
            font=tkFont.Font(family="Helvetica", size=10),
            bg="#1a1a1a",
            fg="#888888",
        )
        self.status_text.pack(pady=(10, 0))

        # Tips and features section
        tips_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        tips_frame.pack(fill="x", pady=(20, 0))

        # Tips title
        tips_title = tk.Label(
            tips_frame,
            text="💡 Quick Tips",
            font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
            bg="#1a1a1a",
            fg="#00ff88",
        )
        tips_title.pack(anchor="w", pady=(0, 10))

        # Tips content
        tips_content = [
            "• Ensure your CSV has columns: image_id, x_min, x_max, y_min, y_max",
            "• Use keyboard shortcuts for faster navigation (H for help)",
            "• Click and drag to create bounding boxes quickly",
            "• Save your work regularly with Ctrl+S",
            "• Use the thumbnail gallery to navigate between images",
        ]

        for tip in tips_content:
            tip_label = tk.Label(
                tips_frame,
                text=tip,
                font=tkFont.Font(family="Helvetica", size=10),
                bg="#1a1a1a",
                fg="#cccccc",
                anchor="w",
            )
            tip_label.pack(anchor="w", pady=(2, 0))

        # Features section
        features_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        features_frame.pack(fill="x", pady=(15, 0))

        # Features title
        features_title = tk.Label(
            features_frame,
            text="🚀 Professional Features",
            font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
            bg="#1a1a1a",
            fg="#00ff88",
        )
        features_title.pack(anchor="w", pady=(0, 10))

        # Features content
        features_content = [
            "• Real-time bounding box visualization and editing",
            "• Batch processing with progress tracking",
            "• Export annotations in multiple formats",
            "• Keyboard shortcuts for power users",
            "• Professional-grade performance optimization",
        ]

        for feature in features_content:
            feature_label = tk.Label(
                features_frame,
                text=feature,
                font=tkFont.Font(family="Helvetica", size=10),
                bg="#1a1a1a",
                fg="#cccccc",
                anchor="w",
            )
            feature_label.pack(anchor="w", pady=(2, 0))

        # Version info
        try:
            from .version import get_version_string

            version_text = tk.Label(
                self.content_frame,
                text=get_version_string(),
                font=tkFont.Font(family="Helvetica", size=9),
                bg="#1a1a1a",
                fg="#555555",
            )
        except ImportError:
            # Fallback if version module is not available
            version_text = tk.Label(
                self.content_frame,
                text="Version 2.1.0 | Professional Edition",
                font=tkFont.Font(family="Helvetica", size=9),
                bg="#1a1a1a",
                fg="#555555",
            )
        version_text.pack(side="bottom", pady=(20, 0))

        # Start loading animation
        self.start_loading_animation()

    def show_welcome_screen(self, select_callback, settings_callback):
        """Display welcome screen with file selection"""
        self.clear_content()
        self.current_mode = "welcome"

        # Ensure logo section is properly positioned at the top
        if self.logo_frame:
            # Force the logo frame to be at the very top
            self.logo_frame.pack_forget()
            # Pack the logo frame first, before any content
            self.logo_frame.pack(pady=(0, 20), before=self.content_frame)
        else:
            # If logo frame doesn't exist, create it
            self.create_logo_section()

        # Description text
        description_text = (
            "Welcome to the professional bounding box visualization tool!\n\n"
            "This advanced tool helps you visualize and annotate bounding box data\n"
            "directly from your CSV files with enterprise-grade features.\n\n"
            "📋 Requirements:\n"
            "• CSV must include: image_id, x_min, x_max, y_min, y_max\n"
            "• Optional: label_* columns or image URL columns\n\n"
            "🚀 Click below to begin your professional workflow.\n"
            "⬇"
        )
        description_label = tk.Label(
            self.content_frame,
            text=description_text,
            font=tkFont.Font(family="Helvetica", size=11),
            justify=tk.CENTER,
            bg="#1a1a1a",
            fg="#cccccc",
            pady=15,
            wraplength=600,
        )
        description_label.pack()

        # Main action button
        select_button = tk.Button(
            self.content_frame,
            text="📁 Select CSV File",
            command=select_callback,
            font=tkFont.Font(family="Helvetica", size=13, weight="bold"),
            bg="#00ff88",
            fg="#1a1a1a",
            activebackground="#00cc6a",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            borderwidth=0,
            padx=40,
            pady=18,
            cursor="hand2",
        )
        select_button.pack(pady=(30, 0))

        # Bottom buttons
        settings_button = tk.Button(
            self.button_frame,
            text="⚙️ Settings",
            command=settings_callback,
            font=tkFont.Font(family="Helvetica", size=13, weight="bold"),
            bg="#333333",
            fg="#ffffff",
            activebackground="#555555",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        settings_button.pack(side="left", padx=(0, 10))

        exit_button = tk.Button(
            self.button_frame,
            text="❌ Exit",
            command=self.root.destroy,
            font=tkFont.Font(family="Helvetica", size=13, weight="bold"),
            bg="#666666",
            fg="#ffffff",
            activebackground="#888888",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        exit_button.pack(side="right", padx=(10, 0))

    def show_progress_screen(self, message, progress=0, total=100):
        """Display progress screen for data processing"""
        self.clear_content()
        self.current_mode = "progress"

        # Title
        title_label = tk.Label(
            self.content_frame,
            text="Processing Your Data",
            font=tkFont.Font(family="Helvetica", size=16, weight="bold"),
            bg="#1a1a1a",
            fg="#ffffff",
        )
        title_label.pack(pady=(0, 20))

        # Status message
        self.status_text = tk.Label(
            self.content_frame,
            text=message,
            font=tkFont.Font(family="Helvetica", size=12),
            bg="#1a1a1a",
            fg="#cccccc",
            wraplength=600,
        )
        self.status_text.pack(pady=(0, 20))

        # Progress bar
        progress_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        progress_frame.pack(fill="x", pady=(0, 10))

        self.progress_bar = tk.Canvas(
            progress_frame, height=12, bg="#333333", highlightthickness=0
        )
        self.progress_bar.pack(fill="x")

        # Progress text
        self.progress_text = tk.Label(
            self.content_frame,
            text=f"Progress: {progress}/{total} ({int(progress/total*100)}%)",
            font=tkFont.Font(family="Helvetica", size=10),
            bg="#1a1a1a",
            fg="#888888",
        )
        self.progress_text.pack()

        # Update progress bar
        bar_width = int((progress / total) * 720) if total > 0 else 0
        self.progress_bar.create_rectangle(
            0, 0, bar_width, 12, fill="#00ff88", outline=""
        )

        self.root.update()

    def show_error_screen(
        self, title, message, button_text="Home", button_callback=None
    ):
        """Display error screen with custom message"""
        self.clear_content()
        self.current_mode = "error"

        # Error icon and title
        title_label = tk.Label(
            self.content_frame,
            text=f"❌ {title}",
            font=tkFont.Font(family="Helvetica", size=18, weight="bold"),
            bg="#1a1a1a",
            fg="#ff4444",
        )
        title_label.pack(pady=(0, 20))

        # Error message
        error_text = tk.Label(
            self.content_frame,
            text=message,
            font=tkFont.Font(family="Helvetica", size=11),
            bg="#1a1a1a",
            fg="#cccccc",
            justify=tk.LEFT,
            wraplength=600,
        )
        error_text.pack(pady=(0, 20))

        # Helpful suggestions section
        suggestions_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        suggestions_frame.pack(fill="x", pady=(10, 0))

        # Suggestions title
        suggestions_title = tk.Label(
            suggestions_frame,
            text="💡 What you can do:",
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#1a1a1a",
            fg="#00ff88",
        )
        suggestions_title.pack(anchor="w", pady=(0, 8))

        # Suggestions content
        suggestions_content = [
            "• Check that your CSV file has the required columns",
            "• Verify the file format and encoding",
            "• Try selecting a different CSV file",
            "• Contact support if the issue persists",
        ]

        for suggestion in suggestions_content:
            suggestion_label = tk.Label(
                suggestions_frame,
                text=suggestion,
                font=tkFont.Font(family="Helvetica", size=10),
                bg="#1a1a1a",
                fg="#cccccc",
                anchor="w",
            )
            suggestion_label.pack(anchor="w", pady=(2, 0))

        # Action button
        action_button = tk.Button(
            self.content_frame,
            text=button_text,
            command=button_callback or self.root.destroy,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#00ff88",
            fg="#1a1a1a",
            activebackground="#00cc6a",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
        )
        action_button.pack(pady=(20, 0))

    def start_loading_animation(self):
        """Start the loading animation"""
        self.spinner_angle = 0
        self.progress_value = 0
        self.current_step = 0
        self.loading_steps = [
            "Checking dependencies...",
            "Loading matplotlib...",
            "Initializing interface...",
            "Preparing welcome screen...",
            "Ready to launch!",
        ]

        self.animate_spinner()
        self.update_loading_progress()

    def animate_spinner(self):
        """Animate the loading spinner"""
        if self.current_mode != "loading" or not self.spinner_canvas:
            return

        self.spinner_canvas.delete("all")

        # Draw spinner
        center_x, center_y = 30, 30
        radius = 25

        # Draw spinner arc
        self.spinner_canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=self.spinner_angle,
            extent=270,
            outline="#00ff88",
            width=3,
            style="arc",
        )

        # Draw center dot
        self.spinner_canvas.create_oval(
            center_x - 3,
            center_y - 3,
            center_x + 3,
            center_y + 3,
            fill="#00ff88",
            outline="",
        )

        self.spinner_angle = (self.spinner_angle + 10) % 360
        self.root.after(50, self.animate_spinner)

    def update_loading_progress(self):
        """Update loading progress"""
        if self.current_mode != "loading" or not self.progress_bar:
            return

        if self.current_step < len(self.loading_steps):
            # Update progress bar
            self.progress_bar.delete("all")
            bar_width = int((self.progress_value / 100) * 720)
            self.progress_bar.create_rectangle(
                0, 0, bar_width, 8, fill="#00ff88", outline=""
            )

            # Update status text
            if self.status_text:
                self.status_text.config(text=self.loading_steps[self.current_step])

            # Update progress text
            if self.progress_text:
                self.progress_text.config(text=f"Progress: {self.progress_value}%")

            # Increment progress
            self.progress_value += 20
            self.current_step += 1

            # Schedule next update
            self.root.after(800, self.update_loading_progress)
        else:
            # Loading complete
            if self.progress_text:
                self.progress_text.config(text="Ready!")
            if self.status_text:
                self.status_text.config(text="Launching application...")

            # Close after delay
            self.root.after(1000, self.root.destroy)

    def update_progress(self, message, progress, total=100):
        """Update progress screen"""
        if (
            self.current_mode == "progress"
            and self.status_text
            and self.progress_text
            and self.progress_bar
        ):
            try:
                # Check if widgets still exist before accessing them
                if (
                    hasattr(self.status_text, "winfo_exists")
                    and self.status_text.winfo_exists()
                ):
                    self.status_text.config(text=message)
                if (
                    hasattr(self.progress_text, "winfo_exists")
                    and self.progress_text.winfo_exists()
                ):
                    self.progress_text.config(
                        text=f"Progress: {progress}/{total} ({int(progress/total*100)}%)"
                    )
                if (
                    hasattr(self.progress_bar, "winfo_exists")
                    and self.progress_bar.winfo_exists()
                ):
                    self.progress_bar.delete("all")
                    bar_width = int((progress / total) * 720)
                    self.progress_bar.create_rectangle(
                        0, 0, bar_width, 12, fill="#00ff88", outline=""
                    )
                if (
                    self.root
                    and hasattr(self.root, "winfo_exists")
                    and self.root.winfo_exists()
                ):
                    self.root.update()
            except Exception as e:
                # Widgets have been destroyed, ignore the error
                print(f"⚠ Progress update skipped - widgets destroyed: {e}")
                pass

    def run(self):
        """Start the main loop"""
        if self.root:
            self.root.mainloop()

    def destroy(self):
        """Destroy the window"""
        if self.root:
            self.root.destroy()


# Global screen manager instance
screen_manager = UnifiedScreenManager()


# --- NEW: Professional Loading Screen ---
def show_loading_screen():
    """Display a professional loading screen with logo and progress feedback"""
    # Ensure clean state
    if screen_manager.root:
        screen_manager.destroy()

    # Create window immediately and center it
    screen_manager.create_unified_window(
        "Unified Plotter | Professional Bounding Box Visualization",
        show_title_bar=False,
    )

    # Force window to appear and center
    screen_manager.root.update()
    screen_manager.root.lift()
    screen_manager.root.focus_force()

    # Show loading content
    screen_manager.show_loading_screen()
    screen_manager.run()


# --- Annotation state for undo/redo/clear, per image_id ---
class AnnotationState:
    def __init__(self):
        self.annotations = []  # List of annotation_entry dicts
        self.markers = []  # List of (marker, label_text, x, y, mark_value)
        self.undone = []  # Stack for redo
        self.counter = 1
        self.mode = "x"
        self.hover_text = None  # Store hover text per image
        self.image_url = None  # Store image URL for this image_id

    def reset(self):
        self.annotations.clear()
        self.markers.clear()
        self.undone.clear()
        if self.hover_text:
            try:
                self.hover_text.remove()
            except (NotImplementedError, ValueError):
                pass
            self.hover_text = None


# --- Generate thumbnails for each image ---
def generate_thumbnail(df_selected):
    """Generate a thumbnail image for the given DataFrame selection"""
    # Skip if df_selected is empty or all bounding box columns are NaN
    if (
        df_selected.empty
        or df_selected["x_min"].isna().all()
        or df_selected["x_max"].isna().all()
        or df_selected["y_min"].isna().all()
        or df_selected["y_max"].isna().all()
    ):
        print(
            f"[Warning] Skipping thumbnail: No valid bounding box data for image_id: {df_selected['image_id'].iloc[0] if not df_selected.empty else 'N/A'}"
        )
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        ax.axis("off")
        fig.canvas.draw()
        img = np.array(fig.canvas.renderer.buffer_rgba())
        plt.close(fig)
        return img

    # Apply quality settings - but maintain consistent thumbnail size
    if global_settings.get("high_quality_thumbnails", True):
        figsize = (2.5, 2.5)  # Keep consistent size regardless of quality
        linewidth = 1.2
        fontsize = 9
        marker_size = 10
    else:
        figsize = (2.5, 2.5)  # Keep consistent size regardless of quality
        linewidth = 0.8
        fontsize = 7
        marker_size = 8

    fig, ax = plt.subplots(figsize=figsize)

    for _, row in df_selected.dropna(
        subset=["x_min", "x_max", "y_min", "y_max"]
    ).iterrows():
        rect = patches.Rectangle(
            (row["x_min"], row["y_min"]),
            row["x_max"] - row["x_min"],
            row["y_max"] - row["y_min"],
            linewidth=linewidth,
            edgecolor="r",
            facecolor="none",
            zorder=1,  # Low z-order so markers appear on top
        )
        ax.add_patch(rect)

        # Add existing marks from CSV 'marked' column to thumbnails
        if "marked" in df.columns:
            marked_value = str(row.get("marked", "")).strip()
            if (
                marked_value
                and marked_value.lower() != "nan"
                and marked_value.lower() != ""
            ):
                x, y = (row["x_min"] + row["x_max"]) / 2, (
                    row["y_min"] + row["y_max"]
                ) / 2

                # Convert "yes" to "x" for display
                if marked_value.lower() == "yes":
                    display_value = "x"
                    marker_color = "green"
                    # Display as X marker with high z-order
                    ax.plot(
                        x,
                        y,
                        marker="x",
                        color=marker_color,
                        markersize=marker_size,
                        mew=1,
                        zorder=10,
                    )
                else:
                    display_value = marked_value
                    marker_color = "purple"
                    # Display as text (no X marker) with high z-order
                    ax.text(
                        x,
                        y,
                        display_value,
                        color=marker_color,
                        fontsize=fontsize,
                        ha="center",
                        va="center",
                        zorder=10,
                    )

    ax.set_xlim(df_selected["x_min"].min() - 10, df_selected["x_max"].max() + 10)

    # Apply Y-axis flip if enabled
    if y_axis_flipped[0]:
        ax.set_ylim(df_selected["y_max"].max() + 10, df_selected["y_min"].min() - 10)
    else:
        ax.set_ylim(df_selected["y_min"].min() - 10, df_selected["y_max"].max() + 10)

    ax.axis("off")
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close(fig)
    return img


# Global variables for plotting
df = None
output_dir = None
image_ids: List[str] = []
annotation_states: Dict[str, dict] = {}
thumbnails: list = []
thumb_axes: list = []
current_image_idx = [0]
label_columns: List[str] = []  # Will be populated with label columns from CSV
image_url_columns: List[str] = []
loaded_images: Dict[str, Any] = {}
labels_enabled = [True]
show_background_image = [False]
y_axis_flipped = [True]
nav_text = None
help_text_box = None
btn_help = None
btn_website = None


# --- NEW: Welcome Screen Function with Settings ---
def show_welcome_screen_and_get_filepath():
    """
    Displays a welcome screen with settings option and handles file selection.
    Returns the selected file path or an empty string if canceled.
    """
    selected_file = None

    def select_file_and_close():
        nonlocal selected_file
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.getcwd(),
        )
        if file_path:
            selected_file = file_path
            screen_manager.destroy()

    def show_settings_page():
        """Show settings page in the main window using UnifiedScreenManager"""
        try:
            # Clear the current content and show settings
            screen_manager.clear_content()
            screen_manager.current_mode = "settings"

            # Hide the logo section for settings
            if screen_manager.logo_frame:
                screen_manager.logo_frame.pack_forget()

            # Create settings content in the main window
            settings_frame = tk.Frame(screen_manager.content_frame, bg="#1a1a1a")
            settings_frame.pack(expand=True, fill="both", padx=10, pady=0)

            # Title
            title_label = tk.Label(
                settings_frame,
                text="⚙️ Settings",
                font=tkFont.Font(family="Helvetica", size=20, weight="bold"),
                bg="#1a1a1a",
                fg="#ffffff",
            )
            title_label.pack(pady=(0, 5))

            # Description
            desc_label = tk.Label(
                settings_frame,
                text="Configure application preferences and performance settings",
                font=tkFont.Font(family="Helvetica", size=12),
                bg="#1a1a1a",
                fg="#cccccc",
            )
            desc_label.pack(pady=(0, 10))

            # Create scrollable frame for settings
            canvas = tk.Canvas(settings_frame, bg="#1a1a1a", highlightthickness=0)
            scrollbar = tk.Scrollbar(
                settings_frame, orient="vertical", command=canvas.yview
            )
            scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Create a container frame for stacked layout
            cards_container = tk.Frame(scrollable_frame, bg="#1a1a1a")
            cards_container.pack(expand=True, fill="both", padx=30)

            # Create a centered container for the cards
            centered_container = tk.Frame(cards_container, bg="#1a1a1a")
            centered_container.pack(expand=True, fill="both")

            # Create the actual cards container with max width for centering
            cards_inner = tk.Frame(centered_container, bg="#1a1a1a")
            cards_inner.pack(expand=True, fill="x", padx=50)

            # Device detection and performance scoring
            def get_device_profile():
                """Get device hardware profile for intelligent suggestions"""
                try:
                    import psutil

                    cpu_cores = psutil.cpu_count()
                    ram_gb = psutil.virtual_memory().total / (1024**3)

                    # Simple storage type detection
                    storage_type = "hdd"  # Default assumption
                    try:
                        if os.path.exists("/sys/block/sda/queue/rotational"):
                            with open("/sys/block/sda/queue/rotational", "r") as f:
                                if f.read().strip() == "0":
                                    storage_type = "ssd"
                    except:
                        pass

                    return {
                        "cpu_cores": cpu_cores,
                        "ram_gb": ram_gb,
                        "storage_type": storage_type,
                    }
                except ImportError:
                    return {"cpu_cores": 4, "ram_gb": 8, "storage_type": "hdd"}

            def calculate_performance_score(profile):
                """Calculate performance score (0-100) based on hardware"""
                score = 0
                score += (
                    min(profile["ram_gb"] / 16, 1) * 40
                )  # RAM: 40 points (16GB = 100%)
                score += (
                    min(profile["cpu_cores"] / 8, 1) * 30
                )  # CPU: 30 points (8 cores = 100%)
                score += (
                    20 if profile["storage_type"] == "ssd" else 10
                )  # Storage: 20 points
                score += 10  # Base score
                return min(100, max(0, int(score)))

            def get_performance_suggestion(score):
                """Get performance mode suggestion based on score"""
                if score >= 80:
                    return "high", "High Performance (All features)"
                elif score >= 50:
                    return "balanced", "Balanced (Recommended)"
                else:
                    return "low", "Low-End Optimized"

            # Device info section
            device_profile = get_device_profile()
            performance_score = calculate_performance_score(device_profile)
            suggested_mode, suggested_text = get_performance_suggestion(
                performance_score
            )

            device_frame = tk.LabelFrame(
                cards_inner,
                text="📱 Device Information",
                font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                bg="#2a2a2a",
                fg="#ffffff",
                padx=15,
                pady=15,
            )
            device_frame.pack(fill="x", pady=(0, 8))

            # Center-aligned device info
            device_info = f"CPU: {device_profile['cpu_cores']} cores | RAM: {device_profile['ram_gb']:.1f}GB | Storage: {device_profile['storage_type'].upper()}"
            device_label = tk.Label(
                device_frame,
                text=device_info,
                font=tkFont.Font(family="Helvetica", size=13),
                bg="#2a2a2a",
                fg="#ffffff",
            )
            device_label.pack(pady=5)

            # Performance score
            score_info = tk.Label(
                device_frame,
                text=f"Performance Score: {performance_score}/100",
                font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
                bg="#2a2a2a",
                fg="#00ff88",
            )
            score_info.pack(pady=(8, 3))

            # Suggested mode
            suggestion_info = tk.Label(
                device_frame,
                text=f"Recommended: {suggested_text}",
                font=tkFont.Font(family="Helvetica", size=12),
                bg="#2a2a2a",
                fg="#cccccc",
            )
            suggestion_info.pack(pady=3)

            # Performance profile section
            profile_frame = tk.LabelFrame(
                cards_inner,
                text="🚀 Performance Profile",
                font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                bg="#2a2a2a",
                fg="#ffffff",
                padx=15,
                pady=15,
            )
            profile_frame.pack(fill="x", pady=(0, 8))

            profile_var = tk.StringVar(value="balanced")

            def on_profile_change():
                selected = profile_var.get()
                apply_performance_profile(selected)
                update_settings_display()

            def apply_performance_profile(profile_name):
                """Apply predefined performance profile settings"""
                if profile_name == "high":
                    settings["show_background_images"].set(False)
                    settings["high_quality_thumbnails"].set(True)
                    settings["real_time_hover"].set(True)
                    settings["smooth_animations"].set(True)
                    settings["anti_aliasing"].set(True)
                    settings["progressive_loading"].set(False)
                    settings["image_caching"].set(True)
                    settings["aggressive_cleanup"].set(False)
                elif profile_name == "balanced":
                    settings["show_background_images"].set(False)
                    settings["high_quality_thumbnails"].set(True)
                    settings["real_time_hover"].set(True)
                    settings["smooth_animations"].set(False)
                    settings["anti_aliasing"].set(True)
                    settings["progressive_loading"].set(False)
                    settings["image_caching"].set(True)
                    settings["aggressive_cleanup"].set(False)
                elif profile_name == "low":
                    settings["show_background_images"].set(False)
                    settings["high_quality_thumbnails"].set(False)
                    settings["real_time_hover"].set(False)
                    settings["smooth_animations"].set(False)
                    settings["anti_aliasing"].set(False)
                    settings["progressive_loading"].set(True)
                    settings["image_caching"].set(False)
                    settings["aggressive_cleanup"].set(True)

            # Center-aligned radio buttons for performance profiles
            tk.Radiobutton(
                profile_frame,
                text="High Performance (All features)",
                variable=profile_var,
                value="high",
                command=on_profile_change,
                font=tkFont.Font(family="Helvetica", size=13),
                bg="#2a2a2a",
                fg="#ffffff",
                selectcolor="#2a2a2a",
            ).pack(anchor="center", pady=2)

            tk.Radiobutton(
                profile_frame,
                text="Balanced (Recommended)",
                variable=profile_var,
                value="balanced",
                command=on_profile_change,
                font=tkFont.Font(family="Helvetica", size=13),
                bg="#2a2a2a",
                fg="#ffffff",
                selectcolor="#2a2a2a",
            ).pack(anchor="center", pady=2)

            tk.Radiobutton(
                profile_frame,
                text="Low-End Optimized",
                variable=profile_var,
                value="low",
                command=on_profile_change,
                font=tkFont.Font(family="Helvetica", size=13),
                bg="#2a2a2a",
                fg="#ffffff",
                selectcolor="#2a2a2a",
            ).pack(anchor="center", pady=2)

            tk.Radiobutton(
                profile_frame,
                text="Custom (Manual configuration)",
                variable=profile_var,
                value="custom",
                command=on_profile_change,
                font=tkFont.Font(family="Helvetica", size=13),
                bg="#2a2a2a",
                fg="#ffffff",
                selectcolor="#2a2a2a",
            ).pack(anchor="center", pady=2)

            # Feature toggles section
            features_frame = tk.LabelFrame(
                cards_inner,
                text="🎨 Feature Toggles",
                font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                bg="#2a2a2a",
                fg="#ffffff",
                padx=15,
                pady=15,
            )
            features_frame.pack(fill="x", pady=(0, 8))

            # Initialize settings variables
            settings = {
                "show_background_images": tk.BooleanVar(value=False),
                "high_quality_thumbnails": tk.BooleanVar(value=True),
                "real_time_hover": tk.BooleanVar(value=True),
                "smooth_animations": tk.BooleanVar(value=False),
                "anti_aliasing": tk.BooleanVar(value=True),
                "progressive_loading": tk.BooleanVar(value=False),
                "image_caching": tk.BooleanVar(value=True),
                "aggressive_cleanup": tk.BooleanVar(value=False),
            }

            def create_feature_checkbox(parent, text, setting_var, description=""):
                frame = tk.Frame(parent, bg="#2a2a2a")
                frame.pack(fill="x", pady=2)

                cb = tk.Checkbutton(
                    frame,
                    text=text,
                    variable=setting_var,
                    font=tkFont.Font(family="Helvetica", size=13),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    selectcolor="#2a2a2a",
                )
                cb.pack(anchor="center")

                if description:
                    desc_label = tk.Label(
                        frame,
                        text=description,
                        font=tkFont.Font(family="Helvetica", size=11),
                        bg="#2a2a2a",
                        fg="#888888",
                    )
                    desc_label.pack(anchor="center", pady=(2, 0))

                return cb

            def update_settings_display():
                """Update the display of settings based on current values"""
                pass  # This will be called when profile changes

            # Create checkboxes for features in single column
            feature_checkboxes = {}

            feature_checkboxes["bg_images"] = create_feature_checkbox(
                features_frame,
                "Background Images",
                settings["show_background_images"],
                "Disabled by default - may impact performance",
            )
            feature_checkboxes["high_quality"] = create_feature_checkbox(
                features_frame,
                "High-Quality Thumbnails",
                settings["high_quality_thumbnails"],
                "Recommended for your device",
            )
            feature_checkboxes["real_time_hover"] = create_feature_checkbox(
                features_frame,
                "Real-Time Hover",
                settings["real_time_hover"],
                "Smooth hover interactions",
            )
            feature_checkboxes["smooth_animations"] = create_feature_checkbox(
                features_frame,
                "Smooth Animations",
                settings["smooth_animations"],
                "UI transition effects",
            )
            feature_checkboxes["anti_aliasing"] = create_feature_checkbox(
                features_frame,
                "Anti-Aliasing",
                settings["anti_aliasing"],
                "Sharp, crisp graphics",
            )

            # Memory management section
            memory_frame = tk.LabelFrame(
                cards_inner,
                text="💾 Memory Management",
                font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                bg="#2a2a2a",
                fg="#ffffff",
                padx=15,
                pady=15,
            )
            memory_frame.pack(fill="x", pady=(0, 8))

            # Create memory management checkboxes in single column
            feature_checkboxes["progressive"] = create_feature_checkbox(
                memory_frame,
                "Progressive Thumbnail Loading",
                settings["progressive_loading"],
                "Recommended for low-end devices",
            )
            feature_checkboxes["caching"] = create_feature_checkbox(
                memory_frame,
                "Image Caching",
                settings["image_caching"],
                "Recommended for your device",
            )
            feature_checkboxes["cleanup"] = create_feature_checkbox(
                memory_frame,
                "Aggressive Memory Cleanup",
                settings["aggressive_cleanup"],
                "Low-end optimization",
            )

            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Update button frame - clear existing buttons and recreate
            for widget in screen_manager.button_frame.winfo_children():
                widget.destroy()

            # Ensure button frame is visible
            screen_manager.button_frame.pack(side="bottom", fill="x", pady=(20, 0))

            # Create button container for centering
            button_container = tk.Frame(screen_manager.button_frame, bg="#1a1a1a")
            button_container.pack(expand=True)

            def save_settings():
                """Save settings and return to welcome screen"""
                print("Settings saved!")
                # Use the original show_welcome_screen method
                screen_manager.show_welcome_screen(
                    select_file_and_close, show_settings_page
                )

            def cancel_settings():
                """Cancel and return to welcome screen"""
                print("Settings cancelled - returning to welcome screen")
                try:
                    # Use the original show_welcome_screen method
                    screen_manager.show_welcome_screen(
                        select_file_and_close, show_settings_page
                    )
                    print("Successfully returned to welcome screen")
                except Exception as e:
                    print(f"Error returning to welcome screen: {e}")

            # Save button
            save_button = tk.Button(
                button_container,
                text="💾 Save Settings",
                command=save_settings,
                font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
                bg="#00ff88",
                fg="#1a1a1a",
                activebackground="#00cc6a",
                activeforeground="#1a1a1a",
                relief=tk.FLAT,
                padx=30,
                pady=12,
                cursor="hand2",
            )
            save_button.pack(side="right", padx=(15, 0))

            # Cancel button
            cancel_button = tk.Button(
                button_container,
                text="❌ Cancel",
                command=cancel_settings,
                font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
                bg="#666666",
                fg="#ffffff",
                activebackground="#888888",
                activeforeground="#ffffff",
                relief=tk.FLAT,
                padx=30,
                pady=12,
                cursor="hand2",
            )
            cancel_button.pack(side="right")

        except Exception as e:
            print(f"Error opening settings: {e}")
            # Fallback to simple message
            print("Settings page would open here")

    # Create unified window and show welcome screen
    screen_manager.create_unified_window(
        "Unified Plotter | Professional Bounding Box Visualization", show_title_bar=True
    )
    screen_manager.show_welcome_screen(select_file_and_close, show_settings_page)
    screen_manager.run()

    return selected_file

    # Device detection
    def get_device_profile():
        """Get device hardware profile for intelligent suggestions"""
        try:
            import psutil

            cpu_cores = psutil.cpu_count()
            ram_gb = psutil.virtual_memory().total / (1024**3)

            # Simple storage type detection
            storage_type = "hdd"  # Default assumption
            try:
                # This is a simplified check - in practice you might want more sophisticated detection
                if os.path.exists("/sys/block/sda/queue/rotational"):
                    with open("/sys/block/sda/queue/rotational", "r") as f:
                        if f.read().strip() == "0":
                            storage_type = "ssd"
            except:
                pass

            return {
                "cpu_cores": cpu_cores,
                "ram_gb": ram_gb,
                "storage_type": storage_type,
            }
        except ImportError:
            # Fallback if psutil not available
            return {"cpu_cores": 4, "ram_gb": 8, "storage_type": "hdd"}

    def calculate_performance_score(profile):
        """Calculate performance score (0-100) based on hardware"""
        score = 0
        score += min(profile["ram_gb"] / 16, 1) * 40  # RAM: 40 points (16GB = 100%)
        score += (
            min(profile["cpu_cores"] / 8, 1) * 30
        )  # CPU: 30 points (8 cores = 100%)
        score += 20 if profile["storage_type"] == "ssd" else 10  # Storage: 20 points
        score += 10  # Base score
        return min(100, max(0, int(score)))

    def get_performance_suggestion(score):
        """Get performance mode suggestion based on score"""
        if score >= 80:
            return "high", "High Performance (All features)"
        elif score >= 50:
            return "balanced", "Balanced (Recommended)"
        else:
            return "low", "Low-End Optimized"

    def apply_performance_profile(profile_name):
        """Apply predefined performance profile settings"""
        if profile_name == "high":
            settings["show_background_images"].set(
                False
            )  # Disabled by default for all profiles
            settings["high_quality_thumbnails"].set(True)
            settings["real_time_hover"].set(True)
            settings["smooth_animations"].set(True)
            settings["anti_aliasing"].set(True)
            settings["progressive_loading"].set(False)
            settings["image_caching"].set(True)
            settings["aggressive_cleanup"].set(False)
            settings["disable_background_image_button"].set(
                True
            )  # Button disabled by default for all profiles
        elif profile_name == "balanced":
            settings["show_background_images"].set(
                False
            )  # Disabled by default for all profiles
            settings["high_quality_thumbnails"].set(True)
            settings["real_time_hover"].set(True)
            settings["smooth_animations"].set(False)
            settings["anti_aliasing"].set(True)
            settings["progressive_loading"].set(False)
            settings["image_caching"].set(True)
            settings["aggressive_cleanup"].set(False)
            settings["disable_background_image_button"].set(
                True
            )  # Button disabled by default for all profiles
        elif profile_name == "low":
            settings["show_background_images"].set(
                False
            )  # Disabled by default for all profiles
            settings["high_quality_thumbnails"].set(False)
            settings["real_time_hover"].set(False)
            settings["smooth_animations"].set(False)
            settings["anti_aliasing"].set(False)
            settings["progressive_loading"].set(True)
            settings["image_caching"].set(False)
            settings["aggressive_cleanup"].set(True)
            settings["disable_background_image_button"].set(
                True
            )  # Button disabled by default for all profiles

    def show_settings_page():
        """Show the settings page in the same window"""
        # Clear main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Create settings page
        settings_frame = tk.Frame(main_frame, bg="#1a1a1a")
        settings_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Settings title
        settings_title = tk.Label(
            settings_frame,
            text="⚙️ Performance Settings",
            font=title_font,
            bg="#1a1a1a",
            fg="#ffffff",
            pady=5,
        )
        settings_title.pack(pady=(0, 10))

        # Create scrollable frame for settings
        canvas = tk.Canvas(settings_frame, bg="#1a1a1a", highlightthickness=0)
        scrollbar = tk.Scrollbar(
            settings_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Device info section
        device_profile = get_device_profile()
        performance_score = calculate_performance_score(device_profile)
        suggested_mode, suggested_text = get_performance_suggestion(performance_score)

        device_frame = tk.LabelFrame(
            scrollable_frame,
            text="📱 Device Information",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=5,
        )
        device_frame.pack(fill="x", padx=5, pady=5)

        device_info = f"RAM: {device_profile['ram_gb']:.1f}GB | CPU: {device_profile['cpu_cores']} cores | Storage: {device_profile['storage_type'].upper()}"
        device_label = tk.Label(
            device_frame, text=device_info, font=body_font, bg="#ffffff", fg="#555555"
        )
        device_label.pack(pady=2)

        score_info = f"Performance Score: {performance_score}/100"
        score_label = tk.Label(
            device_frame, text=score_info, font=body_font, bg="#ffffff", fg="#555555"
        )
        score_label.pack(pady=2)

        suggestion_info = f"Suggested Mode: {suggested_text}"
        suggestion_label = tk.Label(
            device_frame,
            text=suggestion_info,
            font=body_font,
            bg="#ffffff",
            fg="#28a745",
        )
        suggestion_label.pack(pady=2)

        # Performance profile section
        profile_frame = tk.LabelFrame(
            scrollable_frame,
            text="🚀 Performance Profile",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=5,
        )
        profile_frame.pack(fill="x", padx=5, pady=5)

        profile_var = tk.StringVar(value=settings["performance_mode"].get())

        def on_profile_change():
            selected = profile_var.get()
            settings["performance_mode"].set(selected)
            apply_performance_profile(selected)
            update_settings_display()

        tk.Radiobutton(
            profile_frame,
            text="High Performance (All features)",
            variable=profile_var,
            value="high",
            command=on_profile_change,
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w", pady=2)
        tk.Radiobutton(
            profile_frame,
            text="Balanced (Recommended)",
            variable=profile_var,
            value="balanced",
            command=on_profile_change,
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w", pady=2)
        tk.Radiobutton(
            profile_frame,
            text="Low-End Optimized",
            variable=profile_var,
            value="low",
            command=on_profile_change,
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w", pady=2)
        tk.Radiobutton(
            profile_frame,
            text="Custom",
            variable=profile_var,
            value="custom",
            command=on_profile_change,
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w", pady=2)

        # Feature toggles section
        features_frame = tk.LabelFrame(
            scrollable_frame,
            text="🎨 Feature Toggles",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=5,
        )
        features_frame.pack(fill="x", padx=5, pady=5)

        def update_settings_display():
            """Update the display of settings based on current values"""
            pass  # This will be called when profile changes

        # Create checkboxes for features
        feature_checkboxes = {}

        def create_feature_checkbox(parent, text, setting_var, description=""):
            frame = tk.Frame(parent, bg="#ffffff")
            frame.pack(fill="x", pady=2)

            cb = tk.Checkbutton(
                frame,
                text=text,
                variable=setting_var,
                font=body_font,
                bg="#ffffff",
                fg="#333333",
            )
            cb.pack(side="left")

            if description:
                desc_label = tk.Label(
                    frame,
                    text=description,
                    font=tkFont.Font(family="Helvetica", size=9),
                    bg="#ffffff",
                    fg="#888888",
                )
                desc_label.pack(side="left", padx=(10, 0))

            return cb

        feature_checkboxes["bg_images"] = create_feature_checkbox(
            features_frame,
            "Background Images",
            settings["show_background_images"],
            "Disabled by default - may impact performance",
        )
        feature_checkboxes["high_quality"] = create_feature_checkbox(
            features_frame,
            "High-Quality Thumbnails",
            settings["high_quality_thumbnails"],
            "Recommended for your device",
        )
        feature_checkboxes["real_time"] = create_feature_checkbox(
            features_frame, "Real-time Hover Labels", settings["real_time_hover"]
        )
        feature_checkboxes["smooth"] = create_feature_checkbox(
            features_frame,
            "Smooth Animations",
            settings["smooth_animations"],
            "May impact performance",
        )
        feature_checkboxes["anti_aliasing"] = create_feature_checkbox(
            features_frame,
            "Anti-aliasing",
            settings["anti_aliasing"],
            "High-end feature",
        )

        # Additional settings section
        additional_frame = tk.LabelFrame(
            scrollable_frame,
            text="🔧 Additional Settings",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=5,
        )
        additional_frame.pack(fill="x", padx=5, pady=5)

        feature_checkboxes["disable_bg_button"] = create_feature_checkbox(
            additional_frame,
            "Disable Background Image Button",
            settings["disable_background_image_button"],
            "Enabled by default - removes button from UI",
        )
        feature_checkboxes["save_plots"] = create_feature_checkbox(
            additional_frame,
            "Save Plots on Program Close",
            settings["save_plots_on_close"],
            "Automatically save plots when closing",
        )

        # Memory management section
        memory_frame = tk.LabelFrame(
            scrollable_frame,
            text="💾 Memory Management",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=5,
        )
        memory_frame.pack(fill="x", padx=5, pady=5)

        feature_checkboxes["progressive"] = create_feature_checkbox(
            memory_frame,
            "Progressive Thumbnail Loading",
            settings["progressive_loading"],
            "Recommended for low-end",
        )
        feature_checkboxes["caching"] = create_feature_checkbox(
            memory_frame,
            "Image Caching",
            settings["image_caching"],
            "Recommended for your device",
        )
        feature_checkboxes["cleanup"] = create_feature_checkbox(
            memory_frame,
            "Aggressive Memory Cleanup",
            settings["aggressive_cleanup"],
            "Low-end optimization",
        )

        # Thumbnail settings section
        thumbnail_frame = tk.LabelFrame(
            scrollable_frame,
            text="🖼️ Thumbnail Settings",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=5,
        )
        thumbnail_frame.pack(fill="x", padx=5, pady=5)

        # Thumbnail width setting
        width_frame = tk.Frame(thumbnail_frame, bg="#ffffff")
        width_frame.pack(fill="x", pady=2)

        width_label = tk.Label(
            width_frame,
            text="Thumbnail Width (% of figure):",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        )
        width_label.pack(side="left")

        width_var = tk.StringVar(value="5.0")
        width_entry = tk.Entry(
            width_frame, textvariable=width_var, font=body_font, width=8
        )
        width_entry.pack(side="left", padx=(10, 0))

        # Thumbnail padding setting
        padding_frame = tk.Frame(thumbnail_frame, bg="#ffffff")
        padding_frame.pack(fill="x", pady=2)

        padding_label = tk.Label(
            padding_frame,
            text="Thumbnail Padding (% of figure):",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        )
        padding_label.pack(side="left")

        padding_var = tk.StringVar(value="0.8")
        padding_entry = tk.Entry(
            padding_frame, textvariable=padding_var, font=body_font, width=8
        )
        padding_entry.pack(side="left", padx=(10, 0))

        # Logging settings section
        logging_frame = tk.LabelFrame(
            scrollable_frame,
            text="📝 Logging & Debugging",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=5,
        )
        logging_frame.pack(fill="x", padx=5, pady=5)

        # Log retention setting
        retention_frame = tk.Frame(logging_frame, bg="#ffffff")
        retention_frame.pack(fill="x", pady=2)

        retention_label = tk.Label(
            retention_frame,
            text="Log Retention:",
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        )
        retention_label.pack(side="left")

        retention_var = settings["log_retention"]
        retention_menu = tk.OptionMenu(
            retention_frame, retention_var, "Daily", "Weekly", "Monthly", "Yearly"
        )
        retention_menu.config(font=body_font, bg="#ffffff", fg="#333333", width=15)
        retention_menu.pack(side="left", padx=(10, 0))

        # Debug logging toggle
        debug_var = settings["enable_debug_logging"]
        debug_checkbox = tk.Checkbutton(
            logging_frame,
            text="Enable Debug Logging",
            variable=debug_var,
            font=body_font,
            bg="#ffffff",
            fg="#333333",
        )
        debug_checkbox.pack(anchor="w", pady=2)

        # Log management buttons
        log_buttons_frame = tk.Frame(logging_frame, bg="#ffffff")
        log_buttons_frame.pack(fill="x", pady=(10, 0))

        download_logs_btn = tk.Button(
            log_buttons_frame,
            text="📥 Download Logs",
            command=download_logs,
            font=body_font,
            bg="#007bff",
            fg="black",
            activebackground="#0056b3",
            activeforeground="black",
            relief=tk.FLAT,
            borderwidth=1,
            padx=15,
            pady=5,
        )
        download_logs_btn.pack(side="left", padx=(0, 10))

        delete_logs_btn = tk.Button(
            log_buttons_frame,
            text="🗑️ Delete All Logs",
            command=delete_logs,
            font=body_font,
            bg="#dc3545",
            fg="black",
            activebackground="#c82333",
            activeforeground="black",
            relief=tk.FLAT,
            borderwidth=1,
            padx=15,
            pady=5,
        )
        delete_logs_btn.pack(side="left")

        # Apply initial profile
        apply_performance_profile(settings["performance_mode"].get())

        # Buttons section
        buttons_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        buttons_frame.pack(fill="x", padx=5, pady=10)

        def save_settings():
            """Save settings and return to welcome screen"""
            # Store settings in global variables for later use
            global global_settings

            # Convert thumbnail settings from percentage to decimal
            try:
                thumb_width = float(width_var.get()) / 100.0
                thumb_padding = float(padding_var.get()) / 100.0

                # Validate thumbnail settings to ensure they're reasonable
                if thumb_width < 0.02 or thumb_width > 0.15:
                    print("⚠ Thumbnail width out of range (2%-15%), using default 6%")
                    thumb_width = 0.06
                if thumb_padding < 0.005 or thumb_padding > 0.05:
                    print(
                        "⚠ Thumbnail padding out of range (0.5%-5%), using default 1%"
                    )
                    thumb_padding = 0.01

            except ValueError:
                # Use defaults if conversion fails
                print("⚠ Invalid thumbnail settings, using defaults")
                thumb_width = 0.06
                thumb_padding = 0.01

            global_settings = {
                "performance_mode": settings["performance_mode"].get(),
                "show_background_images": settings["show_background_images"].get(),
                "high_quality_thumbnails": settings["high_quality_thumbnails"].get(),
                "real_time_hover": settings["real_time_hover"].get(),
                "smooth_animations": settings["smooth_animations"].get(),
                "anti_aliasing": settings["anti_aliasing"].get(),
                "progressive_loading": settings["progressive_loading"].get(),
                "image_caching": settings["image_caching"].get(),
                "aggressive_cleanup": settings["aggressive_cleanup"].get(),
                "disable_background_image_button": settings[
                    "disable_background_image_button"
                ].get(),
                "save_plots_on_close": settings["save_plots_on_close"].get(),
                "log_retention": retention_var.get(),
                "enable_debug_logging": debug_var.get(),
                "thumbnail_width": thumb_width,
                "thumbnail_padding": thumb_padding,
            }

            # Clean up old logs based on new retention setting
            cleanup_old_logs()

            show_welcome_page()

        def cancel_settings():
            """Cancel settings and return to welcome screen"""
            show_welcome_page()

        save_btn = tk.Button(
            buttons_frame,
            text="Save Settings",
            command=save_settings,
            font=button_font,
            bg="#28a745",
            fg="black",
            activebackground="#218838",
            activeforeground="black",
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=8,
            cursor="",
        )
        save_btn.pack(side="left", padx=(0, 10))

        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            command=cancel_settings,
            font=button_font,
            bg="#6c757d",
            fg="black",
            activebackground="#5a6268",
            activeforeground="black",
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=8,
            cursor="",
        )
        cancel_btn.pack(side="left")

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configure scrolling - Enhanced mouse wheel support for all platforms
        def _on_mousewheel(event):
            # Handle different mouse wheel delta values across platforms
            if event.delta:
                # Windows and some Linux systems
                delta = int(-1 * (event.delta / 120))
            elif event.num == 4:
                # Linux scroll up
                delta = -1
            elif event.num == 5:
                # Linux scroll down
                delta = 1
            else:
                # macOS and other systems
                delta = -1 if event.delta > 0 else 1

            canvas.yview_scroll(delta, "units")

        # Bind mouse wheel to canvas
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Also bind mouse wheel to the scrollable frame for better coverage
        scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

        # Bind mouse wheel to all child widgets in the scrollable frame
        def bind_mousewheel_to_widgets(widget):
            """Recursively bind mouse wheel to all child widgets"""
            widget.bind_all("<MouseWheel>", _on_mousewheel)
            # Also bind Linux-specific scroll events
            widget.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            widget.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
            for child in widget.winfo_children():
                bind_mousewheel_to_widgets(child)

        # Apply mouse wheel binding to all widgets in the scrollable frame
        bind_mousewheel_to_widgets(scrollable_frame)

    def show_welcome_page():
        """Show the main welcome page"""
        # Clear main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Welcome Label with professional branding
        welcome_label = tk.Label(
            main_frame,
            text="Unified Plotter",
            font=title_font,
            bg="#1a1a1a",
            fg="#ffffff",
            pady=15,
        )
        welcome_label.pack(pady=(0, 15))

        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Professional Edition",
            font=tkFont.Font(family="Helvetica", size=16),
            bg="#1a1a1a",
            fg="#00ff88",
            pady=8,
        )
        subtitle_label.pack(pady=(0, 25))

        # Description Text with better formatting
        description_text = (
            "Welcome to the professional bounding box visualization tool!\n\n"
            "This advanced tool helps you visualize and annotate bounding box data\n"
            "directly from your CSV files with enterprise-grade features.\n\n"
            "📋 Requirements:\n"
            "• CSV must include: image_id, x_min, x_max, y_min, y_max\n"
            "• Optional: label_* columns or image URL columns\n\n"
            "🚀 Click below to begin your professional workflow.\n"
            "⬇"
        )
        description_label = tk.Label(
            main_frame,
            text=description_text,
            font=body_font,
            justify=tk.CENTER,
            bg="#1a1a1a",
            fg="#cccccc",
            pady=15,
            wraplength=600,
        )
        description_label.pack()

        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#1a1a1a")
        buttons_frame.pack(pady=(10, 0))

        # Select File Button with professional styling (centered)
        select_button = tk.Button(
            buttons_frame,
            text="📁 Select CSV File",
            command=select_file_and_close,
            font=button_font,
            bg="#00ff88",
            fg="#1a1a1a",
            activebackground="#00cc6a",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            borderwidth=0,
            padx=40,
            pady=18,
            cursor="hand2",
        )
        select_button.pack(pady=(0, 30))  # Center the main button with bottom margin

        # Bottom row for settings and exit buttons
        bottom_buttons_frame = tk.Frame(main_frame, bg="#1a1a1a")
        bottom_buttons_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        # Settings Button (bottom left) - Professional styling
        settings_button = tk.Button(
            bottom_buttons_frame,
            text="⚙️ Settings",
            command=show_settings_page,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#333333",
            fg="#ffffff",
            activebackground="#555555",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        settings_button.pack(side="left", padx=(0, 10))

        # Exit Button (bottom right) - Professional styling
        exit_button = tk.Button(
            bottom_buttons_frame,
            text="❌ Exit",
            command=root.destroy,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#666666",
            fg="#ffffff",
            activebackground="#888888",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        exit_button.pack(side="right", padx=(10, 0))

        # Professional hover effects with smooth transitions
        def on_enter_select(e):
            select_button["background"] = "#00cc6a"  # Darker green on hover
            select_button["relief"] = tk.RAISED  # 3D effect on hover

        def on_leave_select(e):
            select_button["background"] = "#00ff88"  # Return to original green
            select_button["relief"] = tk.FLAT  # Return to flat relief

        def on_enter_settings(e):
            settings_button["background"] = "#555555"  # Darker gray on hover
            settings_button["relief"] = tk.RAISED  # 3D effect on hover

        def on_leave_settings(e):
            settings_button["background"] = "#333333"  # Return to original gray
            settings_button["relief"] = tk.FLAT  # Return to flat relief

        def on_enter_exit(e):
            exit_button["background"] = "#888888"  # Darker gray on hover
            exit_button["relief"] = tk.RAISED  # 3D effect on hover

        def on_leave_exit(e):
            exit_button["background"] = "#666666"  # Return to original gray
            exit_button["relief"] = tk.FLAT  # Return to flat relief

        select_button.bind("<Enter>", on_enter_select)
        select_button.bind("<Leave>", on_leave_select)
        settings_button.bind("<Enter>", on_enter_settings)
        settings_button.bind("<Leave>", on_leave_settings)
        exit_button.bind("<Enter>", on_enter_exit)
        exit_button.bind("<Leave>", on_leave_exit)

    # Configure window size and position - increased size for better content display
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    root.resizable(True, True)  # Allow resizing for settings page

    # Set up fonts with enhanced styling
    title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
    body_font = tkFont.Font(family="Helvetica", size=11)
    button_font = tkFont.Font(family="Helvetica", size=13, weight="bold")

    # Create a main frame with professional styling
    main_frame = tk.Frame(
        root, bg="#1a1a1a", padx=30, pady=30, relief=tk.RAISED, borderwidth=2
    )
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Show initial welcome page
    show_welcome_page()

    # Handle closing the window directly
    def on_closing():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the Tkinter event loop
    root.mainloop()

    return file_path_holder[0]


# Global settings variable to store user preferences - will be initialized in welcome screen
global_settings = {
    "performance_mode": "balanced",
    "show_background_images": False,  # Background images disabled by default
    "high_quality_thumbnails": True,
    "real_time_hover": True,
    "smooth_animations": True,
    "anti_aliasing": True,
    "progressive_loading": False,
    "image_caching": True,
    "aggressive_cleanup": False,
    "disable_background_image_button": True,  # Button disabled by default
    "save_plots_on_close": True,  # Default enabled
    "log_retention": "Monthly",  # How long to keep logs: Daily, Weekly, Monthly, Yearly
    "enable_debug_logging": False,  # Enable detailed debug logging
    "thumbnail_width": 0.05,  # Fixed thumbnail width (5% of figure width)
    "thumbnail_padding": 0.008,  # Fixed padding between thumbnails (0.8% of figure width)
}


# Logging configuration
def setup_logging():
    """Setup logging system with secure storage and rotation"""
    # Create secure log directory in system temp location
    log_dir = os.path.join(tempfile.gettempdir(), "plotter_logs")
    os.makedirs(log_dir, exist_ok=True)

    # Set permissions to be user-only (more secure)
    try:
        os.chmod(log_dir, 0o700)  # User read/write/execute only
    except:
        pass  # Ignore permission errors on some systems

    # Create session-specific log file
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"plotter_session_{session_id}.log")

    # Configure logging - always use INFO level for file logging, but add level info to messages
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),  # Also log to console
        ],
    )

    # Log system information
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("NEW PLOTTER SESSION STARTED")
    logger.info(f"Session ID: {session_id}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info("=" * 60)

    return logger, log_file, log_dir


def cleanup_old_logs():
    """Remove logs older than retention period"""
    try:
        log_dir = os.path.join(tempfile.gettempdir(), "plotter_logs")
        if not os.path.exists(log_dir):
            return

        # Convert retention setting to days
        retention_setting = global_settings.get("log_retention", "Monthly")
        if retention_setting == "Daily":
            retention_days = 1
        elif retention_setting == "Weekly":
            retention_days = 7
        elif retention_setting == "Monthly":
            retention_days = 30
        elif retention_setting == "Yearly":
            retention_days = 365
        else:
            retention_days = 30  # Default to monthly

        cutoff_time = datetime.now().timestamp() - (retention_days * 24 * 3600)

        deleted_count = 0
        for filename in os.listdir(log_dir):
            if filename.startswith("plotter_session_") and filename.endswith(".log"):
                file_path = os.path.join(log_dir, filename)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except:
                        pass

        if deleted_count > 0:
            logging.info(
                f"Cleaned up {deleted_count} old log files (older than {retention_setting} - {retention_days} days)"
            )

    except Exception as e:
        print(f"Warning: Could not cleanup old logs: {e}")


def get_log_summary():
    """Get summary of available logs"""
    try:
        log_dir = os.path.join(tempfile.gettempdir(), "plotter_logs")
        if not os.path.exists(log_dir):
            return []

        logs = []
        for filename in os.listdir(log_dir):
            if filename.startswith("plotter_session_") and filename.endswith(".log"):
                file_path = os.path.join(log_dir, filename)
                try:
                    stat = os.stat(file_path)
                    logs.append(
                        {
                            "filename": filename,
                            "size": stat.st_size,
                            "created": datetime.fromtimestamp(stat.st_ctime),
                            "modified": datetime.fromtimestamp(stat.st_mtime),
                            "path": file_path,
                        }
                    )
                except:
                    pass

        # Sort by creation time (newest first)
        logs.sort(key=lambda x: x["created"], reverse=True)
        return logs

    except Exception as e:
        print(f"Warning: Could not get log summary: {e}")
        return []


def download_logs():
    """Download logs to user-selected location"""
    try:
        logs = get_log_summary()
        if not logs:
            messagebox.showinfo("No Logs", "No log files found to download.")
            return

        # Ask user where to save logs
        save_dir = filedialog.askdirectory(title="Select directory to save logs")
        if not save_dir:
            return

        # Create timestamped folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir = os.path.join(save_dir, f"plotter_logs_export_{timestamp}")
        os.makedirs(export_dir, exist_ok=True)

        # Copy log files
        copied_count = 0
        for log in logs:
            try:
                dest_path = os.path.join(export_dir, log["filename"])
                shutil.copy2(log["path"], dest_path)
                copied_count += 1
            except Exception as e:
                print(f"Warning: Could not copy {log['filename']}: {e}")

        # Create summary file
        summary_file = os.path.join(export_dir, "logs_summary.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("Plotter Logs Export Summary\n")
            f.write("=" * 40 + "\n")
            f.write(f"Export date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total logs: {len(logs)}\n")
            f.write(f"Copied: {copied_count}\n\n")

            for log in logs:
                f.write(f"File: {log['filename']}\n")
                f.write(f"  Size: {log['size']} bytes\n")
                f.write(f"  Created: {log['created'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(
                    f"  Modified: {log['modified'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )

        messagebox.showinfo(
            "Logs Downloaded",
            f"Successfully exported {copied_count} log files to:\n{export_dir}",
        )

        # Open the export directory
        try:
            if sys.platform == "darwin":  # macOS
                os.system(f"open '{export_dir}'")
            elif sys.platform == "win32":  # Windows
                os.system(f"explorer '{export_dir}'")
            else:  # Linux
                os.system(f"xdg-open '{export_dir}'")
        except:
            pass

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download logs: {e}")


def delete_logs():
    """Delete all log files"""
    try:
        logs = get_log_summary()
        if not logs:
            messagebox.showinfo("No Logs", "No log files found to delete.")
            return

        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {len(logs)} log files?\n\n"
            "This action cannot be undone!",
        )
        if not result:
            return

        # Delete log files
        deleted_count = 0
        for log in logs:
            try:
                os.remove(log["path"])
                deleted_count += 1
            except Exception as e:
                print(f"Warning: Could not delete {log['filename']}: {e}")

        messagebox.showinfo(
            "Logs Deleted", f"Successfully deleted {deleted_count} log files."
        )

    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete logs: {e}")


# Main execution will be at the end of the file

# Old main execution code removed - now using main program loop

# Functions and classes moved to top level


# Function to load image from URL
def load_image_from_url(url):
    """Load image from URL and return as numpy array"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        return np.array(img)
    except Exception as e:
        print(f"Error loading image from {url}: {e}")
        return None


# Function to open image in browser
def open_image_in_browser(url):
    """Open image URL in default browser"""
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Error opening URL in browser: {e}")
        messagebox.showerror("Error", f"Could not open image URL: {e}")


# Store loaded images
loaded_images = {}

# Global state variables - these will be set by apply_global_settings()
labels_enabled = [True]  # Default to True, will be updated by settings
show_background_image = [False]  # Track if background image should be shown
# Set default to image-style (origin top-left, y increases downward)
y_axis_flipped = [True]  # True = image-style, False = matplotlib default


# Apply settings from welcome screen
def apply_global_settings():
    """Apply the global settings to the plotting functionality"""
    global labels_enabled, show_background_image

    # Apply performance settings
    if "real_time_hover" in global_settings:
        labels_enabled[0] = global_settings["real_time_hover"]
        print(
            f"✓ Labels enabled set to: {labels_enabled[0]} (from settings: {global_settings['real_time_hover']})"
        )
    else:
        print(
            f"⚠ 'real_time_hover' not found in global_settings. Available keys: {list(global_settings.keys())}"
        )

    if "show_background_images" in global_settings:
        show_background_image[0] = global_settings["show_background_images"]

    # Apply other settings as needed
    print(
        f"✓ Applied performance settings: {global_settings.get('performance_mode', 'balanced')}"
    )
    print(f"✓ Current labels_enabled state: {labels_enabled[0]}")


# Initialize logging system after all functions are defined
logger, current_log_file, log_directory = setup_logging()

# AnnotationState class moved to top level


# generate_thumbnail function moved to top level

# Old main execution code removed - now using modular functions


# --- Drawing and event logic ---
def highlight_thumbnail(index):
    """Highlights the thumbnail at the given index and un-highlights others."""
    for i, ax in enumerate(thumb_axes):
        if i == index:
            ax.spines["bottom"].set_color("blue")
            ax.spines["top"].set_color("blue")
            ax.spines["right"].set_color("blue")
            ax.spines["left"].set_color("blue")
            ax.spines["bottom"].set_linewidth(3)
            ax.spines["top"].set_linewidth(3)
            ax.spines["right"].set_linewidth(3)
            ax.spines["left"].set_linewidth(3)
        else:
            ax.spines["bottom"].set_color("black")
            ax.spines["top"].set_color("black")
            ax.spines["right"].set_color("black")
            ax.spines["left"].set_color("black")
            ax.spines["bottom"].set_linewidth(1)
            ax.spines["top"].set_linewidth(1)
            ax.spines["right"].set_linewidth(1)
            ax.spines["left"].set_linewidth(1)


def update_thumbnail_visibility():
    """Update which thumbnails are visible and center them"""
    global nav_text
    thumb_bbox = thumb_container_ax.get_position()

    # Show all thumbnails in a grid layout
    # Strictly limit to maximum 15 thumbnails for consistent layout
    total_thumbs = len(image_ids)
    current_idx = current_image_idx[0]
    max_visible_thumbs = 15  # Fixed maximum for consistent layout

    # Calculate how many thumbnails to show around the current one
    half_visible = max_visible_thumbs // 2
    start_idx = max(0, current_idx - half_visible)
    end_idx = min(total_thumbs, start_idx + max_visible_thumbs)

    # Adjust start_idx if we're near the end
    if end_idx - start_idx < max_visible_thumbs and start_idx > 0:
        start_idx = max(0, end_idx - max_visible_thumbs)

    num_visible = end_idx - start_idx
    if num_visible == 0:
        return

    # Fixed thumbnail size and padding (in figure coordinates)
    # These values ensure consistent thumbnail sizing regardless of plot area
    # Users can adjust these values in the settings if needed
    fixed_thumb_width = global_settings.get(
        "thumbnail_width", 0.05
    )  # Fixed width for each thumbnail (5% of figure width)
    fixed_padding = global_settings.get(
        "thumbnail_padding", 0.008
    )  # Fixed padding between thumbnails (0.8% of figure width)

    # Ensure we can fit exactly 15 thumbnails with comfortable spacing
    # Calculate if we need to adjust sizing for the maximum case
    if num_visible == 15:
        # For exactly 15 thumbnails, ensure they fit with some margin
        total_needed = (fixed_thumb_width * 15) + (fixed_padding * 14)
        if total_needed > 0.9:  # If we need more than 90% of available width
            # Reduce thumbnail width proportionally
            scale_factor = 0.9 / total_needed
            fixed_thumb_width *= scale_factor
            fixed_padding *= scale_factor

    # Calculate total width needed for visible thumbnails
    total_thumb_width = fixed_thumb_width * num_visible
    total_padding = fixed_padding * (num_visible - 1)
    total_width_needed = total_thumb_width + total_padding

    # Add margin on both sides to prevent boundary breaking
    side_margin = 0.02  # 2% margin on each side
    available_width = thumb_bbox.width - (2 * side_margin)

    # Ensure we don't exceed available width
    if total_width_needed > available_width:
        # Reduce padding further if needed
        excess_width = total_width_needed - available_width
        if num_visible > 1:
            padding_reduction = excess_width / (num_visible - 1)
            fixed_padding = max(
                0.002, fixed_padding - padding_reduction
            )  # Keep minimum padding
            # Recalculate total width
            total_padding = fixed_padding * (num_visible - 1)
            total_width_needed = total_thumb_width + total_padding

    # Center the visible thumbnails with side margins
    start_x = thumb_bbox.x0 + side_margin + (available_width - total_width_needed) / 2

    for i, ax in enumerate(thumb_axes):
        if start_idx <= i < end_idx:
            ax.set_visible(True)
            visible_idx = i - start_idx
            ax.set_position(
                [
                    start_x + visible_idx * (fixed_thumb_width + fixed_padding),
                    thumb_bbox.y0,
                    fixed_thumb_width,
                    thumb_bbox.height,
                ]
            )
        else:
            ax.set_visible(False)

    # Update dataset progress text with dynamic sizing
    if nav_text:
        if total_thumbs > 20:
            # Show percentage for datasets with more than 20 images
            progress_percent = (current_idx + 1) / total_thumbs * 100
            nav_text.set_text(
                f"Dataset Progress: {progress_percent:.1f}% ({current_idx + 1}/{total_thumbs})"
            )
        else:
            # Show simple progress for smaller datasets
            nav_text.set_text(f"Dataset Progress: {current_idx + 1}/{total_thumbs}")

        # Ensure the text is visible
        nav_text.set_visible(True)

        # Dynamically resize the text box to fit the content
        try:
            # Get the current text and calculate approximate width needed
            text_content = nav_text.get_text()
            # Estimate width based on text length and font size
            estimated_width = len(text_content) * 0.6  # Approximate character width
            # Ensure minimum and maximum widths
            estimated_width = max(0.3, min(estimated_width, 0.8))

            # Get current position and update width
            current_pos = nav_text.get_position()
            current_bbox = nav_text.get_bbox_patch()
            if current_bbox:
                # Update the bbox width to fit the text
                current_bbox.set_width(estimated_width)
                # Center the text box
                nav_text.set_position((0.5, current_pos[1]))
        except Exception as e:
            print(f"⚠ Error resizing dataset progress text box: {e}")

    # Update navigation arrows visibility
    try:
        # Get references to the navigation arrows
        left_arrow = None
        right_arrow = None
        for text_obj in thumb_container_ax.texts:
            if text_obj.get_text() == "◀":
                left_arrow = text_obj
            elif text_obj.get_text() == "▶":
                right_arrow = text_obj

        # Show/hide arrows based on thumbnail visibility
        if left_arrow:
            left_arrow.set_visible(start_idx > 0)
        if right_arrow:
            right_arrow.set_visible(end_idx < total_thumbs)

    except Exception as e:
        print(f"⚠ Error updating navigation arrows: {e}")

    fig.canvas.draw_idle()


def draw_main_plot(idx):
    try:
        main_ax.clear()
        img_id = image_ids[idx]
        df_selected = df[df["image_id"] == img_id].copy()

        # Get the annotation state early to avoid scope issues
        state = annotation_states[img_id]

        if df_selected.empty or df_selected["x_min"].isna().all():
            main_ax.text(
                0.5,
                0.5,
                "No bounding box data available",
                ha="center",
                va="center",
                transform=main_ax.transAxes,
                fontsize=12,
            )
            main_ax.set_title(f"Bounding Boxes for image_id: {img_id}")
            main_ax.set_xticks([])
            main_ax.set_yticks([])
            fig.canvas.draw_idle()
            return

        df_selected["width"] = df_selected["x_max"] - df_selected["x_min"]
        df_selected["height"] = df_selected["y_max"] - df_selected["y_min"]
        df_selected["area"] = df_selected["width"] * df_selected["height"]
        df_selected["center_x"] = (df_selected["x_min"] + df_selected["x_max"]) / 2
        df_selected["center_y"] = (df_selected["y_min"] + df_selected["y_max"]) / 2
        for _, row in df_selected.iterrows():
            rect = patches.Rectangle(
                (row["x_min"], row["y_min"]),
                row["width"],
                row["height"],
                linewidth=1,
                edgecolor="r",
                facecolor="none",
                zorder=1,  # Low z-order so markers appear on top
            )
            main_ax.add_patch(rect)

        x_min_all = (
            df_selected["x_min"].min() if not df_selected["x_min"].isnull().all() else 0
        )
        x_max_all = (
            df_selected["x_max"].max()
            if not df_selected["x_max"].isnull().all()
            else 100
        )
        y_min_all = (
            df_selected["y_min"].min() if not df_selected["y_min"].isnull().all() else 0
        )
        y_max_all = (
            df_selected["y_max"].max()
            if not df_selected["y_max"].isnull().all()
            else 100
        )

        # Set axis limits
        main_ax.set_xlim(x_min_all - 10, x_max_all + 10)

        # Apply Y-axis flip if enabled
        if y_axis_flipped[0]:
            main_ax.set_ylim(y_max_all + 10, y_min_all - 10)
        else:
            main_ax.set_ylim(y_min_all - 10, y_max_all + 10)

        # Add background image if enabled and available
        if show_background_image[0] and state.image_url:
            try:
                # Load image if not already loaded
                if state.image_url not in loaded_images:
                    img_array = load_image_from_url(state.image_url)
                    if img_array is not None:
                        loaded_images[state.image_url] = img_array
                    else:
                        print(f"Could not load image from {state.image_url}")
                        loaded_images[state.image_url] = None

                # Display background image
                if loaded_images.get(state.image_url) is not None:
                    img_array = loaded_images[state.image_url]
                    # Invert y-axis for image display (matplotlib vs image coordinates)
                    main_ax.imshow(
                        img_array,
                        extent=[
                            x_min_all - 10,
                            x_max_all + 10,
                            y_min_all - 10,
                            y_max_all + 10,
                        ],
                        alpha=0.7,
                        zorder=0,
                    )
                    main_ax.set_title(
                        f"Bounding Boxes for image_id: {img_id} (with background image)"
                    )
                else:
                    main_ax.set_title(f"Bounding Boxes for image_id: {img_id}")
            except Exception as e:
                print(f"Error displaying background image: {e}")
                main_ax.set_title(f"Bounding Boxes for image_id: {img_id}")
        else:
            main_ax.set_title(f"Bounding Boxes for image_id: {img_id}")

        main_ax.set_xlabel("X")
        main_ax.set_ylabel("Y")

        # Synchronize radio button with current state mode
        if radio.value_selected != state.mode:
            radio.set_active(0 if state.mode == "x" else 1)

        # Clear existing markers safely
        for marker, *_ in getattr(state, "markers", []):
            try:
                if marker and marker in main_ax.get_children():
                    marker.remove()
            except (NotImplementedError, ValueError):
                pass  # Ignore errors when removing already removed artists
        state.markers.clear()

        # Clear hover text safely
        if state.hover_text:
            try:
                if state.hover_text in main_ax.get_children():
                    state.hover_text.remove()
            except (NotImplementedError, ValueError):
                pass
            state.hover_text = None

        # Draw existing annotations (only for new annotations, not existing CSV marks)
        for ann in state.annotations:
            x, y = ann["x"], ann["y"]
            mark_value = ann.get("mark_value", "")

            # Check if this annotation corresponds to an existing CSV mark
            # If so, skip drawing it to avoid duplicates
            skip_drawing = False
            if "marked" in df.columns:
                for _, row in df_selected.iterrows():
                    if (
                        row["x_min"] <= x <= row["x_max"]
                        and row["y_min"] <= y <= row["y_max"]
                    ):
                        existing_mark = str(row.get("marked", "")).strip()
                        if (
                            existing_mark
                            and existing_mark.lower() != "nan"
                            and existing_mark.lower() != ""
                        ):
                            skip_drawing = True
                            break

            if not skip_drawing:
                if state.mode == "number" and str(mark_value).isdigit():
                    (marker,) = main_ax.plot(
                        x,
                        y,
                        marker=f"${mark_value}$",
                        color="red",
                        markersize=14,
                        mew=2,
                    )
                else:
                    (marker,) = main_ax.plot(
                        x, y, marker="x", color="blue", markersize=10, mew=2
                    )
                label_text = ", ".join(
                    str(ann.get(label_col, "")) for label_col in label_columns
                )
                state.markers.append((marker, label_text, x, y, mark_value))

        # Draw existing marks from CSV 'marked' column
        if "marked" in df.columns:
            for _, row in df_selected.iterrows():
                marked_value = str(row.get("marked", "")).strip()
                if (
                    marked_value
                    and marked_value.lower() != "nan"
                    and marked_value.lower() != ""
                ):
                    x, y = (row["x_min"] + row["x_max"]) / 2, (
                        row["y_min"] + row["y_max"]
                    ) / 2

                    # Convert "yes" to "x" for display
                    if marked_value.lower() == "yes":
                        display_value = "x"
                        marker_color = (
                            "green"  # Different color for existing "yes" marks
                        )
                        marker_size = 12
                        # Display as X marker with high z-order
                        (marker,) = main_ax.plot(
                            x,
                            y,
                            marker="x",
                            color=marker_color,
                            markersize=marker_size,
                            mew=2,
                            zorder=10,
                        )
                    else:
                        display_value = marked_value
                        marker_color = (
                            "purple"  # Different color for other existing marks
                        )
                        # Display as text (no X marker) with high z-order
                        marker = main_ax.text(
                            x,
                            y,
                            display_value,
                            color=marker_color,
                            fontsize=12,
                            ha="center",
                            va="center",
                            weight="bold",
                            zorder=10,
                        )

                    # Add to markers list for hover functionality
                    label_text = ", ".join(
                        str(row.get(label_col, "")) for label_col in label_columns
                    )
                    state.markers.append((marker, label_text, x, y, marked_value))

        highlight_thumbnail(idx)
        fig.canvas.draw_idle()
    except Exception as e:
        print(f"Error in draw_main_plot: {e}")
        # Try to recover by redrawing
        try:
            main_ax.clear()
            main_ax.text(
                0.5,
                0.5,
                f"Error displaying plot: {e}",
                ha="center",
                va="center",
                transform=main_ax.transAxes,
                fontsize=10,
                color="red",
            )
            fig.canvas.draw_idle()
        except:
            pass


def onclick_main(event):
    if event.button != 1:  # Only handle left clicks
        return

    # Inline website link handling removed - simplified to single link approach

    # Handle help link clicks
    if (
        "help_text_box" in globals()
        and help_text_box
        and hasattr(help_text_box, "all_links")
    ):
        for link_type, shortcut, link_text in help_text_box.all_links:
            if event.inaxes == link_text.axes:
                # Check if click is within the link text bounds
                bbox = link_text.get_bbox_patch()
                if bbox and bbox.contains(event.x, event.y):
                    print(f"🔍 Help link clicked: {link_type} - {shortcut}")
                    handle_help_link_click(link_type, shortcut)
                    return

    # Handle thumbnail clicks
    for i, ax in enumerate(thumb_axes):
        if event.inaxes == ax:
            current_image_idx[0] = i
            draw_main_plot(i)
            update_thumbnail_visibility()
            return

    # Handle main plot clicks for annotations
    if event.inaxes != main_ax:
        print(f"🔍 Click outside main plot. Clicked on: {event.inaxes}")
        print(f"🔍 Website button ax: {btn_website.ax if btn_website else 'None'}")

        # Check if it's a website button click first (only if button exists)
        if (
            btn_website
            and hasattr(btn_website, "ax")
            and event.inaxes == btn_website.ax
        ):
            print("🔍 Website button clicked via onclick_main")
            on_website_button_click()
            return

        # Hide help page if clicking outside main plot
        hide_help_page()
        return

    idx = current_image_idx[0]
    img_id = image_ids[idx]
    df_selected = df[df["image_id"] == img_id].copy()
    state = annotation_states[img_id]
    x, y = event.xdata, event.ydata

    if df_selected.empty or df_selected["x_min"].isna().all():
        return

    label_text = None
    annotation_entry = {"image_id": img_id, "x": x, "y": y}
    mark_value = ""

    clicked_bb_index = None
    for idx_row, row in df_selected.iterrows():
        if row["x_min"] <= x <= row["x_max"] and row["y_min"] <= y <= row["y_max"]:
            clicked_bb_index = row.name
            break

    if clicked_bb_index is not None:
        row = df.loc[clicked_bb_index]

        # Check if this bounding box already has a mark in the CSV
        existing_mark = str(row.get("marked", "")).strip()
        if (
            existing_mark
            and existing_mark.lower() != "nan"
            and existing_mark.lower() != ""
        ):
            print(
                f"⚠ Bounding box already marked as '{existing_mark}' - cannot add new annotation"
            )
            return

        # Proceed with new annotation only if no existing mark
        if state.mode == "number":
            mark_value = str(state.counter)
            df.loc[row.name, "marked"] = mark_value
            annotation_entry["mark_value"] = mark_value
            state.counter += 1
            print(f"Added number annotation: {mark_value} at ({x:.1f}, {y:.1f})")
        else:
            mark_value = "x"
            df.loc[row.name, "marked"] = "yes"
            annotation_entry["mark_value"] = mark_value
            print(f"Added X annotation at ({x:.1f}, {y:.1f})")

        for label_col in label_columns:
            annotation_entry[label_col] = row[label_col]

        state.annotations.append(annotation_entry)

        draw_main_plot(current_image_idx[0])
        state.undone.clear()


def on_motion_main(event):
    if not labels_enabled[0]:
        print(f"⚠ Labels disabled (labels_enabled[0] = {labels_enabled[0]})")
        idx = current_image_idx[0]
        img_id = image_ids[idx]
        state = annotation_states[img_id]
        if state.hover_text:
            try:
                state.hover_text.set_visible(False)
                fig.canvas.draw_idle()
            except (NotImplementedError, ValueError):
                pass
        return

    # Debug: Print current state
    print(f"🔍 Labels enabled: {labels_enabled[0]}, Label columns: {label_columns}")

    idx = current_image_idx[0]
    img_id = image_ids[idx]
    state = annotation_states[img_id]
    df_selected = df[df["image_id"] == img_id].copy()

    if event.inaxes != main_ax:
        if state.hover_text:
            try:
                state.hover_text.set_visible(False)
                fig.canvas.draw_idle()
            except (NotImplementedError, ValueError):
                pass
        return

    show_label = False
    x, y = event.xdata, event.ydata

    for idx_row, row in df_selected.iterrows():
        if row["x_min"] <= x <= row["x_max"] and row["y_min"] <= y <= row["y_max"]:
            print(f"🔍 Found bounding box at ({x:.1f}, {y:.1f})")
            label_lines = []
            for label_col in label_columns:
                if (
                    label_col in row
                    and str(row[label_col]).strip()
                    and str(row[label_col]).lower() != "nan"
                ):
                    display_name = label_col.replace("label_", "")
                    label_lines.append(f"{display_name}: {row[label_col]}")
                    print(f"  ✓ Found label: {label_col} = {row[label_col]}")
                else:
                    print(f"  ⚠ No label in {label_col}: {row.get(label_col, 'N/A')}")

            # Only show hover text if there are actual labels
            if label_lines:
                print(f"  🎯 Creating hover text with {len(label_lines)} labels")
                hover_text = "\n".join(label_lines)

                # Adjust position to ensure hover text is visible and not cut off by controls
                # Move text slightly to the left to avoid overlapping with right-side controls
                adjusted_x = x - 50  # Move left by 50 pixels
                adjusted_y = y + 20  # Move up by 20 pixels

                # Debug: Check plot limits and positioning
                xlim = main_ax.get_xlim()
                ylim = main_ax.get_ylim()
                print(
                    f"  📏 Plot limits: X({xlim[0]:.1f}, {xlim[1]:.1f}), Y({ylim[0]:.1f}, {ylim[1]:.1f})"
                )
                print(f"  📍 Text position: ({adjusted_x:.1f}, {adjusted_y:.1f})")
                print(f"  🎯 Mouse position: ({x:.1f}, {y:.1f})")

                if state.hover_text is None:
                    try:
                        print(
                            f"  🎨 Creating new hover text at ({adjusted_x:.1f}, {adjusted_y:.1f})"
                        )
                        # Restore original label format with white box and blue text
                        state.hover_text = main_ax.text(
                            adjusted_x,
                            adjusted_y,
                            hover_text,
                            color="blue",
                            fontsize=10,
                            va="bottom",
                            ha="left",
                            bbox=dict(
                                facecolor="white",
                                alpha=0.98,
                                edgecolor="black",
                                boxstyle="round,pad=0.5",
                            ),
                            zorder=10000,
                        )  # Extremely high z-order to appear above everything
                        print(f"  ✅ Hover text created: {state.hover_text}")
                        print(
                            f"  🔍 Text properties: visible={state.hover_text.get_visible()}, alpha={state.hover_text.get_alpha()}"
                        )
                    except (NotImplementedError, ValueError) as e:
                        print(f"  ❌ Error creating hover text: {e}")
                        pass
                else:
                    try:
                        print(
                            f"  🔄 Updating existing hover text at ({adjusted_x:.1f}, {adjusted_y:.1f})"
                        )
                        state.hover_text.set_position((adjusted_x, adjusted_y))
                        state.hover_text.set_text(hover_text)
                        state.hover_text.set_visible(True)
                        # Ensure the text maintains high z-order and proper styling
                        state.hover_text.set_zorder(10000)
                        print(f"  ✅ Hover text updated: {state.hover_text}")
                        print(
                            f"  🔍 Text properties: visible={state.hover_text.get_visible()}, alpha={state.hover_text.get_alpha()}"
                        )
                    except (NotImplementedError, ValueError) as e:
                        print(f"  ❌ Error updating hover text: {e}")
                        pass
                print(f"  🎭 Calling fig.canvas.draw()")
                fig.canvas.draw()  # Force full redraw instead of just draw_idle()
                show_label = True
                break

            # If no labels, don't show any hover text
            else:
                if state.hover_text:
                    try:
                        state.hover_text.set_visible(False)
                        fig.canvas.draw_idle()
                    except (NotImplementedError, ValueError):
                        pass
                show_label = False
                break

    # If no labels were found in any bounding box, hide hover text
    if not show_label and state.hover_text:
        try:
            state.hover_text.set_visible(False)
            fig.canvas.draw_idle()
        except (NotImplementedError, ValueError):
            pass


def on_mode(label):
    """Apply the selected mode (x or number) to all plots in the session"""
    print(f"🎯 Setting annotation mode to '{label}' for all plots in this session")

    # Apply mode to all annotation states
    for img_id, state in annotation_states.items():
        state.mode = label

    # Update the current plot display
    draw_main_plot(current_image_idx[0])

    print(f"✓ Mode '{label}' applied to all {len(annotation_states)} plots")


def on_reset(event):
    """Reset the counter for all plots in the session"""
    print("🔄 Resetting annotation counter for all plots in this session")

    # Reset counter for all annotation states
    for img_id, state in annotation_states.items():
        state.counter = 1

    # Update the current plot display
    draw_main_plot(current_image_idx[0])

    print(f"✓ Counter reset to 1 for all {len(annotation_states)} plots")


def on_undo(event):
    idx = current_image_idx[0]
    img_id = image_ids[idx]
    state = annotation_states[img_id]
    if state.annotations:
        ann = state.annotations.pop()
        state.undone.append(ann)

        # Update the DataFrame to reflect the undone annotation
        # Find the bounding box that was annotated and clear its 'marked' value
        if "mark_value" in ann:
            # For number annotations, we need to find the row with that mark value
            if str(ann["mark_value"]).isdigit():
                # Find rows with this mark value and clear them
                mask = (df["image_id"] == img_id) & (df["marked"] == ann["mark_value"])
                df.loc[mask, "marked"] = ""
            else:
                # For 'x' annotations, find rows marked as 'yes' and clear them
                mask = (df["image_id"] == img_id) & (df["marked"] == "yes")
                df.loc[mask, "marked"] = ""

        draw_main_plot(current_image_idx[0])


def on_redo(event):
    idx = current_image_idx[0]
    img_id = image_ids[idx]
    state = annotation_states[img_id]
    if state.undone:
        ann = state.undone.pop()
        state.annotations.append(ann)

        # Update the DataFrame to reflect the redone annotation
        if "mark_value" in ann:
            # Find the bounding box coordinates and update the 'marked' column
            x, y = ann["x"], ann["y"]
            # Find the row that contains these coordinates
            df_selected = df[df["image_id"] == img_id]
            for idx_row, row in df_selected.iterrows():
                if (
                    row["x_min"] <= x <= row["x_max"]
                    and row["y_min"] <= y <= row["y_max"]
                ):
                    if str(ann["mark_value"]).isdigit():
                        df.loc[idx_row, "marked"] = ann["mark_value"]
                    else:
                        df.loc[idx_row, "marked"] = "yes"
                    break

        draw_main_plot(current_image_idx[0])


def on_clear(event):
    idx = current_image_idx[0]
    img_id = image_ids[idx]
    state = annotation_states[img_id]
    state.reset()
    df.loc[df["image_id"] == img_id, "marked"] = ""
    draw_main_plot(current_image_idx[0])


def on_toggle_labels(event):
    labels_enabled[0] = not labels_enabled[0]
    if labels_enabled[0]:
        btn_toggle_labels.label.set_text("Disable Labels")
    else:
        btn_toggle_labels.label.set_text("Enable Labels")
        idx = current_image_idx[0]
        img_id = image_ids[idx]
        state = annotation_states[img_id]
        if state.hover_text:
            try:
                state.hover_text.set_visible(False)
                fig.canvas.draw_idle()
            except (NotImplementedError, ValueError):
                pass
    fig.canvas.draw_idle()


def on_open_image(event):
    """Open current image in browser"""
    idx = current_image_idx[0]
    img_id = image_ids[idx]
    state = annotation_states[img_id]
    if state.image_url:
        open_image_in_browser(state.image_url)
    else:
        messagebox.showinfo("Info", "No image URL available for this plot.")


def on_toggle_background(event):
    """Toggle background image display"""
    show_background_image[0] = not show_background_image[0]
    if show_background_image[0]:
        if "btn_show_bg" in globals() and btn_show_bg:
            btn_show_bg.label.set_text("Hide Background Image")
    else:
        if "btn_show_bg" in globals() and btn_show_bg:
            btn_show_bg.label.set_text("Show Background Image")
    # Redraw the current plot to show/hide background
    draw_main_plot(current_image_idx[0])


def on_flip_y(event):
    """Flip the Y-axis of the current plot."""
    y_axis_flipped[0] = not y_axis_flipped[0]
    if y_axis_flipped[0]:
        btn_flip_y.label.set_text("Unflip Y-Axis")
    else:
        btn_flip_y.label.set_text("Flip Y-Axis")

    # Regenerate thumbnails with new Y-axis orientation
    global thumbnails
    thumbnails = []
    for img_id in image_ids:
        df_sel = df[df["image_id"] == img_id]
        thumbnails.append(generate_thumbnail(df_sel))

    # Update thumbnail display and redraw main plot
    update_thumbnail_visibility()
    draw_main_plot(current_image_idx[0])


# Thumbnail click handling is now integrated into onclick_main

# Remove the on_slider_change function since we no longer have a slider


def save_annotations(event=None, loading_screen=None):
    """Save annotations and updated input data to CSV files"""
    try:
        annotations = []
        for img_id in image_ids:
            state = annotation_states[img_id]
            annotations.extend(state.annotations)

        # Always save the input file with marked column (even if no annotations)
        marked_input_path = os.path.join(output_dir, "marked_skus.csv")
        df.to_csv(marked_input_path, index=False)
        print(f"✓ Input file saved to: {marked_input_path}")
        print(f"  - {len(df)} total rows")

        # Count marked rows
        marked_rows = df[df["marked"].notna() & (df["marked"] != "")]
        print(f"  - {len(marked_rows)} marked rows")

        if annotations:
            # Create annotations DataFrame with all relevant information
            annotations_df = pd.DataFrame(annotations)

            # Save annotations file
            annotations_path = os.path.join(output_dir, "annotations_marked.csv")
            annotations_df.to_csv(annotations_path, index=False)

            print(f"✓ Annotations saved to: {annotations_path}")
            print(f"  - {len(annotations)} annotation entries")

            # Show summary of what was saved
            marked_counts = marked_rows["marked"].value_counts()
            if not marked_counts.empty:
                print("  Marking summary:")
                for mark, count in marked_counts.items():
                    print(f"    - '{mark}': {count} items")
        else:
            print("ℹ No annotations were made to save.")
            print(f"✓ Input file saved to: {marked_input_path} (no annotations)")

    except Exception as e:
        print(f"✗ Error saving annotations: {e}")
        # Try to save just the input file as a fallback
        try:
            marked_input_path = os.path.join(output_dir, "marked_skus.csv")
            df.to_csv(marked_input_path, index=False)
            print(f"✓ Input file saved as fallback to: {marked_input_path}")

        except Exception as e2:
            print(f"✗ Critical error: Could not save any data: {e2}")
            print(f"  Output directory: {output_dir}")
            print(f"  Current working directory: {os.getcwd()}")


def save_all_annotated_plots(loading_screen=None):
    total_images = len(image_ids)

    for i, img_id in enumerate(image_ids):
        # Update progress
        if loading_screen:
            loading_screen.update_progress(
                i + 1,
                total_images,
                f"Saving plot {i+1} of {total_images} (Image ID: {img_id})",
            )

        df_selected = df[df["image_id"] == img_id].copy()
        fig, ax = plt.subplots(figsize=(6, 6))

        if not df_selected.empty and not df_selected["x_min"].isna().all():
            df_selected["width"] = df_selected["x_max"] - df_selected["x_min"]
            df_selected["height"] = df_selected["y_max"] - df_selected["y_min"]
            for _, row in df_selected.iterrows():
                rect = patches.Rectangle(
                    (row["x_min"], row["y_min"]),
                    row["width"],
                    row["height"],
                    linewidth=1,
                    edgecolor="r",
                    facecolor="none",
                    zorder=1,  # Low z-order so markers appear on top
                )
                ax.add_patch(rect)

            x_min_all = df_selected["x_min"].min()
            x_max_all = df_selected["x_max"].max()
            y_min_all = df_selected["y_min"].min()
            y_max_all = df_selected["y_max"].max()
            ax.set_xlim(x_min_all - 10, x_max_all + 10)

            # Apply Y-axis flip if enabled
            if y_axis_flipped[0]:
                ax.set_ylim(y_max_all + 10, y_min_all - 10)
            else:
                ax.set_ylim(y_min_all - 10, y_max_all + 10)
        else:
            ax.text(
                0.5,
                0.5,
                "No bounding box data available",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=12,
            )
            ax.set_xticks([])
            ax.set_yticks([])

        state = annotation_states[img_id]
        for ann in state.annotations:
            x, y = ann["x"], ann["y"]
            mark_value = ann.get("mark_value", "")
            if state.mode == "number" and str(mark_value).isdigit():
                ax.plot(
                    x, y, marker=f"${mark_value}$", color="red", markersize=10, mew=2
                )
            else:
                ax.plot(x, y, marker="x", color="blue", markersize=10, mew=2)

        # Add existing marks from CSV 'marked' column to saved plots
        if "marked" in df.columns:
            for _, row in df_selected.iterrows():
                marked_value = str(row.get("marked", "")).strip()
                if (
                    marked_value
                    and marked_value.lower() != "nan"
                    and marked_value.lower() != ""
                ):
                    x, y = (row["x_min"] + row["x_max"]) / 2, (
                        row["y_min"] + row["y_max"]
                    ) / 2

                    # Convert "yes" to "x" for display
                    if marked_value.lower() == "yes":
                        display_value = "x"
                        marker_color = (
                            "green"  # Different color for existing "yes" marks
                        )
                        marker_size = 10
                        # Display as X marker with high z-order
                        ax.plot(
                            x,
                            y,
                            marker="x",
                            color=marker_color,
                            markersize=marker_size,
                            mew=2,
                            zorder=10,
                        )
                    else:
                        display_value = marked_value
                        marker_color = (
                            "purple"  # Different color for other existing marks
                        )
                        # Display as text (no X marker) with high z-order
                        ax.text(
                            x,
                            y,
                            display_value,
                            color=marker_color,
                            fontsize=10,
                            ha="center",
                            va="center",
                            weight="light",
                            zorder=10,
                        )

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"Bounding Boxes for image_id: {img_id}")
        out_path = os.path.join(output_dir, f"annotated_{img_id}.png")
        plt.savefig(out_path)
        plt.close(fig)

    # Final progress update
    if loading_screen:
        loading_screen.update_progress(
            total_images,
            total_images,
            f"All plots saved successfully! ({total_images} images)",
        )

    print(f"All annotated plots saved to {output_dir}")


# Global flags to prevent duplicate popups and close operations
_save_popup_showing = False
_close_operation_in_progress = False


# Loading screen class
class LoadingScreen:
    def __init__(self, parent):
        self.parent = parent
        self.loading_window = None
        self.progress_var = None
        self.message_var = None
        self.progress_bar = None

    def show(self, title="Saving...", message="Please wait"):
        """Show the loading screen"""
        if self.loading_window and self.loading_window.winfo_exists():
            return

        self.loading_window = tk.Toplevel(self.parent)
        self.loading_window.title(title)
        self.loading_window.geometry("500x300")
        self.loading_window.resizable(False, False)
        self.loading_window.configure(bg="#1a1a1a")

        # Center the window
        self.loading_window.transient(self.parent)
        self.loading_window.grab_set()

        # Make it modal
        self.loading_window.focus_set()

        # Main frame
        main_frame = tk.Frame(self.loading_window, bg="#1a1a1a")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Title
        title_label = tk.Label(
            main_frame,
            text=title,
            font=tkFont.Font(family="Helvetica", size=20, weight="bold"),
            bg="#1a1a1a",
            fg="#00ff88",
        )
        title_label.pack(pady=(0, 20))

        # Message
        self.message_var = tk.StringVar(value=message)
        message_label = tk.Label(
            main_frame,
            textvariable=self.message_var,
            font=tkFont.Font(family="Helvetica", size=14),
            bg="#1a1a1a",
            fg="#cccccc",
            wraplength=400,
            justify="center",
        )
        message_label.pack(pady=(0, 30))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode="determinate",
        )
        self.progress_bar.pack(pady=(0, 15))

        # Progress text
        self.progress_text_var = tk.StringVar(value="0%")
        progress_text = tk.Label(
            main_frame,
            textvariable=self.progress_text_var,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#1a1a1a",
            fg="#00ff88",
        )
        progress_text.pack()

        # Update the display
        self.loading_window.update()

    def update_progress(self, current, total, message=None):
        """Update progress bar and message"""
        if not self.loading_window or not self.loading_window.winfo_exists():
            return

        percentage = (current / total) * 100 if total > 0 else 0
        self.progress_var.set(percentage)

        # Format progress text as "Saving plot X of Y"
        progress_text = f"Saving plot {current} of {total}"
        self.progress_text_var.set(progress_text)

        if message:
            self.message_var.set(message)

        self.loading_window.update()

    def hide(self):
        """Hide the loading screen"""
        if self.loading_window and self.loading_window.winfo_exists():
            self.loading_window.destroy()
        self.loading_window = None


def show_save_confirmation():
    """Show a custom popup asking user if they want to save plots"""
    global _save_popup_showing

    # Prevent duplicate popups
    if _save_popup_showing:
        return "cancel"

    _save_popup_showing = True

    try:
        # Create custom popup window
        popup = tk.Toplevel()
        popup.title("Unified Plotter - Save Options")
        popup.configure(bg="#1a1a1a")
        popup.resizable(False, False)

        # Center the popup
        popup_width = 600
        popup_height = 450
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        center_x = int(screen_width / 2 - popup_width / 2)
        center_y = int(screen_height / 2 - popup_height / 2)
        popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")

        # Make it modal
        popup.transient()
        popup.grab_set()

        # Create main container
        main_frame = tk.Frame(popup, bg="#1a1a1a", padx=40, pady=30)
        main_frame.pack(expand=True, fill="both")

        # Logo section
        logo_frame = tk.Frame(main_frame, bg="#1a1a1a")
        logo_frame.pack(pady=(0, 25))

        # Logo with gradient effect (simulated with text)
        logo_text = tk.Label(
            logo_frame,
            text="Unified Plotter",
            font=tkFont.Font(family="Helvetica", size=24, weight="bold"),
            bg="#1a1a1a",
            fg="#ffffff",
        )
        logo_text.pack()

        subtitle_text = tk.Label(
            logo_frame,
            text="Professional Bounding Box Visualization",
            font=tkFont.Font(family="Helvetica", size=11),
            bg="#1a1a1a",
            fg="#888888",
        )
        subtitle_text.pack(pady=(5, 0))

        # Question section
        question_frame = tk.Frame(main_frame, bg="#1a1a1a")
        question_frame.pack(fill="x", pady=(0, 25))

        question_text = tk.Label(
            question_frame,
            text="💾 Save Options Before Closing?",
            font=tkFont.Font(family="Helvetica", size=18, weight="bold"),
            bg="#1a1a1a",
            fg="#00ff88",
        )
        question_text.pack()

        # Description
        desc_text = tk.Label(
            question_frame,
            text="Choose how you want to save your work before closing the application:",
            font=tkFont.Font(family="Helvetica", size=12),
            bg="#1a1a1a",
            fg="#cccccc",
            justify=tk.CENTER,
        )
        desc_text.pack(pady=(15, 0))

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#1a1a1a")
        button_frame.pack(fill="x", pady=(25, 0))

        result = [None]  # Use list to store result from callbacks

        def on_yes():
            global _save_popup_showing
            result[0] = "save_all"
            _save_popup_showing = False
            popup.destroy()

        def on_no():
            global _save_popup_showing
            result[0] = "save_annotations_only"
            _save_popup_showing = False
            popup.destroy()

        def on_cancel():
            global _save_popup_showing
            result[0] = "cancel"
            _save_popup_showing = False
            popup.destroy()

        # Yes button - Save all plots and files
        yes_button = tk.Button(
            button_frame,
            text="💾 Yes - save all plots and files",
            command=on_yes,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#00ff88",
            fg="#1a1a1a",
            activebackground="#00cc6a",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        yes_button.pack(fill="x", pady=(0, 10))

        # No button - Save files only if annotations exist
        no_button = tk.Button(
            button_frame,
            text="📄 No - save files only",
            command=on_no,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#ffaa00",
            fg="#1a1a1a",
            activebackground="#cc8800",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        no_button.pack(fill="x", pady=(0, 10))

        # Cancel button - Return to plot screen
        cancel_button = tk.Button(
            button_frame,
            text="↩️ Cancel",
            command=on_cancel,
            font=tkFont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#666666",
            fg="#1a1a1a",
            activebackground="#555555",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        cancel_button.pack(fill="x")

        # Handle window close (X button)
        def on_window_close():
            global _save_popup_showing
            _save_popup_showing = False
            on_cancel()

        popup.protocol("WM_DELETE_WINDOW", on_window_close)

        # Center the popup and wait for user response
        popup.update_idletasks()
        popup.lift()
        popup.focus_force()
        popup.wait_window()

        return result[0]

    except Exception as e:
        logger.error(f"Error showing save confirmation: {e}")
        print(f"Error showing save confirmation: {e}")
        _save_popup_showing = False
        # Default to saving all plots if dialog fails
        return "save_all"


def on_close(event=None):
    """Handle system close events (X button, etc.)"""
    global _close_operation_in_progress

    logger.info("System close event detected...")
    print("System close event detected...")

    # If a close operation is already in progress, ignore this event
    if _close_operation_in_progress:
        print("Close operation already in progress, ignoring duplicate event")
        return

    # Set flag to prevent duplicate close operations
    _close_operation_in_progress = True

    # Show save confirmation popup first
    save_option = show_save_confirmation()

    # Handle cancel case - don't close the plot
    if save_option == "cancel":
        logger.info("User cancelled close operation")
        print("User cancelled close operation")
        _close_operation_in_progress = False
        return

    # Handle save options
    if save_option in ["yes", "no"]:
        try:
            # Create output directory in the same location as input file
            if hasattr(return_to_welcome, "file_path") and return_to_welcome.file_path:
                file_path = return_to_welcome.file_path
            else:
                # Fallback to current directory
                file_path = "current_session"

            # Extract directory from file path
            if os.path.isfile(file_path):
                output_dir = os.path.dirname(file_path)
            else:
                output_dir = os.getcwd()

            # Create timestamped folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plots_folder = os.path.join(output_dir, f"plots_{timestamp}")
            os.makedirs(plots_folder, exist_ok=True)

            print(f"✓ Output folder created: {plots_folder}")

            # Save files if requested
            if save_option in ["yes", "no"]:
                try:
                    # Save CSV with annotations
                    csv_path = os.path.join(plots_folder, "annotations.csv")
                    df_to_save = df.copy()

                    # Add annotation columns if they don't exist
                    if "annotation" not in df_to_save.columns:
                        df_to_save["annotation"] = ""
                    if "confidence" not in df_to_save.columns:
                        df_to_save["confidence"] = 0.0

                    # Update with current annotations
                    for i, row in df_to_save.iterrows():
                        if i < len(annotations):
                            df_to_save.at[i, "annotation"] = annotations[i]
                            df_to_save.at[i, "confidence"] = confidences[i]

                    df_to_save.to_csv(csv_path, index=False)
                    print(f"✓ Annotations saved to: {csv_path}")

                except Exception as e:
                    print(f"✗ Error saving annotations: {e}")

            # Save plots if requested
            if save_option == "yes":
                try:
                    save_all_annotated_plots(plots_folder)
                    print(f"✓ Plots saved to: {plots_folder}")
                except Exception as e:
                    print(f"✗ Error saving plots: {e}")

            print(f"✓ All files saved to: {plots_folder}")

        except Exception as e:
            print(f"✗ Error during save operation: {e}")

    # Close matplotlib window and return to welcome
    try:
        plt.close("all")
        print("✓ Matplotlib window closed")
    except:
        pass

    # Clear the close operation flag
    _close_operation_in_progress = False

    # Return to welcome screen
    try:
        # Check if we have the required functions available
        if "select_file_and_close" in globals() and "show_settings_page" in globals():
            screen_manager.show_welcome_screen(
                select_file_and_close, show_settings_page
            )
            print("✓ Returned to welcome screen")
        else:
            # Fallback: just close the application
            print("ℹ Functions not available, closing application")
            screen_manager.destroy()
    except Exception as e:
        print(f"✗ Error returning to welcome screen: {e}")
        # Fallback: just close the application
        try:
            screen_manager.destroy()
        except:
            pass


def create_plotting_interface():
    """Create the main plotting interface (legacy function for compatibility)"""
    global thumbnails, thumb_axes, current_image_idx

    # Generate thumbnails for each image
    thumbnails = []
    print("Creating thumbnails...")

    # Apply progressive loading if enabled
    if global_settings.get("progressive_loading", False):
        print("ℹ Progressive thumbnail loading enabled for low-end devices")
        # Create placeholder thumbnails first
        for i, img_id in enumerate(image_ids):
            try:
                # Create a simple placeholder thumbnail
                fig, ax = plt.subplots(figsize=(2, 2))
                ax.axis("off")
                ax.text(
                    0.5, 0.5, f"Loading\n{img_id}", ha="center", va="center", fontsize=8
                )
                fig.canvas.draw()
                thumb = np.array(fig.canvas.renderer.buffer_rgba())
                plt.close(fig)
                thumbnails.append(thumb)
            except Exception as e:
                print(f"✗ Error creating placeholder thumbnail for {img_id}: {e}")
                thumbnails.append(np.zeros((200, 200, 4), dtype=np.uint8))

        # Create the main plotting interface
        create_main_plot_interface()

        # Load thumbnails progressively in background
        def load_thumbnail_progressive(img_id, index):
            try:
                df_selected = df[df["image_id"] == img_id].copy()
                if not df_selected.empty:
                    thumb = generate_thumbnail(df_selected)
                    if thumb is not None and index < len(thumbnails):
                        thumbnails[index] = thumb
                        # Update the thumbnail display
                        if thumb_axes and index < len(thumb_axes):
                            thumb_axes[index].imshow(thumb)
                            thumb_axes[index].figure.canvas.draw()
            except Exception as e:
                print(f"✗ Error loading thumbnail for {img_id}: {e}")

        # Start progressive loading
        for i, img_id in enumerate(image_ids):
            if i < len(thumbnails):
                load_thumbnail_progressive(img_id, i)
                if (i + 1) % 10 == 0:
                    print(f"  Loaded {i + 1}/{len(image_ids)} thumbnails")
    else:
        # Standard thumbnail generation
        for i, img_id in enumerate(image_ids):
            try:
                df_selected = df[df["image_id"] == img_id].copy()
                if not df_selected.empty:
                    thumb = generate_thumbnail(df_selected)
                    if thumb is not None:
                        thumbnails.append(thumb)
                    else:
                        # Create a blank thumbnail as fallback
                        fig, ax = plt.subplots(figsize=(2, 2))
                        ax.axis("off")
                        fig.canvas.draw()
                        blank_thumb = np.array(fig.canvas.renderer.buffer_rgba())
                        plt.close(fig)
                        thumbnails.append(blank_thumb)
                else:
                    # Create a blank thumbnail as fallback
                    fig, ax = plt.subplots(figsize=(2, 2))
                    ax.axis("off")
                    fig.canvas.draw()
                    blank_thumb = np.array(fig.canvas.renderer.buffer_rgba())
                    plt.close(fig)
                    thumbnails.append(blank_thumb)

                if (i + 1) % 10 == 0:
                    print(f"  Created {i + 1}/{len(image_ids)} thumbnails")

            except Exception as e:
                print(f"✗ Error creating thumbnail for {img_id}: {e}")
                # Create a blank thumbnail as fallback
                try:
                    fig, ax = plt.subplots(figsize=(2, 2))
                    ax.axis("off")
                    fig.canvas.draw()
                    blank_thumb = np.array(fig.canvas.renderer.buffer_rgba())
                    plt.close(fig)
                    thumbnails.append(blank_thumb)
                except:
                    # Last resort: create a simple array
                    thumbnails.append(np.zeros((200, 200, 4), dtype=np.uint8))
        print(f"✓ Created {len(thumbnails)} thumbnails")

    # Create the main plotting interface
    create_main_plot_interface()


# Memory management based on settings
def manage_memory():
    """Manage memory based on performance settings"""
    if global_settings.get("aggressive_cleanup", False):
        # Clear loaded images if aggressive cleanup is enabled
        loaded_images.clear()
        print("ℹ Aggressive memory cleanup applied")

    if global_settings.get("image_caching", True):
        # Keep images in memory for better performance
        print("ℹ Image caching enabled for better performance")
    else:
        # Clear images to save memory
        loaded_images.clear()
        print("ℹ Image caching disabled to save memory")


# Apply memory management
manage_memory()


# --- NEW: Main Program Loop ---
def main_program_loop():
    """Main program loop that allows returning to welcome screen"""
    logger.info("Starting main program loop")

    # Clean up old logs at startup
    cleanup_old_logs()

    while True:
        try:
            # Show welcome screen and get file path
            logger.info("Showing welcome screen...")
            file_path = show_welcome_screen_and_get_filepath()

            if not file_path:
                logger.info("No file selected. Exiting program.")
                print("No file selected. Exiting program.")
                break

            # Process the selected file
            logger.info(f"Processing file: {file_path}")
            process_csv_file(file_path)

            # After processing, ask if user wants to continue
            logger.info("File processing completed, returning to welcome screen")
            print("\n" + "=" * 50)
            print("File processing completed!")
            print("=" * 50)

        except KeyboardInterrupt:
            logger.info("Program interrupted by user. Exiting...")
            print("\n\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
            print(f"\n\nUnexpected error: {e}")
            print("Returning to welcome screen...")
            continue


def show_processing_progress(message, progress=0, total=100):
    """Show processing progress dialog using unified screen manager"""
    screen_manager.create_unified_window(
        "Unified Plotter | Processing Data", show_title_bar=True
    )
    screen_manager.show_progress_screen(message, progress, total)
    return (
        screen_manager,
        screen_manager.status_text,
        screen_manager.progress_text,
        screen_manager.progress_bar,
    )


def validate_csv_columns(df, file_path):
    """Validate that CSV has required columns and show user-friendly error if not"""
    required_columns = ["image_id", "x_min", "x_max", "y_min", "y_max"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        # Create error message
        error_message = f"""The selected CSV file is missing required columns for bounding box visualization.

Missing columns: {', '.join(missing_columns)}

Required columns:
• image_id - Unique identifier for each image
• x_min - Left boundary of bounding box
• x_max - Right boundary of bounding box
• y_min - Top boundary of bounding box
• y_max - Bottom boundary of bounding box

Please ensure your CSV file contains these columns and try again.

File: {os.path.basename(file_path)}"""

        # Show error using unified screen manager
        def go_home():
            screen_manager.destroy()
            # Return to welcome screen
            file_path = show_welcome_screen_and_get_filepath()
            if file_path:
                process_csv_file(file_path)

        screen_manager.create_unified_window(
            "Unified Plotter | Invalid CSV File", show_title_bar=True
        )
        screen_manager.show_error_screen(
            "Invalid CSV File", error_message, "Home", go_home
        )
        screen_manager.run()
        return False

    return True


def process_csv_file(file_path):
    """Process a single CSV file - this contains the main plotting logic"""
    global df, output_dir, image_ids, annotation_states, thumbnails, thumb_axes, current_image_idx, label_columns, image_url_columns

    logger.info(f"Starting CSV processing: {file_path}")

    # Set output directory to input file's directory (will be created later when saving)
    output_dir = os.path.dirname(file_path)
    logger.info(f"Input file directory: {output_dir}")
    print(f"✓ Input file directory: {output_dir}")

    # Show initial progress
    progress_manager, status_label, progress_text, progress_bar = (
        show_processing_progress("Loading CSV file...", 0, 100)
    )

    try:
        # Load your data
        logger.info("Loading CSV data...")
        df = pd.read_csv(file_path)
        logger.info(
            f"CSV loaded successfully: {len(df)} rows, {len(df.columns)} columns"
        )

        # Update progress
        progress_manager.update_progress("Validating CSV structure...", 20, 100)

        # Validate CSV columns
        if not validate_csv_columns(df, file_path):
            progress_manager.destroy()
            return False

        # Update progress
        progress_manager.update_progress("Processing data columns...", 40, 100)

    except Exception as e:
        progress_manager.destroy()
        # Show error dialog for CSV loading issues
        error_message = f"""Could not load the CSV file. Please check that:

• The file exists and is accessible
• The file is a valid CSV format
• You have permission to read the file
• The file is not corrupted

Error details: {str(e)}

File: {os.path.basename(file_path)}"""

        # Show error using unified screen manager
        def go_home():
            screen_manager.destroy()
            # Return to welcome screen
            file_path = show_welcome_screen_and_get_filepath()
            if file_path:
                process_csv_file(file_path)

        screen_manager.create_unified_window(
            "Unified Plotter | Error Loading CSV", show_title_bar=True
        )
        screen_manager.show_error_screen(
            "Error Loading CSV", error_message, "Home", go_home
        )
        screen_manager.run()
        return False

    # Ensure bounding box columns are numeric, coerce errors to NaN
    df["x_min"] = pd.to_numeric(df["x_min"], errors="coerce")
    df["x_max"] = pd.to_numeric(df["x_max"], errors="coerce")
    df["y_min"] = pd.to_numeric(df["y_min"], errors="coerce")
    df["y_max"] = pd.to_numeric(df["y_max"], errors="coerce")

    # Output directory will be created when saving plots

    # Add a 'marked' column to the DataFrame, default to empty string
    if "marked" not in df.columns:
        df["marked"] = ""

        # Update progress
        progress_manager.update_progress("Analyzing data structure...", 60, 100)

    # Find all label columns
    label_columns = [col for col in df.columns if col.startswith("label_")]
    logger.info(f"Detected label columns: {label_columns}")
    print(f"✓ Detected label columns: {label_columns}")
    print(f"✓ Total columns in CSV: {list(df.columns)}")

    # Detect image URL columns
    image_url_columns = []
    for col in df.columns:
        if any(
            keyword in col.lower() for keyword in ["url", "link", "image", "img", "src"]
        ):
            # Check if the column contains URLs
            sample_values = df[col].dropna().head(10)
            if len(sample_values) > 0:
                # Check if at least some values look like URLs
                url_count = sum(
                    1
                    for val in sample_values
                    if str(val).startswith(("http://", "https://", "www."))
                )
                if url_count > 0:
                    image_url_columns.append(col)

    logger.info(f"Detected image URL columns: {image_url_columns}")
    print(f"Detected potential image URL columns: {image_url_columns}")

    # Store loaded images
    loaded_images = {}

    # Apply settings from welcome screen
    apply_global_settings()

    # Prepare per-image annotation state
    df["image_id"] = df["image_id"].astype(str)
    image_ids = list(df["image_id"].unique())
    annotation_states = {img_id: AnnotationState() for img_id in image_ids}
    logger.info(f"Created annotation states for {len(image_ids)} unique images")

    # Update progress
    progress_manager.update_progress("Preparing image data...", 70, 100)

    # Store image URLs for each image_id
    for img_id in image_ids:
        df_sel = df[df["image_id"] == img_id]
        if not df_sel.empty and image_url_columns:
            # Get the first non-null URL from any image URL column
            for url_col in image_url_columns:
                url = (
                    df_sel[url_col].dropna().iloc[0]
                    if not df_sel[url_col].dropna().empty
                    else None
                )
                if url:
                    annotation_states[img_id].image_url = url
                    break

    # Pre-populate annotation states from 'marked' column if it exists
    if "marked" in df.columns:
        for img_id in image_ids:
            state = annotation_states[img_id]
            df_sel = df[df["image_id"] == img_id]
            for idx, row in df_sel.iterrows():
                mark_val = str(row["marked"]).strip()
                if mark_val and mark_val.lower() != "nan" and mark_val.lower() != "yes":
                    try:
                        ann = {
                            "image_id": img_id,
                            "x": (row["x_min"] + row["x_max"]) / 2,
                            "y": (row["y_min"] + row["y_max"]) / 2,
                        }
                        if mark_val.isdigit():
                            ann["mark_value"] = mark_val
                            # Don't set mode here, let user control it
                        else:
                            ann["mark_value"] = "x"
                            # Don't set mode here, let user control it
                        for label_col in [
                            col for col in df.columns if col.startswith("label_")
                        ]:
                            ann[label_col] = row[label_col]
                        state.annotations.append(ann)
                    except Exception as e:
                        logger.warning(
                            f"Could not process existing annotation for row {idx}: {e}"
                        )
                        print(
                            f"Warning: Could not process existing annotation for row {idx}: {e}"
                        )
                elif mark_val and mark_val.lower() == "yes":
                    try:
                        ann = {
                            "image_id": img_id,
                            "x": (row["x_min"] + row["x_max"]) / 2,
                            "y": (row["y_min"] + row["y_max"]) / 2,
                            "mark_value": "x",
                        }
                        for label_col in [
                            col for col in df.columns if col.startswith("label_")
                        ]:
                            ann[label_col] = row[label_col]
                        state.annotations.append(ann)
                    except Exception as e:
                        logger.warning(
                            f"Could not process existing annotation for row {idx}: {e}"
                        )
                        print(
                            f"Warning: Could not process existing annotation for row {idx}: {e}"
                        )

        # Update progress for thumbnail generation
        progress_manager.update_progress(
            f"Generating thumbnails (0/{len(image_ids)})...", 80, 100
        )

    logger.info("Starting plotting interface creation...")
    
    # Close progress window before creating main interface
    progress_manager.destroy()
    
    # Generate thumbnails and create the main plotting interface
    create_plotting_interface_with_progress(None)

    # Wait for the plot window to be closed before returning
    try:
        # Check if we have an interactive backend
        import matplotlib

        if matplotlib.get_backend() in ["Agg"]:
            print(
                "⚠ Non-interactive backend detected. Plot window cannot be displayed."
            )
            print("Please install tkinter or qt support for interactive plotting.")
            logger.warning("Non-interactive backend - plot window not displayed")
        else:
            # For interactive backends, wait for the window to be closed
            print("✓ Plot window opened. Close the window to return to welcome screen.")
            logger.info("Plot window opened, waiting for user to close it")

            # Keep the main thread alive until the plot window is closed
            import time

            while plt.get_fignums():  # Check if any figures are still open
                time.sleep(0.1)
                try:
                    plt.pause(0.1)  # This allows the GUI to process events
                except:
                    break

    except Exception as e:
        print(f"⚠ Error managing plot window: {e}")
        logger.warning(f"Error managing plot window: {e}")

    logger.info("CSV processing completed successfully")
    return True


def create_plotting_interface_with_progress(progress_manager):
    """Create the main plotting interface with progress feedback for thumbnail generation"""
    global thumbnails, thumb_axes, current_image_idx

    # Generate thumbnails for each image with progress feedback
    thumbnails = []
    total_images = len(image_ids)
    print(f"Creating {total_images} thumbnails...")

    # Apply progressive loading if enabled
    if global_settings.get("progressive_loading", False):
        print("ℹ Progressive thumbnail loading enabled for low-end devices")
        # Create placeholder thumbnails first
        for i, img_id in enumerate(image_ids):
            try:
                # Create a simple placeholder
                placeholder = np.zeros((200, 200, 4), dtype=np.uint8)
                placeholder[:, :, 3] = 255  # Full alpha
                thumbnails.append(placeholder)
            except:
                thumbnails.append(np.zeros((200, 200, 4), dtype=np.uint8))

        # Load thumbnails progressively in background
        def load_thumbnail_progressive(img_id, index):
            try:
                df_sel = df[df["image_id"] == img_id]
                thumb = generate_thumbnail(df_sel)
                thumbnails[index] = thumb
                # Update display if this thumbnail is currently visible
                if index == current_image_idx[0]:
                    update_thumbnail_visibility()
                print(f"  ✓ Loaded thumbnail {index+1}/{total_images}")
            except Exception as e:
                print(f"✗ Error creating thumbnail for {img_id}: {e}")

        # Start progressive loading
        for i, img_id in enumerate(image_ids):
            # Load first few thumbnails immediately
            if i < 5:
                load_thumbnail_progressive(img_id, i)
            else:
                # Schedule others to load later
                root.after(
                    100 * i,
                    lambda idx=i, img=img_id: load_thumbnail_progressive(img, idx),
                )

        print(
            f"✓ Created {len(thumbnails)} placeholder thumbnails (progressive loading enabled)"
        )
    else:
        # Standard loading for high-end devices with progress feedback
        for i, img_id in enumerate(image_ids):
            try:
                # Update progress
                progress_percent = 80 + int(
                    (i / total_images) * 15
                )  # 80-95% for thumbnails
                if progress_manager:
                    progress_manager.update_progress(
                        f"Generating thumbnails ({i+1}/{total_images})...",
                        progress_percent,
                        100,
                    )

                df_sel = df[df["image_id"] == img_id]
                thumb = generate_thumbnail(df_sel)
                thumbnails.append(thumb)

                if (i + 1) % 10 == 0:
                    print(f"  Created {i + 1}/{total_images} thumbnails")

            except Exception as e:
                print(f"✗ Error creating thumbnail for {img_id}: {e}")
                # Create a blank thumbnail as fallback
                try:
                    fig, ax = plt.subplots(figsize=(2, 2))
                    ax.axis("off")
                    fig.canvas.draw()
                    blank_thumb = np.array(fig.canvas.renderer.buffer_rgba())
                    plt.close(fig)
                    thumbnails.append(blank_thumb)
                except:
                    # Last resort: create a simple array
                    thumbnails.append(np.zeros((200, 200, 4), dtype=np.uint8))
        print(f"✓ Created {len(thumbnails)} thumbnails")

    # Update progress for interface creation
    if progress_manager:
        progress_manager.update_progress("Creating interface...", 95, 100)

    # Create the main plotting interface
    create_main_plot_interface()

    # Final progress update
    if progress_manager:
        progress_manager.update_progress("Ready!", 100, 100)


def create_main_plot_interface():
    """Create the main plotting interface with all the matplotlib components"""
    global fig, main_ax, controls_ax, thumb_container_ax, thumb_axes, current_image_idx, btn_help, nav_text, btn_website

    # Get screen size for dynamic sizing with error handling
    try:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
    except Exception as e:
        print(f"Warning: Could not get screen size: {e}")
        screen_width = 1920
        screen_height = 1080

    # Calculate figure size based on screen size (80% of screen)
    fig_width = int(screen_width * 0.8 / 100)
    fig_height = int(screen_height * 0.8 / 100)

    # Ensure minimum and maximum sizes
    fig_width = max(12, min(fig_width, 24))
    fig_height = max(8, min(fig_height, 16))

    # Create figure with error handling
    try:
        # Apply performance settings
        if global_settings.get("anti_aliasing", True):
            # Enable high-quality rendering
            plt.rcParams["figure.dpi"] = 100
            plt.rcParams["savefig.dpi"] = 100
            print("✓ Anti-aliasing enabled for high-quality rendering")
        else:
            # Disable for performance
            plt.rcParams["figure.dpi"] = 72
            plt.rcParams["savefig.dpi"] = 72
            print("ℹ Anti-aliasing disabled for better performance")

        if global_settings.get("smooth_animations", True):
            # Enable smooth animations
            plt.rcParams["animation.html"] = "html5"
            print("✓ Smooth animations enabled")
        else:
            # Disable for performance
            print("ℹ Smooth animations disabled for better performance")

        fig = plt.figure(figsize=(fig_width, fig_height))
        print("✓ Main figure created successfully")
    except Exception as e:
        print(f"✗ Error creating main figure: {e}")
        print("Trying with default size...")
        try:
            fig = plt.figure(figsize=(16, 12))
            print("✓ Main figure created with default size")
        except Exception as e2:
            print(f"✗ Failed to create figure: {e2}")
            return False

    # Set the window title
    try:
        # Method 1: Try canvas manager
        if hasattr(fig.canvas, "manager") and hasattr(
            fig.canvas.manager, "set_window_title"
        ):
            fig.canvas.manager.set_window_title(
                "Unified Plotter - Professional Bounding Box Visualization"
            )
            print("✓ Window title set via canvas manager")
        # Method 2: Try canvas directly
        elif hasattr(fig.canvas, "set_window_title"):
            fig.canvas.set_window_title(
                "Unified Plotter - Professional Bounding Box Visualization"
            )
            print("✓ Window title set via canvas")
        # Method 3: Try setting figure properties
        elif hasattr(fig, "canvas") and hasattr(fig.canvas, "get_tk_widget"):
            try:
                tk_widget = fig.canvas.get_tk_widget()
                if hasattr(tk_widget, "master") and hasattr(tk_widget.master, "title"):
                    tk_widget.master.title(
                        "Unified Plotter - Professional Bounding Box Visualization"
                    )
                    print("✓ Window title set via Tkinter widget")
                else:
                    raise AttributeError("No title method available")
            except:
                raise AttributeError("Tkinter method failed")
        else:
            raise AttributeError("No suitable method found")
    except Exception as e:
        print(f"Warning: Could not set window title: {e}")
        # Final fallback: try to set the figure title
        try:
            fig.suptitle(
                "Unified Plotter - Professional Bounding Box Visualization",
                fontsize=16,
                y=0.95,
            )
            print("✓ Fallback: Set as figure title")
        except:
            print("✗ Could not set any title")

    # Create GridSpec and axes
    try:
        gs = gridspec.GridSpec(
            3,
            2,
            width_ratios=[5, 1],
            height_ratios=[10, 0, 3.5],
            wspace=0.15,
            hspace=0.1,
        )
        print("✓ GridSpec created successfully")
    except Exception as e:
        print(f"✗ Error creating GridSpec: {e}")
        return False

    try:
        main_ax = fig.add_subplot(gs[0, 0])
        main_ax.set_zorder(
            1000
        )  # Set high z-order for main plot so labels can appear above
        controls_ax = fig.add_subplot(gs[0, 1])
        controls_ax.axis("off")
        thumb_container_ax = fig.add_subplot(gs[2, :])
        thumb_container_ax.axis("off")
        print("✓ Main axes created successfully")
    except Exception as e:
        print(f"✗ Error creating main axes: {e}")
        return False

    # Create thumbnail axes
    thumb_axes = []
    print("Creating thumbnail axes...")
    for i in range(len(image_ids)):
        try:
            ax = fig.add_axes(
                [0, 0, 1, 1], frameon=True
            )  # Initially place them off-screen
            ax.imshow(thumbnails[i])
            ax.set_title(
                f"{image_ids[i]}", fontsize=8, y=-0.35
            )  # Consistent y offset for uniform padding
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(True)  # Ensure frame is on for highlighting
            # Set consistent aspect ratio to maintain thumbnail proportions
            ax.set_aspect("equal")
            thumb_axes.append(ax)
        except Exception as e:
            print(f"✗ Error creating thumbnail axis {i}: {e}")
            # Try to create a minimal axis
            try:
                ax = fig.add_axes([0, 0, 1, 1], frameon=True)
                ax.axis("off")
                ax.set_aspect("equal")
                thumb_axes.append(ax)
            except:
                print(f"✗ Failed to create thumbnail axis {i}")
                return False
    print(f"✓ Created {len(thumbnails)} thumbnail axes")

    # Add dataset progress text at the bottom
    try:
        # Create initial dataset progress text with proper positioning
        initial_text = f"Dataset Progress: 1/{len(image_ids)}"
        nav_text = thumb_container_ax.text(
            0.5,
            -0.05,
            initial_text,
            ha="center",
            va="center",
            fontsize=12,
            bbox=dict(
                facecolor="lightblue",
                alpha=0.8,
                edgecolor="black",
                boxstyle="round,pad=0.5",
            ),
        )
        print("✓ Dataset progress text created successfully")
    except Exception as e:
        print(f"✗ Error creating dataset progress text: {e}")
        # Create simple text without bbox
        try:
            initial_text = f"Dataset Progress: 1/{len(image_ids)}"
            nav_text = thumb_container_ax.text(
                0.5, -0.05, initial_text, ha="center", va="center", fontsize=12
            )
            print("✓ Dataset progress text created without bbox")
        except Exception as e2:
            print(f"✗ Failed to create dataset progress text: {e2}")
            return False

    # Add keyboard navigation help text with help button
    try:
        # Create help text
        help_text = thumb_container_ax.text(
            0.5,
            -0.3,
            "Use ←/→ or A/D to navigate, R/S/L/F/B/O for actions, H/?/F1 for professional help",
            ha="center",
            va="center",
            fontsize=9,
            color="gray",
            alpha=0.7,
        )

        # Create help button to the right of the help text
        help_button_ax = fig.add_axes(
            [0.95, 0.02, 0.03, 0.03]
        )  # Position at right side
        help_button_ax.set_zorder(100)
        btn_help = Button(help_button_ax, "?", color="white", hovercolor="lightgray")

        print("✓ Help button created successfully")
    except Exception as e:
        print(f"⚠ Could not create help text and button: {e}")
        help_text = None
        btn_help = None

    # Create website button only if URL is configured
    try:
        # Check if website URL is configured
        website_url = ""  # Set to '' to hide button

        if website_url and website_url.strip() != "":
            # Create website button next to the help button
            website_button_ax = fig.add_axes(
                [0.91, 0.02, 0.03, 0.03]
            )  # Position to the left of help button
            website_button_ax.set_zorder(100)

            # Create website button with reliable icon
            try:
                # Try professional text first (most reliable)
                btn_website = Button(
                    website_button_ax, "WEB", color="white", hovercolor="lightgray"
                )
                print("✓ Website button created with 'WEB' text")
            except Exception as e:
                print(f"⚠ Error creating button with 'WEB' text: {e}")
                try:
                    # Fallback to simple text
                    btn_website = Button(
                        website_button_ax, "LINK", color="white", hovercolor="lightgray"
                    )
                    print("✓ Website button created with 'LINK' text")
                except Exception as e2:
                    print(f"⚠ Error creating button with 'LINK' text: {e2}")
                    # Last resort
                    btn_website = Button(
                        website_button_ax, "WWW", color="white", hovercolor="lightgray"
                    )
                    print("✓ Website button created with 'WWW' text")

            print(f"✓ Website button created: {btn_website}")
            print(f"🔍 Website button ax: {btn_website.ax}")
            print(f"🔍 Global btn_website value: {btn_website}")

            # Verify the button was created properly
            if btn_website is None:
                print("⚠ ERROR: btn_website is None after creation!")
            else:
                print("✓ Website button verification successful")
        else:
            # No website URL configured - don't create button
            btn_website = None
            print("ℹ No website URL configured - website button not created")

    except Exception as e:
        print(f"⚠ Could not create website button: {e}")
        btn_website = None
        import traceback

        traceback.print_exc()

    print(
        "✓ Keyboard navigation help text, help button, and website button creation completed"
    )

    # Add navigation arrows to indicate more thumbnails beyond visible area
    try:
        # Left arrow (previous thumbnails)
        left_arrow = thumb_container_ax.text(
            0.02,
            0.5,
            "◀",
            ha="center",
            va="center",
            fontsize=16,
            color="gray",
            alpha=0.7,
            fontweight="bold",
        )
        # Right arrow (next thumbnails)
        right_arrow = thumb_container_ax.text(
            0.98,
            0.5,
            "▶",
            ha="center",
            va="center",
            fontsize=16,
            color="gray",
            alpha=0.7,
            fontweight="bold",
        )

        print("✓ Navigation arrows created successfully")
    except Exception as e:
        print(f"⚠ Could not create navigation arrows: {e}")
        left_arrow = None
        right_arrow = None

    # Create all the control buttons and widgets
    create_control_widgets()

    # Connect all events and start the interface
    connect_events()

    # Final verification of website button
    print(f"🔍 Final verification - btn_website: {btn_website}")
    if btn_website:
        print(f"🔍 Final verification - button axes: {btn_website.ax}")

    # Final safety check and start
    try:
        update_thumbnail_visibility()
        draw_main_plot(current_image_idx[0])
        print("✓ All components initialized successfully")
        print("✓ Starting plotter...")
        plt.show()
    except Exception as e:
        print(f"✗ Error during final initialization: {e}")
        print("Attempting to save error information...")
        try:
            import traceback

            with open("plotter_error.log", "w") as f:
                f.write(f"Error: {e}\n")
                f.write("Traceback:\n")
                traceback.print_exc(file=f)
            print("Error details saved to plotter_error.log")
        except:
            pass
        return False

    return True


def create_control_widgets():
    """Create all the control widgets and buttons"""
    global radio, btn_reset, btn_undo, btn_redo, btn_clear, btn_flip_y, btn_save, btn_toggle_labels, btn_close, btn_show_bg, image_buttons, btn_website

    # Initialize variables to None to ensure they're always defined
    radio = None
    btn_reset = None
    btn_undo = None
    btn_redo = None
    btn_clear = None
    btn_flip_y = None
    btn_save = None
    btn_toggle_labels = None
    btn_show_bg = None
    btn_close = None
    # btn_website is created in create_main_plot_interface, don't overwrite it
    image_buttons = []

    # Get control panel layout
    bbox = controls_ax.get_position()
    left, bottom, width, height = bbox.x0, bbox.y0, bbox.width, bbox.height

    # Create all buttons
    try:
        ax_mode = fig.add_axes(
            [left + 0.02 * width, bottom + 0.80 * height, 0.9 * width, 0.15 * height]
        )
        ax_mode.set_zorder(100)  # Set low z-order so labels appear above buttons
        radio = RadioButtons(ax_mode, ("x", "number"))
        ax_mode.set_title("Marking Mode")
        print("✓ Mode radio buttons created")
    except Exception as e:
        print(f"✗ Error creating mode radio buttons: {e}")
        return False

    try:
        ax_reset = fig.add_axes(
            [left + 0.02 * width, bottom + 0.71 * height, 0.9 * width, 0.07 * height]
        )
        ax_reset.set_zorder(100)  # Set low z-order so labels appear above buttons
        btn_reset = Button(ax_reset, "Reset Counter")
        print("✓ Reset button created")
    except Exception as e:
        print(f"✗ Error creating reset button: {e}")
        return False

    try:
        ax_undo = fig.add_axes(
            [left + 0.02 * width, bottom + 0.61 * height, 0.9 * width, 0.07 * height]
        )
        ax_undo.set_zorder(100)  # Set low z-order so labels appear above buttons
        btn_undo = Button(ax_undo, "Undo")
        print("✓ Undo button created")
    except Exception as e:
        print(f"✗ Error creating undo button: {e}")
        return False

    try:
        ax_redo = fig.add_axes(
            [left + 0.02 * width, bottom + 0.52 * height, 0.9 * width, 0.07 * height]
        )
        ax_redo.set_zorder(100)  # Set low z-order so labels appear above buttons
        btn_redo = Button(ax_redo, "Redo")
        print("✓ Redo button created")
    except Exception as e:
        print(f"✗ Error creating redo button: {e}")
        return False

    try:
        ax_clear = fig.add_axes(
            [left + 0.02 * width, bottom + 0.43 * height, 0.9 * width, 0.07 * height]
        )
        ax_clear.set_zorder(100)  # Set low z-order so labels appear above buttons
        btn_clear = Button(ax_clear, "Clear All")
        print("✓ Clear button created")
    except Exception as e:
        print(f"✗ Error creating clear button: {e}")
        return False

    try:
        ax_flip_y = fig.add_axes(
            [left + 0.02 * width, bottom + 0.34 * height, 0.9 * width, 0.07 * height]
        )
        ax_flip_y.set_zorder(100)  # Set low z-order so labels appear above buttons
        btn_flip_y = Button(ax_flip_y, "Unflip Y-axis")  # Start with flipped state
        print("✓ Flip Y-axis button created")
    except Exception as e:
        print(f"✗ Error creating flip Y-axis button: {e}")
        return False

    try:
        ax_save = fig.add_axes(
            [left + 0.02 * width, bottom + 0.25 * height, 0.9 * width, 0.07 * height]
        )
        ax_save.set_zorder(100)  # Set low z-order so labels appear above buttons
        btn_save = Button(ax_save, "Save")
        print("✓ Save button created")
    except Exception as e:
        print(f"✗ Error creating save button: {e}")
        return False

    try:
        ax_toggle_labels = fig.add_axes(
            [left + 0.02 * width, bottom + 0.16 * height, 0.9 * width, 0.07 * height]
        )
        ax_toggle_labels.set_zorder(
            100
        )  # Set low z-order so labels appear above buttons
        btn_toggle_labels = Button(ax_toggle_labels, "Disable Labels")
        print("✓ Toggle labels button created")
    except Exception as e:
        print(f"✗ Error creating toggle labels button: {e}")
        return False

    # Add image-related buttons if image URLs are available
    image_buttons = []
    if any(state.image_url for state in annotation_states.values()):
        try:
            # Position buttons below the existing ones with consistent spacing (0.10*height increments)
            ax_open_image = fig.add_axes(
                [
                    left + 0.02 * width,
                    bottom + 0.07 * height,
                    0.9 * width,
                    0.07 * height,
                ]
            )
            ax_open_image.set_zorder(
                100
            )  # Set low z-order so labels appear above buttons
            btn_open_image = Button(ax_open_image, "Open Image")
            image_buttons.append(("open", btn_open_image))
            print("✓ Open image button created")
        except Exception as e:
            print(f"✗ Error creating open image button: {e}")

        # Only show background image button if not disabled in settings
        if not global_settings.get("disable_background_image_button", True):
            try:
                ax_show_bg = fig.add_axes(
                    [
                        left + 0.02 * width,
                        bottom - 0.11 * height,
                        0.9 * width,
                        0.07 * height,
                    ]
                )
                ax_show_bg.set_zorder(
                    100
                )  # Set low z-order so labels appear above buttons
                btn_show_bg = Button(ax_show_bg, "Background Image")
                image_buttons.append(("bg", btn_show_bg))
                print("✓ Background image button created")
            except Exception as e:
                print(f"✗ Error creating background image button: {e}")
        else:
            print("ℹ Background image button disabled by settings")
    else:
        print("ℹ No image URLs found, skipping image-related buttons")

    # Add close button to return to welcome screen (always create this)
    try:
        ax_close = fig.add_axes(
            [left + 0.02 * width, bottom - 0.02 * height, 0.9 * width, 0.07 * height]
        )
        ax_close.set_zorder(100)  # Set low z-order so labels appear above buttons
        btn_close = Button(ax_close, "Close")
        print("✓ Close button created")
    except Exception as e:
        print(f"✗ Error creating close button: {e}")
        return False

    return True


def on_resize(event):
    """Handle window resize events to maintain consistent thumbnail sizing"""
    try:
        # Update thumbnail visibility to maintain consistent sizing
        update_thumbnail_visibility()
        print("✓ Thumbnail layout updated after resize")
    except Exception as e:
        print(f"⚠ Error updating thumbnails after resize: {e}")


def on_key_press(event):
    """Handle keyboard navigation and shortcuts for large datasets"""
    try:
        # Navigation shortcuts
        if event.key == "left" or event.key == "a":
            # Navigate to previous image
            current_image_idx[0] = max(0, current_image_idx[0] - 1)
            draw_main_plot(current_image_idx[0])
            update_thumbnail_visibility()
        elif event.key == "right" or event.key == "d":
            # Navigate to next image
            current_image_idx[0] = min(len(image_ids) - 1, current_image_idx[0] + 1)
            draw_main_plot(current_image_idx[0])
            update_thumbnail_visibility()
        elif event.key == "home":
            # Jump to first image
            current_image_idx[0] = 0
            draw_main_plot(current_image_idx[0])
            update_thumbnail_visibility()
        elif event.key == "end":
            # Jump to last image
            current_image_idx[0] = len(image_ids) - 1
            draw_main_plot(current_image_idx[0])
            update_thumbnail_visibility()
        elif event.key == "pageup":
            # Jump back by 10 images
            current_image_idx[0] = max(0, current_image_idx[0] - 10)
            draw_main_plot(current_image_idx[0])
            update_thumbnail_visibility()
        elif event.key == "pagedown":
            # Jump forward by 10 images
            current_image_idx[0] = min(len(image_ids) - 1, current_image_idx[0] + 10)
            draw_main_plot(current_image_idx[0])
            update_thumbnail_visibility()

        # Button shortcuts
        elif event.key == "r":
            # Reset counter
            on_reset(None)
        elif event.key == "s":
            # Save
            save_annotations()
        elif event.key == "l":
            # Toggle labels
            on_toggle_labels(None)
        elif event.key == "f":
            # Flip Y-axis
            on_flip_y(None)
        elif event.key == "b":
            # Toggle background image (only if button is enabled from global settings)
            if not global_settings.get("disable_background_image_button", True):
                on_toggle_background(None)
        elif event.key == "o" or event.key == "enter" or event.key == "return":
            # Open image in browser (if available) - support Enter/Return key
            if any(state.image_url for state in annotation_states.values()):
                on_open_image(None)
        elif event.key == "escape":
            # Hide help page if it's visible
            hide_help_page()

        # Quick jump shortcuts
        elif event.key.isdigit():
            # Jump to specific image number (1-9 for first 9 images)
            jump_to = int(event.key) - 1
            if 0 <= jump_to < len(image_ids):
                current_image_idx[0] = jump_to
                draw_main_plot(current_image_idx[0])
                update_thumbnail_visibility()

                # Show help page - displays shortcuts in a visual overlay
        elif event.key == "h" or event.key == "?" or event.key == "f1":
            print(f"🔍 Help shortcut triggered: {event.key}")
            show_help_page()

    except Exception as e:
        print(f"⚠ Error in keyboard navigation: {e}")


def on_native_shortcuts(event):
    """Handle native OS shortcuts for undo, redo, and save"""
    try:
        # Check for Ctrl/Cmd combinations
        if event.key == "z" and (event.ctrl or event.cmd):
            # Undo
            on_undo(None)
        elif event.key == "y" and (event.ctrl or event.cmd):
            # Redo
            on_redo(None)
        elif event.key == "s" and (event.ctrl or event.cmd):
            # Save
            save_annotations()
    except Exception as e:
        print(f"⚠ Error in native shortcuts: {e}")


def is_help_system_ready():
    """Check if the help system is ready to display"""
    try:
        # Check if main_ax is available
        if "main_ax" not in globals() or main_ax is None:
            return False, "main_ax not available"

        # Check if fig is available
        if "fig" not in globals() or fig is None:
            return False, "fig not available"

        # Check if canvas is available
        if not hasattr(fig, "canvas") or fig.canvas is None:
            return False, "figure canvas not available"

        return True, "Help system ready"
    except Exception as e:
        return False, f"Error checking help system: {e}"


def create_interactive_help_content():
    """Create interactive help content with clickable links"""
    # Create the main help container
    help_container = fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=True, zorder=10000)
    help_container.set_facecolor("white")
    help_container.set_alpha(0.98)
    help_container.set_xticks([])
    help_container.set_yticks([])
    help_container.set_ylim(0, 1)
    help_container.set_xlim(0, 1)

    # Add border
    help_container.spines["top"].set_color("#2E86AB")
    help_container.spines["bottom"].set_color("#2E86AB")
    help_container.spines["left"].set_color("#2E86AB")
    help_container.spines["right"].set_color("#2E86AB")
    help_container.spines["top"].set_linewidth(2)
    help_container.spines["bottom"].set_linewidth(2)
    help_container.spines["left"].set_linewidth(2)
    help_container.spines["right"].set_linewidth(2)

    # Title
    title_text = help_container.text(
        0.5,
        0.95,
        "KEYBOARD SHORTCUTS REFERENCE",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#2E86AB",
        transform=help_container.transAxes,
    )

    # Navigation section
    nav_title = help_container.text(
        0.1,
        0.85,
        "NAVIGATION",
        fontsize=12,
        fontweight="bold",
        color="#333333",
        transform=help_container.transAxes,
    )

    # Navigation shortcuts with clickable links
    nav_items = [
        ("← / → or A/D", "Navigate to Previous/Next image"),
        ("Home / End", "Jump to First/Last image"),
        ("PageUp / PageDown", "Jump ±10 images"),
        ("1-9", "Jump to specific image (1st-9th)"),
    ]

    nav_links = []
    for i, (shortcut, description) in enumerate(nav_items):
        y_pos = 0.8 - (i * 0.08)
        # Shortcut text (clickable)
        shortcut_text = help_container.text(
            0.15,
            y_pos,
            shortcut,
            fontsize=10,
            color="#0066cc",
            fontweight="bold",
            style="italic",
            transform=help_container.transAxes,
        )
        shortcut_text.set_bbox(
            dict(
                boxstyle="round,pad=0.2",
                facecolor="#f0f8ff",
                edgecolor="#0066cc",
                alpha=0.8,
            )
        )
        nav_links.append(("nav", shortcut, shortcut_text))

        # Description text
        help_container.text(
            0.45,
            y_pos,
            description,
            fontsize=10,
            color="#333333",
            transform=help_container.transAxes,
        )

    # Actions section
    action_title = help_container.text(
        0.1,
        0.55,
        "ACTIONS",
        fontsize=12,
        fontweight="bold",
        color="#333333",
        transform=help_container.transAxes,
    )

    # Action shortcuts with clickable links
    action_items = [
        ("R", "Reset annotation counter"),
        ("S", "Save annotations and data"),
        ("L", "Toggle hover labels on/off"),
        ("F", "Flip Y-axis orientation"),
        ("B", "Toggle background image (if enabled)"),
        ("O or Enter/Return", "Open current image in browser"),
    ]

    action_links = []
    for i, (shortcut, description) in enumerate(action_items):
        y_pos = 0.5 - (i * 0.08)
        # Shortcut text (clickable)
        shortcut_text = help_container.text(
            0.15,
            y_pos,
            shortcut,
            fontsize=10,
            color="#0066cc",
            fontweight="bold",
            style="italic",
            transform=help_container.transAxes,
        )
        shortcut_text.set_bbox(
            dict(
                boxstyle="round,pad=0.2",
                facecolor="#f0f8ff",
                edgecolor="#0066cc",
                alpha=0.8,
            )
        )
        action_links.append(("action", shortcut, shortcut_text))

        # Description text
        help_container.text(
            0.45,
            y_pos,
            description,
            fontsize=10,
            color="#333333",
            transform=help_container.transAxes,
        )

    # Native OS shortcuts section
    native_title = help_container.text(
        0.1,
        0.25,
        "NATIVE OS SHORTCUTS",
        fontsize=12,
        fontweight="bold",
        color="#333333",
        transform=help_container.transAxes,
    )

    # Native shortcuts with clickable links
    native_items = [
        ("Ctrl+Z / Cmd+Z", "Undo last annotation"),
        ("Ctrl+Y / Cmd+Y", "Redo undone annotation"),
        ("Ctrl+S / Cmd+S", "Save (same as S key)"),
    ]

    native_links = []
    for i, (shortcut, description) in enumerate(native_items):
        y_pos = 0.2 - (i * 0.08)
        # Shortcut text (clickable)
        shortcut_text = help_container.text(
            0.15,
            y_pos,
            shortcut,
            fontsize=10,
            color="#0066cc",
            fontweight="bold",
            style="italic",
            transform=help_container.transAxes,
        )
        shortcut_text.set_bbox(
            dict(
                boxstyle="round,pad=0.2",
                facecolor="#f0f8ff",
                edgecolor="#0066cc",
                alpha=0.8,
            )
        )
        native_links.append(("native", shortcut, shortcut_text))

        # Description text
        help_container.text(
            0.45,
            y_pos,
            description,
            fontsize=10,
            color="#333333",
            transform=help_container.transAxes,
        )

    # Additional resources section with website link
    resources_title = help_container.text(
        0.1,
        0.05,
        "ADDITIONAL RESOURCES",
        fontsize=12,
        fontweight="bold",
        color="#333333",
        transform=help_container.transAxes,
    )

    # Website link (clickable)
    website_text = help_container.text(
        0.15,
        0.02,
        "🌐 Visit Developer Website",
        fontsize=10,
        color="#0066cc",
        fontweight="bold",
        style="italic",
        transform=help_container.transAxes,
    )
    website_text.set_bbox(
        dict(
            boxstyle="round,pad=0.2",
            facecolor="#f0f8ff",
            edgecolor="#0066cc",
            alpha=0.8,
        )
    )

    # Store all links for click handling
    all_links = (
        nav_links
        + action_links
        + native_links
        + [("website", "https://raghavendrapratap.com/", website_text)]
    )
    help_container.all_links = all_links

    return help_container


def handle_help_link_click(link_type, shortcut):
    """Handle clicks on help section links"""
    try:
        print(f"🔗 Help link clicked: {link_type} - {shortcut}")

        # Show a tooltip or perform action based on link type
        if link_type == "nav":
            if "←" in shortcut or "→" in shortcut or "A" in shortcut or "D" in shortcut:
                show_help_tooltip(
                    "Use these keys to navigate between images in your dataset"
                )
            elif "Home" in shortcut or "End" in shortcut:
                show_help_tooltip("Jump to the first or last image in your dataset")
            elif "PageUp" in shortcut or "PageDown" in shortcut:
                show_help_tooltip(
                    "Jump 10 images forward or backward for faster navigation"
                )
            elif "1-9" in shortcut:
                show_help_tooltip(
                    "Quick jump to specific image positions (1st through 9th)"
                )

        elif link_type == "action":
            if shortcut == "R":
                show_help_tooltip("Reset the annotation counter back to 1")
            elif shortcut == "S":
                show_help_tooltip(
                    "Save all your annotations and updated data to CSV files"
                )
            elif shortcut == "L":
                show_help_tooltip("Toggle hover labels on/off for bounding boxes")
            elif shortcut == "F":
                show_help_tooltip(
                    "Flip the Y-axis orientation (useful for different coordinate systems)"
                )
            elif shortcut == "B":
                show_help_tooltip(
                    "Toggle background image display (if enabled in settings)"
                )
            elif "O" in shortcut or "Enter" in shortcut:
                show_help_tooltip("Open the current image in your default web browser")

        elif link_type == "native":
            if "Ctrl+Z" in shortcut or "Cmd+Z" in shortcut:
                show_help_tooltip("Undo your last annotation (standard OS shortcut)")
            elif "Ctrl+Y" in shortcut or "Cmd+Y" in shortcut:
                show_help_tooltip(
                    "Redo a previously undone annotation (standard OS shortcut)"
                )
            elif "Ctrl+S" in shortcut or "Cmd+S" in shortcut:
                show_help_tooltip("Save annotations (same as pressing S key)")

        elif link_type == "website":
            # Open the website in the default browser
            try:
                import webbrowser

                webbrowser.open(shortcut)
                show_help_tooltip("Opening website in your default browser...")
            except Exception as e:
                show_help_tooltip(f"Could not open website: {e}")

    except Exception as e:
        print(f"⚠ Error handling help link click: {e}")


def show_help_tooltip(message):
    """Show a tooltip message for help links"""
    try:
        # Create a temporary tooltip
        tooltip_ax = fig.add_axes([0.3, 0.05, 0.4, 0.08], frameon=True, zorder=10002)
        tooltip_ax.set_facecolor("#333333")
        tooltip_ax.set_xticks([])
        tooltip_ax.set_yticks([])
        tooltip_ax.set_ylim(0, 1)
        tooltip_ax.set_xlim(0, 1)

        # Add tooltip text
        tooltip_ax.text(
            0.5,
            0.5,
            message,
            ha="center",
            va="center",
            fontsize=10,
            color="white",
            weight="bold",
            transform=tooltip_ax.transAxes,
        )

        # Auto-remove tooltip after 3 seconds
        def remove_tooltip():
            try:
                tooltip_ax.remove()
                fig.canvas.draw()
            except:
                pass

        # Schedule tooltip removal
        import threading
        import time

        timer = threading.Timer(3.0, remove_tooltip)
        timer.start()

        # Redraw to show tooltip
        fig.canvas.draw()

    except Exception as e:
        print(f"⚠ Error showing help tooltip: {e}")


def on_website_button_click(event=None):
    """Handle website button click - opens website directly"""
    print("🔍 Website button clicked! Function called successfully.")
    try:
        # Single link - your developer website
        website_url = "https://raghavendrapratap.com/"  # Set to '' to hide button
        website_name = "Developer Website"

        # Check if website URL is valid
        if not website_url or website_url.strip() == "":
            print("ℹ No website URL configured - button should be hidden")
            return

        print(f"🌐 Opening {website_name}: {website_url}")
        try:
            import webbrowser

            webbrowser.open(website_url)
            print("✓ Website opened successfully")
        except Exception as e:
            print(f"⚠ Could not open website: {e}")

    except Exception as e:
        print(f"⚠ Error handling website button click: {e}")
        import traceback

        traceback.print_exc()


# Inline website links function removed - simplified to single link approach


def create_professional_icon_button(ax, icon_type="link", fallback_text="LINK"):
    """Create a button with professional icons suitable for corporate use"""
    try:
        # Professional icon mappings using Unicode symbols (not random emojis)
        professional_icons = {
            "link": ["🔗", "LINK"],  # Link symbol
            "website": ["🌐", "WWW"],  # Globe symbol
            "github": ["GIT", "GITHUB"],  # Text-based, professional
            "email": ["@", "EMAIL"],  # At symbol, professional
            "linkedin": ["IN", "LINKEDIN"],  # Text-based, professional
            "twitter": ["X", "TWITTER"],  # Text-based, professional
            "portfolio": ["PORT", "PORTFOLIO"],  # Text-based, professional
            "resume": ["CV", "RESUME"],  # Text-based, professional
            "projects": ["PROJ", "PROJECTS"],  # Text-based, professional
        }

        # Try professional icon libraries first
        icon_created = False

        # Option 1: Try FontAwesome (most professional)
        try:
            import fontawesome as fa

            fa_icon_map = {
                "link": fa.icons["link"],
                "website": fa.icons["globe"],
                "github": fa.icons["github"],
                "email": fa.icons["envelope"],
                "linkedin": fa.icons["linkedin"],
                "twitter": fa.icons["twitter"],
                "portfolio": fa.icons["user"],
                "resume": fa.icons["file-alt"],
                "projects": fa.icons["project-diagram"],
            }

            if icon_type in fa_icon_map:
                try:
                    btn = Button(
                        ax,
                        fa_icon_map[icon_type],
                        color="white",
                        hovercolor="lightgray",
                    )
                    print(
                        f"✓ Button created with FontAwesome icon: {fa_icon_map[icon_type]}"
                    )
                    icon_created = True
                    return btn
                except Exception as e:
                    print(f"⚠ FontAwesome icon failed: {e}")
        except ImportError:
            print("ℹ FontAwesome not available, using professional alternatives")
        except Exception as e:
            print(f"⚠ FontAwesome error: {e}")

        # Option 2: Try Material Icons
        if not icon_created:
            try:
                import material_icons as mi

                mi_icon_map = {
                    "link": mi.icons["link"],
                    "website": mi.icons["language"],
                    "github": mi.icons["code"],
                    "email": mi.icons["mail"],
                    "linkedin": mi.icons["business"],
                    "twitter": mi.icons["chat"],
                    "portfolio": mi.icons["person"],
                    "resume": mi.icons["description"],
                    "projects": mi.icons["dashboard"],
                }

                if icon_type in mi_icon_map:
                    try:
                        btn = Button(
                            ax,
                            mi_icon_map[icon_type],
                            color="white",
                            hovercolor="lightgray",
                        )
                        print(
                            f"✓ Button created with Material icon: {mi_icon_map[icon_type]}"
                        )
                        icon_created = True
                        return btn
                    except Exception as e:
                        print(f"⚠ Material icon failed: {e}")
            except ImportError:
                print("ℹ Material Icons not available")
            except Exception as e:
                print(f"⚠ Material Icons error: {e}")

        # Option 3: Use professional text-based alternatives (no random emojis)
        if not icon_created:
            icons = professional_icons.get(icon_type, professional_icons["link"])

            # Try professional symbols first, then text
            for icon in icons:
                try:
                    btn = Button(ax, icon, color="white", hovercolor="lightgray")
                    print(f"✓ Button created with professional icon: {icon}")
                    return btn
                except Exception as e:
                    print(f"⚠ Failed to create button with '{icon}': {e}")
                    continue

        # Final fallback: professional text
        btn = Button(ax, fallback_text, color="white", hovercolor="lightgray")
        print(f"✓ Button created with professional text: {fallback_text}")
        return btn

    except Exception as e:
        print(f"⚠ Error in create_professional_icon_button: {e}")
        # Last resort: professional text
        return Button(ax, "LINK", color="white", hovercolor="lightgray")


def open_website_and_close(url, dialog):
    """Open website and close the dialog"""
    try:
        import webbrowser

        webbrowser.open(url)
        print(f"🌐 Opening website: {url}")
        dialog.destroy()
    except Exception as e:
        print(f"⚠ Could not open website: {e}")


def show_help_page():
    """Show help page with shortcuts and information in interactive format"""
    global help_text_box

    try:
        # Check if help system is ready
        is_ready, status = is_help_system_ready()
        if not is_ready:
            print(f"⚠ Error: {status}")
            return

        # Create professional tabular help content with clickable links
        help_content = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          KEYBOARD SHORTCUTS REFERENCE                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │                           NAVIGATION                                   │  ║
║  ├────────────────────────────────────────────────────────────────────────┤  ║
║  │  ← / → or A/D           │  Navigate to Previous/Next image             │  ║
║  │  Home / End             │  Jump to First/Last image                    │  ║
║  │  PageUp / PageDown      │  Jump ±10 images                             │  ║
║  │  1-9                    │  Jump to specific image (1st-9th)            │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │                            ACTIONS                                     │  ║
║  ├────────────────────────────────────────────────────────────────────────┤  ║
║  │  R                      │  Reset annotation counter                    │  ║
║  │  S                      │  Save annotations and data                   │  ║
║  │  L                      │  Toggle hover labels on/off                  │  ║
║  │  F                      │  Flip Y-axis orientation                     │  ║
║  │  B                      │  Toggle background image (if enabled)        │  ║
║  │  O or Enter/Return      │  Open current image in browser               │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │                        NATIVE OS SHORTCUTS                             │  ║
║  ├────────────────────────────────────────────────────────────────────────┤  ║
║  │  Ctrl+Z / Cmd+Z        │  Undo last annotation                         │  ║
║  │  Ctrl+Y / Cmd+Y        │  Redo undone annotation                       │  ║
║  │  Ctrl+S / Cmd+S        │  Save (same as S key)                         │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │                              NOTES                                     │  ║
║  ├────────────────────────────────────────────────────────────────────────┤  ║
║  │  • Press H, ?, or F1 to show this help again                           │  ║
║  │  • Press ESC or click the ✕ button to close this help page             │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════════╝"""

        # Create help text box in the main plot area with monospace font for table alignment
        if help_text_box and hasattr(help_text_box, "set_text"):
            try:
                # Update existing help text box
                help_text_box.set_text(help_content)
                help_text_box.set_visible(True)

                # Ensure overlay is also visible
                if (
                    hasattr(help_text_box, "help_overlay")
                    and help_text_box.help_overlay
                ):
                    help_text_box.help_overlay.set_visible(True)

                print("✓ Updated existing help text box")
            except Exception as e:
                print(f"⚠ Error updating existing help text box: {e}")
                # Fall back to creating new one
                help_text_box = None

        if not help_text_box:
            try:
                # Create new help text box with monospace font for proper table alignment
                # Create help text box in figure coordinates for proper centering
                help_text_box = fig.text(
                    0.5,
                    0.5,
                    help_content,
                    ha="center",
                    va="center",
                    fontsize=9,
                    fontfamily="monospace",  # Use monospace for table alignment
                    bbox=dict(
                        facecolor="white",
                        alpha=0.98,
                        edgecolor="#2E86AB",
                        boxstyle="round,pad=1.0",
                        linewidth=2,
                    ),
                    transform=fig.transFigure,
                    zorder=10000,
                )

                # Create a semi-transparent overlay to block interactions
                help_overlay = fig.add_axes([0, 0, 1, 1], frameon=False, zorder=9999)
                help_overlay.set_facecolor("black")
                help_overlay.set_alpha(0.3)
                help_overlay.set_xticks([])
                help_overlay.set_yticks([])
                help_overlay.set_ylim(0, 1)
                help_overlay.set_xlim(0, 1)

                # Store overlay reference for later removal
                help_text_box.help_overlay = help_overlay

                print("✓ Created new help text box")
            except Exception as e:
                print(f"⚠ Error creating new help text box: {e}")
                return

        # Ensure the help text is visible
        try:
            help_text_box.set_visible(True)
            # Redraw the plot to show help
            fig.canvas.draw()
            print("✓ Professional help page displayed successfully")
        except Exception as e:
            print(f"⚠ Error displaying help page: {e}")

        # Verify the help text is actually visible
        if help_text_box and hasattr(help_text_box, "get_visible"):
            is_visible = help_text_box.get_visible()
            print(f"🔍 Help text visibility status: {is_visible}")
            if not is_visible:
                print(
                    "⚠ Warning: Help text should be visible but isn't - forcing visibility"
                )
                help_text_box.set_visible(True)
                fig.canvas.draw()

    except Exception as e:
        print(f"⚠ Error in show_help_page: {e}")
        import traceback

        traceback.print_exc()


# hide_inline_website_links function removed - simplified to single link approach


def hide_help_page():
    """Hide the help page and remove interaction overlay"""
    global help_text_box

    try:
        if help_text_box and hasattr(help_text_box, "set_visible"):
            # Hide the help text
            help_text_box.set_visible(False)

            # Hide the interaction overlay if it exists
            if hasattr(help_text_box, "help_overlay") and help_text_box.help_overlay:
                help_text_box.help_overlay.set_visible(False)
                print("✓ Help overlay hidden")

            # Redraw the plot to hide help
            if "fig" in globals() and fig is not None:
                fig.canvas.draw()
                print("✓ Help page hidden successfully")
            else:
                print("⚠ Warning: Figure not available for redraw")
        else:
            print("ℹ No help page to hide")
    except Exception as e:
        print(f"⚠ Error hiding help page: {e}")
        import traceback

        traceback.print_exc()


def connect_events():
    """Connect all the events and button callbacks"""
    # Connect all events to the main figure
    fig.canvas.mpl_connect("button_press_event", onclick_main)
    fig.canvas.mpl_connect("motion_notify_event", on_motion_main)
    fig.canvas.mpl_connect("resize_event", on_resize)
    fig.canvas.mpl_connect("key_press_event", on_key_press)

    # Connect native OS shortcuts
    fig.canvas.mpl_connect("key_press_event", on_native_shortcuts)

    # Connect button events with safety checks
    if radio:
        radio.on_clicked(on_mode)
    if btn_reset:
        btn_reset.on_clicked(on_reset)
    if btn_undo:
        btn_undo.on_clicked(on_undo)
    if btn_redo:
        btn_redo.on_clicked(on_redo)
    if btn_clear:
        btn_clear.on_clicked(on_clear)
    if btn_save:
        btn_save.on_clicked(save_annotations)
    if btn_toggle_labels:
        btn_toggle_labels.on_clicked(on_toggle_labels)
    if btn_flip_y:
        btn_flip_y.on_clicked(on_flip_y)

    # Connect help button if it exists
    if btn_help:
        btn_help.on_clicked(lambda event: show_help_page())
        print("✓ Help button connected")
    else:
        print("ℹ Help button not available for connection")

    # Connect website button if it exists
    print(f"🔍 About to connect website button. Current value: {btn_website}")
    if btn_website:
        print(f"🔍 Connecting website button: {btn_website}")
        print(f"🔍 Button axes: {btn_website.ax}")
        btn_website.on_clicked(lambda event: on_website_button_click())
        print("✓ Website button connected")
    else:
        print(
            "ℹ Website button not available for connection - button was not created (no URL configured)"
        )

    # Connect close button if it exists
    if btn_close:
        btn_close.on_clicked(return_to_welcome)

    # Connect image buttons if they exist
    for btn_type, btn in image_buttons:
        if btn_type == "open":
            btn.on_clicked(on_open_image)
        elif btn_type == "bg":
            btn.on_clicked(on_toggle_background)

    # Connect close event - only one handler needed
    fig.canvas.mpl_connect("close_event", on_close)

    print("✓ All events connected successfully")


def return_to_welcome(event=None):
    """Return to the welcome screen from the plot screen with loading screen"""
    global _close_operation_in_progress

    # If a close operation is already in progress, ignore this event
    if _close_operation_in_progress:
        print("Close operation already in progress, ignoring duplicate event")
        return

    # Set flag to prevent duplicate close operations
    _close_operation_in_progress = True

    try:
        # Show save confirmation popup first
        save_option = show_save_confirmation()

        # Handle cancel case - don't close the plot
        if save_option == "cancel":
            logger.info("User cancelled close operation")
            print("ℹ Close operation cancelled - returning to plot")
            _close_operation_in_progress = False  # Clear flag
            return False  # Don't close the plot

        # User chose to close, handle saving
        global output_dir

        # Check if there are any annotations to save
        has_annotations = False
        if annotation_states:
            for img_id, state in annotation_states.items():
                if state.annotations or state.markers:
                    has_annotations = True
                    break

        # Create loading screen
        loading_screen = LoadingScreen(screen_manager.root)

        if save_option == "save_all":
            # 1. Close the plot screen
            plt.close("all")
            print("✓ Plot screen closed")

            # 2. Create the output directory, and save all plots and files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_dir is None:
                output_dir = os.path.join(os.getcwd(), f"plots_{timestamp}")
            else:
                output_dir = os.path.join(output_dir, f"plots_{timestamp}")

            # Ensure output directory exists
            try:
                os.makedirs(output_dir, exist_ok=True)
                logger.info(f"Created output directory: {output_dir}")
                print(f"✓ Created output directory: {output_dir}")
            except Exception as e:
                logger.error(f"Error creating output directory: {e}")
                print(f"✗ Error creating output directory: {e}")
                output_dir = os.path.join(os.getcwd(), f"plots_{timestamp}")
                os.makedirs(output_dir, exist_ok=True)

            # 3. Display the loading screen with a progress bar during the saving process
            loading_screen.show(
                "Saving Plots and Files",
                "Preparing to save all plots and annotation files...",
            )

            # Save annotated plots with progress updates
            logger.info("Saving annotated plots...")
            save_all_annotated_plots(loading_screen)
            print("✓ Plots saved successfully")

            # Save annotation CSV files
            loading_screen.update_progress(0, 1, "Saving annotation data...")
            logger.info("Saving annotation data...")
            save_annotations(loading_screen=loading_screen)
            loading_screen.update_progress(1, 1, "All files saved successfully!")

            # 4. Once all plots and files are saved, close the loading screen and open the welcome screen
            loading_screen.hide()
            print("✓ All plots and files saved successfully")

        elif save_option == "save_annotations_only":
            # 1. Close the plot screen
            plt.close("all")
            print("✓ Plot screen closed")

            if has_annotations:
                # 2. Create the output directory, and save files only
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                if output_dir is None:
                    output_dir = os.path.join(os.getcwd(), f"plots_{timestamp}")
                else:
                    output_dir = os.path.join(output_dir, f"plots_{timestamp}")

                # Ensure output directory exists
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    logger.info(f"Created output directory: {output_dir}")
                    print(f"✓ Created output directory: {output_dir}")
                except Exception as e:
                    logger.error(f"Error creating output directory: {e}")
                    print(f"✗ Error creating output directory: {e}")
                    output_dir = os.path.join(os.getcwd(), f"plots_{timestamp}")
                    os.makedirs(output_dir, exist_ok=True)

                # 3. Display the loading screen with a progress bar during the saving process
                loading_screen.show(
                    "Saving Files", "Preparing to save annotation files..."
                )

                # Save annotation CSV files only
                loading_screen.update_progress(0, 1, "Saving annotation data...")
                logger.info("Saving annotation files only...")
                save_annotations(loading_screen=loading_screen)
                loading_screen.update_progress(1, 1, "All files saved successfully!")

                # 4. Once all files are saved, close the loading screen and open the welcome screen
                loading_screen.hide()
                print("✓ Annotation files saved successfully")
            else:
                logger.info("No annotations found, nothing to save")
                print("ℹ No annotations found, nothing to save")
        else:
            # User chose not to save anything
            plt.close("all")
            print("✓ Plot screen closed")
            logger.info("User chose not to save anything")
            print("ℹ Nothing saved")

        # Now return to welcome screen
        print("✓ Returning to welcome screen...")
        # We just need to exit this plotting session
        return True

    except Exception as e:
        print(f"✗ Error returning to welcome screen: {e}")
        _close_operation_in_progress = False  # Clear flag on error
        return False


# --- Main interactive gallery ---

# --- Main execution ---
if __name__ == "__main__":
    try:
        # Show loading screen first
        print("🚀 Starting Unified Plotter...")
        show_loading_screen()

        # Create screen manager for progress updates
        screen_manager = UnifiedScreenManager()
        screen_manager.create_unified_window(
            "Unified Plotter | Professional Bounding Box Visualization",
            show_title_bar=True,
        )

        # Show loading screen with progress updates
        screen_manager.show_loading_screen()

        # Check dependencies with progress updates
        print("Checking dependencies...")

        def update_progress(message, progress):
            """Update loading screen with dependency progress"""
            try:
                screen_manager.update_progress(message, progress, 100)
            except:
                pass  # Ignore errors if screen manager is not ready

        if not check_and_install_dependencies(update_progress):
            print(
                "Some dependencies could not be installed. Please install them manually and try again."
            )
            # Show error screen instead of exiting
            try:
                screen_manager.show_error_screen(
                    "Dependency Error",
                    "Some required packages could not be installed automatically.\n\n"
                    + "Please install them manually using:\n"
                    + "pip install pandas matplotlib numpy pillow requests psutil\n\n"
                    + "Or use a virtual environment:\n"
                    + "python3 -m venv venv\n"
                    + "source venv/bin/activate\n"
                    + "pip install pandas matplotlib numpy pillow requests psutil",
                    "Home",
                )
                screen_manager.run()
            except Exception as e:
                print(f"Error showing error screen: {e}")
                print("Please install dependencies manually and try again.")
            sys.exit(1)

        print("All dependencies are ready!")

        # Import all dependencies now that they are installed
        print("Importing dependencies...")
        update_progress("Importing dependencies...", 100)
        if not import_dependencies():
            print("Failed to import dependencies. Exiting.")
            sys.exit(1)

        # Start the main program loop
        logger.info("Starting Bounding Box Plotter application")
        main_program_loop()
        logger.info("Application exited normally")
    except Exception as e:
        logger.critical(f"Application crashed with error: {e}", exc_info=True)
        print(f"Critical error: {e}")
        # Try to save error information
        try:
            import traceback

            error_file = os.path.join(tempfile.gettempdir(), "plotter_crash.log")
            with open(error_file, "w") as f:
                f.write(f"Plotter Crash Report\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Error: {e}\n")
                f.write("Traceback:\n")
                traceback.print_exc(file=f)
            print(f"Crash details saved to: {error_file}")
        except:
            pass
else:
    # If imported as a module, show loading screen then welcome screen
    try:
        show_loading_screen()

        # Check dependencies
        if not check_and_install_dependencies():
            print(
                "Some dependencies could not be installed. Please install them manually and try again."
            )
            sys.exit(1)

        # Import dependencies
        if not import_dependencies():
            print("Failed to import dependencies. Exiting.")
            sys.exit(1)

        # Use the unified screen manager for consistent welcome screen
        screen_manager = UnifiedScreenManager()

        def select_file_and_close():
            file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialdir=os.getcwd(),
            )
            if file_path:
                screen_manager.destroy()
                process_csv_file(file_path)

        def show_settings_page():
            """Show settings page in the main window using UnifiedScreenManager"""
            try:
                # Clear the current content and show settings
                screen_manager.clear_content()
                screen_manager.current_mode = "settings"

                # Hide the logo section for settings
                if screen_manager.logo_frame:
                    screen_manager.logo_frame.pack_forget()

                # Create settings content in the main window
                settings_frame = tk.Frame(screen_manager.content_frame, bg="#1a1a1a")
                settings_frame.pack(expand=True, fill="both", padx=10, pady=0)

                # Title
                title_label = tk.Label(
                    settings_frame,
                    text="⚙️ Settings",
                    font=tkFont.Font(family="Helvetica", size=20, weight="bold"),
                    bg="#1a1a1a",
                    fg="#ffffff",
                )
                title_label.pack(pady=(0, 5))

                # Description
                desc_label = tk.Label(
                    settings_frame,
                    text="Configure application preferences and performance settings",
                    font=tkFont.Font(family="Helvetica", size=12),
                    bg="#1a1a1a",
                    fg="#cccccc",
                )
                desc_label.pack(pady=(0, 10))

                # Create scrollable frame for settings
                canvas = tk.Canvas(settings_frame, bg="#1a1a1a", highlightthickness=0)
                scrollbar = tk.Scrollbar(
                    settings_frame, orient="vertical", command=canvas.yview
                )
                scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                # Pack canvas and scrollbar
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                # Create a container frame for stacked layout
                cards_container = tk.Frame(scrollable_frame, bg="#1a1a1a")
                cards_container.pack(expand=True, fill="both", padx=30)

                # Create a centered container for the cards
                centered_container = tk.Frame(cards_container, bg="#1a1a1a")
                centered_container.pack(expand=True, fill="both")

                # Create the actual cards container with max width for centering
                cards_inner = tk.Frame(centered_container, bg="#1a1a1a")
                cards_inner.pack(expand=True, fill="x", padx=50)

                # Device detection and performance scoring
                def get_device_profile():
                    """Get device hardware profile for intelligent suggestions"""
                    try:
                        import psutil

                        cpu_cores = psutil.cpu_count()
                        ram_gb = psutil.virtual_memory().total / (1024**3)

                        # Simple storage type detection
                        storage_type = "hdd"  # Default assumption
                        try:
                            if os.path.exists("/sys/block/sda/queue/rotational"):
                                with open("/sys/block/sda/queue/rotational", "r") as f:
                                    if f.read().strip() == "0":
                                        storage_type = "ssd"
                        except:
                            pass

                        return {
                            "cpu_cores": cpu_cores,
                            "ram_gb": ram_gb,
                            "storage_type": storage_type,
                        }
                    except ImportError:
                        return {"cpu_cores": 4, "ram_gb": 8, "storage_type": "hdd"}

                def calculate_performance_score(profile):
                    """Calculate performance score based on device profile"""
                    score = 0
                    # CPU scoring
                    if profile["cpu_cores"] >= 8:
                        score += 40
                    elif profile["cpu_cores"] >= 4:
                        score += 30
                    else:
                        score += 20

                    # RAM scoring
                    if profile["ram_gb"] >= 16:
                        score += 40
                    elif profile["ram_gb"] >= 8:
                        score += 30
                    else:
                        score += 20

                    # Storage scoring
                    if profile["storage_type"] == "ssd":
                        score += 20
                    else:
                        score += 10

                    return min(score, 100)

                def get_performance_suggestion(score):
                    """Get performance suggestion based on score"""
                    if score >= 80:
                        return "high", "High Performance (All features)"
                    elif score >= 60:
                        return "balanced", "Balanced (Recommended)"
                    else:
                        return "low", "Low-End Optimized"

                # Device info section
                device_profile = get_device_profile()
                performance_score = calculate_performance_score(device_profile)
                suggested_mode, suggested_text = get_performance_suggestion(
                    performance_score
                )

                device_frame = tk.LabelFrame(
                    cards_inner,
                    text="📱 Device Information",
                    font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    padx=15,
                    pady=15,
                )
                device_frame.pack(fill="x", pady=(0, 8))

                # Center-aligned device info
                device_info = f"CPU: {device_profile['cpu_cores']} cores | RAM: {device_profile['ram_gb']:.1f}GB | Storage: {device_profile['storage_type'].upper()}"
                device_label = tk.Label(
                    device_frame,
                    text=device_info,
                    font=tkFont.Font(family="Helvetica", size=13),
                    bg="#2a2a2a",
                    fg="#ffffff",
                )
                device_label.pack(pady=5)

                # Performance score
                score_info = tk.Label(
                    device_frame,
                    text=f"Performance Score: {performance_score}/100",
                    font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
                    bg="#2a2a2a",
                    fg="#00ff88",
                )
                score_info.pack(pady=(8, 3))

                # Suggested mode
                suggestion_info = tk.Label(
                    device_frame,
                    text=f"Recommended: {suggested_text}",
                    font=tkFont.Font(family="Helvetica", size=12),
                    bg="#2a2a2a",
                    fg="#cccccc",
                )
                suggestion_info.pack(pady=3)

                # Performance profile section
                profile_frame = tk.LabelFrame(
                    cards_inner,
                    text="🚀 Performance Profile",
                    font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    padx=15,
                    pady=15,
                )
                profile_frame.pack(fill="x", pady=(0, 8))

                profile_var = tk.StringVar(value="balanced")

                def on_profile_change():
                    selected = profile_var.get()
                    if selected != "custom":
                        apply_performance_profile(selected)

                def apply_performance_profile(profile_name):
                    """Apply performance profile settings"""
                    if profile_name == "high":
                        settings["show_background_images"].set(True)
                        settings["high_quality_thumbnails"].set(True)
                        settings["real_time_hover"].set(True)
                        settings["smooth_animations"].set(True)
                        settings["anti_aliasing"].set(True)
                        settings["progressive_loading"].set(False)
                        settings["image_caching"].set(True)
                        settings["aggressive_cleanup"].set(False)
                    elif profile_name == "balanced":
                        settings["show_background_images"].set(False)
                        settings["high_quality_thumbnails"].set(True)
                        settings["real_time_hover"].set(True)
                        settings["smooth_animations"].set(False)
                        settings["anti_aliasing"].set(True)
                        settings["progressive_loading"].set(False)
                        settings["image_caching"].set(True)
                        settings["aggressive_cleanup"].set(False)
                    elif profile_name == "low":
                        settings["show_background_images"].set(False)
                        settings["high_quality_thumbnails"].set(False)
                        settings["real_time_hover"].set(False)
                        settings["smooth_animations"].set(False)
                        settings["anti_aliasing"].set(False)
                        settings["progressive_loading"].set(True)
                        settings["image_caching"].set(False)
                        settings["aggressive_cleanup"].set(True)

                # Center-aligned radio buttons for performance profiles
                tk.Radiobutton(
                    profile_frame,
                    text="High Performance (All features)",
                    variable=profile_var,
                    value="high",
                    command=on_profile_change,
                    font=tkFont.Font(family="Helvetica", size=13),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    selectcolor="#2a2a2a",
                ).pack(anchor="center", pady=2)

                tk.Radiobutton(
                    profile_frame,
                    text="Balanced (Recommended)",
                    variable=profile_var,
                    value="balanced",
                    command=on_profile_change,
                    font=tkFont.Font(family="Helvetica", size=13),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    selectcolor="#2a2a2a",
                ).pack(anchor="center", pady=2)

                tk.Radiobutton(
                    profile_frame,
                    text="Low-End Optimized",
                    variable=profile_var,
                    value="low",
                    command=on_profile_change,
                    font=tkFont.Font(family="Helvetica", size=13),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    selectcolor="#2a2a2a",
                ).pack(anchor="center", pady=2)

                tk.Radiobutton(
                    profile_frame,
                    text="Custom (Manual configuration)",
                    variable=profile_var,
                    value="custom",
                    command=on_profile_change,
                    font=tkFont.Font(family="Helvetica", size=13),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    selectcolor="#2a2a2a",
                ).pack(anchor="center", pady=2)

                # Feature toggles section
                features_frame = tk.LabelFrame(
                    cards_inner,
                    text="🎨 Feature Toggles",
                    font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    padx=15,
                    pady=15,
                )
                features_frame.pack(fill="x", pady=(0, 8))

                # Initialize settings variables
                settings = {
                    "show_background_images": tk.BooleanVar(value=False),
                    "high_quality_thumbnails": tk.BooleanVar(value=True),
                    "real_time_hover": tk.BooleanVar(value=True),
                    "smooth_animations": tk.BooleanVar(value=False),
                    "anti_aliasing": tk.BooleanVar(value=True),
                    "progressive_loading": tk.BooleanVar(value=False),
                    "image_caching": tk.BooleanVar(value=True),
                    "aggressive_cleanup": tk.BooleanVar(value=False),
                }

                def create_feature_checkbox(parent, text, setting_var, description=""):
                    frame = tk.Frame(parent, bg="#2a2a2a")
                    frame.pack(fill="x", pady=2)

                    cb = tk.Checkbutton(
                        frame,
                        text=text,
                        variable=setting_var,
                        font=tkFont.Font(family="Helvetica", size=13),
                        bg="#2a2a2a",
                        fg="#ffffff",
                        selectcolor="#2a2a2a",
                    )
                    cb.pack(anchor="center")

                    if description:
                        desc_label = tk.Label(
                            frame,
                            text=description,
                            font=tkFont.Font(family="Helvetica", size=11),
                            bg="#2a2a2a",
                            fg="#888888",
                        )
                        desc_label.pack(anchor="center", pady=(2, 0))

                    return cb

                def update_settings_display():
                    """Update the display of settings based on current values"""
                    pass  # This will be called when profile changes

                # Create checkboxes for features in single column
                feature_checkboxes = {}

                feature_checkboxes["bg_images"] = create_feature_checkbox(
                    features_frame,
                    "Background Images",
                    settings["show_background_images"],
                    "Disabled by default - may impact performance",
                )
                feature_checkboxes["thumbnails"] = create_feature_checkbox(
                    features_frame,
                    "High-Quality Thumbnails",
                    settings["high_quality_thumbnails"],
                    "Recommended for your device",
                )
                feature_checkboxes["hover"] = create_feature_checkbox(
                    features_frame,
                    "Real-Time Hover",
                    settings["real_time_hover"],
                    "Interactive hover effects",
                )
                feature_checkboxes["animations"] = create_feature_checkbox(
                    features_frame,
                    "Smooth Animations",
                    settings["smooth_animations"],
                    "UI transition effects",
                )
                feature_checkboxes["anti_aliasing"] = create_feature_checkbox(
                    features_frame,
                    "Anti-Aliasing",
                    settings["anti_aliasing"],
                    "Sharp, crisp graphics",
                )

                # Memory management section
                memory_frame = tk.LabelFrame(
                    cards_inner,
                    text="💾 Memory Management",
                    font=tkFont.Font(family="Helvetica", size=15, weight="bold"),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    padx=15,
                    pady=15,
                )
                memory_frame.pack(fill="x", pady=(0, 8))

                # Create memory management checkboxes in single column
                feature_checkboxes["progressive"] = create_feature_checkbox(
                    memory_frame,
                    "Progressive Thumbnail Loading",
                    settings["progressive_loading"],
                    "Recommended for low-end devices",
                )
                feature_checkboxes["caching"] = create_feature_checkbox(
                    memory_frame,
                    "Image Caching",
                    settings["image_caching"],
                    "Recommended for your device",
                )
                feature_checkboxes["cleanup"] = create_feature_checkbox(
                    memory_frame,
                    "Aggressive Memory Cleanup",
                    settings["aggressive_cleanup"],
                    "Low-end optimization",
                )

                # Pack canvas and scrollbar
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                # Update button frame - clear existing buttons and recreate
                for widget in screen_manager.button_frame.winfo_children():
                    widget.destroy()

                # Ensure button frame is visible
                screen_manager.button_frame.pack(side="bottom", fill="x", pady=(20, 0))

                # Create button container for centering
                button_container = tk.Frame(screen_manager.button_frame, bg="#1a1a1a")
                button_container.pack(expand=True)

                def save_settings():
                    """Save settings and return to welcome screen"""
                    print("Settings saved!")
                    # Use the original show_welcome_screen method
                    screen_manager.show_welcome_screen(
                        select_file_and_close, show_settings_page
                    )

                def cancel_settings():
                    """Cancel and return to welcome screen"""
                    print("Settings cancelled - returning to welcome screen")
                    try:
                        # Use the original show_welcome_screen method
                        screen_manager.show_welcome_screen(
                            select_file_and_close, show_settings_page
                        )
                        print("Successfully returned to welcome screen")
                    except Exception as e:
                        print(f"Error returning to welcome screen: {e}")

                # Save button
                save_button = tk.Button(
                    button_container,
                    text="💾 Save Settings",
                    command=save_settings,
                    font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
                    bg="#00ff88",
                    fg="#1a1a1a",
                    activebackground="#00cc6a",
                    activeforeground="#1a1a1a",
                    relief=tk.FLAT,
                    padx=30,
                    pady=12,
                    cursor="hand2",
                )
                save_button.pack(side="right", padx=(15, 0))

                # Cancel button
                cancel_button = tk.Button(
                    button_container,
                    text="❌ Cancel",
                    command=cancel_settings,
                    font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
                    bg="#666666",
                    fg="#ffffff",
                    activebackground="#888888",
                    activeforeground="#ffffff",
                    relief=tk.FLAT,
                    padx=30,
                    pady=12,
                    cursor="hand2",
                )
                cancel_button.pack(side="right")

            except Exception as e:
                print(f"Error opening settings: {e}")
                # Fallback to simple message
                print("Settings page would open here")

        # Create unified window and show welcome screen
        screen_manager.create_unified_window(
            "Unified Plotter | Professional Bounding Box Visualization",
            show_title_bar=True,
        )
        screen_manager.show_welcome_screen(select_file_and_close, show_settings_page)
        screen_manager.run()
    except Exception as e:
        logger.error(f"Error in module mode: {e}", exc_info=True)

# Apply settings
try:
    apply_global_settings()
except Exception as e:
    logger.error(f"Error applying global settings: {e}", exc_info=True)
