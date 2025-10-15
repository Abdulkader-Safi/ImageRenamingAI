"""Main window UI components and layout."""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    LEFT,
    RIGHT,
    BOTH,
    TOP,
    PRIMARY,
    INFO,
    OUTLINE,
    SUCCESS,
)
from tkinter import filedialog
import threading

from models.config import (
    LISTBOX_WIDTH,
    LISTBOX_HEIGHT,
    DEFAULT_OLLAMA_MODEL,
    MAX_TITLE_LENGTH,
)
from ui.image_viewer import ImageViewer
from utils.file_handler import FileHandler
from models.ai_service import OllamaService


class MainWindow:
    """Main application window with UI components."""

    def __init__(self, root):
        """Initialize the main window.

        Args:
            root: The root tkinter window
        """
        self.root = root
        self.file_handler = FileHandler()
        self.image_files: list[str] = []
        self.is_processing = False

        # UI components - will be initialized in _create_widgets
        self.image_listbox: tk.Listbox
        self.image_label: ttk.Label
        self.image_viewer: ImageViewer
        self.status_label: ttk.Label
        self.btn_ai_rename: ttk.Button
        self.model_combo: ttk.Combobox
        self.name_preview_text: tk.Text

        self._create_widgets()

    def _create_widgets(self):
        """Create and layout all UI widgets."""
        self._create_button_frame()
        self._create_content_frame()

    def _create_button_frame(self):
        """Create the top button frame with action buttons."""
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

        # Button 2: AI Rename Images
        self.btn_ai_rename = ttk.Button(
            button_frame,
            text="AI Rename Images",
            bootstyle=SUCCESS,  # type: ignore
            command=self.start_ai_rename,
        )
        self.btn_ai_rename.pack(side=LEFT, padx=5)

        # Button 3: AI Rename Selected Image
        self.btn3 = ttk.Button(
            button_frame,
            text="AI Rename Selected",
            bootstyle=(INFO, OUTLINE),  # type: ignore
            command=self.start_ai_rename_selected,
        )
        self.btn3.pack(side=LEFT, padx=5)

        # Model selection dropdown
        ttk.Label(button_frame, text="Model:", font=("Helvetica", 10)).pack(
            side=LEFT, padx=(20, 5)
        )

        self.model_combo = ttk.Combobox(
            button_frame,
            state="readonly",
            width=20,
        )
        self.model_combo.pack(side=LEFT, padx=5)

        # Status label (create before loading models so it can be updated)
        self.status_label = ttk.Label(
            button_frame, text="Ready", font=("Helvetica", 10)
        )
        self.status_label.pack(side=LEFT, padx=20)

        # Load available models (this will update status_label)
        self._load_available_models()

    def _create_content_frame(self):
        """Create the main content frame with image list and preview."""
        content_frame = ttk.Frame(self.root)
        content_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)

        self._create_left_panel(content_frame)
        self._create_right_panel(content_frame)

    def _create_left_panel(self, parent):
        """Create the left panel with image list.

        Args:
            parent: The parent frame to attach to
        """
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=LEFT, fill=BOTH, padx=(0, 5))

        ttk.Label(left_frame, text="Images:", font=("Helvetica", 12, "bold")).pack(
            anchor=tk.W
        )

        # Listbox with scrollbar
        list_scroll = ttk.Scrollbar(left_frame)
        list_scroll.pack(side=RIGHT, fill=tk.Y)

        self.image_listbox = tk.Listbox(
            left_frame,
            yscrollcommand=list_scroll.set,
            width=LISTBOX_WIDTH,
            height=LISTBOX_HEIGHT,
        )
        self.image_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        list_scroll.config(command=self.image_listbox.yview)

        # Bind selection event
        self.image_listbox.bind("<<ListboxSelect>>", self.on_image_select)

    def _create_right_panel(self, parent):
        """Create the right panel with image preview.

        Args:
            parent: The parent frame to attach to
        """
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        ttk.Label(right_frame, text="Preview:", font=("Helvetica", 12, "bold")).pack(
            anchor=tk.W
        )

        # AI-generated name preview box
        preview_frame = ttk.Frame(right_frame)
        preview_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            preview_frame, text="AI Generated Name:", font=("Helvetica", 10)
        ).pack(anchor=tk.W)

        self.name_preview_text = tk.Text(
            preview_frame,
            height=2,
            wrap=tk.WORD,
            font=("Helvetica", 11, "bold"),
            bg="#2b2b2b",
            fg="#00ff00",
            relief=tk.FLAT,
            padx=10,
            pady=8,
        )
        self.name_preview_text.pack(fill=tk.X)
        self.name_preview_text.insert("1.0", "Ready to process images...")
        self.name_preview_text.config(state=tk.DISABLED)

        # Image display label
        self.image_label = ttk.Label(
            right_frame, text="No image selected", anchor="center"
        )
        self.image_label.pack(fill=BOTH, expand=True, pady=10)

        # Initialize image viewer
        self.image_viewer = ImageViewer(self.image_label)

    def _load_available_models(self):
        """Load available vision-capable Ollama models into the dropdown."""
        models = OllamaService.get_available_models()

        if models:
            self.model_combo["values"] = models
            # Try to select the default model, or first available
            if DEFAULT_OLLAMA_MODEL in models:
                self.model_combo.set(DEFAULT_OLLAMA_MODEL)
            else:
                self.model_combo.current(0)
            self.status_label.config(text=f"Found {len(models)} vision model(s)")
        else:
            # No vision models found - provide helpful guidance
            self.model_combo["values"] = ["No vision models installed"]
            self.model_combo.current(0)
            self.model_combo.config(state="disabled")
            self.btn_ai_rename.config(state="disabled")
            self.status_label.config(
                text="⚠ No vision models! Install: ollama pull llama3.2-vision"
            )

    def select_directory(self):
        """Open dialog to select directory and load images."""
        directory = filedialog.askdirectory(title="Select Image Directory")

        if directory:
            self.file_handler.set_directory(directory)
            self.load_images()
            self.root.title(f"Image Viewer - {directory}")

    def load_images(self):
        """Load all image files from the selected directory."""
        # Clear previous list
        self.image_listbox.delete(0, tk.END)
        self.image_files = []

        try:
            # Get all image files
            self.image_files = self.file_handler.get_image_files()

            # Populate listbox
            for file in self.image_files:
                self.image_listbox.insert(tk.END, file)

            if not self.image_files:
                self.image_viewer.show_message("No images found in this directory")

        except Exception as e:
            self.image_viewer.show_message(f"Error loading directory: {str(e)}")

    def on_image_select(self, event):  # noqa: ARG002
        """Handle image selection from the list.

        Args:
            event: The tkinter event (unused)
        """
        selection = self.image_listbox.curselection()

        if not selection or not self.image_files:
            return

        index = selection[0]
        filename = self.image_files[index]

        try:
            filepath = self.file_handler.get_file_path(filename)
            self.image_viewer.display_image(filepath)
        except Exception as e:
            self.image_viewer.show_message(f"Error: {str(e)}")

    def start_ai_rename(self):
        """Start the AI-powered image renaming process."""
        if self.is_processing:
            return

        if not self.image_files:
            self.status_label.config(text="No images loaded!")
            return

        # Get selected model
        selected_model = self.model_combo.get()
        if not selected_model:
            self.status_label.config(text="Please select a model!")
            return

        # Disable buttons and dropdown during processing
        self.is_processing = True
        self.btn_ai_rename.config(state="disabled")
        self.btn_select_dir.config(state="disabled")
        self.model_combo.config(state="disabled")

        # Start processing in a separate thread to keep UI responsive
        thread = threading.Thread(
            target=self._process_images, args=(selected_model,), daemon=True
        )
        thread.start()

    def start_ai_rename_selected(self):
        """Start the AI-powered renaming process for the selected image only."""
        if self.is_processing:
            return

        if not self.image_files:
            self.status_label.config(text="No images loaded!")
            return

        # Check if an image is selected
        selection = self.image_listbox.curselection()
        if not selection:
            self.status_label.config(text="Please select an image first!")
            return

        # Get selected model
        selected_model = self.model_combo.get()
        if not selected_model:
            self.status_label.config(text="Please select a model!")
            return

        # Disable buttons and dropdown during processing
        self.is_processing = True
        self.btn_ai_rename.config(state="disabled")
        self.btn3.config(state="disabled")
        self.btn_select_dir.config(state="disabled")
        self.model_combo.config(state="disabled")

        # Get selected index
        selected_index = selection[0]

        # Start processing in a separate thread to keep UI responsive
        thread = threading.Thread(
            target=self._process_single_image,
            args=(selected_model, selected_index),
            daemon=True,
        )
        thread.start()

    def _process_images(self, model_name):
        """Process all images with AI (runs in separate thread).

        Args:
            model_name: The Ollama model to use for processing
        """
        # Create AI service with selected model
        ai_service = OllamaService(model_name, MAX_TITLE_LENGTH)

        total_images = len(self.image_files)
        renamed_count = 0
        failed_count = 0

        for index, filename in enumerate(self.image_files[:], 1):
            try:
                # Update status
                self.root.after(
                    0,
                    lambda i=index, t=total_images: self.status_label.config(
                        text=f"Processing {i}/{t}..."
                    ),
                )

                # Select and display the current image
                self.root.after(0, lambda idx=index - 1: self._select_image(idx))

                # Show "Analyzing..." in preview box
                self.root.after(
                    0,
                    lambda f=filename: self._update_name_preview(
                        f"Analyzing: {f}\n⏳ Generating name..."
                    ),
                )

                # Get full filepath
                filepath = self.file_handler.get_file_path(filename)

                # Generate title using AI
                new_title = ai_service.generate_title(filepath)

                # Show generated name in preview box
                self.root.after(
                    0,
                    lambda nt=new_title: self._update_name_preview(
                        f"✓ Generated: {nt}"
                    ),
                )

                # Rename the file
                new_filename = self.file_handler.rename_image(filename, new_title)

                # Update the image_files list
                self.image_files[index - 1] = new_filename

                # Update the listbox immediately with the new name
                self.root.after(
                    0,
                    lambda idx=index - 1, nf=new_filename: self._update_listbox_item(
                        idx, nf
                    ),
                )

                renamed_count += 1

            except Exception as e:
                error_msg = str(e)
                print(f"Error processing {filename}: {error_msg}")
                self.root.after(
                    0,
                    lambda err=error_msg: self._update_name_preview(f"❌ Error: {err}"),
                )
                failed_count += 1
                continue

        # Reload the image list to show new names
        self.root.after(0, self._finalize_rename, renamed_count, failed_count)

    def _process_single_image(self, model_name, image_index):
        """Process a single selected image with AI (runs in separate thread).

        Args:
            model_name: The Ollama model to use for processing
            image_index: The index of the image to process
        """
        # Create AI service with selected model
        ai_service = OllamaService(model_name, MAX_TITLE_LENGTH)

        try:
            filename = self.image_files[image_index]

            # Update status
            self.root.after(
                0,
                lambda: self.status_label.config(text="Processing selected image..."),
            )

            # Show "Analyzing..." in preview box
            self.root.after(
                0,
                lambda: self._update_name_preview(
                    f"Analyzing: {filename}\n⏳ Generating name..."
                ),
            )

            # Get full filepath
            filepath = self.file_handler.get_file_path(filename)

            # Generate title using AI
            new_title = ai_service.generate_title(filepath)

            # Show generated name in preview box
            self.root.after(
                0,
                lambda: self._update_name_preview(f"✓ Generated: {new_title}"),
            )

            # Rename the file
            new_filename = self.file_handler.rename_image(filename, new_title)

            # Update the image_files list
            self.image_files[image_index] = new_filename

            # Update the listbox immediately with the new name
            self.root.after(
                0,
                lambda: self._update_listbox_item(image_index, new_filename),
            )

            # Update status with success message
            self.root.after(
                0,
                lambda: self.status_label.config(
                    text=f"Successfully renamed to: {new_title}"
                ),
            )

        except Exception as e:
            error_msg = str(e)
            print(f"Error processing image: {error_msg}")
            self.root.after(
                0,
                lambda: self._update_name_preview(f"❌ Error: {error_msg}"),
            )
            self.root.after(
                0,
                lambda: self.status_label.config(text=f"Error: {error_msg}"),
            )

        finally:
            # Re-enable buttons and dropdown
            self.root.after(0, self._finalize_single_rename)

    def _finalize_single_rename(self):
        """Re-enable UI controls after processing a single image."""
        self.btn_ai_rename.config(state="normal")
        self.btn3.config(state="normal")
        self.btn_select_dir.config(state="normal")
        self.model_combo.config(state="readonly")
        self.is_processing = False

    def _select_image(self, index):
        """Select an image in the listbox programmatically.

        Args:
            index: The index of the image to select
        """
        self.image_listbox.selection_clear(0, tk.END)
        self.image_listbox.selection_set(index)
        self.image_listbox.see(index)

        # Trigger display
        if index < len(self.image_files):
            filename = self.image_files[index]
            try:
                filepath = self.file_handler.get_file_path(filename)
                self.image_viewer.display_image(filepath)
            except Exception as e:
                print(f"Error displaying image: {str(e)}")

    def _update_name_preview(self, text):
        """Update the AI-generated name preview text box.

        Args:
            text: The text to display in the preview box
        """
        self.name_preview_text.config(state=tk.NORMAL)
        self.name_preview_text.delete("1.0", tk.END)
        self.name_preview_text.insert("1.0", text)
        self.name_preview_text.config(state=tk.DISABLED)

    def _update_listbox_item(self, index, new_filename):
        """Update a single item in the listbox with new filename.

        Args:
            index: The index of the item to update
            new_filename: The new filename to display
        """
        if 0 <= index < self.image_listbox.size():
            self.image_listbox.delete(index)
            self.image_listbox.insert(index, new_filename)
            self.image_listbox.selection_set(index)
            self.image_listbox.see(index)

    def _finalize_rename(self, renamed_count, failed_count):
        """Finalize the rename process and update UI.

        Args:
            renamed_count: Number of successfully renamed images
            failed_count: Number of failed renames
        """
        # Update status
        status_text = f"Complete! Renamed: {renamed_count}"
        if failed_count > 0:
            status_text += f", Failed: {failed_count}"
        self.status_label.config(text=status_text)

        # Update preview box with completion message
        preview_text = f"✅ Processing Complete!\nRenamed: {renamed_count}"
        if failed_count > 0:
            preview_text += f"\nFailed: {failed_count}"
        self._update_name_preview(preview_text)

        # Re-enable buttons and dropdown
        self.btn_ai_rename.config(state="normal")
        self.btn_select_dir.config(state="normal")
        self.model_combo.config(state="readonly")
        self.is_processing = False
