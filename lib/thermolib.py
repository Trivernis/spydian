import Adafruit_DHT


def main():
    humidity, temperature = Adafruit_DHT.read_retry(11, 14)
    print
    '{}|{}'.format(temperature, humidity)


if __name__ == '__main__':
    main()
