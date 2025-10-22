# Quick Start Guide

## For macOS Users (Compatibility Issue)

If you get the error: `macOS 15 (1507) or later required, have instead 15 (1506) !`

**Use the Web Version instead:**

```bash
python3 web_app.py
```

Then open your browser and go to: http://localhost:8080

This version uses Flask web framework and works on all macOS versions without any GUI compatibility issues.

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

- `web_app.py` - Web application (use this one)
- `templates/index.html` - Web interface
- `1Day.csv` - Your sample data

The web version provides the same functionality as the standard version but runs in your browser, avoiding all macOS GUI compatibility issues.
