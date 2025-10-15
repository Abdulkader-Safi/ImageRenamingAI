"""AI service for image analysis using Ollama."""

import base64
from pathlib import Path
import ollama
from ollama import chat


class OllamaService:
    """Handles AI-powered image analysis using Ollama models."""

    def __init__(self, model_name="mistral", max_title_length=30):
        """Initialize the Ollama service.

        Args:
            model_name: Name of the Ollama model to use
            max_title_length: Maximum length for generated titles
        """
        self.model_name = model_name
        self.max_title_length = max_title_length

    def _encode_image(self, image_path):
        """Encode image to base64 for Ollama.

        Args:
            image_path: Path to the image file

        Returns:
            bytes: Base64 encoded image data
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def generate_title(self, image_path):
        """Generate a descriptive title for an image.

        Args:
            image_path: Path to the image file

        Returns:
            str: Generated title for the image (max 30 chars)

        Raises:
            Exception: If the Ollama service fails
        """
        try:
            # Encode image
            image_base64 = self._encode_image(image_path)

            # Create prompt for concise title generation
            prompt = (
                f"Analyze this image and provide ONLY a very short descriptive title "
                f"(maximum {self.max_title_length} characters). "
                f"Be concise, use lowercase with underscores instead of spaces. "
                f"Examples: 'sunset_beach', 'red_car_highway', 'cat_sleeping'. "
                f"Do not include punctuation or file extensions. "
                f"Respond with ONLY the title, nothing else."
            )

            # Send to Ollama
            response = chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_base64],
                    }
                ],
            )

            # Extract and clean the title
            title = response["message"]["content"].strip()

            # Remove quotes if present
            title = title.strip("'\"")

            # Sanitize: lowercase, replace spaces with underscores
            title = title.lower().replace(" ", "_")

            # Remove any non-alphanumeric characters except underscores
            title = "".join(c for c in title if c.isalnum() or c == "_")

            # Truncate to max length
            if len(title) > self.max_title_length:
                title = title[: self.max_title_length]

            # Ensure title is not empty
            if not title:
                title = "unnamed_image"

            return title

        except Exception as e:
            raise Exception(f"Failed to generate title: {str(e)}") from e

    def test_connection(self):
        """Test if Ollama service is available.

        Returns:
            bool: True if service is available, False otherwise
        """
        try:
            # Try a simple chat without image
            response = chat(
                model=self.model_name,
                messages=[{"role": "user", "content": "test"}],
            )
            return response is not None
        except Exception:
            return False

    @staticmethod
    def get_available_models():
        """Get list of available Ollama models installed locally.

        Returns:
            list[str]: List of model names, or empty list if Ollama is unavailable
        """
        try:
            models = ollama.list()
            return [m.model for m in models.models]
        except Exception:
            return []
