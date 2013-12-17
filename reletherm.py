#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from daemon import runner
import yaml

import os
import glob

#GPIO.cleanup()

class App():
    def _read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    def read_temp(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
#            print "CRC ERROR!!!"
            sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
#           temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/reletherm.pid'
        self.pidfile_timeout = 5
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'
        self.config = {'temp_set': 21, 'temp_delta': 0.5, 'valve_work': 20, 'valve_delta': 3}
	
    def read_conf_file(self):
        f=open('/home/pi/reletherm.cfg', 'r')
        self.config = yaml.safe_load(f)
        f.close()
		
    def run(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        LEFT=23
        RIGHT=24

        self.read_conf_file()

        SETTEMP=self.config['temp_set']
        DELTA=self.config['temp_delta']
        
        GPIO.setup(LEFT,GPIO.OUT,initial=True)
        GPIO.setup(RIGHT,GPIO.OUT,initial=True)

        while True:
            curr_temp=self.read_temp()
            if curr_temp < (SETTEMP-DELTA):
                print "Lower than SETTEMP=%r %r" % (SETTEMP, curr_temp)
                GPIO.output(LEFT,False)
                GPIO.output(RIGHT,True)
            if curr_temp > (SETTEMP+DELTA):
                print "Higher than SETTEMP=%r %r" % (SETTEMP, curr_temp)
                GPIO.output(RIGHT,False)
                GPIO.output(LEFT,True)
            if (curr_temp >= (SETTEMP-DELTA)) and (curr_temp <= (SETTEMP+DELTA)) :
                print "SETTEMP=%r is HERE %r" % (SETTEMP, curr_temp)
                GPIO.output(RIGHT,True)
                GPIO.output(LEFT,True)

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
