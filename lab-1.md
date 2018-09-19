# Lab 1
Create a counter for people passing by an ultrasonic sensor.

## Environment

For this lab, we are using a Raspberry Pi 3 installed with Arch Linux ARM.
Additionally, Python 3.7 has been installed, as well as `pip`, which lets us in turn install `gpiozero`, and `RPi.GPIO`.

```
$ pacman -S python python-pip
$ pip install gpiozero rpi.gpio
```

### Hardware

As previously mentioned, we are using a Raspberry Pi 3. The sensor we are using is an HC-SR04 ultrasonic sensor. 
The sensor sends out a high frequency (40,000 Hz) sound, and measures the time it takes for it to be reflected and sent back.

Additionally, we will use two resistors, at 330Ω and 220Ω, although the specific resitance does not matter
as long as the resistance of the two are approximately at a 2/3 ratio. 
These will form a voltage divider between the ground and the echo pin of the ultrasonic sensor.

To recap, here is the complete list of components used in this build. Also, a breadboard is useful, and expect to use some wires.

```
1x Raspberry Pi 3
1x HC-SR04 ultrasonic sensor
1x 330Ω resistor
1x 220Ω resistor
```

#### Schematic and pictures

Here is a simple graphical schematic of the build, as well as a few pictures of my build.

![Image of schematic](https://i.imgur.com/taGtrbJ.png)

**Note**: Apologies for the differing colors of the wiring in the following pictures. 
I only had female to female and male to male cables, so I combined one of each to create a female to male connection, 
but I did not have a chance to match cable colors.

![Image of breadboard](https://i.imgur.com/x92vYzz.jpg)

![Image of Raspberry Pi](https://i.imgur.com/VT5Q5my.jpg)

### Software

This is where Python and the aforementioned libraries come in. 
It is to be noted that `gpiozero` uses `RPi.GPIO` to interface with the Raspberry Pi's GPIO pins, we only need to import
`gpiozero`.

The following code snippet contains what's necessary to connect to the sensor, and read out a single distance value.
Note that you may have to run the script as root in order to have the privileges to read and write to the GPIO pins.

```python
from gpiozero import DistanceSensor

# echo=17 means that we expect the voltage divider to be connected to GPIO pin 17
# trigger=18 means that we expect the trigger to be connected to the GPIO pin 18
# max_distance=400 means that we set the max sensor distance to be 400 cm,
# which according to spec is the maximum distance the HC-SR04 can measure
sensor = DistanceSensor(echo=17, trigger=18, max_distance=400)

# let's print the measured distance in cm, to 2 decimal points
print("{:.2f} cm".format(sensor.distance * 100))
```

It might be obvious how this system will work; the distance must be polled at a regular interval,
and in order to count people passing by the sensor, we need a default value (the distance from the sensor to the opposing wall, 
or as long as the sensor can measure), as well as a current value. 
If the default value and current value differs by a significant amount, we *could* increment a counting variable.
This approach is rather naïve: depending on the polling rate, and how fast/slow people pass by, 
we may get multiple increments for a slow person, or no increments for a fast person. 

Instead, I opted for a falling edge approach, where I also introduced a "previous" value which is updated in certain situations.
When someone passes by, and the sensor notices a major difference from the default value, the "previous" value gets updated.
For every loop where this difference is present, the previous value gets updated.
If this clause is not met, the difference between the previous and current values is checked, if they are far from one another. 
Additionally, the difference between the current and default values is checked, if they are very close to one another.
If this clause is met, we'll count a person to have passed by, and update the previous value for the next loop.

In essence, this means that for as long as the difference between the current and default values is large, only the previous
value is updated, and once the current distance is back to the default, we can make sure a person has passed by. Here's the relevant code:

```python
from gpiozero import DistanceSensor
from time import sleep

def count(sensor):
        count = 0
        default = sensor.distance * 100
        previous = default
        now = 100 + previous
        while True:
                now = sensor.distance * 100
                print("Count: {:<4 distance: {:.2f}\r".format(count, now), end="")
                if default - now > 40:
                        previous = sensor.distance * 100
                elif now - previous > 40 and default - now < 10:
                        previous = sensor.distance * 100
                        count += 1
                sleep(0.1)

sensor = DistanceSensor(echo=17, trigger=18, max_distance=400)
count(sensor)
```


## Limitations

While this approach to measuring people is simple, it also has major limitations. 
If multiple people pass by at once, this algorithm will not be sufficient to accurately measure each person,
nor will the sensor have the capability to notice that there are multiple people passing by side by side.

The polling rate is also very important. A fast rate makes the application rather CPU intensive,
while a slow rate might not be able to count fast people accurately, and a line of people may be counted as a single person.

One of the key goals of the project is also not met with this. Namely measuring the direction of people passing by. 
A single ultrasonic sensor is simply not capable of such measurements. One could have two such sensors in a line, and
between them measure which one is activated first. If sensor A is activated first, and sensor B is activated second, 
the person would be measured as going in the direction of sensor B, the opposite is also true. 
Unfortunately, the aforementioned limitation of the ultrasonic sensor still holds true in this case, the sensors will not
be able to notice multiple people passing by at once, thus resulting in inaccurate counting.

To conclude, this type of sensor is not sufficient for our needs, and other approaches must be researched and tested out.
