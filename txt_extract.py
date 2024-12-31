import streamlit as st
from PIL import Image
import pytesseract
import base64
import io

# Path to Tesseract
path_to_tesseract = '/usr/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

def process_image(data_url):
    """Decode base64 image data from the JavaScript webcam stream."""
    header, encoded = data_url.split(",", 1)
    binary_data = base64.b64decode(encoded)
    image_data = io.BytesIO(binary_data)
    return Image.open(image_data)

def main():
    st.title("Webcam Video Stream with OCR")

    st.subheader("Live Webcam Feed and OCR")

    # JavaScript for webcam stream
    html_code = """
    <video id="video" autoplay></video>
    <button id="capture">Capture</button>
    <canvas id="canvas" style="display:none;"></canvas>
    <img id="photo" alt="Captured Image">
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const photo = document.getElementById('photo');
        const captureButton = document.getElementById('capture');

        // Access the user's webcam
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => { video.srcObject = stream; })
            .catch((err) => { console.error("Webcam not accessible: ", err); });

        // Capture a frame
        captureButton.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const data = canvas.toDataURL('image/png');
            photo.setAttribute('src', data);

            // Send captured image to backend via Streamlit
            fetch('/_st_capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: data })
            }).then(response => response.json())
              .then(data => {
                  console.log("OCR Result:", data.text);
                  document.getElementById('ocr-result').innerText = data.text;
              }).catch(error => console.error("Error:", error));
        });
    </script>
    <div id="ocr-result"></div>
    """

    st.components.v1.html(html_code, height=600)

    # Backend to handle OCR processing
    if "image_data" not in st.session_state:
        st.session_state["image_data"] = None

    def handle_image_upload(data_url):
        img = process_image(data_url)
        text = pytesseract.image_to_string(img)
        return text

    # Mock HTTP endpoint for JavaScript interaction
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    ctx = get_script_run_ctx()
    if ctx is not None:
        # Register a custom Streamlit route
        import streamlit.web.server.websocket_headers as wh

        @wh.app.route("/_st_capture", methods=["POST"])
        def capture_route():
            from flask import request, jsonify
            data = request.json
            image_data = data.get("image")
            if image_data:
                ocr_text = handle_image_upload(image_data)
                return jsonify({"text": ocr_text})
            return jsonify({"error": "No image provided"}), 400

if __name__ == "__main__":
    main()
