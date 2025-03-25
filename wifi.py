import network
import socket
import time

# Wi-Fi Configuration (ESP32 as Access Point)
AP_SSID = "ESP32-S2-AP"
AP_PASSWORD = "password123"

# Set up Access Point
ap = network.WLAN(network.AP_IF)
ap.config(essid=AP_SSID, password=AP_PASSWORD)
ap.active(True)

print("Access Point Active")
print("SSID:", AP_SSID)
print("Password:", AP_PASSWORD)
print("IP Address:", ap.ifconfig()[0])

# HTML Page for Phone Interaction
HTML = """<!DOCTYPE html>
<html>
<head><title>ESP32-S2 Control</title></head>
<body>
<h1>ESP32-S2 Web Server</h1>
<button onclick="location.href='/ledon'">LED ON</button>
<button onclick="location.href='/ledoff'">LED OFF</button>
</body>
</html>
"""

# Handle HTTP Requests
def handle_request(client):
    request = client.recv(1024).decode()
    print("Request:", request)
    
    if "GET / " in request:
        response = HTML
    elif "GET /ledon" in request:
        response = "LED turned ON"
        # Add your LED control code here
    elif "GET /ledoff" in request:
        response = "LED turned OFF"
        # Add your LED control code here
    else:
        response = "404 Not Found"
    
    client.send("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n")
    client.send(response)
    client.close()

# Start Web Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 80))
server.listen(5)

print("Web server started. Connect your phone to the ESP32's Wi-Fi and visit:")
print("http://" + ap.ifconfig()[0])

while True:
    client, addr = server.accept()
    print("Client connected from:", addr)
    handle_request(client)
    time.sleep(1)