#-*- coding:UTF-8 -*-
import serial
import time
import struct
import sys  
sys.path.append('../')

import Sensor

# DeviceID = 343685 
# PM2_5_SenorID = 1 
# PM10_SenorID = 2

GateWayID = "01"
PM2_5_SenorID = "PM25"
PM10_SenorID = "PM10"
CO2_SenorID = "CO2"
CH2O_SenorID = "CH2O"
TVOC_SenorID = "TVOC"

class M701SC(Sensor.Sensor):
    def __init__(self):
        super(M701SC, self).__init__()
        sleep(2*60) #HCHO、CO2、TVOC warmup time

    def GetData(self):
        ser = serial.Serial("/dev/ttyAMA0", 9600)
        # 获得接收缓冲区字符
        while ser.read() != chr(0x3c):
            continue
        recv = ser.read(16)

        sign2,eCO2_H,eCO2_L,eCH2O_H,eCH2O_L,TVOC_H,TVOC_L,pm2_5_H,pm2_5_L,pm10_H,pm10_L,temp_I,temp_F,humi_I,humi_F,checksum = struct.unpack(">bbbbbbbbbbbbbbbb", recv)

        # print sign2,eCO2_H,eCO2_L,eCH2O_H,eCH2O_L,TVOC_H,TVOC_L,pm2_5_H,pm2_5_L,pm10_H,pm10_L,temp_I,temp_F,humi_I,humi_F,checksum
        if sign2 != 0x2:
            return []

        eCO2 = eCO2_H*256+eCO2_L
        eCH2O = eCH2O_H*256+eCH2O_L
        TVOC = TVOC_H*256+TVOC_L
        pm2_5 = pm2_5_H*256+pm2_5_L
        pm10 = pm10_H*256+pm10_L
        Temperature = temp_I+temp_F*0.1
        Humidity = humi_I+humi_F*0.1

        # print "CO2:%d, HCHO:%d, TVOC:%d, pm2_5:%d, pm10:%d, Temperature:%.2f, Humidity:%.2f"%(eCO2,eCH2O,TVOC,pm2_5,pm10,Temperature,Humidity)
        ser.flushInput()
        ser.close()
        return [{
                    "name": "CH2O",
                    "symbol": "ug/m^3",
                    "device": GateWayID,
                    "sensor": CH2O_SenorID,
                    "data": eCH2O
                },
                {
                    "name": "TVOC",
                    "symbol": "ug/m^3",
                    "device": GateWayID,
                    "sensor": TVOC_SenorID,
                    "data": TVOC
                },
                {
                    "name": "CO2",
                    "symbol": "PPM",
                    "device": GateWayID,
                    "sensor": CO2_SenorID,
                    "data": eCO2
                },
                {
                    "name": "PM25",
                    "symbol": "ug/m^3",
                    "device": GateWayID,
                    "sensor": PM2_5_SenorID,
                    "data": pm2_5
                },
                {
                    "name": "PM10",
                    "symbol": "ug/m^3",
                    "device": GateWayID,
                    "sensor": PM10_SenorID,
                    "data": pm10
                }]
if __name__ == '__main__':
    sensor = M701SC()
    print sensor.GetData()
