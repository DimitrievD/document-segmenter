import torch
from ultralytics import YOLO

# --- CONFIGURATION ---
# Load a pre-trained SEGMENTATION model.
MODEL_NAME = 'yolov8n-seg.pt'

# Path to your data configuration file
DATA_CONFIG_PATH = 'dataset/data.yaml'

# Training parameters
EPOCHS = 100
IMAGE_SIZE = 640
PROJECT_NAME = 'Document_Segmentation_Results'
EXPERIMENT_NAME = 'run_1_fixed'

# Batch Size: Use -1 for AutoBatch to maximize GPU usage
BATCH_SIZE = -1

# --- MAIN TRAINING ---
if __name__ == '__main__':
    # Initialize the model with pre-trained segmentation weights
    model = YOLO(MODEL_NAME)

    # Train the model on your custom segmentation dataset
    print("Starting segmentation training with the corrected settings...")
    results = model.train(
        data=DATA_CONFIG_PATH,
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        device='0',
        project=PROJECT_NAME,
        name=EXPERIMENT_NAME,
        batch=BATCH_SIZE,

        # --- THE UNIVERSAL FIX IS HERE ---
        # Setting workers=0 forces single-threaded data loading, which resolves
        # the CUDA resource conflict error across all library versions.
        workers=0
    )

    print("\n✅ Segmentation training complete!")
    print(f"   Your trained model is saved in the '{PROJECT_NAME}/{EXPERIMENT_NAME}' directory.")