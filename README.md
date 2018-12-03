Spydian
===

Summary
---

This python project is the controlling software for the Spydian remote controlled car.
The car can be controlled with a (XBOX) Joystick and consists of a raspberry pi as core unit, 
several sensors (Gyroscope, Ultrasonic, Camera) and a relay for switching lights and motors on
and off. The controlling part is achived by using pygame to get direct access to the controller
events. The software itself is splitted into several libraries for handling specific tasks.

Install
---

To install the requirements execute the install.sh script. This script does not install Python but
uses pip. So first you need to install Python 2 and Python 3 because this software uses both
versions. You also need to connect all sensors and relays to the specific pins.

Usage
---

To execute the software the main.py script needs to be run. Open a console and type 
`sudo python3 main.py`. Notice that the superuser rights are required because the script needs
access to the GPIO-Pins of the raspberry pi.