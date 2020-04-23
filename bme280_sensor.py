import bme280
import smbus2
from time import sleep

port = 1
address = 0x76 #Adress to the BME280 sensor. Found by using the command "i2c detect y- 1" in the consoll on the raspberry.
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def getAllTemp():
    bme280_data = bme280.sample(bus,address)
    return bme280_data.humidity, bme280_data.pressure, bme280_data.temperature
