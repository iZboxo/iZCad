# CLI CAD - Graphical Interface

This is a simple Command Line Interface (CLI) CAD tool with a graphical user interface (GUI) built using Python's Tkinter library.

## Features:
- Draw lines by specifying two points.
- Draw rectangles by specifying two opposite corner points.
- Pan (move) the canvas using the left mouse button.
- Zoom in/out using the mouse scroll wheel.
- Display dimensions (length for lines, width/height for rectangles).

## How to Run:

1.  **Ensure Python 3 and `python3-tk` are installed.**
    If not, you can install them on Debian/Ubuntu-based systems using:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```

2.  **Navigate to the `cli-cad` directory:**
    ```bash
    cd /home/izboxo/cli-cad
    ```

3.  **Run the application:**
    ```bash
    ./cad_tool.py
    ```

## Usage:

-   **Drawing Lines/Rectangles:**
    1.  Enter the X1, Y1, X2, Y2 coordinates in the input fields.
    2.  Click "Draw Line" to draw a line or "Draw Rectangle" to draw a rectangle.

-   **Panning:**
    -   Click and drag the left mouse button on the canvas to move the view.

-   **Zooming:**
    -   Scroll the mouse wheel up to zoom in.
    -   Scroll the mouse wheel down to zoom out.

-   **Clear Canvas:**
    -   Click the "Clear Canvas" button to remove all drawn objects.

## File Structure:

-   `cad_tool.py`: The main application script containing the GUI and drawing logic.
-   `geometry.py`: Contains the `Point`, `Line`, and `Rectangle` classes defining the geometric entities.
-   `auto_push.sh`: (Hidden from Git by `.gitignore`) A script for automatic pushing to GitHub (requires `inotify-tools` and Git credential helper setup).
-   `.gitignore`: Specifies files and directories to be ignored by Git.

