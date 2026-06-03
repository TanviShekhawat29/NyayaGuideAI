import pytesseract
import cv2
import numpy as np
import re
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def preprocess_image(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharp = cv2.filter2D(gray, -1, kernel)

    thresh = cv2.adaptiveThreshold(
        sharp, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"[^\w\s\.,:-]", "", text)
    return " ".join(text.split())


def extract_text(file_path):
    try:
        full_text = ""

        if file_path.lower().endswith(".pdf"):
            try:
                images = convert_from_path(file_path)
            except:
                return "OCR ERROR: Invalid or corrupted PDF"

            for img in images:
                img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                processed = preprocess_image(img)
                text = pytesseract.image_to_string(processed)
                full_text += text + " "

        else:
            img = cv2.imread(file_path)
            processed = preprocess_image(img)
            full_text = pytesseract.image_to_string(processed)

        if not full_text.strip():
            return "OCR ERROR: No text detected"

        return clean_text(full_text)

    except Exception as e:
        return f"OCR ERROR: {str(e)}"