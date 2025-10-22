#!/usr/bin/env python3
"""
Ultra Simple Stock Chart Pattern Drawing Tool
Uses only tkinter and csv - no pandas, no matplotlib, no numpy.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
from datetime import datetime


class UltraSimpleDataHandler:
    """Ultra simple data handler using only csv module."""
    
    def __init__(self):
        self.market_data = []
        self.pattern_strokes = []
    
    def load_market_data(self, filepath):
        """Load market data from CSV file using only csv module."""
        try:
            self.market_data = []
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Parse datetime
                    dt = datetime.strptime(row['datetime'], '%m/%d/%Y %H:%M')
                    # Parse prices
                    data_point = {
                        'datetime': dt,
                        'open': float(row['open']),
                        'high': float(row['high']),
                        'low': float(row['low']),
                        'close': float(row['close']),
                        'volume': int(row['volume'])
                    }
                    self.market_data.append(data_point)
            
            print(f"Loaded {len(self.market_data)} data points")
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
                            price,  # open
                            price,  # high
                            price,  # low
                            price,  # close
                            0       # volume
                        ])
            
            print(f"Pattern exported successfully to {filename}")
            
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
                    
                    dt = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')
                    
                    if last_datetime is not None:
                        time_diff = (dt - last_datetime).total_seconds()
                        if time_diff > 60:  # More than 1 minute gap, new stroke
                            if current_stroke:
                                strokes.append(current_stroke)
                            current_stroke = []
                    
                    current_stroke.append((datetime_str, price))
                    last_datetime = dt
                
                if current_stroke:
                    strokes.append(current_stroke)
            
            self.pattern_strokes = strokes
            print(f"Pattern imported successfully from {filename}")
            return strokes
            
        except Exception as e:
            raise Exception(f"Error importing pattern: {str(e)}")
    
    def add_stroke(self, stroke):
        """Add a new stroke to the pattern."""
        if stroke:
            self.pattern_strokes.append(stroke)
            print(f"Added stroke with {len(stroke)} points")
    
    def clear_patterns(self):
        """Clear all pattern strokes."""
        self.pattern_strokes = []
        print("Patterns cleared")
    
    def get_data_summary(self):
        """Get summary of loaded data."""
        if not self.market_data:
            return "No market data loaded"
        
        prices = [point['close'] for point in self.market_data]
        return {
            'data_points': len(self.market_data),
            'date_range': f"{self.market_data[0]['datetime']} to {self.market_data[-1]['datetime']}",
            'price_range': f"${min(prices):.2f} to ${max(prices):.2f}",
            'pattern_strokes': len(self.pattern_strokes)
        }


class UltraSimpleChartCanvas:
    """Ultra simple chart canvas using only tkinter Canvas."""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Create canvas
        self.canvas = tk.Canvas(parent_frame, bg='white', width=800, height=600)
        self.canvas.pack(fill='both', expand=True)
        
        # Drawing state
        self.is_drawing = False
        self.current_stroke = []
        self.all_strokes = []
        self.drawing_enabled = False
        
        # Data
        self.market_data = []
        self.data_handler = None
        
        # Chart dimensions
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
            text='Ultra Simple Stock Chart Pattern Drawing Tool',
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
        if not self.market_data:
            return
        
        # Clear the chart
        self.canvas.delete('all')
        
        # Calculate data ranges
        prices = [point['close'] for point in self.market_data]
        self.min_price = min(prices)
        self.max_price = max(prices)
        
        # Add some padding
        price_range = self.max_price - self.min_price
        self.min_price -= price_range * 0.05
        self.max_price += price_range * 0.05
        
        # Time range
        self.min_time = 0
        self.max_time = len(self.market_data) - 1
        
        # Draw chart area
        self.draw_chart_area()
        
        # Draw price line
        self.draw_price_line()
        
        # Draw axes
        self.draw_axes()
    
    def draw_chart_area(self):
        """Draw the main chart area."""
        self.canvas.create_rectangle(
            self.margin_left, self.margin_top,
            self.chart_width - self.margin_right, self.chart_height - self.margin_bottom,
            outline='black', width=2
        )
    
    def draw_price_line(self):
        """Draw the price line."""
        if not self.market_data:
            return
        
        prices = [point['close'] for point in self.market_data]
        
        # Convert to canvas coordinates
        points = []
        for i, price in enumerate(prices):
            x = self.time_to_x(i)
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
        if self.market_data:
            num_ticks = min(10, len(self.market_data))
            for i in range(0, len(self.market_data), len(self.market_data) // num_ticks):
                x = self.time_to_x(i)
                
                # Draw tick
                self.canvas.create_line(
                    x, self.chart_height - self.margin_bottom - 5,
                    x, self.chart_height - self.margin_bottom + 5,
                    fill='black'
                )
                
                # Draw label (time)
                if i < len(self.market_data):
                    time_str = self.market_data[i]['datetime'].strftime('%H:%M')
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
        
        if (self.margin_left <= event.x <= self.chart_width - self.margin_right and
            self.margin_top <= event.y <= self.chart_height - self.margin_bottom):
            
            self.is_drawing = True
            self.current_stroke = []
            
            time_val = self.x_to_time(event.x)
            price_val = self.y_to_price(event.y)
            
            if self.market_data and 0 <= time_val < len(self.market_data):
                dt = self.market_data[int(time_val)]['datetime']
                time_str = dt.strftime('%m/%d/%Y %H:%M')
            else:
                time_str = datetime.now().strftime('%m/%d/%Y %H:%M')
            
            self.current_stroke.append((time_str, price_val))
    
    def on_mouse_move(self, event):
        """Handle mouse move events for drawing."""
        if not self.drawing_enabled or not self.is_drawing:
            return
        
        if (self.margin_left <= event.x <= self.chart_width - self.margin_right and
            self.margin_top <= event.y <= self.chart_height - self.margin_bottom):
            
            time_val = self.x_to_time(event.x)
            price_val = self.y_to_price(event.y)
            
            if self.market_data and 0 <= time_val < len(self.market_data):
                dt = self.market_data[int(time_val)]['datetime']
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
        
        if len(self.current_stroke) > 1:
            self.all_strokes.append(self.current_stroke.copy())
            
            if self.data_handler:
                self.data_handler.add_stroke(self.current_stroke)
        
        self.current_stroke = []
        self.update_drawing_preview()
    
    def update_drawing_preview(self):
        """Update the drawing preview on the chart."""
        self.plot_market_data()
        
        # Draw all completed strokes
        for stroke in self.all_strokes:
            if len(stroke) > 1:
                points = []
                for point in stroke:
                    time_str, price = point
                    if self.market_data:
                        try:
                            dt = datetime.strptime(time_str, '%m/%d/%Y %H:%M')
                            time_idx = 0
                            min_diff = float('inf')
                            for i, data_point in enumerate(self.market_data):
                                diff = abs((dt - data_point['datetime']).total_seconds())
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
                if self.market_data:
                    try:
                        dt = datetime.strptime(time_str, '%m/%d/%Y %H:%M')
                        time_idx = 0
                        min_diff = float('inf')
                        for i, data_point in enumerate(self.market_data):
                            diff = abs((dt - data_point['datetime']).total_seconds())
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


class UltraSimpleStockChartApp:
    """Ultra simple main application class using only tkinter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ultra Simple Stock Chart Pattern Drawing Tool")
        self.root.geometry("1000x700")
        
        # Initialize data handler
        self.data_handler = UltraSimpleDataHandler()
        
        # Create GUI components
        self.create_menu_bar()
        self.create_toolbar()
        self.create_main_frame()
        self.create_status_bar()
        
        # Initialize chart canvas
        self.chart_canvas = UltraSimpleChartCanvas(self.main_frame)
        self.chart_canvas.set_data_handler(self.data_handler)
        
        # Application state
        self.drawing_enabled = False
        self.market_data_loaded = False
        
        # Update status
        self.update_status("Ready - Load market data to begin")
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Market Data", command=self.load_market_data)
        file_menu.add_separator()
        file_menu.add_command(label="Export Pattern", command=self.export_pattern)
        file_menu.add_command(label="Import Pattern", command=self.import_pattern)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Pattern", command=self.clear_pattern)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create the application toolbar."""
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Load Market Data button
        self.load_data_btn = ttk.Button(
            self.toolbar, 
            text="Load Market Data", 
            command=self.load_market_data
        )
        self.load_data_btn.pack(side=tk.LEFT, padx=2)
        
        # Drawing mode toggle button
        self.drawing_btn = ttk.Button(
            self.toolbar, 
            text="Enable Drawing Mode", 
            command=self.toggle_drawing_mode,
            state=tk.DISABLED
        )
        self.drawing_btn.pack(side=tk.LEFT, padx=2)
        
        # Clear Pattern button
        self.clear_btn = ttk.Button(
            self.toolbar, 
            text="Clear Pattern", 
            command=self.clear_pattern,
            state=tk.DISABLED
        )
        self.clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Export Pattern button
        self.export_btn = ttk.Button(
            self.toolbar, 
            text="Export Pattern", 
            command=self.export_pattern,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=2)
        
        # Import Pattern button
        self.import_btn = ttk.Button(
            self.toolbar, 
            text="Import Pattern", 
            command=self.import_pattern,
            state=tk.DISABLED
        )
        self.import_btn.pack(side=tk.LEFT, padx=2)
    
    def create_main_frame(self):
        """Create the main frame for the chart."""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    def update_status(self, message):
        """Update the status bar message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def load_market_data(self):
        """Load market data from CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select Market Data CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Load data using data handler
            market_data = self.data_handler.load_market_data(file_path)
            
            # Update chart
            self.chart_canvas.load_market_data(market_data)
            
            # Update application state
            self.market_data_loaded = True
            self.drawing_btn.config(state=tk.NORMAL)
            self.import_btn.config(state=tk.NORMAL)
            
            # Update status
            data_summary = self.data_handler.get_data_summary()
            self.update_status(f"Market data loaded: {data_summary['data_points']} points, "
                             f"Price range: {data_summary['price_range']}")
            
            messagebox.showinfo("Success", "Market data loaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load market data:\n{str(e)}")
            self.update_status("Error loading market data")
    
    def toggle_drawing_mode(self):
        """Toggle drawing mode on/off."""
        if not self.market_data_loaded:
            messagebox.showwarning("Warning", "Please load market data first!")
            return
        
        self.drawing_enabled = not self.drawing_enabled
        
        if self.drawing_enabled:
            self.chart_canvas.enable_drawing()
            self.drawing_btn.config(text="Disable Drawing Mode")
            self.clear_btn.config(state=tk.NORMAL)
            self.export_btn.config(state=tk.NORMAL)
            self.update_status("Drawing mode enabled - Click and drag to draw patterns")
        else:
            self.chart_canvas.disable_drawing()
            self.drawing_btn.config(text="Enable Drawing Mode")
            self.update_status("Drawing mode disabled")
    
    def clear_pattern(self):
        """Clear all drawn patterns."""
        if not self.market_data_loaded:
            messagebox.showwarning("Warning", "Please load market data first!")
            return
        
        result = messagebox.askyesno("Confirm", "Are you sure you want to clear all patterns?")
        if result:
            self.chart_canvas.clear_patterns()
            self.update_status("All patterns cleared")
    
    def export_pattern(self):
        """Export current patterns to CSV file."""
        if not self.market_data_loaded:
            messagebox.showwarning("Warning", "Please load market data first!")
            return
        
        strokes = self.chart_canvas.get_strokes()
        if not strokes:
            messagebox.showwarning("Warning", "No pattern to export. Please draw a pattern first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Pattern As",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.chart_canvas.export_patterns(file_path)
                messagebox.showinfo("Success", f"Pattern exported successfully to:\n{file_path}")
                self.update_status(f"Pattern exported to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export pattern:\n{str(e)}")
    
    def import_pattern(self):
        """Import patterns from CSV file."""
        if not self.market_data_loaded:
            messagebox.showwarning("Warning", "Please load market data first!")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Pattern CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                success = self.chart_canvas.import_patterns(file_path)
                if success:
                    messagebox.showinfo("Success", f"Pattern imported successfully from:\n{file_path}")
                    self.update_status(f"Pattern imported from {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("Error", "Failed to import pattern")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import pattern:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """Ultra Simple Stock Chart Pattern Drawing Tool v1.0

A Python desktop application for drawing and analyzing patterns on stock market charts.

Features:
• Load market data from CSV files
• Interactive chart visualization (pure tkinter)
• Freehand pattern drawing
• Export/import patterns as CSV
• Pattern persistence and accuracy

This ultra simple version uses only tkinter and csv modules
for maximum compatibility with all macOS versions.

Created for educational and personal use."""
        
        messagebox.showinfo("About", about_text)


def main():
    """Main function to run the application."""
    try:
        root = tk.Tk()
        app = UltraSimpleStockChartApp(root)
        
        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
