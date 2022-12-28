# A Christmas gift of hardware and code for Annie, Arthur, and Casey 2022
#
# Controls an attached strip of RGB LEDs.
# Has code to read from a PIR (proxemity) sensor if you want to use that.
#
# The microcontroller is an Adafruit KB2040. I just happened to have
# a bunch of these lying around, you could use a Raspberry Pi Pico or
# Adafruit Feather just as easily.
#
# The strip is a set of LEDs all wired together like this one
#   https://www.amazon.com/Lepro-RGB-LED-Strip-Lights/dp/B07RFFJ7YL?th=1

# Some of this code is derived from my LED workshop example in C++
#   https://github.com/ericzundel/steam_workshop_ledstrip/blob/main/examples/workshop_example/workshop_example.ino
# Which itself is based on the Adafruit NEOPIXEL library examples
#   https://github.com/adafruit/Adafruit_NeoPixel/tree/master/examples

import board
import digitalio
import neopixel
import pwmio
import time

# Declare global variables here. We could also initialize them but that is
# done in the setup() function instead following the pattern of Arduino.

# Green LED attached to pin A3
board_led = None

# Pushbutton attached to D6
pushbutton = None

# PIR sensor attached to D7
pir_sensor = None

# KB2040 onboard neopixel
board_neopixel = None

# LED strip attached to pins D3, D4, D5
colorstrip_r = None
colorstrip_g = None
colorstrip_b = None

# A color definition you can use in your code
# A few notes on the next line:
# - A value inside of parenthesis is called a tuple.
# - You can pass a tuple as a single argument in python.
# - The values for a color can range from 0 to 255 in decimal (base 10)
#   or you can use the values 0x00 to 0xFF in hexadecimal (base 16).
# - Purple is 62.7% red, 12.5% green and 94.1% blue. Changing to values from
#   0-255 yields PURPLE = (160, 32, 240)
# - People often use hex for encoding colors so I'm going to use it.
PURPLE = (0xA0, 0x20, 0xF0)

# Here are some other standard colors
# - Want more colors? Visit https://www.rapidtables.com/web/color/RGB_Color.html
RED     = (0xFF, 0x00, 0x00)
GREEN   = (0x00, 0xFF, 0x00)
BLUE    = (0x00, 0x00, 0xFF)
YELLOW  = (0xFF, 0xFF, 0x00)
CYAN    = (0x00, 0xFF, 0xFF)
MAGENTA = (0xFF, 0x00, 0xFF)
WHITE   = (0xFF, 0xFF, 0xFF)
BLACK   = (0x00, 0x00, 0x00) # Not actually black, turns the LED off

def setup():
    """One time initialization code.
    """

    # Variables declared for all functions need to be referenced
    # with the 'global' keyword so that Python doesn't create a
    # local variable instead that disappears after the function exits.
    global board_led
    global board_neopixel
    global pushbutton
    global pir_sensor
    global colorstrip_r
    global colorstrip_g
    global colorstrip_b

    board_led = digitalio.DigitalInOut(board.A3)
    board_led.direction = digitalio.Direction.OUTPUT

    board_neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

    pushbutton = digitalio.DigitalInOut(board.D6)
    pushbutton.direction = digitalio.Direction.INPUT
    pushbutton.pull = digitalio.Pull.UP

    pir_sensor = digitalio.DigitalInOut(board.D7)
    pir_sensor.direction = digitalio.Direction.INPUT
    pir_sensor.pull = digitalio.Pull.DOWN

    colorstrip_r = pwmio.PWMOut(board.D3, frequency=5000, duty_cycle=0)
    colorstrip_b = pwmio.PWMOut(board.D4, frequency=5000, duty_cycle=0)
    colorstrip_g = pwmio.PWMOut(board.D5, frequency=5000, duty_cycle=0)

def loop():
    """Gets called in an infinite loop from the main code.
    """
    # Check the pushbutton. If it is pressed, the value will be low (false)
    pushbutton_value = pushbutton.value;
    print("Pushbutton is:", pushbutton_value)
    if pushbutton_value is False:
        print("Detected pushbutton press!")
        # blink the external LED 3 times
        for i in range(0,3):
                delay = .5
                board_led.value = False
                time.sleep(delay)
                board_led.value = True
                time.sleep(delay)

    # Check the PIR sensor. If it is pressed, the value will be high
    motion_detected = wait_for_pir_sensor(10) # Timeout after 10 seconds
    if (motion_detected is True):
        for i in range(0,10):
                delay = .1
                board_led.value = False
                time.sleep(delay)
                board_led.value = True
                time.sleep(delay)

    time.sleep(1)

def wait_for_pir_sensor(max_wait):
    """Wait for the PIR sensor to be active.

        max_wait : float
            Time to wait for the sensor to become active in seconds

    :rtype: True if the sensor detects something, False if it times out
    """
    global pir_sensor

    delay = .25  # Wait 250 ms between checking the value
    elapsed = 0
    print("Waiting for PIR Sensor", end='')
    while (elapsed < max_wait):
        if (pir_sensor.value is True):
            print("Detected!")
            return True
        time.sleep(delay)
        elapsed += delay
        print(".", end='')

    print("Timeout")
    return False


###################################################################
# No need to edit below this line.
#
# Call 'setup()' once to initialize everything and 'loop()'
# in an infinite while loop after that.
if __name__ == "__main__":
    setup()
    while True:
        loop()
