#-*- coding:UTF-8 -*-
import smbus
import time
import sys  
sys.path.append('../')

import Sensor
from Util import getShort, getUshort

DeviceID = your_device_ID
Tempature_SenorID = your_SenorID
Pressure_SenorID = your_SenorID

I2c_Number = 1
I2c_addr = 0x77

class BMP180(Sensor.Sensor):
    def __init__(self):
        super(BMP180, self).__init__()
        self.bus = smbus.SMBus(I2c_Number)

    def GetData(self):
        # Register Addresses
        REG_CALIB  = 0xAA
        REG_MEAS   = 0xF4
        REG_MSB    = 0xF6
        REG_LSB    = 0xF7
        # Control Register Address
        CRV_TEMP   = 0x2E
        CRV_PRES   = 0x34
        # Oversample setting
        OVERSAMPLE = 3    # 0 - 3

        # Read calibration data
        # Read calibration data from EEPROM
        cal = self.bus.read_i2c_block_data(I2c_addr, REG_CALIB, 22)

        # Convert byte data to word values
        AC1 = getShort(cal, 0)
        AC2 = getShort(cal, 2)
        AC3 = getShort(cal, 4)
        AC4 = getUshort(cal, 6)
        AC5 = getUshort(cal, 8)
        AC6 = getUshort(cal, 10)
        B1  = getShort(cal, 12)
        B2  = getShort(cal, 14)
        MB  = getShort(cal, 16)
        MC  = getShort(cal, 18)
        MD  = getShort(cal, 20)

        # Read temperature
        self.bus.write_byte_data(I2c_addr, REG_MEAS, CRV_TEMP)
        time.sleep(0.005)
        (msb, lsb) = self.bus.read_i2c_block_data(I2c_addr, REG_MSB, 2)
        UT = (msb << 8) + lsb

        # Read pressure
        self.bus.write_byte_data(I2c_addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
        time.sleep(0.04)
        (msb, lsb, xsb) = self.bus.read_i2c_block_data(I2c_addr, REG_MSB, 3)
        UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

        # Refine temperature
        X1 = ((UT - AC6) * AC5) >> 15
        X2 = (MC << 11) / (X1 + MD)
        B5 = X1 + X2
        temperature = (B5 + 8) >> 4

        # Refine pressure
        B6  = B5 - 4000
        B62 = B6 * B6 >> 12
        X1  = (B2 * B62) >> 11
        X2  = AC2 * B6 >> 11
        X3  = X1 + X2
        B3  = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

        X1 = AC3 * B6 >> 13
        X2 = (B1 * B62) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> OVERSAMPLE)

        P = (B7 * 2) / B4

        X1 = (P >> 8) * (P >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * P) >> 16
        pressure = P + ((X1 + X2 + 3791) >> 4)

        temperature = temperature/10.0
        pressure = pressure/100.0

        return [{
                    "name": "Tempature-BMP180",
                    "symbol": "C",
                    "device": DeviceID,
                    "sensor": Tempature_SenorID,
                    "data": temperature
                },
                {
                    "name": "Air Pressure",
                    "symbol": "hPa",
                    "device": DeviceID,
                    "sensor": Pressure_SenorID,
                    "data": pressure
                }]
if __name__ == '__main__':
    sensor = BMP180()
    print sensor.GetData()