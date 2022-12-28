# A Christmas gift of hardware and code for Annie, Arthur, and Casey 2022
#
# Controls an attached strip of neopixels

import board
import digitalio
import neopixel
import pwmio
import time

# Declare global variables here. We could also initialize them but that is
# done in the setup() function instead following the pattern of Arduino.

# Green LED attached to pin A3
board_led = None

# KB2040 onboard neopixel
board_neopixel = None

# Neopixel strip attached to pin D8
strip_neopixel = None

# LED strip attached to pins D2,D3,D4
colorstrip_r = None
colorstrip_g = None
colorstrip_b = None

#
#
# A few notes on the next lines:
# - A value inside of parenthesis is called a tuple.
# - You can pass a tuple as a single argument in python.
# - The values for a color can range from 0 to 255 in decimal (base 10)
#   or you can use the values 0x00 to 0xFF in hexadecimal (base 16).
# - Purple is 62.7% red, 12.5% green and 94.1% blue. Changing to values from
#   0-255 yields PURPLE = (160, 32, 240)
# - People often use hex for encoding colors so I'm going to use it.
PURPLE = (0xA0, 0x20, 0xF0)
RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
YELLOW = (0xFF, 0xFF, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00) # Not actually black, turns the LED off

# setup()
# One time initialization code
def setup():
    # Variables declared for all functions need to be referenced
    # with the 'global' keyword so that Python doesn't create a
    # local variable instead that disappears after the function exits.
    global board_led
    global board_neopixel
    global strip_neopixel
    global colorstrip_r
    global colorstrip_g
    global colorstrip_b

    board_led = digitalio.DigitalInOut(board.A3)
    board_led.direction = digitalio.Direction.OUTPUT
    board_neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
    strip_neopixel = neopixel.NeoPixel(board.D9, 100)
    colorstrip_r = pwmio.PWMOut(board.D3, frequency=5000, duty_cycle=0)
    colorstrip_b = pwmio.PWMOut(board.D4, frequency=5000, duty_cycle=0)
    colorstrip_g = pwmio.PWMOut(board.D5, frequency=5000, duty_cycle=0)

# loop()
# Gets called in an infinite loop from the main code.
# Follows the pattern of the Arduino development environment.
def loop():
    # Indentation is important in Python. Make sure everything lines up if you want it
    # to live inside of a function or a loop.

    # Prints "Hello world!" to the Serial (CircuitPython REPL) window in Mu Editor
    print("Hello World!")
    board_led.value = True
    time.sleep(1)
    board_led.value = False

    # Set the onboard neopixel to purple (see function defined below)
    set_onboard_neopixel(PURPLE)

    # Fade the strip in and out
    fade_colorstrip(PURPLE, 0, 1.0, 2)
    time.sleep(1)
    fade_colorstrip(PURPLE, 1.0, 0, 2)

    for brightness in (1.0, .5, .1):
        delay = .25
        set_colorstrip(RED, brightness)
        time.sleep(delay)
        set_colorstrip(GREEN, brightness)
        time.sleep(delay)
        set_colorstrip(BLUE, brightness)
        time.sleep(delay)
        set_colorstrip(YELLOW, brightness)
        time.sleep(delay)
        set_colorstrip(PURPLE, brightness)
        time.sleep(delay)
        set_colorstrip(BLACK, brightness)


    # Make the lights chase down the neopixel strip
    light_chase([PURPLE, RED, YELLOW, WHITE], .25, 10)
    time.sleep(1)

# set_onboard_neopixel(value)
# Sets the value of the onboard neopixel to a specific color
#   color - a tuple of 3 values for (red, green, blue) each from 0 - 255
def set_onboard_neopixel(color):
    global board_neopixel
    board_neopixel[0] = color
    board_neopixel.show()


def fade_colorstrip(color, start_brightness, end_brightness, duration):
    interval = duration / 100
    brightness_increment = (end_brightness - start_brightness) / 100
    for i in range(0, 100):
        brightness = start_brightness + (i * brightness_increment)
        set_colorstrip(color, brightness)
        time.sleep(interval)

# set_colorstrip(color, brightness)
# Set the color strip to the specified color and brightness
#  color - an r,g,b color tuple with values 0-255 for each color
#  brightness - 1.0 is brightest, 0.0 is off
def set_colorstrip(color, brightness):
    # Scale the 0-255 value for each color to 65535-0
    colorstrip_r.duty_cycle = 65535-int(brightness * ((color[0] / 255.0) * 65535.0))  # Red
    colorstrip_g.duty_cycle = 65535-int(brightness * ((color[1] / 255.0) * 65535.0))  # Green
    colorstrip_b.duty_cycle = 65535-int(brightness * ((color[2] / 255.0) * 65535.0))  # Blue

# light_chase(colors, delay, loops)
# Make the lights chase each other down the strip
#   colors - a list of color tuples to write to the strip
#   delay - delay in seconds before making the light move one pixel
#   loops - number of times to repeat the chase
def light_chase(colors, delay, loops):
    for loop in range(0,loops):
        pass

if __name__ == "__main__":
    setup()
    while True:
        loop()
