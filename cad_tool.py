#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, simpledialog # Import simpledialog
import math
from geometry import Point, Line, Rectangle # Import from new file

class CADApp:
    def __init__(self, master):
        print("CADApp __init__ called.") # Debug print
        self.master = master
        master.title("CLI CAD - Graphical Interface")

        self.canvas_width = 800 # Increased canvas size
        self.canvas_height = 600
        self.scale = 10.0 # 1 unit in CAD = 10 pixels on canvas
        self.offset_x = self.canvas_width / 2 # Center origin
        self.offset_y = self.canvas_height / 2 # Center origin

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white", borderwidth=2, relief="groove")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bind mouse events for pan and zoom
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel) # For Windows/macOS
        self.canvas.bind("<Button-4>", self.on_mouse_wheel) # For Linux (scroll up)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel) # For Linux (scroll down)

        # Bind click event for dimension text
        self.canvas.tag_bind("dimension_text", "<Button-1>", self.on_dimension_click)

        self.last_x = 0
        self.last_y = 0

        # Input Frame
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Label(self.input_frame, text="X1:").grid(row=0, column=0, padx=5, pady=2)
        self.x1_entry = tk.Entry(self.input_frame, width=10)
        self.x1_entry.grid(row=0, column=1, padx=5, pady=2)
        self.x1_entry.insert(0, "0")

        tk.Label(self.input_frame, text="Y1:").grid(row=0, column=2, padx=5, pady=2)
        self.y1_entry = tk.Entry(self.input_frame, width=10)
        self.y1_entry.grid(row=0, column=3, padx=5, pady=2)
        self.y1_entry.insert(0, "0")

        tk.Label(self.input_frame, text="X2:").grid(row=1, column=0, padx=5, pady=2)
        self.x2_entry = tk.Entry(self.input_frame, width=10)
        self.x2_entry.grid(row=1, column=1, padx=5, pady=2)
        self.x2_entry.insert(0, "10")

        tk.Label(self.input_frame, text="Y2:").grid(row=1, column=2, padx=5, pady=2)
        self.y2_entry = tk.Entry(self.input_frame, width=10)
        self.y2_entry.grid(row=1, column=3, padx=5, pady=2)
        self.y2_entry.insert(0, "5")

        self.draw_line_button = tk.Button(self.input_frame, text="Draw Line", command=self.draw_line)
        self.draw_line_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.draw_rect_button = tk.Button(self.input_frame, text="Draw Rectangle", command=self.draw_rectangle)
        self.draw_rect_button.grid(row=2, column=2, columnspan=2, pady=10)

        self.clear_button = tk.Button(self.input_frame, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.grid(row=3, column=0, columnspan=4, pady=10)

        self.objects = [] # Store all drawn objects (lines, rectangles)

    def cad_to_canvas(self, x_cad, y_cad):
        # Convert CAD coordinates to canvas pixel coordinates
        x_canvas = self.offset_x + x_cad * self.scale
        y_canvas = self.offset_y - y_cad * self.scale # Y-axis is inverted in canvas
        return x_canvas, y_canvas

    def on_button_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_mouse_drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.offset_x += dx
        self.offset_y += dy
        self.last_x = event.x
        self.last_y = event.y
        self.redraw_all()

    def on_mouse_wheel(self, event):
        zoom_factor = 1.1 # Zoom in/out by 10%
        # Get mouse position in CAD coordinates before zoom
        mouse_x_cad_before = (event.x - self.offset_x) / self.scale
        mouse_y_cad_before = (self.offset_y - event.y) / self.scale

        if event.num == 5 or event.delta < 0: # Scroll down (zoom out) -> Linux event.num 5, Windows/macOS event.delta < 0
            self.scale /= zoom_factor
        elif event.num == 4 or event.delta > 0: # Scroll up (zoom in) -> Linux event.num 4, Windows/macOS event.delta > 0
            self.scale *= zoom_factor
        
        # Adjust offset to zoom towards mouse cursor
        mouse_x_cad_after = (event.x - self.offset_x) / self.scale
        mouse_y_cad_after = (self.offset_y - event.y) / self.scale

        self.offset_x += (mouse_x_cad_before - mouse_x_cad_after) * self.scale
        self.offset_y -= (mouse_y_cad_before - mouse_y_cad_after) * self.scale

        self.redraw_all()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.objects = []

    def redraw_all(self):
        self.canvas.delete("all") # Clear canvas
        for obj in self.objects:
            if isinstance(obj, Line):
                self._draw_line_on_canvas(obj)
            elif isinstance(obj, Rectangle):
                self._draw_rectangle_on_canvas(obj)

    def _draw_line_on_canvas(self, line_obj):
        canvas_x1, canvas_y1 = self.cad_to_canvas(line_obj.start.x, line_obj.start.y)
        canvas_x2, canvas_y2 = self.cad_to_canvas(line_obj.end.x, line_obj.end.y)
        self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue", width=2)

        # Draw dimension for line
        self._draw_linear_dimension(line_obj.start, line_obj.end, line_obj.length(), "red", obj=line_obj, dim_type="length")

    def _draw_rectangle_on_canvas(self, rect_obj):
        print("Drawing rectangle on canvas.") # Debug print
        # Get the four corner points of the rectangle in CAD coordinates
        p_bl = Point(min(rect_obj.p1.x, rect_obj.p2.x), min(rect_obj.p1.y, rect_obj.p2.y)) # Bottom-left
        p_br = Point(max(rect_obj.p1.x, rect_obj.p2.x), min(rect_obj.p1.y, rect_obj.p2.y)) # Bottom-right
        p_tl = Point(min(rect_obj.p1.x, rect_obj.p2.x), max(rect_obj.p1.y, rect_obj.p2.y)) # Top-left
        p_tr = Point(max(rect_obj.p1.x, rect_obj.p2.x), max(rect_obj.p1.y, rect_obj.p2.y)) # Top-right

        # Convert to canvas coordinates for drawing
        canvas_x1, canvas_y1 = self.cad_to_canvas(p_bl.x, p_tl.y) # Top-left corner of bounding box
        canvas_x2, canvas_y2 = self.cad_to_canvas(p_br.x, p_bl.y) # Bottom-right corner of bounding box

        self.canvas.create_rectangle(canvas_x1, canvas_y1, canvas_x2, canvas_y2, outline="green", width=2)

        # Draw dimensions for width and height
        # Width dimension (horizontal)
        self._draw_linear_dimension(p_bl, p_br, rect_obj.width(), "purple", offset_direction="down", obj=rect_obj, dim_type="width")
        # Height dimension (vertical)
        self._draw_linear_dimension(p_bl, p_tl, rect_obj.height(), "purple", offset_direction="left", obj=rect_obj, dim_type="height")


    def _draw_linear_dimension(self, p_start_cad, p_end_cad, value, color, offset_distance=20, offset_direction="auto", obj=None, dim_type=None):
        # Convert CAD points to canvas points
        canvas_x1, canvas_y1 = self.cad_to_canvas(p_start_cad.x, p_start_cad.y)
        canvas_x2, canvas_y2 = self.cad_to_canvas(p_end_cad.x, p_end_cad.y)

        # Calculate angle of the line
        angle = math.atan2(canvas_y2 - canvas_y1, canvas_x2 - canvas_x1)

        # Determine offset for dimension line
        if offset_direction == "auto":
            # Default offset direction based on angle
            if -math.pi/4 < angle <= math.pi/4: # Horizontal or near horizontal
                offset_dx = 0
                offset_dy = offset_distance
            elif math.pi/4 < angle <= 3*math.pi/4: # Vertical or near vertical (up-right)
                offset_dx = -offset_distance
                offset_dy = 0
            elif -3*math.pi/4 < angle <= -math.pi/4: # Vertical or near vertical (down-left)
                offset_dx = offset_distance
                offset_dy = 0
            else: # Vertical or near vertical (up-left or down-right)
                offset_dx = -offset_distance
                offset_dy = 0
        elif offset_direction == "down":
            offset_dx = 0
            offset_dy = offset_distance
        elif offset_direction == "up":
            offset_dx = 0
            offset_dy = -offset_distance
        elif offset_direction == "left":
            offset_dx = -offset_distance
            offset_dy = 0
        elif offset_direction == "right":
            offset_dx = offset_distance
            offset_dy = 0
        else:
            offset_dx = 0
            offset_dy = offset_distance # Default to down

        # Calculate points for dimension line and extension lines
        dim_line_x1 = canvas_x1 + offset_dx
        dim_line_y1 = canvas_y1 + offset_dy
        dim_line_x2 = canvas_x2 + offset_dx
        dim_line_y2 = canvas_y2 + offset_dy

        # Draw extension lines
        self.canvas.create_line(canvas_x1, canvas_y1, dim_line_x1, dim_line_y1, fill=color, dash=(3, 3))
        self.canvas.create_line(canvas_x2, canvas_y2, dim_line_x2, dim_line_y2, fill=color, dash=(3, 3))

        # Draw dimension line
        self.canvas.create_line(dim_line_x1, dim_line_y1, dim_line_x2, dim_line_y2, fill=color, arrow=tk.BOTH, arrowshape=(8, 10, 3))

        # Draw dimension text
        text_x = (dim_line_x1 + dim_line_x2) / 2
        text_y = (dim_line_y1 + dim_line_y2) / 2
        
        # Create text with tags for interactivity
        self.canvas.create_text(
            text_x, text_y - 10, 
            text=f"{value:.2f}", 
            fill=color, 
            font=("Arial", 10, "bold"),
            tags=("dimension_text", f"obj_{id(obj)}", dim_type) # Add tags for object reference and dimension type
        )

    def on_dimension_click(self, event):
        # Get the ID of the clicked canvas item
        item_id = self.canvas.find_closest(event.x, event.y)[0]
        
        # Get tags associated with the item
        tags = self.canvas.gettags(item_id)
        
        # Find the object ID and dimension type from tags
        obj_id = None
        dim_type = None
        for tag in tags:
            if tag.startswith("obj_"):
                obj_id = int(tag.split("_")[1])
            elif tag in ["length", "width", "height"]:
                dim_type = tag
        
        if obj_id and dim_type:
            # Find the actual object in self.objects list
            target_obj = None
            for obj in self.objects:
                if id(obj) == obj_id:
                    target_obj = obj
                    break
            
            if target_obj:
                current_value = 0.0
                if dim_type == "length" and isinstance(target_obj, Line):
                    current_value = target_obj.length()
                elif dim_type == "width" and isinstance(target_obj, Rectangle):
                    current_value = target_obj.width()
                elif dim_type == "height" and isinstance(target_obj, Rectangle):
                    current_value = target_obj.height()
                
                new_value = simpledialog.askfloat(
                    f"Edit {dim_type.capitalize()}", 
                    f"Enter new {dim_type} for {target_obj.__class__.__name__}:", 
                    initialvalue=current_value
                )
                
                if new_value is not None:
                    print(f"New {dim_type} for {target_obj.__class__.__name__} (ID: {obj_id}): {new_value}")
                    # Apply the new dimension to the object
                    if dim_type == "length" and isinstance(target_obj, Line):
                        target_obj.set_length(new_value)
                    elif dim_type == "width" and isinstance(target_obj, Rectangle):
                        target_obj.set_width(new_value)
                    elif dim_type == "height" and isinstance(target_obj, Rectangle):
                        target_obj.set_height(new_value)
                    
                    self.redraw_all() # Redraw the canvas to reflect changes
            else:
                print(f"Error: Object with ID {obj_id} not found.")
        else:
            print("Clicked item is not a dimension text or missing tags.")


    def draw_line(self):
        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for coordinates.")
            return

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        self.objects.append(line)
        self.redraw_all()

    def draw_rectangle(self):
        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for coordinates.")
            return

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        rect = Rectangle(p1, p2)
        self.objects.append(rect)
        self.redraw_all()

if __name__ == "__main__":
    root = tk.Tk()
    app = CADApp(root)
    root.mainloop()
