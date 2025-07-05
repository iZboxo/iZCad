import math

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

    def set_length(self, new_length):
        if self.length() == 0: # Avoid division by zero if line has no length
            if new_length == 0:
                return # Nothing to do
            else: # Line has no length, but new_length is not zero. Extend in X direction.
                self.end.x = self.start.x + new_length
                self.end.y = self.start.y
                return

        current_length = self.length()
        if current_length == new_length:
            return # No change needed

        # Calculate direction vector
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y

        # Calculate new end point based on new length
        ratio = new_length / current_length
        self.end.x = self.start.x + dx * ratio
        self.end.y = self.start.y + dy * ratio

class Rectangle:
    def __init__(self, p1, p2):
        if not isinstance(p1, Point) or not isinstance(p2, Point):
            raise ValueError("Corner points must be instances of Point.")
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Rectangle({self.p1}, {self.p2})"

    def width(self):
        return abs(self.p2.x - self.p1.x)

    def height(self):
        return abs(self.p2.y - self.p1.y)

    def set_width(self, new_width):
        # Adjust p2.x based on p1.x and new_width
        if self.p2.x >= self.p1.x:
            self.p2.x = self.p1.x + new_width
        else:
            self.p2.x = self.p1.x - new_width

    def set_height(self, new_height):
        # Adjust p2.y based on p1.y and new_height
        if self.p2.y >= self.p1.y:
            self.p2.y = self.p1.y + new_height
        else:
            self.p2.y = self.p1.y - new_height