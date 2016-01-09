#-*- coding:UTF-8 -*-
import smbus
import time
import sys  
sys.path.append('../')

import Sensor
from Util import getShort, getUshort

I2c_Number = 1
GY30_addr = 0x23

DeviceID = your_device_ID
Light_SenorID = your_SenorID

class GY30(Sensor.Sensor):
    def __init__(self):
        super(GY30, self).__init__()
        self.bus = smbus.SMBus(I2c_Number)

    def GetData(self):
        data = self.bus.read_i2c_block_data(GY30_addr, 0x11)
        value = (data[1] + (256 * data[0])) / 1.2
        return [{
                    "name": "Lux(GY30)",
                    "symbol": "lux",
                    "device": DeviceID,
                    "sensor": Light_SenorID,
                    "data": "%.2f"%value
                }]

if __name__ == '__main__':
    sensor = GY30()
    print sensor.GetData()


