"""
Simple Chart Canvas for Stock Chart Pattern Drawing Tool
Uses tkinter Canvas instead of matplotlib for better compatibility.
"""
import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime
import math


class SimpleChartCanvas:
    """Simple chart canvas using tkinter Canvas widget."""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Create main frame
        self.main_frame = ttk.Frame(parent_frame)
        self.main_frame.pack(fill='both', expand=True)
        
        # Create canvas with scrollbars
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=800, height=600)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient='vertical', command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient='horizontal', command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack canvas and scrollbars
        self.canvas.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Drawing state
        self.is_drawing = False
        self.current_stroke = []
        self.all_strokes = []
        self.drawing_enabled = False
        
        # Data
        self.market_data = None
        self.data_handler = None
        
        # Chart dimensions and scaling
        self.chart_width = 800
        self.chart_height = 600
        self.margin_left = 60
        self.margin_right = 20
        self.margin_top = 20
        self.margin_bottom = 60
        
        # Data ranges
        self.min_price = 0
        self.max_price = 1000
        self.min_time = 0
        self.max_time = 100
        
        # Connect events
        self.canvas.bind('<Button-1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)
        
        # Initialize empty chart
        self.setup_chart()
    
    def setup_chart(self):
        """Setup the chart appearance."""
        self.canvas.delete('all')
        
        # Draw title
        self.canvas.create_text(
            self.chart_width // 2, 10,
            text='Stock Chart Pattern Drawing Tool',
            font=('Arial', 14, 'bold'),
            fill='black'
        )
        
        # Draw initial message
        self.canvas.create_text(
            self.chart_width // 2, self.chart_height // 2,
            text='Load market data to begin',
            font=('Arial', 16),
            fill='gray'
        )
    
    def set_data_handler(self, data_handler):
        """Set the data handler reference."""
        self.data_handler = data_handler
    
    def load_market_data(self, market_data):
        """Load and display market data."""
        self.market_data = market_data
        self.plot_market_data()
    
    def plot_market_data(self):
        """Plot the market data on the chart."""
        if self.market_data is None:
            return
        
        # Clear the chart
        self.canvas.delete('all')
        
        # Calculate data ranges
        prices = self.market_data['close'].values
        self.min_price = min(prices)
        self.max_price = max(prices)
        
        # Add some padding
        price_range = self.max_price - self.min_price
        self.min_price -= price_range * 0.05
        self.max_price += price_range * 0.05
        
        # Time range (use index)
        times = list(range(len(self.market_data)))
        self.min_time = min(times)
        self.max_time = max(times)
        
        # Draw chart area
        self.draw_chart_area()
        
        # Draw price line
        self.draw_price_line()
        
        # Draw axes
        self.draw_axes()
    
    def draw_chart_area(self):
        """Draw the main chart area."""
        # Chart rectangle
        self.canvas.create_rectangle(
            self.margin_left, self.margin_top,
            self.chart_width - self.margin_right, self.chart_height - self.margin_bottom,
            outline='black', width=2
        )
    
    def draw_price_line(self):
        """Draw the price line."""
        if self.market_data is None:
            return
        
        prices = self.market_data['close'].values
        times = list(range(len(prices)))
        
        # Convert to canvas coordinates
        points = []
        for i, (time, price) in enumerate(zip(times, prices)):
            x = self.time_to_x(time)
            y = self.price_to_y(price)
            points.extend([x, y])
        
        # Draw the line
        if len(points) >= 4:
            self.canvas.create_line(points, fill='blue', width=2, smooth=True)
    
    def draw_axes(self):
        """Draw the axes and labels."""
        # Y-axis (price)
        self.canvas.create_line(
            self.margin_left, self.margin_top,
            self.margin_left, self.chart_height - self.margin_bottom,
            fill='black', width=2
        )
        
        # X-axis (time)
        self.canvas.create_line(
            self.margin_left, self.chart_height - self.margin_bottom,
            self.chart_width - self.margin_right, self.chart_height - self.margin_bottom,
            fill='black', width=2
        )
        
        # Y-axis labels
        num_ticks = 5
        for i in range(num_ticks + 1):
            price = self.min_price + (self.max_price - self.min_price) * i / num_ticks
            y = self.price_to_y(price)
            
            # Draw tick
            self.canvas.create_line(
                self.margin_left - 5, y,
                self.margin_left + 5, y,
                fill='black'
            )
            
            # Draw label
            self.canvas.create_text(
                self.margin_left - 10, y,
                text=f'${price:.2f}',
                font=('Arial', 10),
                anchor='e'
            )
        
        # X-axis labels (time)
        if self.market_data is not None:
            num_ticks = min(10, len(self.market_data))
            for i in range(0, len(self.market_data), len(self.market_data) // num_ticks):
                time = i
                x = self.time_to_x(time)
                
                # Draw tick
                self.canvas.create_line(
                    x, self.chart_height - self.margin_bottom - 5,
                    x, self.chart_height - self.margin_bottom + 5,
                    fill='black'
                )
                
                # Draw label (time)
                if i < len(self.market_data):
                    time_str = self.market_data.index[i].strftime('%H:%M')
                    self.canvas.create_text(
                        x, self.chart_height - self.margin_bottom + 20,
                        text=time_str,
                        font=('Arial', 10),
                        anchor='n'
                    )
    
    def time_to_x(self, time):
        """Convert time value to x coordinate."""
        if self.max_time == self.min_time:
            return self.margin_left
        return self.margin_left + (time - self.min_time) / (self.max_time - self.min_time) * (self.chart_width - self.margin_left - self.margin_right)
    
    def price_to_y(self, price):
        """Convert price value to y coordinate."""
        if self.max_price == self.min_price:
            return self.margin_top
        return self.chart_height - self.margin_bottom - (price - self.min_price) / (self.max_price - self.min_price) * (self.chart_height - self.margin_top - self.margin_bottom)
    
    def x_to_time(self, x):
        """Convert x coordinate to time value."""
        if self.chart_width - self.margin_left - self.margin_right == 0:
            return self.min_time
        return self.min_time + (x - self.margin_left) / (self.chart_width - self.margin_left - self.margin_right) * (self.max_time - self.min_time)
    
    def y_to_price(self, y):
        """Convert y coordinate to price value."""
        if self.chart_height - self.margin_top - self.margin_bottom == 0:
            return self.min_price
        return self.min_price + (self.chart_height - self.margin_bottom - y) / (self.chart_height - self.margin_top - self.margin_bottom) * (self.max_price - self.min_price)
    
    def enable_drawing(self):
        """Enable pattern drawing mode."""
        self.drawing_enabled = True
        self.canvas.config(cursor='crosshair')
    
    def disable_drawing(self):
        """Disable pattern drawing mode."""
        self.drawing_enabled = False
        self.canvas.config(cursor='')
    
    def on_mouse_press(self, event):
        """Handle mouse press events for drawing."""
        if not self.drawing_enabled:
            return
        
        # Check if click is within chart area
        if (self.margin_left <= event.x <= self.chart_width - self.margin_right and
            self.margin_top <= event.y <= self.chart_height - self.margin_bottom):
            
            self.is_drawing = True
            self.current_stroke = []
            
            # Convert to data coordinates
            time_val = self.x_to_time(event.x)
            price_val = self.y_to_price(event.y)
            
            # Convert to datetime string format
            if self.market_data is not None and 0 <= time_val < len(self.market_data):
                dt = self.market_data.index[int(time_val)]
                time_str = dt.strftime('%m/%d/%Y %H:%M')
            else:
                time_str = datetime.now().strftime('%m/%d/%Y %H:%M')
            
            self.current_stroke.append((time_str, price_val))
    
    def on_mouse_move(self, event):
        """Handle mouse move events for drawing."""
        if not self.drawing_enabled or not self.is_drawing:
            return
        
        # Check if move is within chart area
        if (self.margin_left <= event.x <= self.chart_width - self.margin_right and
            self.margin_top <= event.y <= self.chart_height - self.margin_bottom):
            
            # Convert to data coordinates
            time_val = self.x_to_time(event.x)
            price_val = self.y_to_price(event.y)
            
            # Convert to datetime string format
            if self.market_data is not None and 0 <= time_val < len(self.market_data):
                dt = self.market_data.index[int(time_val)]
                time_str = dt.strftime('%m/%d/%Y %H:%M')
            else:
                time_str = datetime.now().strftime('%m/%d/%Y %H:%M')
            
            self.current_stroke.append((time_str, price_val))
            self.update_drawing_preview()
    
    def on_mouse_release(self, event):
        """Handle mouse release events for drawing."""
        if not self.drawing_enabled or not self.is_drawing:
            return
        
        self.is_drawing = False
        
        # Add the completed stroke
        if len(self.current_stroke) > 1:
            self.all_strokes.append(self.current_stroke.copy())
            
            # Add to data handler if available
            if self.data_handler:
                self.data_handler.add_stroke(self.current_stroke)
        
        self.current_stroke = []
        self.update_drawing_preview()
    
    def update_drawing_preview(self):
        """Update the drawing preview on the chart."""
        # Redraw the chart
        self.plot_market_data()
        
        # Draw all completed strokes
        for stroke in self.all_strokes:
            if len(stroke) > 1:
                points = []
                for point in stroke:
                    time_str, price = point
                    # Convert back to canvas coordinates
                    if self.market_data is not None:
                        try:
                            dt = datetime.strptime(time_str, '%m/%d/%Y %H:%M')
                            # Find closest time in market data
                            time_idx = 0
                            min_diff = float('inf')
                            for i, market_time in enumerate(self.market_data.index):
                                diff = abs((dt - market_time).total_seconds())
                                if diff < min_diff:
                                    min_diff = diff
                                    time_idx = i
                            x = self.time_to_x(time_idx)
                        except:
                            x = self.margin_left
                    else:
                        x = self.margin_left
                    
                    y = self.price_to_y(price)
                    points.extend([x, y])
                
                if len(points) >= 4:
                    self.canvas.create_line(points, fill='red', width=2, smooth=True)
        
        # Draw current stroke being drawn
        if len(self.current_stroke) > 1:
            points = []
            for point in self.current_stroke:
                time_str, price = point
                # Convert back to canvas coordinates
                if self.market_data is not None:
                    try:
                        dt = datetime.strptime(time_str, '%m/%d/%Y %H:%M')
                        # Find closest time in market data
                        time_idx = 0
                        min_diff = float('inf')
                        for i, market_time in enumerate(self.market_data.index):
                            diff = abs((dt - market_time).total_seconds())
                            if diff < min_diff:
                                min_diff = diff
                                time_idx = i
                        x = self.time_to_x(time_idx)
                    except:
                        x = self.margin_left
                else:
                    x = self.margin_left
                
                y = self.price_to_y(price)
                points.extend([x, y])
            
            if len(points) >= 4:
                self.canvas.create_line(points, fill='red', width=2, smooth=True, dash=(5, 5))
    
    def clear_patterns(self):
        """Clear all drawn patterns."""
        self.all_strokes = []
        self.current_stroke = []
        
        if self.data_handler:
            self.data_handler.clear_patterns()
        
        # Redraw the chart without patterns
        self.plot_market_data()
    
    def load_patterns(self, strokes):
        """Load patterns from data handler."""
        self.all_strokes = strokes.copy()
        self.update_drawing_preview()
    
    def get_strokes(self):
        """Get all current strokes."""
        return self.all_strokes.copy()
    
    def export_patterns(self, filename):
        """Export current patterns to CSV."""
        if self.data_handler and self.all_strokes:
            self.data_handler.export_pattern_to_csv(self.all_strokes, filename)
            return True
        return False
    
    def import_patterns(self, filename):
        """Import patterns from CSV."""
        if self.data_handler:
            strokes = self.data_handler.import_pattern_from_csv(filename)
            self.load_patterns(strokes)
            return True
        return False
