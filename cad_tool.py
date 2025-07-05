#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Line:
    def __init__(self, start_point, end_point):
        if not isinstance(start_point, Point) or not isinstance(end_point, Point):
            raise ValueError("Start and end points must be instances of Point.")
        self.start = start_point
        self.end = end_point

    def __repr__(self):
        return f"Line({self.start}, {self.end})"

    def length(self):
        return ((self.end.x - self.start.x)**2 + (self.end.y - self.start.y)**2)**0.5

class CADApp:
    def __init__(self, master):
        self.master = master
        master.title("CLI CAD - Grafické rozhraní")

        self.canvas_width = 600
        self.canvas_height = 400
        self.scale = 10 # 1 unit in CAD = 10 pixels on canvas
        self.offset_x = self.canvas_width / 2 # Center origin
        self.offset_y = self.canvas_height / 2 # Center origin

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white", borderwidth=2, relief="groove")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

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
        self.y2_entry.insert(0, "0")

        self.draw_button = tk.Button(self.input_frame, text="Nakreslit čáru", command=self.draw_line)
        self.draw_button.grid(row=2, column=0, columnspan=4, pady=10)

        self.lines = [] # Store drawn lines

    def cad_to_canvas(self, x_cad, y_cad):
        # Convert CAD coordinates to canvas pixel coordinates
        x_canvas = self.offset_x + x_cad * self.scale
        y_canvas = self.offset_y - y_cad * self.scale # Y-axis is inverted in canvas
        return x_canvas, y_canvas

    def draw_line(self):
        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Chyba vstupu", "Prosím zadejte platná čísla pro souřadnice.")
            return

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        self.lines.append(line)

        # Convert CAD coordinates to canvas coordinates
        canvas_x1, canvas_y1 = self.cad_to_canvas(p1.x, p1.y)
        canvas_x2, canvas_y2 = self.cad_to_canvas(p2.x, p2.y)

        # Draw the line on canvas
        self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue", width=2)

        # Display dimension (length)
        mid_x = (canvas_x1 + canvas_x2) / 2
        mid_y = (canvas_y1 + canvas_y2) / 2
        length_text = f"{line.length():.2f}"
        self.canvas.create_text(mid_x, mid_y - 10, text=length_text, fill="red", font=("Arial", 10, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = CADApp(root)
    root.mainloop()
