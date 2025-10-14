import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, RIGHT, BOTH, TOP, PRIMARY, INFO, OUTLINE
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("1000x700")

        self.current_directory = None
        self.image_files = []
        self.current_image = None

        # Supported image extensions
        self.image_extensions = (
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".webp",
            ".tiff",
        )

        self.create_widgets()

    def create_widgets(self):
        # Top frame with 3 buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=TOP, fill=tk.X, padx=10, pady=10)

        # Button 1: Select Directory
        self.btn_select_dir = ttk.Button(
            button_frame,
            text="Select Directory",
            bootstyle=PRIMARY,  # type: ignore
            command=self.select_directory,
        )
        self.btn_select_dir.pack(side=LEFT, padx=5)

        # Button 2: Placeholder
        self.btn2 = ttk.Button(
            button_frame, text="Button 2", bootstyle=(INFO, OUTLINE)  # type: ignore
        )
        self.btn2.pack(side=LEFT, padx=5)

        # Button 3: Placeholder
        self.btn3 = ttk.Button(
            button_frame, text="Button 3", bootstyle=(INFO, OUTLINE)  # type: ignore
        )
        self.btn3.pack(side=LEFT, padx=5)

        # Main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)

        # Left side: Image list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=LEFT, fill=BOTH, padx=(0, 5))

        ttk.Label(left_frame, text="Images:", font=("Helvetica", 12, "bold")).pack(
            anchor=tk.W
        )

        # Listbox with scrollbar
        list_scroll = ttk.Scrollbar(left_frame)
        list_scroll.pack(side=RIGHT, fill=tk.Y)

        self.image_listbox = tk.Listbox(
            left_frame, yscrollcommand=list_scroll.set, width=25, height=30
        )
        self.image_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        list_scroll.config(command=self.image_listbox.yview)

        # Bind selection event
        self.image_listbox.bind("<<ListboxSelect>>", self.on_image_select)

        # Right side: Image display
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        ttk.Label(right_frame, text="Preview:", font=("Helvetica", 12, "bold")).pack(
            anchor=tk.W
        )

        # Image display label
        self.image_label = ttk.Label(
            right_frame, text="No image selected", anchor="center"
        )
        self.image_label.pack(fill=BOTH, expand=True, pady=10)

    def select_directory(self):
        """Open dialog to select directory and load images"""
        directory = filedialog.askdirectory(title="Select Image Directory")

        if directory:
            self.current_directory = directory
            self.load_images()

    def load_images(self):
        """Load all image files from the selected directory"""
        if not self.current_directory:
            return

        # Clear previous list
        self.image_listbox.delete(0, tk.END)
        self.image_files = []

        try:
            # Get all files in directory
            files = os.listdir(self.current_directory)

            # Filter only image files
            for file in files:
                if file.lower().endswith(self.image_extensions):
                    self.image_files.append(file)
                    self.image_listbox.insert(tk.END, file)

            # Update window title with directory path
            self.root.title(f"Image Viewer - {self.current_directory}")

            if not self.image_files:
                self.image_label.config(
                    text="No images found in this directory", image=""
                )

        except Exception as e:
            self.image_label.config(text=f"Error loading directory: {str(e)}", image="")

    def on_image_select(self, event):  # noqa: ARG002
        """Handle image selection from the list"""
        selection = self.image_listbox.curselection()

        if not selection or not self.current_directory:
            return

        index = selection[0]
        filename = self.image_files[index]
        filepath = os.path.join(self.current_directory, filename)

        self.display_image(filepath)

    def display_image(self, filepath):
        """Display the selected image"""
        try:
            # Open and resize image to fit the display area
            image = Image.open(filepath)

            # Get display area size
            display_width = self.image_label.winfo_width()
            display_height = self.image_label.winfo_height()

            # Use reasonable defaults if window not yet rendered
            if display_width <= 1:
                display_width = 600
            if display_height <= 1:
                display_height = 600

            # Calculate resize ratio maintaining aspect ratio
            img_width, img_height = image.size
            ratio = min(display_width / img_width, display_height / img_height)

            new_width = int(img_width * ratio * 0.95)  # 95% to add some padding
            new_height = int(img_height * ratio * 0.95)

            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Keep a reference to prevent garbage collection
            self.current_image = photo

            # Display image
            self.image_label.config(image=photo, text="")

        except Exception as e:
            self.image_label.config(text=f"Error loading image: {str(e)}", image="")


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = ImageViewerApp(root)
    root.mainloop()
