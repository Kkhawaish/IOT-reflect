from machine import Pin, ADC, I2C
import time

# Test GPIO by blinking an LED
led = Pin(2, Pin.OUT)  # GPIO2 is often linked to an onboard LED

def blink_led(times=5, delay=0.5):
    for _ in range(times):
        led.value(1)
        time.sleep(delay)
        led.value(0)
        time.sleep(delay) 


# Run tests
if __name__ == "__main__":
    print("Testing ESP32-Kaluga-1 board...")
    
    print("Blinking LED...")
    blink_led() 
    
    print("Test complete!")
