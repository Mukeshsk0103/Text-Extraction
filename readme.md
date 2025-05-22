# Text Extraction Application

## Description
This application provides Optical Character Recognition (OCR) functionality using PaddleOCR. It supports extracting text from static images as well as live webcam streaming with automatic image capture and text extraction via a Flask web interface.

## Features
- Extract text from images using PaddleOCR.
- Live webcam streaming with automatic image capture every 2 seconds.
- Web interface to display extracted text in real-time.
- Simple Flask backend to handle image uploads and text extraction.

## Installation

1. Clone the repository or download the source code.
2. (Optional but recommended) Create a Python virtual environment:
   ```bash
   python -m venv virtual_env
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     virtual_env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source virtual_env/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Extract text from a static image
Run the script `extractText.py` to extract text from a sample image (`test_image1.png`):
```bash
python extractText.py
```

### Live webcam text extraction web app
Run the Flask application `text_extract_from_cam.py`:
```bash
python text_extract_from_cam.py
```
- Open your browser and navigate to `http://127.0.0.1:5000/`.
- Allow webcam access when prompted.
- The app will automatically capture images from your webcam every 2 seconds and display the extracted text on the page.

## File Overview

- `extractText.py`: Script to extract text from a static image using PaddleOCR.
- `text_extract_from_cam.py`: Flask web application for live webcam text extraction.
- `templates/text_extract_html.html`: HTML template for the live webcam streaming interface.
- `requirements.txt`: Python dependencies for the project.
- `uploads/`: Directory where uploaded images are saved during Flask app runtime.
- `test_image1.png`, `test_img1.jpg`: Sample images for testing.

## Dependencies

Key Python packages used:
- Flask
- PaddleOCR
- OpenCV (opencv-python)
- Pillow
- numpy
- pytesseract (commented out in code but included in requirements)

Refer to `requirements.txt` for the full list of dependencies.

## Folder Structure

```
.
├── extractText.py
├── text_extract_from_cam.py
├── requirements.txt
├── templates/
│   └── text_extract_html.html
├── uploads/
│   └── (uploaded images)
├── test_image1.png
├── test_img1.jpg
└── other_env/ (Python virtual environment)
```

## License

This project is licensed under the MIT License. (Modify as needed)

## Contact

For questions or feedback, please contact the project maintainer.
