import smbus
import time
import math

bus = smbus.SMBus(1)
address = 0x4d

count = 0
values = []
volts = {2.9: 0,
         2.0: 30,
         2.2: 60,
         0.4: 90,
         1.1: 120,
         0.7: 150,
         1.5: 180,
         1.3: 215,
         2.6: 215,
         2.4: 215,
         3.1: 270,
         3.3: 315}


def read():
        data = bus.read_byte_data(address, 1)
        data=data/15
        return data
    
def get_average(angles):
    sin_sum=0.0
    cos_sum=0.0
    
    for angle in angles:
        r=math.radians(angle)
        sin_sum+=math.sin(r)
        cos_sum+=math.cos(r)
        
    flen = float(len(angles))
    s=sin_sum/flen
    c=cos_sum/flen
    arc = math.degrees(math.atan(s/c))
    average = 0.0
    
    if s>0 and c>0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360
    average=round(average, 0)
        
    return 0 if average == 360 else int(average)

def get_value(length=5):
    data=[]
    #print("Measuring wind direction for %d seconds..." % length)
    start_time=time.time()
    
    while time.time() - start_time <= length:
        wind = round(read()*3.3,1)
        if not wind in volts:
            print ("Unknown value " + str(wind))
        else:
            data.append(volts[wind])
    return get_average(data)
        

#while True:
#    data=get_value()
#    print(data)
        
