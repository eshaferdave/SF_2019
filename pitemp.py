#! /usr/bin/env python
import argparse
import os
import glob
import time
import calendar
import random
import sys

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

starttime = None
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
#device_file = device_folder + '/w1_slave'

print(glob.glob(base_dir + '28*'))

def read_temp_raw(sensor):
    device_file = device_folder[sensor] + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensor):
    lines = read_temp_raw(sensor)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

# def read_temp():
#     return random.random() + random.randint(1,1000)

def get_seconds():
    return calendar.timegm(time.gmtime())

def time_offset():
    global starttime
    if not starttime:
        starttime = get_seconds()
    return get_seconds() - starttime

def ParseCmdLine():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--sensor", help="Number value of the sensor to use (0-3)", default=0)
    args = parser.parse_args()
    if args.address not in range(3):
        print("Invalid sensor")
        return None
    return args


def main():

    args = ParseCmdLine()

    for i in range(360):
        print("{:>3}, {:.3f}".format(time_offset(), read_temp(args.sensor)))
        sys.stdout.flush()
        time.sleep(5)


if __name__=='__main__':
    sys.exit(main())
