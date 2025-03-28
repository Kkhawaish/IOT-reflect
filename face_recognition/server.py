from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import face_recognition
import time

app = Flask(__name__)
SAVE_DIR = "received_images"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Receive raw image bytes
        file_data = request.data
        img_array = np.frombuffer(file_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Save image for debugging
        timestamp = int(time.time())
        img_name = f"received_{timestamp}.jpg"
        img_path = os.path.join(SAVE_DIR, img_name)
        cv2.imwrite(img_path, img)

        # Face detection
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_img)

        if face_locations:
            return jsonify({"status": "Face Detected", "count": len(face_locations)})
        else:
            return jsonify({"status": "No Face Detected"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

