from machine import Pin, SPI
import st7789
import framebuf

# Initialize SPI and Display
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

# BMP loader function
def load_bmp(filename):
    with open(filename, 'rb') as f:
        f.read(54)  # Skip 54-byte header for BMP
        img_data = bytearray(f.read())

    # BMP files store pixels in BGR format and inverted vertically
    fb = framebuf.FrameBuffer(img_data, 240, 320, framebuf.RGB565)
    return fb

# Load your BMP
fb = load_bmp('image.bmp')

# Display BMP on LCD
tft.blit_buffer(fb, 0, 0, 240, 320)
