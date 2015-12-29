# -*- coding: utf-8 -*- 
import os
import imp
import time
import requests
import json

api_url='http://api.yeelink.net/v1.0'
api_key=your_api_key
api_headers={'U-ApiKey':api_key,'content-type': 'application/json'}

sensors = []

def upload_data_to_yeelink(device, sensor, data):
    url=r'%s/device/%s/sensor/%s/datapoints' % (api_url,device,sensor)
    strftime=time.strftime("%Y-%m-%dT%H:%M:%S")
    data={"timestamp":strftime , "value": data}
    res=requests.post(url,headers=api_headers,data=json.dumps(data))


def load_sensors():
    sensor_path = os.path.abspath("Sensor") + "/"
    sensor_files = os.listdir(sensor_path)

    for filename in sensor_files:
        if filename[-3:] != ".py":
            continue
        try:
            sensor_name = filename[:-3]
            module = imp.load_source(sensor_name, sensor_path + filename)
            class_obj = getattr(module, sensor_name)
            instance = class_obj()
            sensors.append(instance)
        except Exception, e:
            print "Sensor %s load error:%s"%(filename, e)

def run():
    while True:
        for sensor in sensors:
            try:
                result = sensor.GetData()
                for data in result:
                    upload_data_to_yeelink(data["device"], data["sensor"], data["data"])
            except Exception, e:
                print str(e)
        time.sleep(1*60)

if __name__ == '__main__':
    load_sensors()
    run()
        