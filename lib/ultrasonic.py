import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


class Sensor(object):
    def init(self, TRIG, ECHO):
        self.TRIGGER = TRIG
        self.ECHO = ECHO
        self.lastValues = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
            # print(time.time()-abs_start)
            pass
        pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1 and (time.time() - abs_start) < 0.02:
            # print(time.time()-abs_start)
            pass
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)
        self.lastValues.append(distance)
        self.lastValues = self.lastValues[1:]
        distance = round((sum(self.lastValues)) / (len(self.lastValues)), 2)
        # print(self.lastValues)
        # print("Distance: {}".format(distance))
        return distance

    def clean(self):
        GPIO.cleanup()
