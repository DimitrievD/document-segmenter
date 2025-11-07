import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
# IMPORTANT: Update this path to point to your results.csv file.
CSV_PATH = 'Document_Segmentation_Results/run_1_fixed/results.csv'

# --- MAIN SCRIPT ---
def plot_training_results():
    """
    Reads the results.csv file from a training run and creates custom plots
    for loss, mAP, precision, and recall.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f"Error: The file was not found at '{CSV_PATH}'")
        print("Please make sure the path is correct.")
        return

    # The column names in results.csv can have leading spaces, so we strip them.
    df.columns = df.columns.str.strip()

    # --- Create Plots ---
    # We'll create a figure with 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('YOLOv8 Segmentation Training Metrics', fontsize=16)

    # 1. Plot Loss (Training vs. Validation)
    axs[0, 0].plot(df['epoch'], df['train/box_loss'], label='Train Box Loss')
    axs[0, 0].plot(df['epoch'], df['val/box_loss'], label='Validation Box Loss')
    axs[0, 0].plot(df['epoch'], df['train/seg_loss'], label='Train Seg Loss', linestyle='--')
    axs[0, 0].plot(df['epoch'], df['val/seg_loss'], label='Validation Seg Loss', linestyle='--')
    axs[0, 0].set_title('Box & Segmentation Loss vs. Epochs')
    axs[0, 0].set_xlabel('Epoch')
    axs[0, 0].set_ylabel('Loss')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # 2. Plot mAP Scores
    axs[0, 1].plot(df['epoch'], df['metrics/mAP50(M)'], label='mAP50 (Mask)')
    axs[0, 1].plot(df['epoch'], df['metrics/mAP50-95(M)'], label='mAP50-95 (Mask)')
    axs[0, 1].set_title('Mean Average Precision (mAP) vs. Epochs')
    axs[0, 1].set_xlabel('Epoch')
    axs[0, 1].set_ylabel('mAP Score')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # 3. Plot Precision and Recall (for Masks)
    axs[1, 0].plot(df['epoch'], df['metrics/precision(M)'], label='Precision (Mask)')
    axs[1, 0].plot(df['epoch'], df['metrics/recall(M)'], label='Recall (Mask)')
    axs[1, 0].set_title('Precision & Recall vs. Epochs')
    axs[1, 0].set_xlabel('Epoch')
    axs[1, 0].set_ylabel('Score')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # 4. Hide the last empty subplot
    axs[1, 1].axis('off')

    # Adjust layout and display the plots
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


if __name__ == '__main__':
    plot_training_results()