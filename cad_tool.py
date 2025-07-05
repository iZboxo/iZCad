#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, simpledialog
import math
from geometry import Point, Line, Rectangle

class CADApp:
    def __init__(self, master):
        print("CADApp __init__ called.")
        self.master = master
        master.title("CLI CAD - Graphical Interface")

        self.canvas_width = 800
        self.canvas_height = 600
        self.scale = 10.0
        self.offset_x = self.canvas_width / 2
        self.offset_y = self.canvas_height / 2

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white", borderwidth=2, relief="groove")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bind mouse events for pan and zoom
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)

        # Bind click event for dimension text
        self.canvas.tag_bind("dimension_text", "<Button-1>", self.on_dimension_click)

        # Bind mouse events for interactive drawing
        self.canvas.bind("<Button-1>", self.on_canvas_click) # Left click for drawing
        self.canvas.bind("<Motion>", self.on_mouse_move) # Mouse move for preview

        self.last_x = 0
        self.last_y = 0

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

        self.draw_line_button = tk.Button(self.input_frame, text="Draw Line (Manual)", command=self.draw_line_manual)
        self.draw_line_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.draw_rect_button = tk.Button(self.input_frame, text="Draw Rectangle (Manual)", command=self.draw_rectangle_manual)
        self.draw_rect_button.grid(row=2, column=2, columnspan=2, pady=10)

        self.draw_rect_interactive_button = tk.Button(self.input_frame, text="Draw Rectangle (Interactive)", command=self.activate_interactive_rectangle_drawing)
        self.draw_rect_interactive_button.grid(row=3, column=0, columnspan=4, pady=10)

        self.clear_button = tk.Button(self.input_frame, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.grid(row=4, column=0, columnspan=4, pady=10)

        self.objects = []
        self.current_drawing_mode = "none" # "none", "draw_rectangle_interactive"
        self.interactive_start_point_cad = None
        self.preview_rectangle_id = None
        self.preview_dim_ids = []

        self.redraw_all()

    def cad_to_canvas(self, x_cad, y_cad):
        x_canvas = self.offset_x + x_cad * self.scale
        y_canvas = self.offset_y - y_cad * self.scale
        return x_canvas, y_canvas

    def canvas_to_cad(self, x_canvas, y_canvas):
        x_cad = (x_canvas - self.offset_x) / self.scale
        y_cad = (self.offset_y - y_canvas) / self.scale
        return x_cad, y_cad

    def on_button_press(self, event):
        # Only pan if not in drawing mode
        if self.current_drawing_mode == "none":
            self.last_x = event.x
            self.last_y = event.y

    def on_mouse_drag(self, event):
        # Only pan if not in drawing mode
        if self.current_drawing_mode == "none":
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.offset_x += dx
            self.offset_y += dy
            self.last_x = event.x
            self.last_y = event.y
            self.redraw_all()

    def on_mouse_wheel(self, event):
        zoom_factor = 1.1
        mouse_x_cad_before, mouse_y_cad_before = self.canvas_to_cad(event.x, event.y)

        if event.num == 5 or event.delta < 0:
            self.scale /= zoom_factor
        elif event.num == 4 or event.delta > 0:
            self.scale *= zoom_factor
        
        mouse_x_cad_after, mouse_y_cad_after = self.canvas_to_cad(event.x, event.y)

        self.offset_x += (mouse_x_cad_before - mouse_x_cad_after) * self.scale
        self.offset_y -= (mouse_y_cad_before - mouse_y_cad_after) * self.scale

        self.redraw_all()

    def on_canvas_click(self, event):
        if self.current_drawing_mode == "draw_rectangle_interactive":
            clicked_cad_x, clicked_cad_y = self.canvas_to_cad(event.x, event.y)
            clicked_point = Point(clicked_cad_x, clicked_cad_y)

            if self.interactive_start_point_cad is None:
                # First click: define start point
                self.interactive_start_point_cad = clicked_point
            else:
                # Second click: define end point and create rectangle
                rect = Rectangle(self.interactive_start_point_cad, clicked_point)
                self.objects.append(rect)
                self.current_drawing_mode = "none"
                self.interactive_start_point_cad = None
                self.canvas.delete(self.preview_rectangle_id) # Clear preview
                for dim_id in self.preview_dim_ids:
                    self.canvas.delete(dim_id)
                self.preview_rectangle_id = None
                self.preview_dim_ids = []
                self.redraw_all()
                # Re-bind pan/zoom events after interactive drawing is done
                self.canvas.bind("<ButtonPress-1>", self.on_button_press)
                self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def on_mouse_move(self, event):
        if self.current_drawing_mode == "draw_rectangle_interactive" and self.interactive_start_point_cad is not None:
            # Clear previous preview
            self.canvas.delete(self.preview_rectangle_id)
            for dim_id in self.preview_dim_ids:
                self.canvas.delete(dim_id)
            self.preview_dim_ids = []

            current_cad_x, current_cad_y = self.canvas_to_cad(event.x, event.y)
            current_point = Point(current_cad_x, current_cad_y)

            temp_rect = Rectangle(self.interactive_start_point_cad, current_point)

            canvas_x1, canvas_y1 = self.cad_to_canvas(min(temp_rect.p1.x, temp_rect.p2.x), max(temp_rect.p1.y, temp_rect.p2.y))
            canvas_x2, canvas_y2 = self.cad_to_canvas(max(temp_rect.p1.x, temp_rect.p2.x), min(temp_rect.p1.y, temp_rect.p2.y))

            self.preview_rectangle_id = self.canvas.create_rectangle(canvas_x1, canvas_y1, canvas_x2, canvas_y2, outline="gray", dash=(5, 5))

            # Display dynamic dimensions for preview
            p_bl = Point(min(temp_rect.p1.x, temp_rect.p2.x), min(temp_rect.p1.y, temp_rect.p2.y))
            p_br = Point(max(temp_rect.p1.x, temp_rect.p2.x), min(temp_rect.p1.y, temp_rect.p2.y))
            p_tl = Point(min(temp_rect.p1.x, temp_rect.p2.x), max(temp_rect.p1.y, temp_rect.p2.y))

            # Width dimension
            dim_id_w = self._draw_linear_dimension_preview(p_bl, p_br, temp_rect.width(), "gray", offset_direction="down")
            self.preview_dim_ids.append(dim_id_w)
            # Height dimension
            dim_id_h = self._draw_linear_dimension_preview(p_bl, p_tl, temp_rect.height(), "gray", offset_direction="left")
            self.preview_dim_ids.append(dim_id_h)

    def activate_interactive_rectangle_drawing(self):
        self.current_drawing_mode = "draw_rectangle_interactive"
        self.interactive_start_point_cad = None
        messagebox.showinfo("Interactive Drawing", "Click on the canvas to define the first corner of the rectangle.")
        # Unbind pan/zoom events temporarily
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")


    def clear_canvas(self):
        self.canvas.delete("all")
        self.objects = []
        self.current_drawing_mode = "none"
        self.interactive_start_point_cad = None
        self.preview_rectangle_id = None
        self.preview_dim_ids = []
        self.redraw_all()

    def redraw_all(self):
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_origin()
        for obj in self.objects:
            if isinstance(obj, Line):
                self._draw_line_on_canvas(obj)
            elif isinstance(obj, Rectangle):
                self._draw_rectangle_on_canvas(obj)

    def _draw_grid(self):
        grid_color = "#E0E0E0"
        grid_line_width = 1

        cad_grid_spacing = 1.0
        if self.scale < 5:
            cad_grid_spacing = 10.0
        elif self.scale < 20:
            cad_grid_spacing = 5.0
        else:
            cad_grid_spacing = 1.0

        x_min_cad, y_max_cad = self.canvas_to_cad(0, 0)
        x_max_cad, y_min_cad = self.canvas_to_cad(self.canvas_width, self.canvas_height)

        start_x = math.floor(x_min_cad / cad_grid_spacing) * cad_grid_spacing
        end_x = math.ceil(x_max_cad / cad_grid_spacing) * cad_grid_spacing
        for x_cad in self._frange(start_x, end_x + cad_grid_spacing, cad_grid_spacing):
            x_canvas, _ = self.cad_to_canvas(x_cad, 0)
            self.canvas.create_line(x_canvas, 0, x_canvas, self.canvas_height, fill=grid_color, width=grid_line_width)

        start_y = math.floor(y_min_cad / cad_grid_spacing) * cad_grid_spacing
        end_y = math.ceil(y_max_cad / cad_grid_spacing) * cad_grid_spacing
        for y_cad in self._frange(start_y, end_y + cad_grid_spacing, cad_grid_spacing):
            _, y_canvas = self.cad_to_canvas(0, y_cad)
            self.canvas.create_line(0, y_canvas, self.canvas_width, y_canvas, fill=grid_color, width=grid_line_width)

    def _frange(self, start, stop, step):
        while start < stop:
            yield start
            start += step

    def _draw_origin(self):
        origin_x_canvas, origin_y_canvas = self.cad_to_canvas(0, 0)

        self.canvas.create_line(0, origin_y_canvas, self.canvas_width, origin_y_canvas, fill="gray", width=2, arrow=tk.LAST)
        self.canvas.create_text(self.canvas_width - 20, origin_y_canvas - 10, text="X", fill="gray", font=("Arial", 10, "bold"))

        self.canvas.create_line(origin_x_canvas, self.canvas_height, origin_x_canvas, 0, fill="gray", width=2, arrow=tk.LAST)
        self.canvas.create_text(origin_x_canvas + 10, 20, text="Y", fill="gray", font=("Arial", 10, "bold"))

    def _draw_line_on_canvas(self, line_obj):
        canvas_x1, canvas_y1 = self.cad_to_canvas(line_obj.start.x, line_obj.start.y)
        canvas_x2, canvas_y2 = self.cad_to_canvas(line_obj.end.x, line_obj.end.y)
        self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue", width=2)

        self._draw_linear_dimension(line_obj.start, line_obj.end, line_obj.length(), "red", obj=line_obj, dim_type="length")

    def _draw_rectangle_on_canvas(self, rect_obj):
        print("Drawing rectangle on canvas.")
        p_bl = Point(min(rect_obj.p1.x, rect_obj.p2.x), min(rect_obj.p1.y, rect_obj.p2.y))
        p_br = Point(max(rect_obj.p1.x, rect_obj.p2.x), min(rect_obj.p1.y, rect_obj.p2.y))
        p_tl = Point(min(rect_obj.p1.x, rect_obj.p2.x), max(rect_obj.p1.y, rect_obj.p2.y))
        p_tr = Point(max(rect_obj.p1.x, rect_obj.p2.x), max(rect_obj.p1.y, rect_obj.p2.y))

        canvas_x1, canvas_y1 = self.cad_to_canvas(p_bl.x, p_tl.y)
        canvas_x2, canvas_y2 = self.cad_to_canvas(p_br.x, p_bl.y)

        self.canvas.create_rectangle(canvas_x1, canvas_y1, canvas_x2, canvas_y2, outline="green", width=2)

        self._draw_linear_dimension(p_bl, p_br, rect_obj.width(), "purple", offset_direction="down", obj=rect_obj, dim_type="width")
        self._draw_linear_dimension(p_bl, p_tl, rect_obj.height(), "purple", offset_direction="left", obj=rect_obj, dim_type="height")

    def _draw_linear_dimension(self, p_start_cad, p_end_cad, value, color, offset_distance=20, offset_direction="auto", obj=None, dim_type=None):
        canvas_x1, canvas_y1 = self.cad_to_canvas(p_start_cad.x, p_start_cad.y)
        canvas_x2, canvas_y2 = self.cad_to_canvas(p_end_cad.x, p_end_cad.y)

        angle = math.atan2(canvas_y2 - canvas_y1, canvas_x2 - canvas_x1)

        if offset_direction == "auto":
            if -math.pi/4 < angle <= math.pi/4:
                offset_dx = 0
                offset_dy = offset_distance
            elif math.pi/4 < angle <= 3*math.pi/4:
                offset_dx = -offset_distance
                offset_dy = 0
            elif -3*math.pi/4 < angle <= -math.pi/4:
                offset_dx = offset_distance
                offset_dy = 0
            else:
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
            offset_dy = offset_distance

        dim_line_x1 = canvas_x1 + offset_dx
        dim_line_y1 = canvas_y1 + offset_dy
        dim_line_x2 = canvas_x2 + offset_dx
        dim_line_y2 = canvas_y2 + offset_dy

        self.canvas.create_line(canvas_x1, canvas_y1, dim_line_x1, dim_line_y1, fill=color, dash=(3, 3))
        self.canvas.create_line(canvas_x2, canvas_y2, dim_line_x2, dim_line_y2, fill=color, dash=(3, 3))

        self.canvas.create_line(dim_line_x1, dim_line_y1, dim_line_x2, dim_line_y2, fill=color, arrow=tk.BOTH, arrowshape=(8, 10, 3))

        text_x = (dim_line_x1 + dim_line_x2) / 2
        text_y = (dim_line_y1 + dim_line_y2) / 2
        
        return self.canvas.create_text(
            text_x, text_y - 10,
            text=f"{value:.2f}",
            fill=color,
            font=("Arial", 10, "bold"),
            tags=("dimension_text", f"obj_{id(obj)}", dim_type)
        )

    def _draw_linear_dimension_preview(self, p_start_cad, p_end_cad, value, color, offset_distance=20, offset_direction="auto"):
        # This is a simplified version for preview, does not bind to object
        canvas_x1, canvas_y1 = self.cad_to_canvas(p_start_cad.x, p_start_cad.y)
        canvas_x2, canvas_y2 = self.cad_to_canvas(p_end_cad.x, p_end_cad.y)

        angle = math.atan2(canvas_y2 - canvas_y1, canvas_x2 - canvas_x1)

        if offset_direction == "auto":
            if -math.pi/4 < angle <= math.pi/4:
                offset_dx = 0
                offset_dy = offset_distance
            elif math.pi/4 < angle <= 3*math.pi/4:
                offset_dx = -offset_distance
                offset_dy = 0
            elif -3*math.pi/4 < angle <= -math.pi/4:
                offset_dx = offset_distance
                offset_dy = 0
            else:
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
            offset_dy = offset_distance

        dim_line_x1 = canvas_x1 + offset_dx
        dim_line_y1 = canvas_y1 + offset_dy
        dim_line_x2 = canvas_x2 + offset_dx
        dim_line_y2 = canvas_y2 + offset_dy

        self.canvas.create_line(canvas_x1, canvas_y1, dim_line_x1, dim_line_y1, fill=color, dash=(3, 3))
        self.canvas.create_line(canvas_x2, canvas_y2, dim_line_x2, dim_line_y2, fill=color, dash=(3, 3))

        self.canvas.create_line(dim_line_x1, dim_line_y1, dim_line_x2, dim_line_y2, fill=color, arrow=tk.BOTH, arrowshape=(8, 10, 3))

        text_x = (dim_line_x1 + dim_line_x2) / 2
        text_y = (dim_line_y1 + dim_line_y2) / 2
        
        return self.canvas.create_text(
            text_x, text_y - 10,
            text=f"{value:.2f}",
            fill=color,
            font=("Arial", 10, "bold")
        )

    def on_dimension_click(self, event):
        item_id = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item_id)
        
        obj_id = None
        dim_type = None
        for tag in tags:
            if tag.startswith("obj_"):
                obj_id = int(tag.split("_")[1])
            elif tag in ["length", "width", "height"]:
                dim_type = tag
        
        if obj_id and dim_type:
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
                    if dim_type == "length" and isinstance(target_obj, Line):
                        target_obj.set_length(new_value)
                    elif dim_type == "width" and isinstance(target_obj, Rectangle):
                        target_obj.set_width(new_value)
                    elif dim_type == "height" and isinstance(target_obj, Rectangle):
                        target_obj.set_height(new_value)
                    
                    self.redraw_all()
            else:
                print(f"Error: Object with ID {obj_id} not found.")
        else:
            print("Clicked item is not a dimension text or missing tags.")

    def draw_line_manual(self):
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

    def draw_rectangle_manual(self):
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

    def activate_interactive_rectangle_drawing(self):
        self.current_drawing_mode = "draw_rectangle_interactive"
        self.interactive_start_point_cad = None
        messagebox.showinfo("Interactive Drawing", "Click on the canvas to define the first corner of the rectangle.")
        # Unbind pan/zoom events temporarily
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")


if __name__ == "__main__":
    root = tk.Tk()
    app = CADApp(root)
    root.mainloop()