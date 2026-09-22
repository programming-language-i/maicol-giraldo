# crear 5 sensores a partir de hilos y que den su temperatura.

import threading
import random
import time

def sensor_temperatura(sensor_id):
    while True:
        temperatura = random.uniform(20.0, 30.0)  
        print(f"Sensor {sensor_id}: {temperatura:.2f} °C")
        time.sleep(random.uniform(1, 3))  


for i in range(5):
    sensor_thread = threading.Thread(target=sensor_temperatura, args=(i+1,))  
    sensor_thread.start()

print("Lectura de sensores completa.")




