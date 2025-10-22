#!/usr/bin/env python3
"""
Web-based Stock Chart Pattern Drawing Tool
Uses Flask web framework to avoid macOS tkinter compatibility issues.
"""
import csv
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
import io
import base64

app = Flask(__name__)

class WebDataHandler:
    """Web-based data handler using only csv module."""
    
    def __init__(self):
        self.market_data = []
        self.pattern_strokes = []
    
    def load_market_data(self, filepath):
        """Load market data from CSV file."""
        try:
            self.market_data = []
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    dt = datetime.strptime(row['datetime'], '%m/%d/%Y %H:%M')
                    data_point = {
                        'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
                        'open': float(row['open']),
                        'high': float(row['high']),
                        'low': float(row['low']),
                        'close': float(row['close']),
                        'volume': int(row['volume'])
                    }
                    self.market_data.append(data_point)
            
            return self.market_data
            
        except Exception as e:
            raise Exception(f"Error loading market data: {str(e)}")
    
    def export_pattern_to_csv(self, strokes, filename):
        """Export pattern strokes to CSV file."""
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['datetime', 'open', 'high', 'low', 'close', 'volume'])
                
                for stroke in strokes:
                    for point in stroke:
                        datetime_str, price = point
                        writer.writerow([
                            datetime_str,
                            price, price, price, price, 0
                        ])
            
            return True
            
        except Exception as e:
            raise Exception(f"Error exporting pattern: {str(e)}")
    
    def import_pattern_from_csv(self, filename):
        """Import pattern strokes from CSV file."""
        try:
            strokes = []
            current_stroke = []
            last_datetime = None
            
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    datetime_str = row['datetime']
                    price = float(row['close'])
                    
                    # Try multiple datetime formats
                    dt = None
                    formats_to_try = [
                        '%m/%d/%Y %H:%M',      # 3/12/2025 9:30
                        '%m/%d/%Y %H:%M:%S',   # 3/12/2025 9:30:00
                        '%Y-%m-%d %H:%M:%S',   # 2025-03-12 09:30:00
                        '%Y-%m-%d %H:%M',      # 2025-03-12 09:30
                        '%m/%d/%Y',            # 3/12/2025
                        '%Y-%m-%d'             # 2025-03-12
                    ]
                    
                    for fmt in formats_to_try:
                        try:
                            dt = datetime.strptime(datetime_str, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if dt is None:
                        # If all formats fail, use current time
                        dt = datetime.now()
                        print(f"Warning: Could not parse datetime '{datetime_str}', using current time")
                    
                    if last_datetime is not None:
                        time_diff = (dt - last_datetime).total_seconds()
                        if time_diff > 60:
                            if current_stroke:
                                strokes.append(current_stroke)
                            current_stroke = []
                    
                    current_stroke.append((datetime_str, price))
                    last_datetime = dt
                
                if current_stroke:
                    strokes.append(current_stroke)
            
            return strokes
            
        except Exception as e:
            raise Exception(f"Error importing pattern: {str(e)}")

# Global data handler
data_handler = WebDataHandler()

@app.route('/')
def index():
    """Main page."""
    return send_from_directory('.', 'index.html')

@app.route('/api/load_data', methods=['POST'])
def load_data():
    """Load market data from uploaded file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        temp_filename = 'temp_data.csv'
        file.save(temp_filename)
        
        # Load data
        market_data = data_handler.load_market_data(temp_filename)
        
        # Clean up temp file
        os.remove(temp_filename)
        
        return jsonify({
            'success': True,
            'data': market_data,
            'count': len(market_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save_pattern', methods=['POST'])
def save_pattern():
    """Save pattern data."""
    try:
        pattern_data = request.json.get('pattern')
        if not pattern_data:
            return jsonify({'error': 'No pattern data'}), 400
        
        # Save to temporary file
        temp_filename = 'temp_pattern.csv'
        data_handler.export_pattern_to_csv(pattern_data, temp_filename)
        
        # Read file content
        with open(temp_filename, 'r') as f:
            content = f.read()
        
        # Clean up
        os.remove(temp_filename)
        
        return jsonify({
            'success': True,
            'content': content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load_pattern', methods=['POST'])
def load_pattern():
    """Load pattern from uploaded file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        temp_filename = 'temp_pattern.csv'
        file.save(temp_filename)
        
        # Load pattern
        strokes = data_handler.import_pattern_from_csv(temp_filename)
        
        # Clean up
        os.remove(temp_filename)
        
        return jsonify({
            'success': True,
            'pattern': strokes
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Web-based Stock Chart Pattern Drawing Tool...")
    print("Open your browser and go to: http://localhost:8080")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
