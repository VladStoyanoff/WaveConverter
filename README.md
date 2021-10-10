# Project Description
This project builds a converter that turns alpha and beta waves into words and sentences to the user's liking. It's intended to be coupled with good EEG hardware, so that one could communicate to a computer only by changing between concentrated and relaxed state. This repository will go over everything that I did in the process of building the converter.

Video showcasing the converter in action:

This project took place over a timespan of 3 weeks, but given this step-by-step guide, I believe a novice in electronics and coding, could finish it in <= 3 days.

# Big Picture

## Brain Waves

Brain waves have frequency and amplitude. The frequency is how fast a wave repeats itself for 1 second (50 Hz would be 50 iterations per second), and amplitude is the highest voltage the wave reaches in either direction. So a wave with an amplitude of 1V, would mean that it also has an amplitude of -1V. This is not to be mistaken with Vpp (peak-to-peak Voltage) - this is the ampitlude in both directions. In the aforementioned example, this would mean that the Vpp is 2V. This is necessary to bear in mind, because our wave generator (Open Scope MZ), generates waves based on the Vpp, rather than amplitude.

## Generated Waves

To test our circuit and prove that it works, we need a wave generator and an oscillator. The oscillator measures voltage as a function of time. In other words, this is a multimeter that measures voltage in a continuous timeframe and plots the result. In this guide, we are using Open Scope MZ as a wave generator and an oscillator.

## Amplify and Filter

Alpha and beta brain waves that are emitted from the brain have a frequency of 12-30 HZ and a relatively low ampltiude - 15µV to 50µV. To process those waves, we have to amplify the signal. In digital signal processing terms, when we amplify a signal we apply a gain to it's amplitude. For example, a wave with an amplitude of 200 mV that has a gain of 90 would result in a wave with an amplitude of 18V and a Vpp of 36V. With amplifying the signal, we also amplify noise. Noise is anything else that's outside the frequency that we want. So we also need filters. Filters hinder a specific frequency to be amplified. In this guide we are using AD622ANZ as our amplifier and TL084 as our integrated circuit that filters the signal at specific frequencies.

## Convert

After we have amplified and filtered our signal, we must feed it to an ADC (Analog-to-Digital Converter). This  turns the signal from analog to digital, so that our computer can process the signal and apply the code that converts it to the specified letters and output it. In this guide we have used ADS 1015 as our ADC and Raspberry Pi 3B+ as our computer.

# Bill of materials
* Multimeter (not mandatory, but troubleshooting without a multimeter would be way harder)
* Raspberry Pi 3B+ and an SD card with atleast 8GB memory
* [Quad Operational Amplifier TL084](https://www.ti.com/lit/ds/symlink/tl081a.pdf?HQS=dis-dk-null-digikeymode-dsf-pf-null-wwe&ts=1619312373475&ref_url=https%253A%252F%252Fwww.digikey.ca%252F)
* [Instrumental Amplifier AD622ANZ](https://www.analog.com/media/en/technical-documentation/data-sheets/AD622.pdf)
* [ADS 1015](https://www.ti.com/lit/ds/symlink/ads1015.pdf) and a soldering iron to solder the legs to the ADC
* Capacitors and Resistors
* Bread board and wires
* Two 9V batteries
* [Open Scope MZ](https://s3-us-west-2.amazonaws.com/digilent/resources/instrumentation/openscope-mz/digilent-openscope_workbook-final.pdf)

To most of the components in the BOM (Bill of materials), I have also attached the readings that I have referred to when I was troubleshooting. Read them and explore them as often as you need.

# Wiring

(diagram with the wiring)

# Circuit Schematic

(circuit schematic)

The circuit consists of the following sections:

* Low Pass Filter (Fc = 32.9 Hz, gain = 1)
* Instrumental Amplifier (gain ~91)
* High Pass Filter (Fc = 7.2 Hz, gain = 1)
* Notch Filter (50 Hz)

Each section is discussed in details below.

## Low Pass Filter (Fc = 32.9 Hz)

(photo of the filter in the schematic + photo of the plot from Ryan)

The EEG waves that are of interest to us are between the 12-30 Hz frequency range. So we filter out anything over that. A second order filter design is used and the formula used to control the filter is the following: fc = 1/2πRC ((only if the both the resistors and both the capacitors have the same values), where R is the resistor value to the power of 3 and C is the capacitor value (220 nF in the formula would be written as 220 x 10 to the power of -6).

[More information on second order filters](https://www.electronics-tutorials.ws/filter/second-order-filters.html)

## Instrumental Amplifier (gain ~91)

(photo of the filter in the schematic)

Alpha wave signals are 15-50 uV so we need a lot of amplification in the circuit to reach the range in which the ADC reads. An instrumentation amplifier takes as its inputs 2 voltages, and outputs the difference between the two multiplied by some gain given by: G = 1 + (50.5 kOhm)/R, where R is the total resistance between pin 1 and 8. With this converter we use only 1 amplifier with a set gain of ~91, because Open Scope MZ cannot generate waves with an amplitude as low as the ones from the brain. To make it as realistic as possible, we generate a wave with an amplitude of 2.7 mV - this is the amplitude that you would have if you amplified a wave with an amplitude of 30uV with another amplifier with a set gain of ~91. So realistically, if you have good measuring equipment, all you need to add is another amplifier that's the same as this one to the circuit.

## High Pass Filter (Fc = 7.2 Hz, gain = 1)

(photo of the filter in the schematic + photo of the plot from Ryan)

Conversely to the low pass filter, the high pass one, filters everything under the frequency range we care about. The formula for controlling the filter is: fc = 1/2πRC (only if the both the resistors and both the capacitors have the same values).

## Notch Filter (50 Hz)

(photo of the filter in the schematic + photo of the plot from Ryan)

This filter is specific and unlike the others. It filters out a specific frequency while leaving the frequncies prior to the target and after the target the same.
We use a notch filter because, there's a very sharp noise signal at around 50 Hz for Raspberry Pi 3B+ and 60 Hz for Raspberry Pi 4. It is normal and is called power line intereference. While using a notch filter will not completely remove it, it helps a lot. When adding an additional amplifier to the circuit, I strongly recommend having another notch filter just like this one, because the interference will get amplified.

# ADC and Raspberry Pi

Now comes the time when you have to setup the connection between the Raspberry Pi and the ADC. As a quick reminder, the ADC turns the amplified and filtered analog signal into a digital one, so that the RPI can understand it.

## Raspberry Pi 3B+

There are several ways one can set up a Raspberry Pi, but what I will describe here will suffice for Windows 10. What you will need is a monitor and a mouse.
The very first thing you will want to do is install an operating system for the Raspberry Pi. 

You will do that by installing Raspberry Pi Imager for your main computer from here - https://www.raspberrypi.com/software/. Follow the instructions from the website, it should be pretty straightforward, but if there's any problem whatsover you can contact raspberry support or email me (in case you're using Windows 10).

Then upload the OS to the SD card



Supply the ADC chip with 5V from Rpi to ensure the maximum input voltage range possible. The pin configuration and connection in the image above is correct, but it is recommended to double check the connection, because wiring mistakes can lead to damaging the chip and/or the Rpi.



