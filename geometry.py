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
