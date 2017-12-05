#-*- coding:UTF-8 -*-
import serial
import time
import struct
import sys  
sys.path.append('../')

import Sensor

DeviceID = your_device_ID
PM2_5_SenorID = your_SenorID
PM10_SenorID = your_SenorID

class PMS5003(Sensor.Sensor):
    def __init__(self):
        super(PMS5003, self).__init__()
        

    def GetData(self):
        while True:
            # 获得接收缓冲区字符
            self.ser = serial.Serial("/dev/ttyAMA0", 9600)
            count = self.ser.inWaiting()
            if count >=32:
                recv = self.ser.read(32)

                sign1,sign2,frame_length,pm1_0_cf,pm2_5_cf,pm10_cf,pm1_0,pm2_5,pm10,cnt_03,cnt_05,cnt_10,cnt_25,cnt_50,cnt_100,reserve,checksum = struct.unpack(">bbHHHHHHHHHHHHHHH", recv)
                d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13 = struct.unpack(">xxxxxBxBxBxBxBxBxBxBxBxBxBxBxBxx", recv)

                if sign1 == 0x42 and sign2 == 0x4d:
                    break
            self.ser.close()
            time.sleep(1)
        return [{
                    "name": "PM2.5",
                    "symbol": "ug/m^3",
                    "device": DeviceID,
                    "sensor": PM2_5_SenorID,
                    "data": pm2_5
                },
                {
                    "name": "PM10",
                    "symbol": "ug/m^3",
                    "device": DeviceID,
                    "sensor": PM10_SenorID,
                    "data": pm10
                }]
if __name__ == '__main__':
    sensor = PMS5003()
    print sensor.GetData()