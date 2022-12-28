# [HO HO HO 2022](https://github.com/ericzundel/hohoho2022)
Merry Christmas 2022 Annie, Arthur, and Casey

TL;DR Install [Mu Editor](https://codewith.mu/) on your computer. 
Plug a USB cable into the circuit board and you will see the code 
that controls the lightstrip in "code.py" that you can modify to 
control the light strip. 

# Overview
"Be nice to me or I will replace you with a very small shell script." - popular geeky tshirt

This Christmas I want to show you how you could make good on this threat
by practicing coding 
[Python](https://www.coursera.org/articles/what-is-python-used-for-a-beginners-guide-to-using-python) on an LED strip
if you don't already know it.
Python is being used to automate a lot of real world 
tasks and it is used by folks whose primary job is not software development.

# Hardware
I've soldered together a small Raspberry Pi RP2040 based 
[Adafruit KB2040 microprocessor](https://www.adafruit.com/product/5302) with 
an onboard neopixel LED that can change colors.  I also wired 
in a few components:

- A single color external LED just for fun
- A pushbutton
- A dumb LED strip with all the LEDs wires so you can control the color of all
of them at once.  
- A [PIR sensor](https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor) that can detect a person nearby. This is used for turning on
lights automatically, burglar alarms, and and things like that.

## Wiring
```
    +-----------------------------------+
    |                                   |
    |                           button  |
    +-------+                           |
USB )  MCU  |   +             +     -   |
    +-------+   3V G  R  B    3V S  GND |
    |           |  |  |  |    |  |  |   |
    +-----------------------------------+
            LEDSTRIP        PIR 
```

The PIR sensor is marked with red and green marker to show you where power and 
ground should be connected. The middle pin is the signal pin.
The PIR sensor has two tiny potentiometers you can adjust with a small screwdriver.
- T : adjusts the time the PIR signal will remain high. Turn clockwise to lower.
- S : adjusts the sensitivity of the PIR signal. Turn clockwise to lower.

The LED strip is marked +5V, R, G, B on the strip itself. The four pins 
connect closest to the microprocessor. The power pin is labeled iwth red marker on the circuit board.

## About the LED Strip
I found this bargain LED strip at Home Depot on sale gathering dust. Don't be 
fooled like I was, this LED strip has to be all the same color
at once, no matter what packaging designers want you to think with 
their [colorful advertising](https://www.amazon.com/LED-Light-Strip-RGB-Changing-Phone-Remote-Bedroom/dp/B08JH5M6N3). Also, someone goofed when printing up the circuit. R == Red, G == Blue and B == Green. No wonder it was so cheap.

This strip is sticky on the back so that you can put it somewhere like
behind a TV or under a shelf. It's also designed so that you can cut it 
where you see the copper contacts and silkscreend "+5V G R B" label. You
can also solder it together and attach multiple strips to the same controller,
but keep in mind you'll have to carefully remove the silicone waterproof
cover. I did this with an Xacto knife.

# Software
I put [CircuitPython](http://circuitpython.org) onto the microcontroller
and an example program for controlling the lightstrip. This is a version of
python that runs natively on really small computers.  Use the program
[Mu Editor](https://codewith.mu/) to edit your code.  The microprocessor runs
"code.py" ever time you save the file or the processor restarts. Use the
"Serial" button to see any output from your script or errors.

 - code.py : The code that is currently active
 - code-default.py : A copy of the code initially shipped with the project
 - code-example.py : An example of other things you can do
 - code-pir-only.py : A diagnostic to test the PIR sensor

# Future Improvements

## 3.3V  to 5V for LED power
To make sure the processor doesn't have an early death, I wired up the 
LEDs to the 3.3V regulator so the processor pins connected to the R, G, and B
lines on the strip wouldn't go over 3.3V.

- The strip is designed for 5V, so the LEDs aren't as bright as they could be.
- It only provides 500ma of power so the LEDs aren't as bright as they could be.

There are a number of ways improve this.  One way is to add a [level shifter chip](https://learn.adafruit.com/neopixel-levelshifter) to allow the full 5V power from the USB cable using the RAW pin of the KB2040. Another way would be to buy a board from Adafruit that drives LEDs through the Stemma QT port.

## Use a "smart" neopixel strip
There are other so-called ["smart" strips](https://www.amazon.com/ALITOVE-Individual-Addressable-Programmable-Non-Waterproof/dp/B01MG49QKD) 
also known as Neopixel strips or WS2811/WS2812 strips where you can 
separately control every light on the strip. Casey and I were discussing 
the finer aspects of this in the car back in November.  Make sure you get a
5 Volt version. I included a terminal on the board so you could hook one of these up without soldering anything.

## Expand using the Stemma QT port
The KB2040 has an Adafruit [Stemma QT](https://learn.adafruit.com/introducing-adafruit-stemma-qt port)
This port is also known as Qwiik in products from Sparkfun and allows you
to communicate with other devices using the I2C protocol.
You can hook up any number of things to this port with no soldering!
