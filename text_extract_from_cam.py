from flask import Flask, request, jsonify, render_template
from paddleocr import PaddleOCR
from PIL import Image
import os
import cv2
from datetime import datetime
# import pytesseract

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    # Render the template without extracted text initially
    return render_template('text_extract_html.html', extracted_text=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file
    filepath = os.path.join(UPLOAD_FOLDER, "test_image.png")
    file.save(filepath)

    # Extract text from the saved image
    extracted_text = text_extract(filepath)

    # Render the template with the extracted text
    # return render_template('text_extract_html.html', extracted_text=extracted_text)
    return jsonify({"extracted_text": extracted_text}) 

# def text_extract(image_path):
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # For Windows

#     # Check if the file exists
#     if not os.path.exists(image_path):
#         return "Error: File does not exist."

#     # Read the image
#     image = cv2.imread(image_path)
#     if image is None:
#         return "Error: Could not read the file."

#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Enhance the image
#     resized_image = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
#     denoised_image = cv2.bilateralFilter(resized_image, d=9, sigmaColor=75, sigmaSpace=75)
#     _, thresholded_image = cv2.threshold(denoised_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

#     # Extract text using Tesseract
#     # extracted_text = pytesseract.image_to_string(thresholded_image, lang='eng')
#     extracted_text = pytesseract.image_to_string('test_img1.jpg', config="--psm 6")
#     print(extracted_text)
#     return extracted_text

def text_extract(image_path):
    ocr = PaddleOCR(use_angle_cls=True, rec_algorithm='SVTR_LCNet') # need to run only once to download and load model into memory
    
    result = ocr.ocr(image_path, cls=True)
    print(result)
    # for line in result:
    #     print(line)
    return result[0][0][1][0]



if __name__ == '__main__':
    app.run(debug=True)
