"""
Version information for Unified Plotter
"""

import os
from datetime import datetime

# Version information
__version__ = "2.1.0"
__build__ = datetime.now().strftime("%Y%m%d")
__author__ = "Raghavendra Pratap"
__email__ = "contact@raghavendrapratap.com"
__website__ = "https://raghavendrapratap.com/"
__github__ = "https://github.com/Raghavendra-Pratap/Plotter"

# Update server configuration
UPDATE_SERVER = "https://raghavendrapratap.com/updates"
UPDATE_CHANNEL = "stable"  # stable, beta, alpha

# Application metadata
APP_NAME = "Unified Plotter"
APP_DESCRIPTION = (
    "Professional tool for visualizing and annotating bounding box data from CSV files"
)
APP_KEYWORDS = [
    "bounding box",
    "annotation",
    "computer vision",
    "data visualization",
    "CSV",
    "matplotlib",
]

# Build information
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")
BUILD_PLATFORM = "cross-platform"
BUILD_TYPE = "release"  # release, debug, development

# Minimum system requirements
MIN_PYTHON_VERSION = "3.8"
MIN_MEMORY_MB = 512
RECOMMENDED_MEMORY_MB = 2048

# Feature flags
FEATURES = {
    "auto_update": True,
    "background_images": True,
    "real_time_annotations": True,
    "export_formats": ["CSV", "PNG", "JSON"],
    "keyboard_shortcuts": True,
    "performance_profiles": True,
    "logging": True,
    "help_system": True,
    "cross_platform": True,
    "gui_interface": True,
}


def get_version_info():
    """Get complete version information"""
    return {
        "version": __version__,
        "build": __build__,
        "build_date": BUILD_DATE,
        "build_platform": BUILD_PLATFORM,
        "build_type": BUILD_TYPE,
        "author": __author__,
        "email": __email__,
        "website": __website__,
        "github": __github__,
        "app_name": APP_NAME,
        "app_description": APP_DESCRIPTION,
        "min_python": MIN_PYTHON_VERSION,
        "min_memory_mb": MIN_MEMORY_MB,
        "recommended_memory_mb": RECOMMENDED_MEMORY_MB,
        "features": FEATURES,
    }


def is_compatible_version():
    """Check if current Python version is compatible"""
    import sys

    current_version = sys.version_info
    min_version = tuple(map(int, MIN_PYTHON_VERSION.split(".")))
    return current_version >= min_version


def get_update_url():
    """Get the update check URL"""
    return f"{UPDATE_SERVER}/check/{UPDATE_CHANNEL}/{__version__}"


def get_download_url():
    """Get the download URL for updates"""
    return f"{UPDATE_SERVER}/download/{UPDATE_CHANNEL}/{__version__}"


def get_version_string():
    """Get a formatted version string"""
    return f"{APP_NAME} v{__version__} (Build {__build__})"


def check_for_updates():
    """Check for available updates"""
    try:
        import requests

        response = requests.get(get_update_url(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
    except Exception as e:
        print(f"Update check failed: {e}")
    return None
