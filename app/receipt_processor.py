import cv2
import re
import json
import logging
import os
import base64
import numpy as np
from rapidfuzz import process, fuzz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReceiptProcessor:
    def __init__(self, db_path='database/mock_db.json', lang='mk'):
        """
        Initializes the ReceiptProcessor (OCR models loaded lazily).
        """
        self.lang = lang
        self.ocr = None
        self.db_path = db_path
        self.db = {'vendors': [], 'items': []}
        self._load_db()

    def _load_db(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            full_db_path = os.path.join(base_dir, self.db_path)
            with open(full_db_path, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            logger.info("Mock database loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load mock database: {e}")

    def _init_ocr(self):
        if self.ocr is None:
            from paddleocr import PaddleOCR
            logger.info(f"Initializing PaddleOCR with lang='{self.lang}'...")
            self.ocr = PaddleOCR(use_angle_cls=True, lang=self.lang, show_log=False)

    def process_image(self, image, do_ocr=True):
        """
        Processes a receipt image. If do_ocr is False, it skips OCR.
        """
        if not do_ocr:
            return {"status": "skipped", "message": "OCR disabled"}

        self._init_ocr()
        processing_steps = []
        
        # Step 0: Original
        processing_steps.append({"name": "Original", "image": self._img_to_base64(image)})
        
        # Step 1: Preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        processing_steps.append({"name": "Grayscale", "image": self._img_to_base64(gray)})
        
        # Step 2: OCR with Bounding Boxes
        logger.info("Starting OCR processing...")
        ocr_result = self.ocr.ocr(image, cls=True)
        
        lines_with_boxes = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result[0]:
                box = line[0]  # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                text = line[1][0]
                confidence = line[1][1]
                lines_with_boxes.append({"box": box, "text": text, "conf": confidence})

        # Step 3: Vertical Alignment (Group by Y-coordinate proximity)
        grouped_lines = self._group_lines_by_y(lines_with_boxes)
        
        # Step 4: Normalization and Cleaning
        processed_lines = []
        for line_text in grouped_lines:
            cleaned = self.clean_text(line_text)
            processed_lines.append({
                "original": line_text,
                "cleaned": cleaned
            })

        # Step 5: Fuzzy Matching
        matches = self.check_database(processed_lines)
        
        raw_text_full = "\n".join(grouped_lines)
        
        return {
            "raw_text": raw_text_full,
            "matches": matches,
            "processing_steps": processing_steps,
            "text_segments": self._generate_segments(raw_text_full, matches)
        }

    def _group_lines_by_y(self, boxes, threshold=15):
        """
        Groups OCR blocks that are on the same horizontal line.
        """
        if not boxes:
            return []
            
        # Sort by top Y coordinate
        boxes.sort(key=lambda x: x['box'][0][1])
        
        grouped_lines = []
        current_line = [boxes[0]]
        
        for i in range(1, len(boxes)):
            # Calculate average Y of current line
            avg_y = sum([b['box'][0][1] for b in current_line]) / len(current_line)
            curr_y = boxes[i]['box'][0][1]
            
            if abs(curr_y - avg_y) < threshold:
                current_line.append(boxes[i])
            else:
                # Sort current line by X coordinate
                current_line.sort(key=lambda x: x['box'][0][0])
                grouped_lines.append(" ".join([b['text'] for b in current_line]))
                current_line = [boxes[i]]
        
        # Last line
        current_line.sort(key=lambda x: x['box'][0][0])
        grouped_lines.append(" ".join([b['text'] for b in current_line]))
        
        return grouped_lines

    def clean_text(self, text):
        """
        Step 2: The Cleaner (Normalization)
        """
        if not text: return ""
        text = text.lower()
        # Remove weights/volumes
        text = re.sub(r'\d+(\.\d+)?\s*(л|гр|г|мл|кг|мг)', ' ', text)
        # Remove prices
        text = re.sub(r'\d+([.,]\d{2})?', ' ', text)
        # Remove noise
        text = re.sub(r'[*#%\-+=:;]', ' ', text)
        return " ".join(text.split())

    def check_database(self, processed_lines, threshold=85):
        """
        Step 3: Fuzzy Matching with RapidFuzz
        """
        found_data = {"vendor": None, "items_found": []}
        
        vendor_choices = self.db.get('vendors', [])
        item_choices = self.db.get('items', [])
        
        for line in processed_lines:
            cleaned = line['cleaned']
            if not cleaned or len(cleaned) < 3: continue
            
            # Vendor check
            if not found_data['vendor']:
                res = process.extractOne(cleaned, vendor_choices, scorer=fuzz.WRatio)
                if res and res[1] >= threshold:
                    found_data['vendor'] = {
                        "name": res[0],
                        "confidence": res[1],
                        "original_text": line['original']
                    }
                    continue

            # Item check
            res = process.extractOne(cleaned, item_choices, scorer=fuzz.WRatio)
            if res and res[1] >= threshold:
                found_data['items_found'].append({
                    "name": res[0],
                    "confidence": res[1],
                    "original_text": line['original']
                })
                
        return found_data

    def _img_to_base64(self, img):
        _, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer).decode('utf-8')

    def _generate_segments(self, full_text, matches):
        # We want to highlight portions of the text that were matched
        terms_to_highlight = []
        if matches.get("vendor"):
            terms_to_highlight.append(matches["vendor"]["original_text"])
        for item in matches.get("items_found", []):
            terms_to_highlight.append(item["original_text"])
            
        segments = []
        lines = full_text.split('\n')
        for i, line in enumerate(lines):
            # If the whole line is matched, highlight words in it
            line_matched = any(term in line for term in terms_to_highlight)
            
            words = line.split(' ')
            for j, word in enumerate(words):
                segments.append({
                    "text": word, 
                    "matched": line_matched and len(word.strip(',. ')) > 2
                })
                if j < len(words) - 1:
                    segments.append({"text": " ", "matched": False})
            
            if i < len(lines) - 1:
                segments.append({"text": "\n", "matched": False})
                
        return segments
