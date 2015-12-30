# -*- coding: utf-8 -*- 
import os
import sys
import imp
import time
import requests
import json

api_url='http://api.yeelink.net/v1.0'
api_key=your_api_key
api_headers={'U-ApiKey':api_key,'content-type': 'application/json'}

sensors = []

def logout(str):
    print "[%s]%s"%(time.strftime("%Y-%m-%d %H:%M:%S"), str)
    sys.stdout.flush()


def upload_data_to_yeelink(device, sensor, data):
    url=r'%s/device/%s/sensor/%s/datapoints' % (api_url,device,sensor)
    strftime=time.strftime("%Y-%m-%dT%H:%M:%S")
    data={"timestamp":strftime , "value": data}
    res=requests.post(url,headers=api_headers,data=json.dumps(data))
    if res.status_code != 200:
        return (False, res.status_code)
    else:
        return (True, None)

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
            logout("Sensor %s load error:%s"%(filename, e)) 

def run():
    while True:
        for sensor in sensors:
            try:
                logout("Sensor %s fetching data..."%sensor.__class__.__name__) 
                result = sensor.GetData()
                for data in result:
                    res, err = upload_data_to_yeelink(data["device"], data["sensor"], data["data"])
                    logout("SensorID: %s Data: %s Uploaed: %s"%(str(data["sensor"]), str(data["data"]), "Success" if res else "Failed: %s"%err)) 
            except Exception, e:
                logout(str(e))
        logout( "Sleep")
        time.sleep(1*60)

if __name__ == '__main__':    
    load_sensors()
    run()