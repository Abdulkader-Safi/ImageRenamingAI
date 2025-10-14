"""Image viewer component for displaying images."""

from PIL import Image, ImageTk
from models.config import DEFAULT_DISPLAY_SIZE, IMAGE_DISPLAY_PADDING


class ImageViewer:
    """Handles image display operations."""

    def __init__(self, image_label):
        """Initialize the image viewer.

        Args:
            image_label: The tkinter Label widget to display images in
        """
        self.image_label = image_label
        self.current_image = None

    def display_image(self, filepath):
        """Display an image from the given filepath.

        Args:
            filepath: Path to the image file to display

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open and resize image to fit the display area
            image = Image.open(filepath)

            # Get display area size
            display_width = self.image_label.winfo_width()
            display_height = self.image_label.winfo_height()

            # Use reasonable defaults if window not yet rendered
            if display_width <= 1:
                display_width = DEFAULT_DISPLAY_SIZE
            if display_height <= 1:
                display_height = DEFAULT_DISPLAY_SIZE

            # Calculate resize ratio maintaining aspect ratio
            img_width, img_height = image.size
            ratio = min(display_width / img_width, display_height / img_height)

            new_width = int(img_width * ratio * IMAGE_DISPLAY_PADDING)
            new_height = int(img_height * ratio * IMAGE_DISPLAY_PADDING)

            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Keep a reference to prevent garbage collection
            self.current_image = photo

            # Display image
            self.image_label.config(image=photo, text="")
            return True

        except Exception as e:
            self.image_label.config(text=f"Error loading image: {str(e)}", image="")
            self.current_image = None
            return False

    def clear_image(self):
        """Clear the current image display."""
        self.image_label.config(image="", text="No image selected")
        self.current_image = None

    def show_message(self, message):
        """Show a text message in the image display area.

        Args:
            message: The message to display
        """
        self.image_label.config(text=message, image="")
        self.current_image = None
