from gpiozero import Button

rain_sensor=Button(6)
rain_count = 0
BUCKET_SIZE = 0.2794

def bucket_tipped():
    global count
    rain_count = rain_count +1
    print (count*BUCKET_SIZE)
    
rain_sensor.when_pressed = bucket_tipped

def resetRainfall():
    global rain_count
    raincount=0