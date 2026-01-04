import cv2
import numpy as np
import os
from receipt_processor import ReceiptProcessor

def test_ocr_fallback():
    print("Testing ReceiptProcessor with OCR fallback and Macedonian support...")
    try:
        processor = ReceiptProcessor(lang='mk')
        print("Initialization successful!")
        
        # Create a dummy image with some noise or low contrast to force preprocessing
        # For simple test, we just use a blank image which should fail across all steps if empty,
        # but the processor should still return all steps.
        dummy_image = np.full((300, 300, 3), 200, dtype=np.uint8)
        # Add some text-like noise
        cv2.putText(dummy_image, "TECT", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        result = processor.process_image(dummy_image)
        
        print("\nProcessing Result:")
        print(f"Used OCR Step: {result.get('used_ocr_step')}")
        print(f"Raw Text Lines: {result.get('raw_text').splitlines()}")
        print(f"Processing Steps Found: {[step['name'] for step in result.get('processing_steps', [])]}")
        
        if result.get('processing_steps'):
            print("Processing steps captured successfully.")
        else:
            print("ERROR: No processing steps captured!")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_ocr_fallback()
