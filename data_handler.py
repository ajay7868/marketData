"""
Data Handler for Stock Chart Pattern Drawing Tool
Handles loading market data and exporting/importing pattern coordinates.
"""
import pandas as pd
import csv
import os
from datetime import datetime


class DataHandler:
    """Handles market data loading and pattern coordinate management."""
    
    def __init__(self):
        self.market_data = None
        self.pattern_strokes = []
    
    def load_market_data(self, filepath):
        """
        Load market data from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            pandas.DataFrame: Market data with datetime index
        """
        try:
            # Read CSV file
            df = pd.read_csv(filepath)
            
            # Convert datetime column to datetime type
            df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%Y %H:%M')
            
            # Set datetime as index
            df.set_index('datetime', inplace=True)
            
            # Store the data
            self.market_data = df
            
            return df
            
        except Exception as e:
            raise Exception(f"Error loading market data: {str(e)}")
    
    def export_pattern_to_csv(self, strokes, filename):
        """
        Export pattern strokes to CSV file.
        
        Args:
            strokes (list): List of strokes, each stroke is a list of (datetime, price) tuples
            filename (str): Output CSV filename
        """
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header with stroke_id column
                writer.writerow(['stroke_id', 'datetime', 'open', 'high', 'low', 'close', 'volume'])
                
                # Write pattern data
                for stroke_id, stroke in enumerate(strokes):
                    for point in stroke:
                        datetime_str, price = point
                        
                        # Format datetime to match 1Day.csv format
                        if isinstance(datetime_str, str):
                            dt = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')
                        else:
                            dt = datetime_str
                        
                        formatted_datetime = dt.strftime('%m/%d/%Y %H:%M')
                        
                        # Write row with same structure as 1Day.csv plus stroke_id
                        # For pattern data, we use the same price for all OHLC values
                        writer.writerow([
                            stroke_id,      # stroke_id to identify stroke boundaries
                            formatted_datetime,
                            price,  # open
                            price,  # high
                            price,  # low
                            price,  # close
                            0       # volume (0 for pattern data)
                        ])
            
            print(f"Pattern exported successfully to {filename}")
            
        except Exception as e:
            raise Exception(f"Error exporting pattern: {str(e)}")
    
    def import_pattern_from_csv(self, filename):
        """
        Import pattern strokes from CSV file.
        
        Args:
            filename (str): Input CSV filename
            
        Returns:
            list: List of strokes, each stroke is a list of (datetime, price) tuples
        """
        try:
            strokes = []
            current_stroke = []
            last_stroke_id = None
            
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    # Check if stroke_id column exists (new format)
                    if 'stroke_id' in row:
                        stroke_id = int(row['stroke_id'])
                        datetime_str = row['datetime']
                        price = float(row['close'])  # Use close price for pattern
                        
                        # If this is a new stroke, start a new stroke
                        if last_stroke_id is not None and stroke_id != last_stroke_id:
                            if current_stroke:
                                strokes.append(current_stroke)
                            current_stroke = []
                        
                        current_stroke.append((datetime_str, price))
                        last_stroke_id = stroke_id
                    else:
                        # Fallback for old format without stroke_id
                        datetime_str = row['datetime']
                        price = float(row['close'])
                        
                        # Parse datetime
                        dt = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')
                        
                        # If this is a new time point (not consecutive), start new stroke
                        if last_stroke_id is not None:
                            time_diff = (dt - last_stroke_id).total_seconds()
                            if time_diff > 30:  # More than 30 seconds gap, new stroke
                                if current_stroke:
                                    strokes.append(current_stroke)
                                current_stroke = []
                        
                        current_stroke.append((datetime_str, price))
                        last_stroke_id = dt
                
                # Add the last stroke
                if current_stroke:
                    strokes.append(current_stroke)
            
            self.pattern_strokes = strokes
            print(f"Pattern imported successfully from {filename}")
            return strokes
            
        except Exception as e:
            raise Exception(f"Error importing pattern: {str(e)}")
    
    def get_market_data(self):
        """Get the loaded market data."""
        return self.market_data
    
    def get_pattern_strokes(self):
        """Get the current pattern strokes."""
        return self.pattern_strokes
    
    def clear_patterns(self):
        """Clear all pattern strokes."""
        self.pattern_strokes = []
        print("Patterns cleared")
    
    def add_stroke(self, stroke):
        """
        Add a new stroke to the pattern.
        
        Args:
            stroke (list): List of (datetime, price) tuples
        """
        if stroke:
            self.pattern_strokes.append(stroke)
            print(f"Added stroke with {len(stroke)} points")
    
    def get_data_summary(self):
        """Get summary of loaded data."""
        if self.market_data is None:
            return "No market data loaded"
        
        summary = {
            'data_points': len(self.market_data),
            'date_range': f"{self.market_data.index.min()} to {self.market_data.index.max()}",
            'price_range': f"${self.market_data['close'].min():.2f} to ${self.market_data['close'].max():.2f}",
            'pattern_strokes': len(self.pattern_strokes)
        }
        
        return summary
