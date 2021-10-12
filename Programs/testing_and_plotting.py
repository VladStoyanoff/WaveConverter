from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1015 as ADS
import matplotlib.pyplot as plt
from pygame import mixer
import numpy as np
import pygame
import busio
import board
import time

i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1015(i2c, address=0x48)
chan = AnalogIn(adc, ADS.P1)

num_of_measurements = 100

while True:
    try:
        measurements = int(input('Please enter the number of measurements you wish to take:'))
        break
    except:
        print('Please enter an integer')
        
        
x = []
y = []

for i in range(measurements):
    freq = int(input('Please enter the frequency of the wave that is currently running through the circuit:'))
    simplelist = []
    for i in range(num_of_measurements):
        simplelist.append(chan.voltage)
        time.sleep(2/num_of_measurements)
    max_voltage_of_freq = max(simplelist)
    x.append(freq)
    y.append(max_voltage_of_freq*1000)
         
plt.xlim([0, 100])
plt.xticks([0,3,6,9,15,25,40,50,60,70,80,90,100])
plt.ylim([0, 325])
plt.yticks(np.arange(0, 325, 25))
plt.xlabel('x - Frequency')
plt.ylabel('y - Voltage in mV')
plt.title('Voltage as a function of frequency')
plt.scatter(x, y)
plt.show()
    

