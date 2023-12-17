import os
import glob
import time
from display_code import *
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# pasteurization happens above 50° C, pasteurization units are 
# calculated as following: PU = time[min] * 1.393 exp((temp-60))
# see https://www.homebrewtalk.com/threads/pasteurization-time-and-temperature-for-cider.581913/ for sources
def calculate_pasteurization(current_temp):
    pu_per_second = (1.393  ** ((current_temp - 60)))/60
    return pu_per_second

current_pus = 0
while True:
    current_temperature = read_temp()
    if current_temperature >= 50.0:
        current_pus += calculate_pasteurization(current_temperature)
    current_temp_str = "Temperature: " + str(current_temperature)
    current_pu_str = "PUs: " + str(round(current_pus,1))
    print(current_temp_str)
    print(current_pu_str)
    send_to_display(current_temp_str, current_pu_str)
    time.sleep(1)
 



