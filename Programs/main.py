from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1015 as ADS
import numpy as np
import pygame
import busio
import board
import time

i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1015(i2c, address=0x48)
chan = AnalogIn(adc, ADS.P1)

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

def get_letter_from_binary(binary):                                                         #a function to turn the binaries into words. Credits to Ryan Lopez from UCSB for creating this
    
    string = ''
    for i in range(int(len(binary)/5)):
        binary_char = binary[5*i:5*(i+1)]
        character = list(alphabet.keys())[list(alphabet.values()).index(binary_char)] 
        string += character
    return string

def get_cutoff(num_samples, adc):                                                            #calibrates according to your own specific brain waves, so that it gives out a good cutoff voltage
    
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

time.sleep(buffer)                                     #call the program to wait

rms_values = []                                        #empty list
binary_data = []                                       #empty list
list_for_means = []                                    #empty list

while True:                                            #loops forever until the program is stopped
    for i in range(number_of_readings):                #a for loop that loops for the value of number_of_readings
        list_for_means.append(chan.voltage)            #adding a voltage reading to the list list_for_means
        time.sleep(binarytime/number_of_readings)      #calls the program to wait. We wait the value of binarytime seconds in all cases
    rms_values.append(np.mean(list_for_means))         #we add the mean of the list_for_means (which now contains several dozens of readings) to a new list called rms_values
    list_for_means = []                                #we clear the list list_for_means so that on the new run it is ready to take measurements for the new binary
    x = len(rms_values) / 5                            #we divide the lenght of rms_values by 5 and assign that value to x
    if (x - int(x) == 0):                              #we check x. if x - int(x) is 0, then we continue. This would happen only if x is equal to one (if we divide 5 by 5 we get a whole number 1). This essentially allows the code to decide whether to decipher the accumulated binaries or to continue measuring
        for i in range(0, 5):                          #a for loop that loops for 5 times (check every values in rms_values and assigns it the appropriate binary
            if rms_values[i] < float(cutoff):          #this allows to loop through every measurement and check it according to the cutoff voltage
                binary_data.append(0)                  #add the binary to binary_data
            else:                                      
                binary_data.append(1)                  #add the binary to binary_data
            i = i+1                                    #this allows the loop to loop through every value in rms_values in order
        rms_values = []                                #we clear the list so that it is ready to take new mean values
        letter = get_letter_from_binary(binary_data)   #we decipher the accumulated 5 binaries into a letter, according to the alphabet above
        print(letter)                                  #print the letter and start the loop from line 105 again

