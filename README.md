# hohoho2022
Merry Christmas 2022 Annie Arthur and Casey

Original code is on [github](https://github.com/ericzundel/hohoho2022)

TL;DR  Install [Mu Editor](https://codewith.mu/) on your computer. 
Plug a USB cable into the circuit board and you will see the code 
that controls the lightstrip in "code.py" that you can modify to 
control the light strip. 

"Be nice to me or I will replace you with a very small shell script"
 - geeky tshirt

This Christmas I want to show you how you could make good on this threat
by practicing coding an LED strip with  
[Python](https://www.coursera.org/articles/what-is-python-used-for-a-beginners-guide-to-using-python), 
if you don't already know some.  It's not a shell script, but I think 
it's better because Python is being used to automate a lot of real world 
tasks and it is used by folks whose primary job is not software development.

I've soldered together a small Raspberry Pi RP2040 based 
[microprocessor](https://www.adafruit.com/product/5302) with 
an onboard neopixel LED that can change colors.  I also wired 
in a few components:

- An external LED just for fun
- A dumb LED strip with all the LEDs wires so you can control the color of all
of them at once.  
- A PIR sensor that can detect a person nearby. This is used for turning on
lights automatically, burglar alarms, and and things like that.

I put [CircuitPython](http://circuitpython.org) onto the microcontroller
and an example program for controlling the lightstrip. This is a version of
python that runs natively on really small computers.  Use the program
[Mu Editor](https://codewith.mu/) to edit your code.  The microprocessor runs
"code.py" ever time you save the file or the processor restarts. Use the
"Serial" button to see any output from your script or errors.

I found this bargain LED strip at Home Depot on sale gathering dust. Don't be 
fooled like I was, this LED strip has to be all the same color
at once, no matter what packaging designers want you to think with 
their [colorful advertising](https://www.amazon.com/LED-Light-Strip-RGB-Changing-Phone-Remote-Bedroom/dp/B08JH5M6N3). No wonder it was so cheap.

This strip is sticky on the back so that you can put it somewhere like
behind a TV or under a shelf. It's also designed so that you can cut it 
where you see the copper contacts and silkscreend "+5V G R B" label. You
can also solder it together and attach multiple strips to the same controller,
but keep in mind you'll have to carefully remove the silicone waterproof
cover. I did this with an Xacto knife.

There are other so-called ["smart" strips](https://www.amazon.com/ALITOVE-Individual-Addressable-Programmable-Non-Waterproof/dp/B01MG49QKD) 
also known as Neopixel strips or WS2811/WS2812 strips where you can 
separately control every light on the strip. Casey and I were discussing 
the finer aspects of this in the car back in November.  Make sure you get a
5 Volt version. I included a terminal on the board so you could hook one of these up without soldering anything.
