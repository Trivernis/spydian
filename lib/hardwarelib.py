from subprocess import call, check_output
from lib import ultrasonic
import RPi.GPIO as GPIO
import time


class Navigator:
    """Forward Motor with relais, Steering with servo"""

    def __init__(self, mrelaispin):
        self.mrelpin = mrelaispin
        self.steer = None
        GPIO.setup(self.mrelpin, GPIO.OUT)
        self.stop()

    def left(self):
        if self.steer != 'left':
            call(['python', './lib/servolib.py', 'left'])
            self.steer = 'left'

    def right(self):
        if self.steer != 'right':
            call(['python', './lib/servolib.py', 'right'])
            self.steer = 'right'

    def straight(self):
        if self.steer:
            call(['python', './lib/servolib.py'])
            self.steer = None

    def forward(self):
        GPIO.output(self.mrelpin, False)

    def stop(self):
        GPIO.output(self.mrelpin, True)


class Light:
    """Light switched with a relays"""

    def __init__(self, lightpin):
        self.pin = lightpin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, True)
        self.shine = False

    def switch(self):
        print('light switch {}'.format(self.shine))
        GPIO.output(self.pin, not self.shine)
        self.shine = not self.shine

    def switch_on(self):
        GPIO.output(self.pin, False)

    def switch_of(self):
        GPIO.output(self.pin, True)


class Ultrasonic:
    """A ultrasonic sensor"""

    def __init__(self, trigger, echo):
        self.sensor = ultrasonic.Sensor()
        self.sensor.init(trigger, echo)
        self.time = 0
        self.distance = 0

    def get_distance(self):
        if (time.time() - self.time) > 1:
            self.distance = self.sensor.echo()
            self.time = time.time()
        return self.distance

    def __del__(self):
        self.sensor.cleanup()


class Temperature:
    """A temperature sensor"""

    def __init__(self):
        pass

    @staticmethod
    def get_temperature():
        outp = check_output(['python', '-u', './lib/thermolib.py']).decode('ISO-8859-1')
        temp, hum = outp.split('|')
        return temp

    @staticmethod
    def get_humidity():
        outp = check_output(['python', '-u', './lib/thermolib.py']).decode('ISO-8859-1')
        temp, hum = outp.split('|')
        return hum
