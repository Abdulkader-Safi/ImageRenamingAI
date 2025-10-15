"""File handling utilities for image operations."""

import os
from models.config import IMAGE_EXTENSIONS


class FileHandler:
    """Handles file system operations for image files."""

    def __init__(self, directory=None):
        """Initialize the file handler.

        Args:
            directory: The directory path to work with
        """
        self.directory = directory

    def set_directory(self, directory):
        """Set the working directory.

        Args:
            directory: The directory path to set
        """
        self.directory = directory

    def get_image_files(self):
        """Get all image files from the current directory.

        Returns:
            list: List of image filenames

        Raises:
            ValueError: If no directory is set
            OSError: If directory cannot be read
        """
        if not self.directory:
            raise ValueError("No directory set")

        image_files = []
        files = os.listdir(self.directory)

        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                image_files.append(file)

        return sorted(image_files)

    def get_file_path(self, filename):
        """Get the full path for a filename.

        Args:
            filename: The name of the file

        Returns:
            str: Full path to the file

        Raises:
            ValueError: If no directory is set
        """
        if not self.directory:
            raise ValueError("No directory set")

        return os.path.join(self.directory, filename)

    def rename_image(self, old_filename, new_title):
        """Rename an image file with a new title.

        Args:
            old_filename: Current filename
            new_title: New title (without extension)

        Returns:
            str: The new filename

        Raises:
            ValueError: If no directory is set
            OSError: If rename operation fails
        """
        if not self.directory:
            raise ValueError("No directory set")

        # Get the file extension from the old filename
        _, ext = os.path.splitext(old_filename)

        # Create new filename
        new_filename = f"{new_title}{ext}"

        # Handle filename collisions
        counter = 1
        while os.path.exists(os.path.join(self.directory, new_filename)):
            new_filename = f"{new_title}_{counter}{ext}"
            counter += 1

        # Get full paths
        old_path = os.path.join(self.directory, old_filename)
        new_path = os.path.join(self.directory, new_filename)

        # Rename the file
        os.rename(old_path, new_path)

        return new_filename
