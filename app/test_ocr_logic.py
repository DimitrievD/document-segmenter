import sys
import os
import cv2
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from receipt_processor import ReceiptProcessor

def test_cleaning_logic():
    print("Testing Cleaning Logic...")
    processor = ReceiptProcessor()
    
    test_cases = [
        ("Млеκо Битолсκо 3.2%", "млеко битолско"),
        ("КОКА КОЛА 1.5Л 75.00", "кока кола"),
        ("ЈОГУРТ БИТОЛСКИ 500гр", "јогурт битолски"),
        ("ЛЕБ БЕЛ СЕЧЕН *1", "леб бел сечен"),
    ]
    
    for original, expected in test_cases:
        cleaned = processor.clean_text(original)
        print(f"Original: '{original}' -> Cleaned: '{cleaned}'")
        # Note: 'млеко' vs 'млеκо' (kappa vs k) - regex or replacement might be needed if OCR misreads
        # But let's see if fuzzy match handles it.

def test_fuzzy_matching():
    print("\nTesting Fuzzy Matching...")
    processor = ReceiptProcessor()
    
    # Mock items in DB
    processor.db['items'] = [
        "МЛЕКО БИТОЛСКО 3.2%",
        "КОКА КОЛА 1.5Л",
        "ЈОГУРТ БИТОЛСКИ"
    ]
    
    test_lines = [
        {"original": "Млеκо Битолсκо 3.2%", "cleaned": "млеко битолско"},
        {"original": "БИТ0ЛСК0 МЛЕК0", "cleaned": "бит0лск0 млек0"},
        {"original": "КОКА КОЛА 75.00", "cleaned": "кока кола"}
    ]
    
    matches = processor.check_database(test_lines)
    print("Matches found:", matches)

def test_vertical_alignment():
    print("\nTesting Vertical Alignment Logic...")
    processor = ReceiptProcessor()
    
    # Mock OCR blocks
    # Product name on left, price on right with same Y
    boxes = [
        {"box": [[10, 100], [100, 100], [100, 120], [10, 120]], "text": "МЛЕКО"},
        {"box": [[110, 100], [200, 100], [200, 120], [110, 120]], "text": "БИТОЛСКО"},
        {"box": [[400, 100], [500, 100], [500, 120], [400, 120]], "text": "75.00"},
        {"box": [[10, 150], [100, 150], [100, 170], [10, 170]], "text": "ЛЕБ"},
        {"box": [[400, 150], [500, 150], [500, 170], [400, 170]], "text": "30,00"}
    ]
    
    grouped = processor._group_lines_by_y(boxes)
    print("Grouped Lines:")
    for line in grouped:
        print(f"- {line}")

if __name__ == "__main__":
    test_cleaning_logic()
    test_fuzzy_matching()
    test_vertical_alignment()
