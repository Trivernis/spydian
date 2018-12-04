from lib import ultrasonic

sensor = ultrasonic.Sensor()
sensor.init(11, 7)
print('Beginn der Messung')
print(sensor.echo())
sensor.cleanup()
