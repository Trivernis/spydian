import gyro
import time
while True:
    print(gyro.getAllOut()['rot'])
    time.sleep(1)
