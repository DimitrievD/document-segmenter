import cv2
import sys
import os
import json

# Ensure we can import from the app directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from receipt_processor import ReceiptProcessor

def test_receipt_processing(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    print(f"Processing image: {image_path}")
    
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Failed to load image.")
            return

        # Initialize processor
        processor = ReceiptProcessor()
        
        # Process
        result = processor.process_image(image)
        
        # Output results
        print("\n--- Processing Results ---")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_receipt.py <path_to_image>")
    else:
        test_receipt_processing(sys.argv[1])
