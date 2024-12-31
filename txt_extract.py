import streamlit as st
from PIL import Image
import pytesseract
import base64
import io

# Path to Tesseract
path_to_tesseract = '/usr/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

def decode_image(data_url):
    """Decode base64 image data from the JavaScript webcam stream."""
    header, encoded = data_url.split(",", 1)
    binary_data = base64.b64decode(encoded)
    image_data = io.BytesIO(binary_data)
    return Image.open(image_data)

def process_image(image):
    """Extract text from an image using Tesseract OCR."""
    text = pytesseract.image_to_string(image)
    return text

def main():
    st.title("Webcam Video Stream with OCR")

    st.subheader("Live Webcam Feed and OCR")

    # JavaScript to capture webcam frame and send it to Streamlit
    html_code = """
    <video id="video" autoplay></video>
    <button id="capture">Capture Frame</button>
    <canvas id="canvas" style="display:none;"></canvas>
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
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
            
            // Send data to Streamlit via session state
            Streamlit.setComponentValue(data);
        });
    </script>
    """

    # Placeholder for the webcam feed and OCR result
    st.components.v1.html(html_code, height=600)
    st.subheader("Captured Frame and OCR Result")

    # OCR Result Placeholder
    ocr_result_placeholder = st.empty()

    # Handle incoming image data
    def handle_image_data(data_url):
        image = decode_image(data_url)
        st.image(image, caption="Captured Frame", use_column_width=True)
        text = process_image(image)
        ocr_result_placeholder.write(f"**Extracted Text:**\n{text}")

    # Custom Streamlit component to listen for JavaScript events
    image_data = st.text_input("Webcam Image Data (hidden input)", value="", key="webcam_data")
    if image_data:
        handle_image_data(image_data)

if __name__ == "__main__":
    main()

























# # import streamlit as st
# # from PIL import Image
# # import pytesseract
# # import base64
# # import io

# # # Path to Tesseract
# # path_to_tesseract = '/usr/bin/tesseract'
# # pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

# # def decode_image(data_url):
# #     """Decode base64 image data from the JavaScript webcam stream."""
# #     header, encoded = data_url.split(",", 1)
# #     binary_data = base64.b64decode(encoded)
# #     image_data = io.BytesIO(binary_data)
# #     return Image.open(image_data)

# # def process_image(image):
# #     """Extract text from an image using Tesseract OCR."""
# #     text = pytesseract.image_to_string(image)
# #     return text

# # def main():
# #     st.title("Webcam Video Stream with OCR")

# #     st.subheader("Live Webcam Feed and OCR")

# #     # JavaScript to capture webcam frame and send it to Streamlit
# #     html_code = """
# #     <video id="video" autoplay></video>
# #     <button id="capture">Capture</button>
# #     <canvas id="canvas" style="display:none;"></canvas>
# #     <script>
# #         const video = document.getElementById('video');
# #         const canvas = document.getElementById('canvas');
# #         const captureButton = document.getElementById('capture');

# #         // Access the user's webcam
# #         navigator.mediaDevices.getUserMedia({ video: true })
# #             .then((stream) => { video.srcObject = stream; })
# #             .catch((err) => { console.error("Webcam not accessible: ", err); });

# #         // Capture a frame
# #         captureButton.addEventListener('click', () => {
# #             const context = canvas.getContext('2d');
# #             canvas.width = video.videoWidth;
# #             canvas.height = video.videoHeight;
# #             context.drawImage(video, 0, 0, canvas.width, canvas.height);
# #             const data = canvas.toDataURL('image/png');
            
# #             // Send data to Streamlit via session state
# #             Streamlit.setComponentValue(data);
# #         });
# #     </script>
# #     """

# #     # Placeholder for the webcam feed and OCR result
# #     st.components.v1.html(html_code, height=600)
# #     st.subheader("OCR Result")
# #     if "ocr_result" in st.session_state:
# #         st.text(st.session_state.ocr_result)

# #     # Handle incoming image data
# #     def handle_image_data(data_url):
# #         image = decode_image(data_url)
# #         st.image(image, caption="Captured Image", use_column_width=True)
# #         text = process_image(image)
# #         st.session_state.ocr_result = text

# #     # Custom Streamlit component to listen for JavaScript events
# #     image_data = st.text_input("Webcam Image Data (hidden input)", value="", key="webcam_data")
# #     if image_data:
# #         handle_image_data(image_data)

# # if __name__ == "__main__":
# #     main()
