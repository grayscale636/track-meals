from flask import Flask, render_template, request, jsonify, Response
from functions import load_labels, tflite_detect_objects, generate_frames
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No image uploaded'})

    npimg = np.fromstring(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    labels = load_labels('labelmap.txt')
    detections = tflite_detect_objects(image, labels)
    return jsonify({'predictions': detections})

@app.route('/video_feed')
def video_feed():
    labels = load_labels('labelmap.txt')
    return Response(generate_frames(labels), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
