import cv2
import os
import numpy as np
from ultralytics import YOLO
import shutil

# --- CONFIGURATION ---
# IMPORTANT: Update this path to point to your best trained model weights.
MODEL_PATH = "Document_Segmentation_Results/run_1_fixed/weights/best.pt"

# Folder containing the images you want to process.
IMAGE_FOLDER = "test_images"

# Main folder where subfolders for each processed image will be created.
OUTPUT_FOLDER = "extracted_documents_verified"

# --- ADVANCED CONFIGURATION ---
# Confidence threshold for the model. Detections below this will be ignored.
CONFIDENCE_THRESHOLD = 0.5 

# Add a small pixel buffer around the cropped documents to prevent cutting off edges.
CROP_BUFFER = 10 # Increased buffer slightly for better cropping

# --- CORE FUNCTIONS ---

def refine_and_save(image_crop, model, output_path_prefix, doc_counter):
    """
    Recursively analyzes an image crop. If the crop contains more than one document,
    it splits them and refines each piece. If it contains only one, it saves it.

    Args:
        image_crop (np.ndarray): The cropped image segment to analyze.
        model (YOLO): The loaded YOLO segmentation model.
        output_path_prefix (str): The base path and name for saving files (e.g., "output/image1/image1").
        doc_counter (int): The current document number for unique naming.

    Returns:
        int: The updated document counter after processing.
    """
    if image_crop.size == 0:
        print("  - Warning: Received an empty image crop for refinement.")
        return doc_counter

    print(f"  - Refining potential document...")
    
    # Run the model on the specific crop
    results = model(image_crop, conf=CONFIDENCE_THRESHOLD)
    
    # Check for detected masks within the crop
    masks = results[0].masks
    
    # CASE 1: Composite Document Found (more than 1 mask)
    # This is the core of the multi-check. The crop is not a single document.
    if masks and len(masks) > 1:
        print(f"    - Composite document detected. Found {len(masks)} sub-documents. Splitting...")
        
        # For each new mask found inside the crop, create a new, smaller crop
        sub_doc_index = 1
        for polygon in masks.xy:
            x, y, w, h = cv2.boundingRect(np.array(polygon, dtype=np.int32))
            
            # Crop the sub-document from the *current* image_crop
            sub_crop = image_crop[
                max(0, y - CROP_BUFFER): y + h + CROP_BUFFER,
                max(0, x - CROP_BUFFER): x + w + CROP_BUFFER
            ]
            
            # Recursively call the refinement function on the new, smaller piece
            # Pass the original doc_counter to be used as a base for naming
            new_prefix = f"{output_path_prefix}_doc_{doc_counter}_sub_{sub_doc_index}"
            doc_counter = refine_and_save(sub_crop, model, new_prefix, doc_counter)
            sub_doc_index += 1
            
    # CASE 2: Single or No Document Found
    # This is the base case. The crop is considered final and should be saved.
    else:
        print(f"    - Verified as a single document. Saving.")
        final_save_path = f"{output_path_prefix}_doc_{doc_counter}.jpg"
        cv2.imwrite(final_save_path, image_crop)
        print(f"      ✔ Saved final document to: {final_save_path}")
        doc_counter += 1
        
    return doc_counter


def extract_and_verify_documents():
    """
    Main function to load the model and process all images. It performs an
    initial scan and then passes each finding to a recursive refinement process.
    """
    # Clean and create the main output directory
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)

    # Check for model and image folder
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model file not found at '{MODEL_PATH}'")
        return
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: The folder '{IMAGE_FOLDER}' does not exist.")
        return
        
    print(f"Loading model from: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)

    # Process each image in the source folder
    for image_name in os.listdir(IMAGE_FOLDER):
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        
        if os.path.isfile(image_path) and image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"\n{'='*20}\nProcessing image: {image_name}\n{'='*20}")

            # Create a dedicated folder for this image's results
            base_name, _ = os.path.splitext(image_name)
            image_specific_folder = os.path.join(OUTPUT_FOLDER, base_name)
            os.makedirs(image_specific_folder, exist_ok=True)
            print(f"  - Created output folder: {image_specific_folder}")

            original_image = cv2.imread(image_path)
            if original_image is None:
                print("  - Could not read image.")
                continue

            # --- 1. INITIAL SCAN ---
            # Perform the first pass on the entire image
            print("  - Performing initial scan on the full image...")
            initial_results = model(original_image, conf=CONFIDENCE_THRESHOLD)
            
            if initial_results[0].masks is None:
                print("  - No documents detected in the initial scan.")
                continue
                
            initial_masks = initial_results[0].masks
            print(f"  - Initial scan found {len(initial_masks)} potential document(s).")

            # --- 2. REFINE EACH INITIAL FINDING ---
            doc_counter = 1
            for polygon in initial_masks.xy:
                # Crop each potential document from the original image
                x, y, w, h = cv2.boundingRect(np.array(polygon, dtype=np.int32))
                initial_crop = original_image[
                    max(0, y - CROP_BUFFER): y + h + CROP_BUFFER,
                    max(0, x - CROP_BUFFER): x + w + CROP_BUFFER
                ]
                
                # Define the base name for any files that result from this crop
                output_prefix = os.path.join(image_specific_folder, base_name)
                
                # Kick off the recursive refinement process for this crop
                doc_counter = refine_and_save(initial_crop, model, output_prefix, doc_counter)

if __name__ == '__main__':
    extract_and_verify_documents()