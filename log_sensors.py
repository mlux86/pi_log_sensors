#!/usr/bin/python3

import Adafruit_DHT
import time
from bmp180.Adafruit_BMP085 import BMP085

ts = int(round(time.time()))

sensor = Adafruit_DHT.DHT22
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

bmp = BMP085(0x77)
pressure = bmp.readPressure() / 100.0

print('%d\t%.01f\t%.01f\t%.01f' % (ts, temperature, humidity, pressure))
