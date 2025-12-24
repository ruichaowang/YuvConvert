import cv2
import glob
import os
import argparse

def convert_bgr_to_rgb(input_dir, output_prefix="rgb_"):
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    # Get all png files
    files = glob.glob(os.path.join(input_dir, "*.png"))
    print(f"Found {len(files)} files in {input_dir}")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        if filename.startswith(output_prefix):
            continue
            
        print(f"Processing {filename}...")
        img = cv2.imread(file_path)
        
        if img is None:
            print(f"Failed to read {filename}")
            continue
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        output_filename = f"{output_prefix}{filename}"
        output_path = os.path.join(input_dir, output_filename)
        
        cv2.imwrite(output_path, img_rgb)
        print(f"Saved to {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images from BGR to RGB.")
    parser.add_argument("--input_dir", type=str, default="data/rgb_test", help="Directory containing images")
    args = parser.parse_args()
    
    convert_bgr_to_rgb(args.input_dir)
