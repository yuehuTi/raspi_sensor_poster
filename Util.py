#-*- coding:UTF-8 -*-
from ctypes import c_short

def convertToString(data):
  # Simple function to convert binary data into
  # a string
  return str((data[1] + (256 * data[0])) / 1.2)
 
def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index]<< 8) + data[index + 1]).value
 
def getUshort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index]<< 8) + data[index + 1]