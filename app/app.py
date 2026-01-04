# app.py
import cv2
import os
import numpy as np
from ultralytics import YOLO
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io

# --- CONFIGURATION ---
# IMPORTANT: Update this path to point to your best trained model weights.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

# --- ADVANCED CONFIGURATION ---
CONFIDENCE_THRESHOLD = 0.5 
CROP_BUFFER = 10

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)
CORS(app)

# Initialize Receipt Processor lazily
processor = None

def get_processor():
    global processor
    if processor is None:
        try:
            from receipt_processor import ReceiptProcessor
            # Use 'mk' for Macedonian
            processor = ReceiptProcessor(lang='mk')
            print("ReceiptProcessor initialized with Macedonian support.")
        except Exception as e:
            print(f"Failed to initialize ReceiptProcessor: {e}")
    return processor

# --- LOAD THE MODEL (Done once when the server starts) ---
print("Loading YOLO model...")
try:
    model = YOLO(MODEL_PATH)
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- CORE PROCESSING LOGIC (Adapted for API) ---

def refine_and_collect(image_crop, model):
    """
    Recursively analyzes an image crop and returns a list of final, verified document images.
    
    Args:
        image_crop (np.ndarray): The cropped image segment to analyze.
        model (YOLO): The loaded YOLO segmentation model.

    Returns:
        list: A list of NumPy arrays, where each array is a final cropped document.
    """
    final_documents = []
    if image_crop.size == 0:
        return final_documents

    # Run the model on the specific crop
    results = model(image_crop, conf=CONFIDENCE_THRESHOLD, verbose=False)
    masks = results[0].masks
    
    # CASE 1: Composite Document Found (more than 1 mask)
    if masks and len(masks) > 1:
        print(f"  - Composite document detected, splitting into {len(masks)} pieces...")
        for polygon in masks.xy:
            x, y, w, h = cv2.boundingRect(np.array(polygon, dtype=np.int32))
            sub_crop = image_crop[
                max(0, y - CROP_BUFFER): y + h + CROP_BUFFER,
                max(0, x - CROP_BUFFER): x + w + CROP_BUFFER
            ]
            # Recursively refine the new, smaller piece and add its results
            final_documents.extend(refine_and_collect(sub_crop, model))
            
    # CASE 2: Single or No Document Found (Base case)
    else:
        # This crop is considered a final, single document
        print("  - Verified as a single document.")
        final_documents.append(image_crop)
        
    return final_documents


# --- API ENDPOINT ---

@app.route('/segment', methods=['POST'])
def segment_document():
    """
    API endpoint to receive an image, segment it, and return the documents.
    """
    if model is None:
        return jsonify({"status": "error", "message": "Model is not loaded"}), 500

    # 1. Check if an image file is in the request
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    try:
        # 2. Read and decode the image from the request
        image_bytes = file.read()
        image_np_array = np.frombuffer(image_bytes, np.uint8)
        original_image = cv2.imdecode(image_np_array, cv2.IMREAD_COLOR)

        if original_image is None:
            return jsonify({"status": "error", "message": "Could not decode image"}), 400

        print("\n--- New Request Received ---")
        print("Performing initial scan on the uploaded image...")
        
        # 3. Perform the initial scan
        initial_results = model(original_image, conf=CONFIDENCE_THRESHOLD, verbose=False)
        if initial_results[0].masks is None:
            return jsonify({"status": "success", "documents": [], "message": "No documents detected"})

        # 4. Get processing mode
        mode = request.form.get('mode', 'segment') # 'segment' or 'ocr'
        do_ocr = (mode == 'ocr')

        # 5. Refine each initially found document
        all_final_docs = []
        for polygon in initial_results[0].masks.xy:
            x, y, w, h = cv2.boundingRect(np.array(polygon, dtype=np.int32))
            initial_crop = original_image[
                max(0, y - CROP_BUFFER): y + h + CROP_BUFFER,
                max(0, x - CROP_BUFFER): x + w + CROP_BUFFER
            ]
            
            # This function will handle the recursive splitting
            all_final_docs.extend(refine_and_collect(initial_crop, model))

        # 6. Process each document (Encode + Receipt Processing)
        processed_documents = []
        for i, doc_image in enumerate(all_final_docs):
            # Encode image
            _, buffer = cv2.imencode('.jpg', doc_image)
            encoded_string = base64.b64encode(buffer).decode('utf-8')
            
            doc_data = {
                "filename": f"doc_{i+1}.jpg",
                "data": encoded_string,
                "receipt_data": None
            }
            
            # Run Receipt Processor
            if do_ocr:
                proc = get_processor()
                if proc:
                    print(f"Processing receipt for document {i+1} with OCR...")
                    receipt_info = proc.process_image(doc_image, do_ocr=True)
                    doc_data["receipt_data"] = receipt_info
                    # Add flattened fields for convenience
                    doc_data["extracted_text"] = receipt_info.get("raw_text", "")
                    doc_data["matches"] = receipt_info.get("matches", {"vendor": None, "items_found": []})
            
            processed_documents.append(doc_data)
        
        print(f"Request complete. Returning {len(processed_documents)} documents.")
        return jsonify({"status": "success", "documents": processed_documents})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- RUN THE FLASK APP ---
if __name__ == '__main__':
    # Use host='0.0.0.0' to make the server accessible from other devices on your network
    app.run(host='0.0.0.0', port=5000, debug=True)