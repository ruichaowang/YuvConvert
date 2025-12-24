# Converty - Raw Image Converter

A simple command-line tool to convert raw YUV images (UYVY, NV12) into PNG format.
Designed to support SS2, SS3, and SS4 camera formats easily.

## Features

- **Multi-format support**: Handles `UYVY` and `NV12` raw data.
- **Project Presets**:
    - `ss2`: 1920 x 1280 (UYVY)
    - `ss3`: 1920 x 1536 (UYVY)
    - `ss4`: 1920 x 1536 (NV12)
- **Batch Processing**: Can convert a single file or recursively process an entire directory.
- **Zero Dependencies** (aside from `opencv` and `numpy`).

## Requirements

- Python 3 with `numpy` and `opencv-python`.

## Quick Start
You can check the help menu at any time:
```bash
python3 converty.py --help
```

### 1. Using Presets (Recommended)
The easiest way is to use the `--type` flag corresponding to your data:

**For SS2:**
```bash
python3 converty.py /path/to/SS2_dir --type ss2
```

**For SS3:**
```bash
python3 converty.py /path/to/SS3_dir --type ss3
```

**For SS4:**
```bash
python3 converty.py /path/to/SS4_dir --type ss4
```

### 2. Manual Configuration
If you have a file with a different resolution or format, you can specify them manually:

```bash
python3 converty.py input.raw --width 640 --height 480 --format nv12
```

### 3. Custom Output Directory
By default, a `png` folder is created inside your input location. You can override this:

```bash
python3 converty.py input_dir --type ss2 --output /Users/me/Desktop/converted
```
# yuv_raw_image_convert
# YuvConvert
# YuvConvert
