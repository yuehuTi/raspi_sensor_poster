树莓派传感器数据上传yeelink的代码

Notice:
 - python-smbus python-serial库:apt-get install python-smbus python-serial
 - python的wiringpi2: pip install wiringpi2
 - 
 - 使用前修改yeelink_poster.py中的api_key, 在yeelink上面获得
 - 修改Sensor下面各个传感器deviceID和sensorID，对应yeelink上自己创建的设备和传感器id
 - 自己添加传感器可按照Sensor.py，继承sensor类，实现getdata方法，放到sensor文件夹下面即可
 - 长期运行建议使用supervisor
