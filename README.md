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
* [Quad Operational Amplifier TL084](https://www.ti.com/lit/ds/symlink/tl081a.pdf?HQS=dis-dk-null-digikeymode-dsf-pf-null-wwe&ts=1619312373475&ref_url=https%253A%252F%252Fwww.digikey.ca%252F)
* [Instrumental Amplifier AD622ANZ](https://www.analog.com/media/en/technical-documentation/data-sheets/AD622.pdf)
* Capacitors and Resistors
* Bread board and wires
* Two 9V batteries
* Raspberry Pi 3B+
* [Open Scope MZ](https://s3-us-west-2.amazonaws.com/digilent/resources/instrumentation/openscope-mz/digilent-openscope_workbook-final.pdf)
* [ADS 1015](https://www.ti.com/lit/ds/symlink/ads1015.pdf)

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

(photo of the filter in the schematic + photo of the plot from Ryan)

The EEG waves that are of interest to us are between the 12-30 Hz frequency range. So we filter out anything over that. A second order filter design is used and the formula used to control the filter is the following - fc = 1/2πRC, where R is the resistor value to the power of 3 and C is the capacitor value (220 nF in the formula would be written as 220 x 10 to the power of -6).

[More information on second order filters](https://www.electronics-tutorials.ws/filter/second-order-filters.html)



This filter is specific and unlike the others. It filters out a specific frequency There's a very sharp noise signal at around 50 Hz for Raspberry Pi 3B+ and 60 Hz for Raspberry Pi 4. It is normal and is called power line intereference.



