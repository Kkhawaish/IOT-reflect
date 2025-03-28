from machine import Pin, PWM
from time import sleep

# Initialize the PWM object on GPIO 18 (as mentioned in your script)
buzzer = PWM(Pin(18))

# Extracted frequencies and calculated durations from the CSV
melody = [440.0, 369.99, 440.0, 349.23, 349.23, 349.23, 311.13, 349.23, 349.23, 369.99]
durations = [2.843, 0.179, 1.127, 0.891, 1.227, 0.346, 0.346, 0.413, 0.245, 0.914]  # Durations in seconds

# Function to play a single note
def play_tone(freq, duration):
    buzzer.freq(int(freq))  # Set the frequency for the note
    buzzer.duty_u16(32768)  # Set the duty cycle to 50% to maximize volume
    sleep(duration)  # Play the note for the duration of the tone
    buzzer.duty_u16(0)  # Turn off buzzer between notes to prevent clicking sound

# Play the melody multiple times
for _ in range(3):  # Repeat the sequence three times
    for tone, duration in zip(melody, durations):
        play_tone(tone, duration)

# Turn off the PWM signal
buzzer.deinit()

