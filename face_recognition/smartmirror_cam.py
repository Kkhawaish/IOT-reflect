import network
import urequests
import time
from machine import Pin
from camera import Camera  # Must be included in firmware or uploaded

# Wi-Fi credentials
SSID = "your_wifi_name"
PASSWORD = "your_wifi_password"

# Flask server address (change to your PC's IP)
SERVER_URL = "http://192.168.x.x:5001/upload"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected! IP:", wifi.ifconfig())

# Initialize camera
cam = Camera()
cam.init()

# Main loop
while True:
    print("Capturing image...")
    img = cam.capture()

    if img:
        print("Sending image to server...")
        headers = {"Content-Type": "image/jpeg"}
        try:
            res = urequests.post(SERVER_URL, data=img, headers=headers)
            print("Server response:", res.text)
            res.close()
        except Exception as e:
            print("Error sending image:", e)
    else:
        print("Failed to capture image.")

    time.sleep(5)
