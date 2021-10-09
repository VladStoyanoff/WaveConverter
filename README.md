# Project Description
This project builds a converter that turns alpha and beta waves into words and sentences to the user's liking. It's intended to be coupled with good EEG hardware, so that one could communicate to a computer only by changing between concentrated and relaxed state. This repository will go over everything that I did in the process of building the converter.

Video showcasing the converter in action:

This project took place over a timespan of 3 weeks, but given this step-by-step guide, I believe a novice in electronics and coding, could finish it in <= 3 days.

# Big Picture

* Brain Waves

Brain waves have frequency and amplitude. The frequency is how fast a wave repeats itself for 1 second (50 Hz would be 50 iterations per second), and amplitude is the highest voltage the wave reaches in either direction. So a wave with an amplitude of 1V, would mean that it also has an amplitude of -1V. This is not to be mistaken with Vpp (peak-to-peak Voltage) - this is both the amplitudes combined. In the aforementioned example, this would mean that the Vpp is 2V. This is necessary to bear in mind, because our wave generator (Open Scope MZ), generates waves based on the Vpp, rather than amplitude.

* Amplify and filter

Alpha and beta brain waves that are emitted from the brain have a frequency of 12-30 HZ and a relatively low ampltiude - 15µV to 50µV. To process those waves, we have to amplify the signal. With amplifying the signal, we also amplify noise. Noise is anything else that's outside the frequency that we want. So we also need filters.

* Convert

After we have amplified and filtered our signal, we must feed it to an ADC (Analog-to-Digital Converter). This  turns the signal from analog to digital, so that our computer (Raspberry Pi) can process the signal and apply the code that converts it to the specified letters.

# Bill of materials
* Raspberry Pi 3B+
* ADS 1015
* Instrumental Amplifier AD622ANZ
* Quad Operational Amplifier TL084
* Capacitors and Resistors
* Two 9V batteries
* Bread board and wires
* Multimeter (not mandatory, but troubleshooting without a multimeter would be way harder)
* Open Scope MZ
