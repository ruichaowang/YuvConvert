#!/usr/bin/env python3
import argparse
import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Presets configuration
PRESETS = {
    'ss2': {'width': 1920, 'height': 1280, 'format': 'uyvy'},
    'ss3': {'width': 1920, 'height': 1536, 'format': 'uyvy'},
    'ss4': {'width': 1920, 'height': 1536, 'format': 'nv12'},
}

SUPPORTED_EXTENSIONS = ['.raw', '.yuv', '.bin']

def get_files(path, extensions):
    """Recursively find files with given extensions."""
    path = Path(path)
    if path.is_file():
        return [path]
    
    files = []
    for ext in extensions:
        files.extend(path.rglob(f"*{ext}"))
    return sorted(files)

def convert_uyvy(data, width, height):
    """Convert UYVY data to BGR."""
    try:
        # UYVY is 2 bytes per pixel
        expected_size = width * height * 2
        if data.size != expected_size:
            print(f"Error: File size {data.size} does not match resolution {width}x{height} for UYVY (expected {expected_size})")
            return None
            
        img_uyvy = data.reshape(height, width, 2)
        rgb = cv2.cvtColor(img_uyvy, cv2.COLOR_YUV2BGR_UYVY)
        return rgb
    except Exception as e:
        print(f"Error converting UYVY: {e}")
        return None

def convert_nv12(data, width, height):
    """Convert NV12 data to BGR."""
    try:
        # NV12 is 1.5 bytes per pixel (Y full res + UV half res interleaved)
        expected_size = int(width * height * 1.5)
        if data.size != expected_size:
             print(f"Error: File size {data.size} does not match resolution {width}x{height} for NV12 (expected {expected_size})")
             return None

        # cvtColor for NV12 expects input of size (height * 1.5, width) single channel
        img_nv12 = data.reshape(int(height * 1.5), width)
        rgb = cv2.cvtColor(img_nv12, cv2.COLOR_YUV2BGR_NV12)
        return rgb
    except Exception as e:
        print(f"Error converting NV12: {e}")
        return None

def process_file(file_path, output_dir, width, height, fmt):
    print(f"Processing: {file_path}")
    
    try:
        data = np.fromfile(file_path, dtype=np.uint8)
    except Exception as e:
        print(f"Failed to read file {file_path}: {e}")
        return

    img = None
    if fmt == 'uyvy':
        img = convert_uyvy(data, width, height)
    elif fmt == 'nv12':
        img = convert_nv12(data, width, height)
    else:
        print(f"Unknown format: {fmt}")
        return

    if img is not None:
        # Determine output path
        # If input was a directory recursion, we might want to mirror structure or just flat output.
        # User request simple "converty", let's keep it simple: output to specified dir.
        
        file_name = file_path.stem
        output_path = output_dir / f"{file_name}.png"
        
        # Handle duplicates if flattening directory structure
        counter = 1
        while output_path.exists():
            output_path = output_dir / f"{file_name}_{counter}.png"
            counter += 1
            
        cv2.imwrite(str(output_path), img)
        print(f"Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert raw YUV images (UYVY/NV12) to PNG.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  1. Convert all files in a directory using a preset:
     python3 converty.py examples/SS2_2M --type ss2

  2. Convert a single file with custom settings:
     python3 converty.py image.raw --width 1920 --height 1280 --format uyvy

  3. Convert and save to a specific folder:
     python3 converty.py inputs/ --type ss3 --output results/
     
Available Presets:
  ss2: 1920x1280, uyvy
  ss3: 1920x1536, uyvy
  ss4: 1920x1536, nv12
"""
    )
    parser.add_argument('input', help='Input file or directory path')
    parser.add_argument('--type', choices=PRESETS.keys(), help='Preset type (ss2, ss3, ss4). Sets default width, height, and format.')
    parser.add_argument('--width', type=int, help='Image width (overrides preset)')
    parser.add_argument('--height', type=int, help='Image height (overrides preset)')
    parser.add_argument('--format', choices=['uyvy', 'nv12'], help='Image pixel format (overrides preset)')
    parser.add_argument('--output', help='Output directory. Defaults to <input_dir>/png')

    args = parser.parse_args()

    # Determine settings
    width = args.width
    height = args.height
    fmt = args.format

    if args.type:
        preset = PRESETS[args.type]
        if width is None: width = preset['width']
        if height is None: height = preset['height']
        if fmt is None: fmt = preset['format']
    
    # Validation
    if not width or not height or not fmt:
        print("Error: You must specify --type OR provide --width, --height, and --format.")
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist.")
        sys.exit(1)

    # Determine files
    files_to_process = get_files(input_path, SUPPORTED_EXTENSIONS)
    if not files_to_process:
        print("No matching files found (.raw, .yuv, .bin).")
        sys.exit(0)

    # Determine output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        if input_path.is_file():
             output_dir = input_path.parent / "png"
        else:
             output_dir = input_path / "png"
    
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Settings: Type={args.type or 'Custom'}, Size={width}x{height}, Format={fmt}")
    print(f"Found {len(files_to_process)} files.")
    print(f"Output directory: {output_dir}")

    for f in files_to_process:
        process_file(f, output_dir, width, height, fmt)

    print("Done.")

if __name__ == '__main__':
    main()
