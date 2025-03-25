import network
import urequests
import time
from machine import Pin
import camera  # Ensure a compatible camera module is available

# Wi‑Fi and Firebase Storage configuration
SSID = "Annie21"
PASSWORD = "annie12345"
# Replace these with your Firebase Storage bucket details:
FIREBASE_STORAGE_URL = "https://firebasestorage.googleapis.com/v0/b/your-bucket.appspot.com/o"
FIREBASE_STORAGE_TOKEN = "YOUR_FIREBASE_STORAGE_TOKEN"  # If required

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi‑Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected to Wi‑Fi. IP address:", wlan.ifconfig()[0])

def init_camera():
    # Reinitialize the camera (adjust parameters as needed for your module)
    try:
        camera.deinit()  # In case it's already initialized
    except Exception as e:
        pass  # Ignore if not yet initialized
    camera.init(0, format=camera.JPEG)
    camera.framesize(camera.FRAME_QVGA)  # e.g., 320x240 for faster capture
    camera.quality(10)  # Lower value means higher compression; adjust as needed
    print("Camera initialized.")

def capture_image(filename):
    print("Capturing image...")
    buf = camera.capture()
    if buf:
        with open(filename, "wb") as f:
            f.write(buf)
        print("Image captured and saved as", filename)
    else:
        print("Failed to capture image.")

def upload_to_firebase(filename):
    # Build the URL for upload (using uploadType=media)
    url = FIREBASE_STORAGE_URL + "?uploadType=media&name=" + filename + "&token=" + FIREBASE_STORAGE_TOKEN
    print("Uploading image to Firebase Storage...")
    with open(filename, "rb") as f:
        file_data = f.read()
    headers = {"Content-Type": "image/jpeg"}
    try:
        response = urequests.post(url, data=file_data, headers=headers)
        print("Upload response:", response.text)
        response.close()
    except Exception as e:
        print("Upload failed:", e)

def capture_and_upload():
    init_camera()
    filename = "capture.jpg"
    capture_image(filename)
    upload_to_firebase(filename)

def main():
    connect_wifi()
    capture_and_upload()

if __name__ == "__main__":
    main()
