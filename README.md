# CLI CAD - Graphical Interface

This is a simple Command Line Interface (CLI) CAD tool with a graphical user interface (GUI) built using Python's Tkinter library.

## Features:
- Draw lines by specifying two points.
- Draw rectangles by specifying two opposite corner points.
- Pan (move) the canvas using the left mouse button.
- Zoom in/out using the mouse scroll wheel (zooms towards mouse cursor).
- Display dimensions (length for lines, width/height for rectangles) with extension lines and arrows.
- Edit dimensions interactively: Click on a dimension text to open a dialog and change its value. The geometry of the object will update accordingly.
- **Background Grid:** A visual grid helps with orientation and precise drawing.
- **Origin (X/Y Axes):** Clearly marked X and Y axes provide a reference point.

## How to Run:

1.  **Ensure Python 3 and `python3-tk` are installed.**
    If not, you can install them on Debian/Ubuntu-based systems using:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd your/project/directory
    ```
    (Replace `your/project/directory` with the actual path to the `cli-cad` folder.)

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
    -   Scroll the mouse wheel up to zoom in (towards cursor).
    -   Scroll the mouse wheel down to zoom out (away from cursor).

-   **Editing Dimensions:**
    -   Click on the dimension text (e.g., length of a line, width/height of a rectangle) on the canvas.
    -   A dialog will appear. Enter the new desired value and press Enter.
    -   The object's geometry will update to reflect the new dimension.

-   **Clear Canvas:**
    -   Click the "Clear Canvas" button to remove all drawn objects.

## File Structure:

-   `cad_tool.py`: The main application script containing the GUI and drawing logic.
-   `geometry.py`: Contains the `Point`, `Line`, and `Rectangle` classes defining the geometric entities with dimension editing capabilities.
-   `auto_push.sh`: (Hidden from Git by `.gitignore`) A script for automatic pushing to GitHub (requires `inotify-tools` and Git credential helper setup).
-   `.gitignore`: Specifies files and directories to be ignored by Git.

