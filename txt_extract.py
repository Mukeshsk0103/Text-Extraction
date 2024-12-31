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
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Camera Stream</title>
</head>
<body>
    <h1>Live Camera Stream</h1>
    <video id="video" width="640" height="480" autoplay></video>
    <button id="capture">Capture Image</button>
    <canvas id="canvas" style="display: none;"></canvas>
    <img id="captured-image" alt="Captured Image" style="display:none;">

    <script>
        const video = document.getElementById('video');
        const captureButton = document.getElementById('capture');
        const canvas = document.getElementById('canvas');
        const capturedImage = document.getElementById('captured-image');

        // Get the webcam stream and display it in the video element
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
            })
            .catch(err => {
                console.error("Error accessing webcam: ", err);
            });

        // Capture the image when the button is clicked
        captureButton.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            // Set canvas size to match video dimensions
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            // Draw the current frame from the video onto the canvas
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Convert the canvas to an image and display it
            const imageData = canvas.toDataURL('image/png');
            capturedImage.src = imageData;
            capturedImage.style.display = 'block'; // Show the captured image

            // Create a link for the image data to simulate a download
            const link = document.createElement('a');
            link.href = imageData;
            link.download = 'captured-image.png'; // Set default file name

            // Automatically trigger the download without clicking
            link.click();
        });
    </script>
</body>
</html>
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
