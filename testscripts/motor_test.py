import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def full_step(phase, pins):
    pin1, pin2, pin3, pin4 = pins

    if phase == 0:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 0)

    if phase == 1:
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 1)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 0)

    if phase == 2:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 1)
        GPIO.output(pin3, 1)
        GPIO.output(pin4, 0)

    if phase == 3:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 1)
        GPIO.output(pin4, 1)

    if phase == 4:
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 1)


def half_step(phase, pins):
    pin1, pin2, pin3, pin4 = pins

    if phase == 0:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 0)

    if phase == 1:
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 0)

    if phase == 2:
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 1)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 0)

    if phase == 3:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 1)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 0)

    if phase == 4:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 1)
        GPIO.output(pin3, 1)
        GPIO.output(pin4, 0)

    if phase == 5:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 1)
        GPIO.output(pin4, 0)

    if phase == 6:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 1)
        GPIO.output(pin4, 1)

    if phase == 7:
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 1)

    if phase == 8:
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 0)
        GPIO.output(pin3, 0)
        GPIO.output(pin4, 1)


def full_phase(pins):
    # order=[1,2,3,4]
    order = [4, 3, 2, 1]
    print("Moving in {}-order".format(order))
    for i in order:
        full_step(i, pins)
        time.sleep(0.005)


def half_phase(pins):
    for i in range(0, 8):
        half_step(i, pins)
        time.sleep(0.0025)


def forward(pins):
    half_phase(pins)


def backward(pins):
    (pins[0], pins[1], pins[2], pins[3]) = (pins[1], pins[0], pins[2], pins[3])
    half_phase(pins)


if __name__ == '__main__':
    pins = [6, 13, 19, 26]
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
    while True:
        try:
            start = time.time()
            while (time.time() < start + 10):
                forward(pins)
            start = time.time()
            while (time.time() < start + 10):
                backward(pins)
        except KeyboardInterrupt:
            break
    GPIO.cleanup()
