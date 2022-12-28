# A Christmas gift of hardware and code for Annie, Arthur, and Casey 2022
# Author: Eric Ayers <ericzundel@gmail.com>
# Date: December 28, 2022
#
# Example code to control an attached strip of RGB LEDs.
# Has code to read from a PIR (proxemity) sensor if you want to use that.
# For more information, see README.md
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

########################################################
# Add your new code into loop() or define new constants
# and globals below.


def loop():
    """Gets called in an infinite loop from the main code.
    """

    # Indentation is important in Python. Make sure everything lines up if you want it
    # to live inside of a function or a loop.

    # Prints "Hello world!" to the Serial (CircuitPython REPL) window in Mu Editor
    print("Hello World!")

    # Blink an LED just to show how that's done.
    # Note that this LED is wired up with its ground lead to the MCU pin
    # so that it turns on when the pin is low (False) and turns off when
    # the pin is high (True)
    board_led.value = False
    time.sleep(1)
    board_led.value = True
    time.sleep(1)

    # Blink the onboard neopixel to purple (see function defined below)
    set_onboard_neopixel(PURPLE)
    time.sleep(1)
    set_onboard_neopixel(BLACK)
    time.sleep(1)

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
        # blink the neopixel Cyan 3 times
        for i in range(0,3):
            delay = .5
            set_onboard_neopixel(CYAN)
            time.sleep(1)
            set_onboard_neopixel(BLACK)
            break

    # Set the colorstrip to one color for a moment
    set_colorstrip(PURPLE, 1.0)
    time.sleep(2)

    # Use a loop to set some colors manually
    for brightness in (1.0, .5, .1):
        # Indentation is important in Python. Make sure everything lines
        # up if you want it to live inside of a function or a loop.
        delay = .25
        set_colorstrip(RED, brightness)
        time.sleep(delay)
        set_colorstrip(GREEN, brightness)
        time.sleep(delay)
        set_colorstrip(BLUE, brightness)
        time.sleep(delay)
        set_colorstrip(YELLOW, brightness)
        time.sleep(delay)
        set_colorstrip(CYAN, brightness)
        time.sleep(delay)
        set_colorstrip(MAGENTA, brightness)
        time.sleep(delay)
        set_colorstrip(BLACK, brightness)


    # Fade the strip in and out in one color
    linearfade_colorstrip(PURPLE, 0, 1.0, 2)
    time.sleep(1)
    linearfade_colorstrip(PURPLE, 1.0, 0, 2)

    # Rainbow effect for 10 seconds
    for i in range(0,5):
        rainbow(1.0, 2)

    set_colorstrip(BLACK, 0.0)

    time.sleep(1)


###################################################################
# Add your new code above. No need to edit below this line.
#
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

def set_onboard_neopixel(color):
    """Sets the value of the onboard neopixel to a specific color

        color : tuple
            Three values for (red, green, blue) each from 0 - 255
    """
    global board_neopixel
    board_neopixel[0] = color
    board_neopixel.show()

def linearfade_colorstrip(color, start_brightness, end_brightness, duration):
    """Fade the colorstrip from one brightness level to another over linearly the specified time

        color : tuple of (int, int, int)
            Color to use for the fade operation
        start_brightness : float
            Value from 0 (off) to 1.0 (full on) to start the fade operation
        end_brightness : float
            Value from 0 (off) to 1.0 (full on) to end the fade operation.  The colorstrip
            will be left at this value when the function exits.
        duration : float
            Amount of time in seconds that the fade should last.
    """
    interval = duration / 100
    brightness_increment = (end_brightness - start_brightness) / 100
    for i in range(0, 100):
        brightness = start_brightness + (i * brightness_increment)
        set_colorstrip(color, brightness)
        time.sleep(interval)

def rainbow(brightness, duration):
    """Make all LEDs on the strip change colors in a rainbow pattern over time.

        brightness : float
            Intensity of the lightstrip. 1.0 is brightest, 0.0 is off

        duration : float
            The number of seconds to run the rainbow effect.
    """
    interval = duration / 100.0

    for j in range(0,255):
        set_colorstrip(colorwheel(j), brightness)
        time.sleep(interval)

def set_colorstrip(color, brightness):
    """Set the color strip to the specified color and brightness

        color : tuple of (int, int, int)
            An r,g,b color tuple with values 0-255 for each color
        brightness : float
            Intensity of the lightstrip. 1.0 is brightest, 0.0 is off
    """
    # Scale the 0-255 value for each color to 65535-0
    colorstrip_r.duty_cycle = 65535-int(brightness * ((color[0] / 255.0) * 65535.0))  # Red
    colorstrip_g.duty_cycle = 65535-int(brightness * ((color[1] / 255.0) * 65535.0))  # Green
    colorstrip_b.duty_cycle = 65535-int(brightness * ((color[2] / 255.0) * 65535.0))  # Blue

def colorwheel(color_wheel_position):
    """Use the colorwheel model where a single value maps to an RGB color.

        color_wheel_position : int
            Value from 0-255 representing a single color on the colorwheel.
            The colors are a transition r - g - b - back to r.
    """
    # Did you accidentally pass a value out of range? Let me fix that for you.
    color_wheel_position = abs(int(color_wheel_position) % 256)

    # 0-84 is in the red to green range
    color_wheel_position = 255 - color_wheel_position
    if (color_wheel_position < 85):
        return (255 - color_wheel_position * 3, 0, color_wheel_position * 3);

    # 85-169 is in the green to blue range
    if (color_wheel_position < 170):
        color_wheel_position -= 85;
        return (0, color_wheel_position * 3, 255 - color_wheel_position * 3);

    # 170-255 is in the blue to red range
    color_wheel_position -= 170;
    return (color_wheel_position * 3, 255 - color_wheel_position * 3, 0);

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

    # Duty cycle 100% means that the GPIO pins are high, meaning no
    # current should flow through the LEDs, turning them off.
    colorstrip_r = pwmio.PWMOut(board.D3, frequency=5000, duty_cycle=65535)
    colorstrip_b = pwmio.PWMOut(board.D4, frequency=5000, duty_cycle=65535)
    colorstrip_g = pwmio.PWMOut(board.D5, frequency=5000, duty_cycle=65535)

# mainline code
# Call 'setup()' once to initialize everything and 'loop()'
# in an infinite while loop after that.
if __name__ == "__main__":
    setup()
    while True:
        loop()
