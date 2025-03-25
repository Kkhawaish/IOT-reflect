from machine import Pin, PWM
import network
import socket
import time


# Wi-Fi Configuration (ESP32 as Access Point)
AP_SSID = "ESP32-S2-Servo"
AP_PASSWORD = "password123"

# Servo Configuration
SERVO_PIN = 18  # GPIO pin connected to servo
servo_pwm = PWM(Pin(SERVO_PIN), freq=50)  # 50 Hz for servos

# Set up Access Point
ap = network.WLAN(network.AP_IF)
ap.config(essid=AP_SSID, password=AP_PASSWORD)
ap.active(True)

print("Servo Control AP Active")
print("SSID:", AP_SSID)
print("Password:", AP_PASSWORD)
print("IP Address:", ap.ifconfig()[0])

# HTML Page with Servo Controls
HTML = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32-S2 Servo Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {font-family: Arial; text-align: center; margin: 0 auto; padding: 20px;}
        button {padding: 12px 24px; font-size: 18px; margin: 10px;}
        .slider {width: 80%; margin: 20px 0;}
    </style>
</head>
<body>
    <h1>Servo Control</h1>
    <button onclick="location.href='/angle/0'">0°</button>
    <button onclick="location.href='/angle/90'">90°</button>
    <button onclick="location.href='/angle/180'">180°</button>
    
    <form action="/angle">
        <input type="range" name="deg" min="0" max="180" value="90" class="slider">
        <input type="submit" value="Set Custom Angle">
    </form>
    
    <p>Current Angle: %s°</p>
</body>
</html>
"""

current_angle = 90  # Track current servo position

def set_angle(angle):
    global current_angle
    angle = max(0, min(180, int(angle)))  # Clamp angle to 0-180
    duty = int(40 + (angle / 180) * 115)  # Convert angle to duty cycle
    servo_pwm.duty(duty)
    current_angle = angle
    time.sleep(0.5)

def handle_request(client):
    global current_angle
    request = client.recv(1024).decode()
    print("Request:", request)
    
    response = HTML % current_angle  # Insert current angle into HTML
    
    if "GET /angle/0 " in request:
        set_angle(0)
    elif "GET /angle/90 " in request:
        set_angle(90)
    elif "GET /angle/180 " in request:
        set_angle(180)
    elif "GET /angle?deg=" in request:
        angle = request.split('deg=')[1].split(' ')[0]
        set_angle(angle)
    
    client.send("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n")
    client.send(response)
    client.close()

# Start Web Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 80))
server.listen(5)

print("Web server started. Connect to:")
print("http://" + ap.ifconfig()[0])

try:
    while True:
        client, addr = server.accept()
        print("Client connected from:", addr)
        handle_request(client)
except KeyboardInterrupt:
    servo_pwm.deinit()
    print("Server stopped")