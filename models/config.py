"""Configuration constants for the Image Viewer application."""

# Window settings
WINDOW_TITLE = "Image Viewer"
WINDOW_GEOMETRY = "1000x700"
THEME_NAME = "cyborg"

# Supported image extensions
IMAGE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff",
)

# UI settings
LISTBOX_WIDTH = 25
LISTBOX_HEIGHT = 30
IMAGE_DISPLAY_PADDING = 0.95  # 95% to add some padding
DEFAULT_DISPLAY_SIZE = 600

# AI settings
DEFAULT_OLLAMA_MODEL = "mistral:latest"  # Fallback if model list fails to load
MAX_TITLE_LENGTH = 30
