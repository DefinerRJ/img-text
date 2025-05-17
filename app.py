from flask import Flask, request, render_template, redirect, url_for
import cv2
from PIL import Image
import os
import easyocr  

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])  # Initialize once globally

# OCR Pipeline Functions

def preprocess_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    resized = cv2.resize(thresh, (800, 800))
    return resized

def extract_text(image):
    result = reader.readtext(image)
    text = " ".join([item[1] for item in result])
    return text

def post_process(text):
    cleaned = " ".join(text.split())  # Simple cleanup
    return cleaned


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            processed_image = preprocess_image(filepath)
            text = extract_text(processed_image)
            cleaned_text = post_process(text)
            return render_template('index.html', text=cleaned_text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
