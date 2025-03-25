import network
import urequests
import time
from machine import Pin, PWM

# Servo motor setup
servo_pin = 18  # GPIO pin connected to the servo signal wire
pwm = None  # Initialize pwm as None

# Function to set servo angle
def set_servo_angle(angle):
    global pwm
    if pwm is None:
        pwm = PWM(Pin(servo_pin), freq=50)  # Reinitialize PWM if inactive
    duty = int(40 + (angle / 180) * 115)  # Convert angle to duty cycle
    pwm.duty(duty)
    time.sleep(0.5)  # Wait for the servo to reach the position

# Replace with your Wi-Fi credentials
SSID = "Annie21"
PASSWORD = "annie12345"

# Replace with your Firebase project credentials
FIREBASE_URL = "https://iot-reflect-default-rtdb.europe-west1.firebasedatabase.app/"
FIREBASE_SECRET = "AIzaSyBBYFLCVPN-bEAU30w5laUOqwUGvVKtc08"

# Pin Configuration
LED_PIN = 2  # Replace with your LED pin

# Connect to Wi-Fi
def connect_wifi():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(SSID, PASSWORD)
    while not sta.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    print("Connected to Wi-Fi")
    print("IP Address:", sta.ifconfig()[0])

# Read data from Firebase
def read_firebase(path):
    url = FIREBASE_URL + path + ".json?auth=" + FIREBASE_SECRET
    response = urequests.get(url)
    data = response.json()
    response.close()
    return data

# Write data to Firebase
def write_firebase(path, data):
    url = FIREBASE_URL + path + ".json?auth=" + FIREBASE_SECRET
    response = urequests.put(url, json=data)
    response.close()

# Control LED and servo based on Firebase data
def control_led():
    global pwm
    led_status = read_firebase("led_status")  # Read from path "led_status"
    print(led_status)
    if led_status == "ON":
        set_servo_angle(90)  # Move servo to 90 degrees
        # Add code to turn on LED (e.g., Pin(LED_PIN, Pin.OUT).value(1))
    else:
        if pwm is not None:
            pwm.deinit()  # Turn off the PWM signal
            pwm = None  # Set pwm to None to indicate it's inactive
        # Add code to turn off LED (e.g., Pin(LED_PIN, Pin.OUT).value(0))

# Main Loop
def main():
    connect_wifi()
    while True:
        control_led()
        time.sleep(2)  # Check Firebase every 2 seconds

# Run the program
main()