import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


class Sensor(object):
    def __init__(self, trigger, echo):
        self.TRIGGER = trigger
        self.ECHO = echo
        self.lastValue = 0
        self.lastValuesCount = 1
        GPIO.setup(self.TRIGGER, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIGGER, False)
        print('Waiting for Sensor to settle')
        time.sleep(2)

    def echo(self):
        GPIO.output(self.TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER, False)
        abs_start = time.time()

        while GPIO.input(self.ECHO) == 0 and (time.time() - abs_start) < 0.02:
            pass
        pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1 and (time.time() - abs_start) < 0.02:
            pass
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)
        lastc = self.lastValuesCount
        self.lastValue = (1/lastc) * distance + ((lastc-1)/lastc) * self.lastValue
        distance = self.lastValue
        return distance

    @staticmethod
    def cleanup():
        GPIO.cleanup()
