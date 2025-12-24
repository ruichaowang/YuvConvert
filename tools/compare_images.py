
import cv2
import glob
import os
import numpy as np

def compute_sharpness(img):
    """Compute the variance of the Laplacian of the image.
    Higher values indicate more edges/sharpness.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def detect_corners(img):
    """Detect corners using Shi-Tomasi corner detection."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting up to 100 corners, quality level 0.01, min distance 10
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    if corners is not None:
        corners = np.int32(corners)
    return corners

def draw_info(img, sharpness, corners, label):
    """Draw sharpness score, corner count, and label on the image."""
    # Make a copy to avoid modifying the original if passed by reference
    res_img = img.copy()
    
    # Draw corners
    corner_count = 0
    if corners is not None:
        corner_count = len(corners)
        for i in corners:
            x, y = i.ravel()
            cv2.circle(res_img, (x, y), 3, (0, 0, 255), -1) # Red dots
            
    # Draw text background for readability
    text_info = [
        f"{label}",
        f"Sharpness: {sharpness:.2f}",
        f"Corners: {corner_count}"
    ]
    
    y_pos = 30
    for text in text_info:
        cv2.putText(res_img, text, (10, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        y_pos += 30
        
    return res_img

import argparse

def compare_batches(dir1, dir2, results_dir):
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    # Get files from batch1
    files1 = glob.glob(os.path.join(dir1, "*.png"))
    
    # Process matching files
    for f1 in files1:
        filename = os.path.basename(f1)
        f2 = os.path.join(dir2, filename)
        
        if not os.path.exists(f2):
            print(f"Skipping {filename}: Not found in {dir2}")
            continue
            
        print(f"Comparing {filename}...")
        
        img1 = cv2.imread(f1)
        img2 = cv2.imread(f2)
        
        if img1 is None or img2 is None:
            print(f"Error reading images for {filename}")
            continue
            
        # 1. Compute Metrics
        sharp1 = compute_sharpness(img1)
        sharp2 = compute_sharpness(img2)
        
        corners1 = detect_corners(img1)
        corners2 = detect_corners(img2)
        
        # 2. visual annotation
        res1 = draw_info(img1, sharp1, corners1, "Batch 1")
        res2 = draw_info(img2, sharp2, corners2, "Batch 2")
        
        # 3. Concatenate side-by-side
        # Resize if heights differ
        if res1.shape[0] != res2.shape[0]:
            h = min(res1.shape[0], res2.shape[0])
            # Maintain aspect ratio? Or just resize?
            # Let's resize res2 to match res1's height if needed, keeping AR
            scale = h / res2.shape[0]
            w = int(res2.shape[1] * scale)
            res2 = cv2.resize(res2, (w, h))
            
            scale1 = h / res1.shape[0]
            w1 = int(res1.shape[1] * scale1)
            res1 = cv2.resize(res1, (w1, h))
            
        combined = np.hstack((res1, res2))
        
        # Save
        save_path = os.path.join(results_dir, f"compare_{filename}")
        cv2.imwrite(save_path, combined)
        print(f"Saved comparison to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two batches of images for sharpness/corners.")
    parser.add_argument("--batch1", default="data/comparison/batch1", help="First image directory")
    parser.add_argument("--batch2", default="data/comparison/batch2", help="Second image directory")
    parser.add_argument("--results", default="data/comparison/results", help="Output directory")
    
    args = parser.parse_args()
    
    compare_batches(args.batch1, args.batch2, args.results)
