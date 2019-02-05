import os
import time
class TemperatureSensor:
    def __init__(self, numero):
        self.numero = numero
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

    def read_temp_raw(self):
        device_file = '/sys/bus/w1/devices/'+ str(self.numero)+ '/w1_slave'
        f = open(device_file, 'r')  # Ouvre le dichier
        lines = f.readlines()  # Returns the text
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()

        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
