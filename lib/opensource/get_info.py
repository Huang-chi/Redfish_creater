#!/usr/bin/env python
# ---------------------------
# Linux Temperature Utility
# coordinate with lm_sensors
# by Bunko
# ---------------------------
 
from subprocess import Popen, PIPE, STDOUT
 
def get_sensors():
    """Get Core Temperature, FAN Speed and MB Temperature"""
    result_sensor = Popen("sensors", stdout=PIPE, stderr=STDOUT).communicate()[0]
    results = result_sensor.split('\n')
    cores = {}
    fans = {}
    boards = {}
    for line in results:
        data = line.split()
        print(data)
        if len(data) :
            # Core Temp
            if data[0].startswith('Core'):
                corevar = data[0] + data[1][:-1]
                coretemp = data[2][:-3]
                coretemp = coretemp[1:]
                cores[corevar] = coretemp
            # -----------------
            if data[0].startswith('CPU'):
                if data[1] == 'FAN':
                    # CPU FAN Speed
                    fans[data[0]] = data[3]
                if data[1] == 'Temperature:':
                    # CPU Temperature
                    ctemp = data[2][:-3]
                    ctemp = ctemp[1:]
                    boards[data[0]] = ctemp
            # ----------------
            if data[0].startswith('CHASSIS'):
                # CHASSIS FAN Speed
                speed = data[2][6:]
                fans[data[0]] = speed
            #
            if data[0].startswith('MB'):
                # MB Temperature
                mtemp = data[2][:-3]
                mtemp = mtemp[1:]
                boards[data[0]] = mtemp
            #
    # -------------------------
    return cores, boards, fans
# ------------------------------------------
 
if __name__ == '__main__':
    cores,boards,fans = get_sensors()
    print 'Cores:', cores
    print 'Boards:', boards
    print 'FAN Speeds:', fans
