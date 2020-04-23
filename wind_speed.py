from gpiozero import Button
import math
import time
import statistics

store_speeds = []

wind_count = 0
radius_cm = 9.0
wind_interval = 5
comp_val=1.18


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


while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        time.sleep(wind_interval)
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)

    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    print(wind_speed, wind_gust)


#Loop to measure wind speed and report at 5-seconds intervals
#def getWindSpeed(timeInterval=5):
#    wind_count = 0
#    time.sleep(timeInterval)
    #print(calculate_speed(wind_interval), "m/s")
#    return calculate_speed(timeInterval)

