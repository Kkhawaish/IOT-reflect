import time
from machine import Pin, PWM

def play_audio():
    speaker_pin = 26  # Change this to the appropriate GPIO for your speaker
    speaker = PWM(Pin(speaker_pin))
    
    # Define a melody as a list of (frequency in Hz, duration in ms) tuples.
    melody = [
        (440, 500),  # A4
        (494, 500),  # B4
        (523, 500),  # C5
        (587, 500)   # D5
    ]
    
    print("Playing melody...")
    for freq, duration in melody:
        speaker.freq(freq)
        speaker.duty(512)  # Mid-range duty cycle (0–1023)
        time.sleep_ms(duration)
        speaker.duty(0)    # Stop tone between notes
        time.sleep_ms(50)
    speaker.deinit()
    print("Melody finished.")

if __name__ == "__main__":
    play_audio()
