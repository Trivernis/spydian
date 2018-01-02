import sys
import Adafruit_DHT

while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, 14)

    print 'Temp: {} C  Humidity: {} %'.format(temperature, humidity)