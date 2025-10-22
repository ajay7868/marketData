"""
Main GUI Application for Stock Chart Pattern Drawing Tool
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from data_handler import DataHandler
from chart_canvas import ChartCanvas


class StockChartApp:
    """Main application class for the Stock Chart Pattern Drawing Tool."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Chart Pattern Drawing Tool")
        self.root.geometry("1200x800")
        
        # Initialize data handler
        self.data_handler = DataHandler()
        
        # Create GUI components
        self.create_menu_bar()
        self.create_toolbar()
        self.create_main_frame()
        self.create_status_bar()
        
        # Initialize chart canvas
        self.chart_canvas = ChartCanvas(self.main_frame)
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
        about_text = """Stock Chart Pattern Drawing Tool v1.0

A Python desktop application for drawing and analyzing patterns on stock market charts.

Features:
• Load market data from CSV files
• Interactive chart visualization
• Freehand pattern drawing
• Export/import patterns as CSV
• Pattern persistence and accuracy

Created for educational and personal use."""
        
        messagebox.showinfo("About", about_text)


def main():
    """Main function to run the application."""
    try:
        root = tk.Tk()
        app = StockChartApp(root)
        
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