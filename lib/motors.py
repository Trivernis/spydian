from time import sleep
import RPi.GPIO as GPIO
from thread import start_new_thread
import sys


class Motor(object):
    def __init__(self, pins):
        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]
        self.deg_per_step = 5.625 / 64
        self.steps_per_rev = int(360 / self.deg_per_step)  # 4096
        self.step_angle = 0  # Assume the way it is pointing is zero degrees
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

    def __exit__(self, type_of_motor, value, traceback):
        self.clean_pins_up()

    def _set_rpm(self, rpm):
        """Set the turn speed in RPM."""
        self._rpm = rpm
        # T is the amount of time to stop between signals
        self._T = (60.0 / rpm) / self.steps_per_rev

    # This means you can set "rpm" as if it is an attribute and
    # behind the scenes it sets the _T attribute
    rpm = property(lambda self: self._rpm, _set_rpm)

    def clean_pins_up(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

    def move_to(self, angle):
        """Take the shortest route to a particular angle (degrees)."""
        # Make sure there is a 1:1 mapping between angle and stepper angle
        target_step_angle = 8 * (int(angle / self.deg_per_step) / 8)
        steps = target_step_angle - self.step_angle
        steps = (steps % self.steps_per_rev)
        if steps > self.steps_per_rev / 2:
            steps -= self.steps_per_rev
            print("moving " + repr(steps) + " steps")
            self._move_acw(-steps / 8)
        else:
            print("moving " + repr(steps) + " steps")
            self._move_cw(steps / 8)
        # self.step_angle = target_step_angle #in case you want to keep track of the position
        self.step_angle = 0

    def _move_acw(self, big_steps):
        self.clean_pins_up()
        for _ in range(big_steps):
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)
        self.clean_pins_up()

    def _move_cw(self, big_steps):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)
        for _ in range(big_steps):
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)
        self.clean_pins_up()


if __name__ == "__main__":
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    m_l = Motor([6, 13, 19, 26])
    # m_r = Motor([10, 9, 11, 25])
    m_l.rpm = float(sys.argv[1])
    # m_r.rpm = float(sys.argv[1])
    print("Pause in seconds: " + repr(m_l._T))
    i = 1
    while i < 5:
        start_new_thread(m_l.move_to, (int(sys.argv[2]),))
        # start_new_thread(m_r.move_to, (int(sys.argv[3]),))
        sleep(2)
        i = i + 1
    GPIO.cleanup()
