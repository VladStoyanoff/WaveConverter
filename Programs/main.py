from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1015 as ADS
from pygame import mixer
import numpy as np
import pygame
import busio
import board
import time

mixer.init()
alert=mixer.Sound('/home/pi/Downloads/beep.wav')

i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1015(i2c, address=0x48)
chan = AnalogIn(adc, ADS.P0)

buffer = 1
binarytime = 1
number_of_readings = binarytime*10

alphabet = {
    'a': [0,0,0,0,0],
    'b': [1,0,0,0,0],
    'c': [1,1,1,1,1],
    'd': [0,0,1,0,0],
    'e': [0,0,0,1,0],
    'f': [0,1,1,1,1],
    'g': [1,1,1,1,0],
    'h': [1,0,0,0,1],
    'i': [1,1,1,0,0],
    'j': [0,0,1,0,1],
    'k': [0,0,1,1,0],
    'l': [0,1,0,0,0],
    'm': [0,1,0,0,1],
    'n': [0,1,1,1,0],
    'o': [0,0,1,1,1],
    'p': [0,1,0,1,1],
    'q': [0,1,0,1,0],
    'r': [0,1,1,0,0],
    's': [0,1,1,0,1],
    't': [1,0,0,1,0],
    'u': [0,0,0,1,1],
    'v': [1,0,0,1,1],
    'w': [1,0,1,1,1],
    'x': [1,0,1,0,1],
    'y': [0,0,0,0,1],
    'z': [1,0,1,0,1],
    ' ': [1,1,0,0,0]
}

def get_letter_from_binary(binary):
    
    string = ''
    for i in range(int(len(binary)/5)):
        binary_char = binary[5*i:5*(i+1)]
        character = list(alphabet.keys())[list(alphabet.values()).index(binary_char)] 
        string += character
    return string

def get_cutoff(num_samples, adc):
    
    relaxed = []
    concentrated = []
    relaxed_and_concentrated_means = []
    for i in range(num_samples):
        input("Press <Enter> to record relaxed state. This will take 2+1 seconds.")
        time.sleep(buffer)
        for i in range(20):
            relaxed.append(chan.voltage)
            time.sleep(binarytime/number_of_readings)
        input("Press <Enter> to record concentrated state. This will take 2+1 seconds.")
        time.sleep(buffer)
        for i in range(20):
            concentrated.append(chan.voltage)
            time.sleep(binarytime/number_of_readings)
    mean_voltage_relaxed = np.mean(relaxed)
    mean_voltage_concentrated = np.mean(concentrated)
    relaxed_and_concentrated_means.append(mean_voltage_relaxed)
    relaxed_and_concentrated_means.append(mean_voltage_concentrated)
    cutoff = np.mean(relaxed_and_concentrated_means)
    return cutoff
        
while True:
    response = input('Enter good cutoff voltage (number) or type c to calibrate (c):' )
    if response == 'c':
        cutoff = get_cutoff(3, adc)
        print('You have cutoff voltage',cutoff)
        break
    try:
        cutoff = float(response)
        break
    except:
        print('Please enter correct format input')

print('You will have %.1f second/s before recording starts, you should move onto the next character every %.2f seconds and will be notified of this with a beep.'%(buffer,binarytime))
input('Press <Enter> to start')
print()

time.sleep(buffer)

rms_values = []
binary_data = []
list_for_means = []

while True:
    for i in range(number_of_readings):
        list_for_means.append(chan.voltage)
        time.sleep(binarytime/number_of_readings)
    rms_values.append(np.mean(list_for_means))
    list_for_means = []
    x = len(rms_values) / 5
    if (x - int(x) == 0):
        for i in range(0, 5):
            if rms_values[i] < float(cutoff):
                binary_data.append(0)
            else:
                binary_data.append(1)
            i = i+1
        rms_values = []
        letter = get_letter_from_binary(binary_data)
        print(letter)

