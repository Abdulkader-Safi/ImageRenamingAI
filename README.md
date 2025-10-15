# Image Renaming AI

An intelligent image renaming application powered by local AI vision models. This application uses Ollama's vision-capable models to automatically analyze images and generate descriptive, human-readable filenames.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Ollama](https://img.shields.io/badge/Ollama-Vision_Models-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Project Idea

Have you ever had hundreds of images with cryptic names like `IMG_0001.jpg`, `DSC_1234.jpg`, or `Screenshot_20231015.png`? This application solves that problem by using AI to:

1. **Analyze** the content of each image
2. **Generate** a descriptive, concise filename (max 30 characters)
3. **Rename** the file automatically with meaningful names

Instead of `IMG_0001.jpg`, you get `sunset_beach.jpg`. Instead of `DSC_1234.jpg`, you get `red_sports_car.jpg`. The AI understands what's in your images and creates names that make sense!

## ✨ Features

- **AI-Powered Analysis**: Uses local Ollama vision models for privacy and speed
- **Real-Time Preview**: See AI-generated names as they're created
- **Immediate Updates**: Listbox updates after each rename, not at the end
- **Modern UI**: Built with ttkbootstrap for a sleek, themed interface
- **Batch Processing**: Rename entire directories at once
- **Smart Naming**: Generates concise, filesystem-friendly names
- **Collision Handling**: Automatically handles duplicate names
- **Progress Tracking**: Visual feedback during processing
- **Model Selection**: Choose from multiple installed vision models
- **Error Handling**: Graceful recovery from processing failures

## 🖥️ Screenshots

```overview
┌─────────────────────────────────────────────────────────────────┐
│ [Select Directory] [AI Rename Images] Model: [llava ▼] | Ready  │
├─────────────────┬───────────────────────────────────────────────┤
│ Images:         │ Preview:                                      │
│                 │                                               │
│ IMG_001.jpg     │ AI Generated Name:                            │
│ IMG_002.jpg     │ ┌────────────────────────────────────────────┐│
│ IMG_003.jpg     │ │ ✓ Generated: sunset_beach                  ││
│ IMG_004.jpg     │ └────────────────────────────────────────────┘│
│ IMG_005.jpg     │                                               │
│                 │ [Image preview area]                          │
│                 │                                               │
└─────────────────┴───────────────────────────────────────────────┘
```

## Getting Started

### Prerequisites

1. **Python 3.8 or higher**

   ```bash
   python --version
   ```

2. **Ollama** (for running AI models locally)

   - Download and install from [ollama.com](https://ollama.com)
   - Or use: `curl -fsSL https://ollama.com/install.sh | sh` (Linux/macOS)

3. **Git** (for cloning the repository)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ImageRenamingAI.git
   cd ImageRenamingAI
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

4. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Required packages:

   - `ttkbootstrap` - Modern themed tkinter UI
   - `Pillow` - Image processing
   - `ollama` - Ollama Python client

5. **Install a vision-capable Ollama model**

   ⚠️ **Important**: This application requires a **vision model** that can analyze images. Standard text-only models like `mistral`, `llama2`, or `llama3.2` will NOT work.

   **Recommended (Best Quality/Performance Balance):**

   ```bash
   ollama pull llama3.2-vision
   ```

   Requires: ~8GB VRAM | Best balance of speed and accuracy

   **Alternative Options:**

   ```bash
   # LLaVA - Good general purpose
   ollama pull llava            # 7B model, ~6GB VRAM
   ollama pull llava:13b        # 13B model, ~10GB VRAM, better quality
   ollama pull llava:34b        # 34B model, ~20GB VRAM, excellent quality

   # Other options
   ollama pull bakllava         # Lighter alternative, ~4GB VRAM
   ollama pull moondream        # Very fast and small, ~2GB VRAM
   ollama pull qwen2-vl         # Qwen's vision model
   ```

## Usage

### Running the Application

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

### Step-by-Step Guide

1. **Launch the application**

   ```bash
   python main.py
   ```

2. **Select your vision model**

   - Check the "Model:" dropdown at the top
   - Should show your installed vision model (e.g., `llava:latest`)
   - If empty, see [Troubleshooting](#-troubleshooting)

3. **Load images**

   - Click **"Select Directory"**
   - Choose a folder containing images
   - Images will appear in the left listbox

4. **Start AI renaming**

   - Click **"AI Rename Images"**
   - Watch the magic happen! 🎉

5. **Observe the process**

   - 🖼️ Each image is selected and displayed
   - ⏳ Preview box shows "Analyzing..."
   - ✓ AI-generated name appears in green
   - 📝 Filename updates in the listbox immediately
   - 🔄 Moves to the next image automatically

6. **Check results**
   - All images are renamed with descriptive names
   - Original extensions are preserved
   - Completion summary shows success/failure count

### Example Transformation

**Before:**

- IMG_0001.jpg
- IMG_0002.jpg
- DSC_1234.jpg
- Screenshot_20231015.png

**After:**

- sunset_beach.jpg
- golden_retriever_playing.jpg
- red_sports_car_highway.jpg
- code_editor_screenshot.png

## Project Structure

```folders
ImageRenamingAI/
├── main.py                      # Application entry point
├── models/
│   ├── __init__.py
│   ├── ai_service.py           # Ollama AI integration
│   └── config.py               # Configuration constants
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # Main application window
│   └── image_viewer.py         # Image display component
├── utils/
│   ├── __init__.py
│   └── file_handler.py         # File operations
├── test_vision_models.py       # Diagnostic tool
├── test_ai_service.py          # Connection test
├── VISION_MODELS_GUIDE.md      # Detailed guide
├── CLAUDE.md                   # Development documentation
└── README.md                   # This file
```

## Configuration

You can customize the application by editing [models/config.py](models/config.py):

```python
# Window settings
WINDOW_TITLE = "Image Viewer"
WINDOW_GEOMETRY = "1000x700"
THEME_NAME = "cyborg"  # ttkbootstrap theme

# Supported image formats
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff")

# AI settings
DEFAULT_OLLAMA_MODEL = "llama3.2-vision:latest"
MAX_TITLE_LENGTH = 30  # Maximum filename length
```

## 🎨 Available Themes

Change the `THEME_NAME` in config.py to any ttkbootstrap theme:

- `cyborg` (dark, default)
- `darkly` (dark)
- `solar` (dark)
- `superhero` (dark)
- `flatly` (light)
- `cosmo` (light)
- `journal` (light)
- `litera` (light)

## 🔧 Troubleshooting

### No Vision Models Found

**Symptom:** App shows "⚠ No vision models! Install: ollama pull llama3.2-vision"

**Solution:**

```bash
# Install a vision model
ollama pull llama3.2-vision

# Restart the application
python main.py
```

### Filenames Like "im*sorry_but_i_cant*..."

**Problem:** You're using a text-only model that can't process images

**Solution:** Install a vision model:

```bash
ollama pull llava
```

See [VISION_MODELS_GUIDE.md](VISION_MODELS_GUIDE.md) for detailed explanation.

### Ollama Connection Error

**Symptom:** "Could not connect to Ollama"

**Solution:**

```bash
# Make sure Ollama is running
ollama serve

# Or restart Ollama service
```

### Images Not Loading

**Supported formats:**

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)
- TIFF (.tiff)

If your images don't appear, check the file extension.

### Application Freezes

The UI uses threading to stay responsive. If it freezes:

1. Check if Ollama is responding: `ollama list`
2. Try a lighter model: `ollama pull moondream`
3. Reduce image resolution if very large files

## Testing

### Test Vision Model Detection

```bash
python test_vision_models.py
```

Shows which models are vision-capable vs text-only.

### Test Ollama Connection

```bash
python test_ai_service.py
```

Verifies Ollama service is running and accessible.

### Verify Installation

```bash
python -c "from ui.main_window import MainWindow; print('✓ All imports successful')"
```

## Performance Comparison

| Model               | VRAM   | Speed     | Quality   | Best For               |
| ------------------- | ------ | --------- | --------- | ---------------------- |
| moondream           | 2-4 GB | Very Fast | Good      | Quick batch processing |
| llava:7b            | 4-6 GB | Fast      | Good      | General use            |
| llama3.2-vision     | 8 GB   | Medium    | Excellent | **Recommended**        |
| llava:13b           | 10 GB  | Medium    | Very Good | High quality           |
| llava:34b           | 20 GB  | Slow      | Excellent | Best quality           |
| llama3.2-vision:90b | 64 GB  | Very Slow | Best      | Maximum accuracy       |

## Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add undo/redo functionality
- [ ] Support for video files
- [ ] Custom naming templates
- [ ] Batch export of rename logs
- [ ] Multi-language support
- [ ] Cloud model integration (OpenAI, Anthropic)
- [ ] Image tagging/categorization
- [ ] Duplicate image detection

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Ollama** - For making local AI accessible
- **Meta** - For LLaMA models
- **Haotian Liu et al.** - For LLaVA models
- **ttkbootstrap** - For the modern UI framework
- **Pillow** - For image processing capabilities

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ImageRenamingAI/issues)
- **Model Help**: [Ollama Library](https://ollama.com/library)

## Roadmap

### Version 1.0 (Current)

- Basic image renaming with AI
- Real-time preview
- Multiple model support
- Error handling

### Version 1.1 (Planned)

- Undo/redo functionality
- Custom naming patterns
- Batch processing history
- Image metadata preservation

### Version 2.0 (Future)

- Video file support
- Cloud model integration
- Advanced filtering/search
- Automated organization

## Tips for Best Results

1. **Use high-quality images** - Better input = better names
2. **Choose the right model** - Balance speed vs accuracy for your needs
3. **Process in batches** - Group similar images together
4. **Review generated names** - AI is good but not perfect
5. **Keep backups** - Always backup originals before batch renaming

## Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ and AI** | Powered by [Abdulkader Safi](https://abdulkadersafi.com)
