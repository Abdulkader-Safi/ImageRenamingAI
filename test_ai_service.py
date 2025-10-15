"""Test script for AI service functionality."""

from models.ai_service import OllamaService

def test_connection():
    """Test Ollama service connection."""
    service = OllamaService("mistral", 30)

    print("Testing Ollama connection...")
    if service.test_connection():
        print("✓ Connection successful!")
        return True
    else:
        print("✗ Connection failed. Make sure Ollama is running.")
        return False

if __name__ == "__main__":
    test_connection()
