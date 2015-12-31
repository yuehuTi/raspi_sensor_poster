#-*- coding:UTF-8 -*-
import os
import sys  
sys.path.append('../')

import Sensor
import Util

device_id=your_device_ID
sensor_id=your_SenorID

class RasPi(Sensor.Sensor):
    def __init__(self):
        super(RasPi, self).__init__()

    def GetData(self):
        res = os.popen('vcgencmd measure_temp').readline()
        temparure = res.replace("temp=","").replace("'C\n","")
        return [{
                    "name": "CPU Temp",
                    "symbol": "C",
                    "device": device_id,
                    "sensor": sensor_id,
                    "data": temparure
                }]
if __name__ == '__main__':
    sensor = RasPi()
    print sensor.GetData()