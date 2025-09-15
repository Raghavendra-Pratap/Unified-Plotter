# 🎯 Unified Plotter

**Professional bounding box visualization tool for computer vision datasets**

[![Release](https://img.shields.io/badge/release-v2.0.0-blue.svg)](https://github.com/Raghavendra-Pratap/Unified-Plotter/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Raghavendra-Pratap/Unified-Plotter/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **This is the official distribution repository for Unified Plotter - a production-ready tool for visualizing and analyzing bounding box data in computer vision projects.**

## ✨ Key Features

- **🎨 Interactive Visualization**: Create stunning plots with zoom, pan, and selection capabilities
- **📊 Data Analysis**: Built-in statistics, filtering, and data exploration tools
- **💾 Multiple Export Formats**: Save plots as PNG, SVG, PDF, or interactive HTML
- **🔧 Easy Setup**: Native executables for Windows, macOS, and Linux - no installation required
- **📈 Performance Optimized**: Handles large datasets efficiently with smart rendering
- **🎯 Professional UI**: Clean, intuitive interface designed for researchers and developers

## 🚀 Quick Start

### Download & Run

Download the latest release from [GitHub Releases](https://github.com/Raghavendra-Pratap/Unified-Plotter/releases):

- **Windows**: `unified-plotter-v2.0.0-windows.exe`
- **macOS**: `unified-plotter-v2.0.0-macos.dmg`
- **Linux**: `unified-plotter-v2.0.0-linux.AppImage`

### System Requirements

- **Windows**: Windows 10/11 (64-bit)
- **macOS**: macOS 10.14+ (Intel/Apple Silicon)
- **Linux**: Ubuntu 18.04+ or equivalent (with FUSE for AppImage)

### CSV Format

Your CSV file should contain these columns:
- `image_path`: Path to the image file
- `x_min`, `y_min`, `x_max`, `y_max`: Bounding box coordinates
- `class_name`: Object class/category (optional)
- `confidence`: Detection confidence score (optional)

## 🎯 Use Cases

- **Computer Vision Research**: Visualize and analyze object detection datasets
- **Data Quality Assessment**: Identify annotation errors and inconsistencies
- **Model Evaluation**: Compare ground truth vs predictions
- **Dataset Exploration**: Understand data distribution and patterns
- **Presentation & Reporting**: Create publication-ready visualizations

## 🔧 Technical Details

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter with custom styling
- **Plotting**: Matplotlib with interactive features
- **Data Processing**: Pandas for efficient data handling
- **Packaging**: PyInstaller for native executables
- **Cross-Platform**: Tested on Windows, macOS, and Linux

## 📈 Version History

- **v2.0.0** (Latest): Professional release with native executables
- **v1.x.x**: Development and beta versions

## 🤝 Support

- **Issues**: [Report bugs or request features](https://github.com/Raghavendra-Pratap/Unified-Plotter/issues)
- **Discussions**: [Community discussions](https://github.com/Raghavendra-Pratap/Unified-Plotter/discussions)
- **Documentation**: Check the [Wiki](https://github.com/Raghavendra-Pratap/Unified-Plotter/wiki) for detailed guides

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and the amazing open-source community
- Special thanks to contributors and testers who helped shape this tool
- Inspired by the need for better data visualization in computer vision research

---

**Ready to visualize your bounding box data? [Download now](https://github.com/Raghavendra-Pratap/Unified-Plotter/releases) and start creating professional visualizations!**
