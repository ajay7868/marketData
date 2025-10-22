"""
Chart Canvas for Stock Chart Pattern Drawing Tool
Interactive matplotlib chart with pattern drawing functionality.
"""
import matplotlib
# Use Agg backend for compatibility with older macOS versions
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np


class ChartCanvas:
    """Interactive matplotlib chart with pattern drawing functionality."""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.figure = Figure(figsize=(12, 8), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, parent_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Drawing state
        self.is_drawing = False
        self.current_stroke = []
        self.all_strokes = []
        self.drawing_enabled = False
        
        # Data
        self.market_data = None
        self.data_handler = None
        
        # Connect events
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        
        # Initialize empty chart
        self.setup_chart()
    
    def setup_chart(self):
        """Setup the chart appearance and formatting."""
        self.ax.set_title('Stock Chart Pattern Drawing Tool', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Time', fontsize=12)
        self.ax.set_ylabel('Price', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        
        # Format x-axis for dates
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        
        # Rotate x-axis labels
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Set initial message
        self.ax.text(0.5, 0.5, 'Load market data to begin', 
                    transform=self.ax.transAxes, ha='center', va='center',
                    fontsize=16, alpha=0.5)
        
        self.canvas.draw()
    
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
        self.ax.clear()
        self.setup_chart()
        
        # Plot the price data
        self.ax.plot(self.market_data.index, self.market_data['close'], 
                    'b-', linewidth=2, label='Close Price', alpha=0.8)
        
        # Format the chart
        self.ax.set_title('Stock Chart Pattern Drawing Tool', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Time', fontsize=12)
        self.ax.set_ylabel('Price', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        # Format x-axis for dates
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Set y-axis formatting
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
        
        # Refresh the canvas
        self.canvas.draw()
    
    def enable_drawing(self):
        """Enable pattern drawing mode."""
        self.drawing_enabled = True
        self.ax.set_title('Stock Chart Pattern Drawing Tool - Drawing Mode ON', 
                         fontsize=14, fontweight='bold', color='green')
        self.canvas.draw()
    
    def disable_drawing(self):
        """Disable pattern drawing mode."""
        self.drawing_enabled = False
        self.ax.set_title('Stock Chart Pattern Drawing Tool - Drawing Mode OFF', 
                         fontsize=14, fontweight='bold', color='black')
        self.canvas.draw()
    
    def on_mouse_press(self, event):
        """Handle mouse press events for drawing."""
        if not self.drawing_enabled or event.inaxes != self.ax:
            return
        
        self.is_drawing = True
        self.current_stroke = []
        
        # Convert screen coordinates to data coordinates
        x_data, y_data = self.screen_to_data_coords(event.xdata, event.ydata)
        
        if x_data is not None and y_data is not None:
            self.current_stroke.append((x_data, y_data))
    
    def on_mouse_move(self, event):
        """Handle mouse move events for drawing."""
        if not self.drawing_enabled or not self.is_drawing or event.inaxes != self.ax:
            return
        
        # Convert screen coordinates to data coordinates
        x_data, y_data = self.screen_to_data_coords(event.xdata, event.ydata)
        
        if x_data is not None and y_data is not None:
            self.current_stroke.append((x_data, y_data))
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
    
    def screen_to_data_coords(self, x_screen, y_screen):
        """Convert screen coordinates to data coordinates."""
        if x_screen is None or y_screen is None:
            return None, None
        
        # Convert matplotlib datetime to string format
        if isinstance(x_screen, (int, float)):
            # Convert numeric timestamp to datetime
            x_datetime = datetime.fromtimestamp(x_screen)
        else:
            x_datetime = x_screen
        
        # Format datetime to match CSV format
        x_formatted = x_datetime.strftime('%m/%d/%Y %H:%M')
        
        return x_formatted, y_screen
    
    def update_drawing_preview(self):
        """Update the drawing preview on the chart."""
        # Clear and redraw everything
        self.plot_market_data()
        
        # Draw all completed strokes
        for stroke in self.all_strokes:
            if len(stroke) > 1:
                x_coords = [datetime.strptime(point[0], '%m/%d/%Y %H:%M') for point in stroke]
                y_coords = [point[1] for point in stroke]
                self.ax.plot(x_coords, y_coords, 'r-', linewidth=2, alpha=0.8)
        
        # Draw current stroke being drawn
        if len(self.current_stroke) > 1:
            x_coords = [datetime.strptime(point[0], '%m/%d/%Y %H:%M') for point in self.current_stroke]
            y_coords = [point[1] for point in self.current_stroke]
            self.ax.plot(x_coords, y_coords, 'r-', linewidth=2, alpha=0.6, linestyle='--')
        
        self.canvas.draw()
    
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
