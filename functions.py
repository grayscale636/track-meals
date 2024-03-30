import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter

def load_labels(label_path):
    with open(label_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def tflite_detect_objects(image, labels):
    # Load the TensorFlow Lite model into memory
    interpreter = Interpreter(model_path='model/model-fix-final.tflite')
    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    # Load image and resize to expected shape [1xHxWx3]
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values
    input_mean = 127.5
    input_std = 127.5
    input_data = (np.float32(input_data) - input_mean) / input_std

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[1]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[3]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[0]['index'])[0] # Confidence of detected objects

    detections = []

    # Loop over all detections and store if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > 0.5) and (scores[i] <= 1.0)):  # Change the confidence threshold if needed
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            label = labels[int(classes[i])]
            detections.append({'label': label, 'confidence': float(scores[i]), 'bbox': [int(xmin), int(ymin), int(xmax), int(ymax)]})

    return detections

def generate_frames(labels):
    cap = cv2.VideoCapture(0)
    while True:
        # Read the frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection on the frame
        detections = tflite_detect_objects(frame, labels)

        # Draw bounding boxes on the frame
        for detection in detections:
            xmin, ymin, xmax, ymax = detection['bbox']
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, f"{detection['label']} {round(detection['confidence']*100, 2)}%", (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
