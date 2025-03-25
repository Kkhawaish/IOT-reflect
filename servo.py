from machine import Pin, PWM
import time

# Servo motor setup
servo_pin = 18  # GPIO pin connected to the servo signal wire
pwm = PWM(Pin(servo_pin), freq=50)  # 50 Hz frequency for servo control

# Function to set servo angle
def set_servo_angle(angle):
    duty = int(40 + (angle / 180) * 115)  # Convert angle to duty cycle
    pwm.duty(duty)
    time.sleep(0.5)  # Wait for the servo to reach the position

# Test the servo
try:
    while True:
        set_servo_angle(0)    # Move to 0 degrees
        time.sleep(1)
        set_servo_angle(90)   # Move to 90 degrees
        time.sleep(1)
        set_servo_angle(180)   # Move to 180 degrees
        time.sleep(1)
except KeyboardInterrupt:
    pwm.deinit()  # Turn off the PWM signal
    print("Servo test stopped.")