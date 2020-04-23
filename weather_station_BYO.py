from gpiozero import Button
from PiToDB import *
import time
import math
import bme280_sensor
import wind_direction
import statistics
store_speeds = []
store_directions = []

ref = GetDbRef("key.json", "https://jolyu-ntnu.firebaseio.com/")

wind_count = 0
rain_count=0
radius_cm = 9.0
wind_interval = 5
comp_val=1.18
BUCKET_SIZE = 0.2794


def spin():
    global wind_count
    wind_count = wind_count + 1
    #print("spin" + str(wind_count))

#Calculate wind speed
def calculate_speed(time_sec):
    global wind_count
    circumference=(2*math.pi)*radius_cm/100
    rotations=wind_count/2.0
    #Calculate distance travvelled by a cup in cm
    dist=circumference*rotations
    speed=dist/time_sec*comp_val
    return speed

def reset_wind():
    global wind_count
    wind_count=0

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin

def bucket_tipped():
    global rain_count
    rain_count = rain_count + 1
    #print (rain_count * BUCKET_SIZE)

def reset_rainfall():
    global rain_count
    rain_count = 0

rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped

while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        wind_start_time = time.time()
        reset_wind()
        #time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append( wind_direction.get_value())
            
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    wind_dir = wind_direction.get_average(store_directions)
    
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    
    #rainfall
    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()
    
    #bme280
    humidity, pressure, temp = bme280_sensor.getAllTemp()

    print("Wind speed: ", round(wind_speed,1), "\n",
          "Wind gust: ", round(wind_gust,1), "\n",
          "Wind direction: ", wind_dir, "\n",
          "Humidity: ", round(humidity,1), "\n",
          "Pressure: ", round(pressure,1), "\n",
          "Temperature ", round(temp,1), "\n",
          "Rainfall ", round(rainfall,1), "\n",
          )
    
    data = {"birds": 1,
            "Wind speed": round(wind_speed,3),
          "Wind gust": round(wind_gust,3), 
          "Wind direction": wind_dir, 
          "Humidity": round(humidity,1),
          "Pressure": round(pressure,1), 
          "Temperature": round(temp,3), 
          "Rainfall": round(rainfall,1)
    }
    
    PushDB(ref, data)
   
    store_speeds = []
    store_directions = []
