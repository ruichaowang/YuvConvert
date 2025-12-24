# Image Utility Tools

A collection of Python tools for processing and converting image data, specifically for SS2/SS3/SS4 raw formats and general analysis.

## Project Structure
```text
.
├── tools/                 # Python scripts
│   ├── image_converter.py # Convert Raw YUV -> PNG
│   ├── compare_images.py  # Compare two batches of images
│   └── bgr_to_rgb.py      # Swap BGR channels to RGB
├── data/                  # Test data
│   ├── raw/               # Raw YUV files (SS2, SS3, SS4)
│   ├── rgb_test/          # Images for BGR->RGB testing
│   └── comparison/        # Images for comparison testing
└── requirements.txt
```

## Requirements
- Python 3
- `numpy`, `opencv-python`

Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Tools

### 1. Image Converter (`image_converter.py`)
Converts raw YUV images (UYVY, NV12) into PNG format.
**Previously `converty.py`.**

**Usage:**
```bash
# Using presets (ss2, ss3, ss4)
python3 tools/image_converter.py data/raw/SS2_2M --type ss2

# Manual configuration
python3 tools/image_converter.py input.raw --width 1920 --height 1080 --format nv12
```

### 2. Compare Images (`compare_images.py`)
Compares two batches of images (e.g. from different algorithms) side-by-side, calculating sharpness (Laplacian variance) and detecting corners.

**Usage:**
```bash
python3 tools/compare_images.py \
    --batch1 data/comparison/batch1 \
    --batch2 data/comparison/batch2 \
    --results data/comparison/results
```

### 3. BGR to RGB Converter (`bgr_to_rgb.py`)
Swaps Blue and Red channels for all PNG files in a directory. Useful if images were saved with wrong channel order.

**Usage:**
```bash
python3 tools/bgr_to_rgb.py --input_dir data/rgb_test
```
