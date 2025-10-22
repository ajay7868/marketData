# Stock Chart Pattern Drawing Tool

A desktop application for drawing patterns on stock charts and exporting/importing them as CSV files with the same structure as your market data.

## Features

- **Drawing:** Click and drag to draw freehand patterns on the chart
- **Coordinate mapping:** Convert screen pixels to data coordinates automatically
- **Pattern storage:** Store each stroke as a separate group in memory
- **Export format:** CSV with columns stroke_id, datetime, open, high, low, close, volume
- **Import:** Load pattern CSV and redraw all strokes accurately on the current chart view
- **Compatibility:** CSV structure matches your 1Day.csv format for seamless integration

## Installation

1. **Install Python 3.7+** if not already installed
2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   
   **Standard Version** (requires macOS 15.1+):
   ```bash
   python3 main.py
   ```
   
   **Web Version** (compatible with all macOS versions):
   ```bash
   python3 web_app.py
   ```
   Then open your browser and go to: http://localhost:8080

## Usage

### 1. Load Market Data
- Click **"Load Market Data"** button or use File → Load Market Data
- Select your CSV file (e.g., 1Day.csv)
- The chart will display your market data

### 2. Enable Drawing Mode
- Click **"Enable Drawing"** button or use View → Toggle Drawing Mode
- The chart title will turn green indicating drawing mode is active

### 3. Draw Patterns
- Click and drag on the chart to draw patterns
- Each continuous stroke is stored as a separate pattern
- Release mouse to complete a stroke

### 4. Export Patterns
- Click **"Export Pattern"** button or use File → Export Pattern
- Choose filename and location
- Patterns are saved as CSV with stroke_id column for stroke identification

### 5. Import Patterns
- Click **"Import Pattern"** button or use File → Import Pattern
- Select a previously exported pattern CSV
- Patterns will be redrawn on the chart

### 6. Clear Patterns
- Click **"Clear Patterns"** button or use Edit → Clear Patterns
- All drawn patterns will be removed

## CSV Format

The exported CSV maintains compatibility with your market data format:

```csv
stroke_id,datetime,open,high,low,close,volume
0,03/12/2025 10:00,560.0,560.0,560.0,560.0,0
0,03/12/2025 10:30,558.0,558.0,558.0,558.0,0
1,03/12/2025 12:00,555.0,555.0,555.0,555.0,0
```

- **stroke_id:** Identifies which stroke each point belongs to
- **datetime:** Time in MM/DD/YYYY HH:MM format (matches 1Day.csv)
- **open, high, low, close:** Price values (same for pattern points)
- **volume:** Set to 0 for pattern data

## File Structure

```
StockMR/
├── main.py                 # Main GUI application (matplotlib version)
├── simple_main.py          # Simple GUI application (tkinter version)
├── ultra_simple_main.py    # Ultra simple GUI (tkinter + csv only)
├── web_app.py              # Web application (Flask + HTML5 Canvas)
├── templates/
│   └── index.html          # Web interface template
├── data_handler.py         # Data loading and CSV export/import
├── chart_canvas.py         # Interactive matplotlib chart
├── simple_chart_canvas.py  # Simple tkinter-based chart
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── 1Day.csv              # Your market data file
```

## Testing

Run the test script to verify all functionality:

```bash
python test_workflow.py
```

This will test:
- Market data loading
- Pattern creation
- Pattern export/import
- Pattern verification
- CSV structure compatibility

## Troubleshooting

### macOS Compatibility Issues
If you encounter "macOS 15 (1507) or later required" errors, use the web version:
- **Standard version** (`main.py`) requires macOS 15.1+ due to matplotlib backend requirements
- **Simple version** (`simple_main.py`) uses pure tkinter but may still have pandas/numpy issues
- **Ultra Simple version** (`ultra_simple_main.py`) uses only tkinter and csv modules but may have tkinter issues
- **Web version** (`web_app.py`) uses Flask web framework and HTML5 Canvas - works on all macOS versions
- All versions provide the same functionality with different rendering backends

### Drawing Not Working
- Ensure drawing mode is enabled (button should show "Disable Drawing")
- Make sure market data is loaded first
- Try clicking and dragging on the chart area

### Import/Export Issues
- Check that CSV files have the correct format
- Ensure datetime format matches MM/DD/YYYY HH:MM
- Verify stroke_id column is present in exported files

## Technical Details

- **Backend:** Tkinter for GUI, Matplotlib for charting
- **Data Processing:** Pandas for CSV handling
- **Coordinate System:** Automatic pixel-to-data coordinate conversion
- **Pattern Storage:** In-memory stroke groups with export/import capability

## License

This tool is provided as-is for stock chart pattern analysis and drawing.