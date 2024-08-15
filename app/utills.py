# app/utils.py

import pdfplumber
import fitz  # PyMuPDF
import os
import uuid
import io
import base64
from PIL import Image
import pytesseract


def extract_text_from_pdf(pdf_path):
    dct = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            dct[page] = page.extract_text()
    return dct


def extract_img_from_pdf(file):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    unique_folder_name = str(uuid.uuid4())
    folder_path = os.path.join('app/static/img/', unique_folder_name)
    os.makedirs(folder_path, exist_ok=True)

    pdf_document = fitz.open(file)
    images = []
    texts = []

    for i in range(len(pdf_document)):
        page = pdf_document[i]
        img_list = page.get_images(full=True)

        for img in img_list:
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)

            # Perform OCR to extract text from the image
            text = pytesseract.image_to_string(image)
            texts.append(text)

    image_b64_list = []
    for image in images:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        image_b64_list.append(img_str)

    pdf_document.close()
    return image_b64_list, texts