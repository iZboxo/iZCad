#!/usr/bin/env python3

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

# Příklad použití (pro testování)
if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    p3 = Point(10, 5)

    line1 = Line(p1, p2)
    line2 = Line(p2, p3)

    print(f"Line 1: {line1}, Length: {line1.length():.2f}")
    print(f"Line 2: {line2}, Length: {line2.length():.2f}")