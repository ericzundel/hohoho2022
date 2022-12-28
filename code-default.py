# A Christmas gift of hardware and code for Annie, Arthur, and Casey 2022
# Author: Eric Ayers <ericzundel@gmail.com>
# Date: December 28, 2022
#
# Pseudocode to control a strip of LEDs.
#  Flash the external LED when the power is turned on
#  Loop:
#    Wait for the proxemity sensor to come on or the pushbutton to be pressed
#    Fade in some warm light
#    Keep the light on
#    While the proxemity sensor has been tripped in the last 60 seconds,
#      If the pushbutton is pressed, break out of the loop
#      Blink the neopixel
#      Keep the light on for another 10 minutes
#    Fade out the light
#
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

INITIAL_ON_SECS   = 60 * 10 # Keep the light on for at least this long
PIR_TIMEOUT_SECS  = 60      # Wait this many seconds with no motion before turning off light

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

# A color definition for "gold"
# See https://www.rapidtables.com/web/color/RGB_Color.html
COLOR = (0xFF, 0xD7, 0x00)

def loop():
    """Gets called in an infinite loop from the main code.
    """
    global pushbutton
    global pir_sensor

    # Indentation is important in Python. Make sure everything lines up if you want it
    # to live inside of a function or a loop.

    # Prints "Hello world!" to the Serial (CircuitPython REPL) window in Mu Editor
    print("Default code for HO HO HO 2022")

    # Blink an LED just to show how that's done.
    # Note that this LED is wired up with its ground lead to the MCU pin
    # so that it turns on when the pin is low (False) and turns off when
    # the pin is high (True)
    board_led.value = False
    time.sleep(.5)
    board_led.value = True
    time.sleep(.5)

    # Testing: Set the colorstrip to one color for a moment
    #set_colorstrip((0xff, 0, 0), 1.0)
    #time.sleep(2)
    #set_colorstrip((0, 0xff, 0), 1.0)
    #time.sleep(2)
    #set_colorstrip((0, 0, 0xff), 1.0)
    #time.sleep(2)

    # Wait for the pushbutton or the PIR sensor to activate
    print("Waiting for pushbutton or motion", end='')
    while True:
        if pushbutton.value is False:
            print()
            print("Button press detected.")
            break

        if pir_sensor.value is True:
            print()
            print("Motion detected.");
            board_led.value = False
            break

        time.sleep(.25)
        print(".", end="")
    print()

    print("Turning on light.")

    # Fade in the color
    linearfade_colorstrip(COLOR, 0, 1.0, 3)

    # Keep track of how long ago the PIR was triggered
    pir_last_detected_secs = 0
    # Keep track of how many seconds have elapsed since the light turned on
    elapsed_secs = 0


    print("Waiting to turn off light")
    while True:
        if pushbutton.value is False:
            print()
            print("Button press detected.")
            # exit the while loop
            break

        if pir_sensor.value is True:
            print("+", end='')
            board_led.value = False
            pir_last_detected_secs = 0
        else:
            print("-", end='')
            board_led.value = True
            pir_last_detected_secs = pir_last_detected_secs + 1

        if (elapsed_secs > INITIAL_ON_SECS and pir_last_detected_secs > PIR_TIMEOUT_SECS):
            print()
            print("Minimum time of %d seconds has expired." % (INITIAL_ON_SECS))
            print("No motion for %d seconds." % (PIR_TIMEOUT_SECS))
            # exit the while loop
            break

        time.sleep(1)
        elapsed_secs = elapsed_secs + 1


    # Fade out the color to off
    print("Turning out light.")
    linearfade_colorstrip(COLOR, 1.0, 0, 3)

    time.sleep(1)

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
