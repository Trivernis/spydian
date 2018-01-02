import Adafruit_PCA9685 as ServoLib
import sys

pwm = ServoLib.PCA9685()
pwm.set_pwm_freq(60)

def left():
    pwm.set_pwm(0,0,261)

def right():
    pwm.set_pwm(0,0,479)

def reset():
    pwm.set_pwm(0,0,370)

if __name__ == '__main__':
    args=sys.argv
    if 'left' in args:
        left()
    elif 'right' in args:
        right()
    else:
        reset()