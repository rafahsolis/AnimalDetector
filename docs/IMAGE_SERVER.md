# Image Server Documentation

## Overview

The Image Server is a lightweight HTTP server for browsing, viewing, and managing image files. It provides a clean web interface to navigate through image directories with keyboard shortcuts and delete functionality.

## Features

- **Grid Gallery View**: Browse all images in a directory with thumbnail previews
- **Full Image Viewer**: View images at full resolution with navigation
- **Keyboard Shortcuts**: Navigate with arrow keys, delete with 'D' key
- **Delete Functionality**: Remove unwanted images directly from the browser
- **Responsive Design**: Clean, dark-themed UI that works on desktop and mobile

## Quick Start

### Running the Server

From the project root directory:

```bash
cd /home/rafa/PycharmProjects/AnimalDetector
python3 -m image_server --dir datasets/fototrampeo_bosque/images/ --port 8000
```

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--dir`  | Yes      | N/A     | Directory containing images to serve |
| `--port` | No       | 8000    | Port number for the HTTP server |
| `--ip`   | No       | 127.0.0.1 | IP address to bind to |

### Examples

**Serve images from a specific directory:**
```bash
python3 -m image_server --dir datasets/fototrampeo_bosque/images/ --port 8000
```

**Use a different port:**
```bash
python3 -m image_server --dir images/ --port 8080
```

**Bind to all network interfaces:**
```bash
python3 -m image_server --dir images/ --ip 0.0.0.0 --port 8000
```

## Alternative Ways to Run

### 1. Using the Standalone Script

```bash
cd /home/rafa/PycharmProjects/AnimalDetector
python3 image_server.py --dir datasets/fototrampeo_bosque/images/ --port 8000
```

### 2. Make it Executable

```bash
cd /home/rafa/PycharmProjects/AnimalDetector
chmod +x image_server.py
./image_server.py --dir datasets/fototrampeo_bosque/images/ --port 8000
```

## Usage

### Accessing the Server

Once the server is running, open your web browser and navigate to:

```
http://127.0.0.1:8000/
```

Or if you specified a different IP/port:

```
http://<your-ip>:<your-port>/
```

### Keyboard Shortcuts

When viewing an image:

- **← (Left Arrow)**: Previous image
- **→ (Right Arrow)**: Next image
- **D or Delete**: Delete current image

### Navigation

1. **Gallery View** (`/`): Shows all images as thumbnails in a grid
2. **Image Viewer** (`/view?name=<filename>`): Full-size image with navigation
3. **Raw Image** (`/raw?name=<filename>`): Direct image file access

## Supported Image Formats

- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.bmp`

## Security Features

- **Path Traversal Protection**: Prevents access to files outside the specified directory
- **Safe File Validation**: Only serves files within the designated root directory
- **Type Checking**: Only serves recognized image file types

## Architecture

The image server is built with a modular architecture:

```
image_server/
├── __init__.py          # Package initialization
├── __main__.py          # Module entry point (CLI)
├── server.py            # HTTP server setup
├── handlers.py          # Request handlers
├── path_utils.py        # Path safety and image detection
├── template_loader.py   # HTML template rendering
└── templates/           # HTML templates
    ├── index.html       # Gallery view
    └── view.html        # Image viewer
```

## Development

### Running Tests

```bash
cd /home/rafa/PycharmProjects/AnimalDetector
python3 -m pytest tests/test_image_server.py -v
```

Or with unittest:

```bash
python3 -m unittest tests.test_image_server -v
```

### Code Structure

The server follows Clean Code principles:

- **Single Responsibility**: Each module has a focused purpose
- **Short Functions**: Functions are kept under 4 lines where possible
- **Type Hints**: All functions use static typing
- **No Ternary/Lambda**: Explicit if/else and named functions
- **SOLID Principles**: Modular, testable, maintainable code

## Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'image_server'`

**Solution**: Make sure you're running the command from the project root directory:
```bash
cd /home/rafa/PycharmProjects/AnimalDetector
python3 -m image_server --dir <path> --port 8000
```

**Problem**: `Can't open file 'image_server.py'`

**Solution**: The `image_server.py` file is in the project root, not in the `image_server/` subdirectory. Navigate to the project root first.

**Problem**: Port already in use

**Solution**: Use a different port:
```bash
python3 -m image_server --dir <path> --port 8001
```

**Problem**: No images showing up

**Solution**: 
- Verify the directory path is correct
- Ensure images have supported extensions (.jpg, .png, .gif, .bmp)
- Check file permissions

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Integration with Animal Detector

The image server is particularly useful when working with the Animal Detector project:

1. **Review Training Data**: Browse dataset images before training
2. **Clean Datasets**: Delete corrupted or inappropriate images
3. **Verify Results**: View detection results and output images
4. **Quality Control**: Quick visual inspection of image batches

### Example Workflow

```bash
# 1. Start the image server to review your dataset
python3 -m image_server --dir datasets/fototrampeo_bosque/images/ --port 8000

# 2. Browse images in your browser at http://127.0.0.1:8000/
# 3. Delete any problematic images using the web interface
# 4. Stop the server with Ctrl+C
# 5. Proceed with training or detection
```

## API Endpoints

- `GET /` - Gallery view (main page)
- `GET /view?name=<filename>` - Image viewer
- `GET /raw?name=<filename>` - Raw image file
- `POST /delete` - Delete image (form data: `name=<filename>`)

## Configuration

No configuration files are needed. All settings are passed as command-line arguments.

## License

Part of the Animal Detector project.

## See Also

- [Dataset Management](DATASET_MANAGEMENT.md)
- [Training Guide](TRAINING_GUIDE.md)
- [Quick Start Training](QUICK_START_TRAINING.md)

