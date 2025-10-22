# Quick Start Guide

## Web-Based Stock Chart Pattern Drawing Tool

This application uses a web-based interface that works on all systems without GUI compatibility issues.

```bash
python3 web_app.py
```

Then open your browser and go to: http://localhost:8080

This version uses Flask web framework and works on all operating systems without any GUI compatibility issues.

## Quick Usage

1. **Start the application:**
   ```bash
   python3 web_app.py
   ```
   
2. **Open your browser:**
   - Go to: http://localhost:8080

3. **Load your data:**
   - Click "Load Market Data"
   - Select `1Day.csv` (or any CSV with datetime,open,high,low,close,volume columns)

4. **Draw patterns:**
   - Click "Enable Drawing Mode"
   - Click and drag on the chart to draw patterns
   - Click "Disable Drawing Mode" when done

5. **Save your work:**
   - Click "Export Pattern"
   - The CSV file will be downloaded automatically

6. **Load patterns later:**
   - Load market data first
   - Click "Import Pattern"
   - Select your saved pattern file
   - The application now supports multiple datetime formats for better compatibility

## Features

✅ **Works on all macOS versions** (no GUI compatibility issues)
✅ **Same functionality** as the standard version
✅ **Pattern drawing** with mouse
✅ **Export/Import** patterns as CSV
✅ **Compatible** with your 1Day.csv format
✅ **Modern web interface** with HTML5 Canvas

## File Structure

- `web_app.py` - Web application
- `templates/index.html` - Web interface
- `1Day.csv` - Your sample data
- `requirements.txt` - Dependencies (Flask only)

The web version provides full functionality and runs in your browser, avoiding all GUI compatibility issues.
