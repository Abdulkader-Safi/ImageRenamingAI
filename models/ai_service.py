"""AI service for image analysis using Ollama."""

import base64
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

            # Detect if model doesn't support vision (common error responses)
            error_indicators = [
                "sorry",
                "can't",
                "cannot",
                "unable",
                "don't have",
                "no image",
                "as an ai",
                "language model",
            ]
            title_lower = title.lower()
            if any(indicator in title_lower for indicator in error_indicators):
                raise Exception(
                    f"Model '{self.model_name}' appears to not support vision. "
                    f"Response: {title[:100]}... "
                    f"Please use a vision-capable model like llama3.2-vision, llava, etc."
                )

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
        """Get list of available vision-capable Ollama models installed locally.

        Only returns models that support image analysis (multimodal models).
        Text-only models like standard mistral, llama2, llama3.2 are filtered out.

        Returns:
            list[str]: List of vision-capable model names, or empty list if none available
        """
        # Known vision-capable model identifiers
        VISION_MODELS = [
            "llama3.2-vision",
            "llama4",  # Llama 4 models are multimodal
            "llava",
            "bakllava",
            "qwen2-vl",
            "qwen-vl",
            "mistral-small",  # Mistral Small 3.1 has vision
            "pixtral",  # Mistral's vision model
            "moondream",
            "cogvlm",
        ]

        try:
            all_models = ollama.list()
            if not all_models or not all_models.models:
                return []

            model_names = [m.model for m in all_models.models]

            # Filter to only vision-capable models
            vision_models = []
            for model in model_names:
                if model is not None:
                    model_lower = model.lower()
                    # Check if model name contains any vision model identifier
                    if any(vision_id in model_lower for vision_id in VISION_MODELS):
                        vision_models.append(model)

            return vision_models
        except Exception:
            return []
