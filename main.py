"""Main entry point for the Image Viewer application."""

import ttkbootstrap as ttk

from models.config import WINDOW_TITLE, WINDOW_GEOMETRY, THEME_NAME
from ui.main_window import MainWindow


def main():
    """Initialize and run the application."""
    root = ttk.Window(themename=THEME_NAME)
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_GEOMETRY)

    _ = MainWindow(root)  # Keep reference to prevent garbage collection
    root.mainloop()


if __name__ == "__main__":
    main()
