import st7789
import framebuf
from machine import Pin, SPI
import time

def init_display():
    # Initialize SPI and the ST7789 display
    spi = SPI(2, baudrate=40000000, polarity=1, phase=1, sck=Pin(15), mosi=Pin(9))
    tft = st7789.ST7789(
        spi, 240, 320,
        reset=Pin(16, Pin.OUT),
        cs=Pin(11, Pin.OUT),
        dc=Pin(13, Pin.OUT),
        backlight=Pin(6, Pin.OUT),
        xstart=0,
        ystart=0
    )
    tft.init()
    return tft

def load_bmp(filename):
    # Load a BMP file assuming a 54-byte header and a 240x320 RGB565 image.
    with open(filename, 'rb') as f:
        f.read(54)  # Skip BMP header
        img_data = bytearray(f.read())
    fb = framebuf.FrameBuffer(img_data, 240, 320, framebuf.RGB565)
    return fb

def display_image(filename):
    print("Displaying image:", filename)
    tft = init_display()
    fb = load_bmp(filename)
    tft.blit_buffer(fb, 0, 0, 240, 320)
    print("Image displayed on screen.")

if __name__ == "__main__":
    display_image("image.bmp")
    # Keep running (or add additional logic) so the image remains visible.
    while True:
        pass
