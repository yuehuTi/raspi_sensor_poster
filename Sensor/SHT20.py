#-*- coding:UTF-8 -*-
import smbus
import time
import sys  
sys.path.append('../')

import Sensor
from Util import getShort, getUshort

I2c_Number = 1

DeviceID = your_device_ID
Tempature_SenorID = your_SenorID
RH_SenorID = your_SenorID

eSHT2xAddress       = 0x40
eTempHoldCmd        = 0xE3
eRHumidityHoldCmd   = 0xE5
eTempNoHoldCmd      = 0xF3
eRHumidityNoHoldCmd = 0xF5
writeUserRegister   = 0xE6
readUserRegister    = 0xE7
softReset           = 0xFE

def getRHumidity(bus):
        return (-6.0 + 125.0 / 65536.0 * float(readSensor(bus, eRHumidityNoHoldCmd)))
        
    


#**********************************************************
#* GetTemperature
#*  Gets the current temperature from the sensor.
#*
#* @return float - The temperature in Deg C
#**********************************************************/
def getTemperature(bus):
        return (-46.85 + 175.72 / 65536.0 * float(readSensor(bus, eTempNoHoldCmd)))
    


#******************************************************************************
#* Private Functions
#******************************************************************************/
def readSensor(bus, command):    
        bus.write_quick(eSHT2xAddress)
        bus.write_byte(eSHT2xAddress,command)
        time.sleep(0.1)
        result =(bus.read_byte(eSHT2xAddress)<<8)
        result += bus.read_byte(eSHT2xAddress)
        result &= ~0x0003   # clear two low bits (status bits)(0x0003=00000000 00000011 =>~0x0003=11111111 11111100=> &=xxxxxxxx xxxxxx00)
        return result

class SHT20(Sensor.Sensor):
    def __init__(self):
        super(SHT20, self).__init__()
        self.bus = smbus.SMBus(I2c_Number)

    def GetData(self):
        return [{
                    "device": DeviceID,
                    "sensor": Tempature_SenorID,
                    "data": "%.2f" %getTemperature(self.bus)
                },
                {
                    "device": DeviceID,
                    "sensor": RH_SenorID,
                    "data": "%.2f" %getRHumidity(self.bus)
                }]
if __name__ == '__main__':
    sensor = SHT20()
    print sensor.GetData()