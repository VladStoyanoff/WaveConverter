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
* 2 power cables: 5V at 2.5A. One for the Raspberry and one for the Open Scope MZ
* [ADS 1015](https://www.ti.com/lit/ds/symlink/ads1015.pdf) and a soldering iron to solder the legs to the ADC
* Raspberry Pi 3B+ and an SD card with atleast 8GB memory
* [Quad Operational Amplifier TL084](https://www.ti.com/lit/ds/symlink/tl081a.pdf?HQS=dis-dk-null-digikeymode-dsf-pf-null-wwe&ts=1619312373475&ref_url=https%253A%252F%252Fwww.digikey.ca%252F)
* [Instrumental Amplifier AD622ANZ](https://www.analog.com/media/en/technical-documentation/data-sheets/AD622.pdf)
* Capacitors and Resistors
* Bread board and wires
* Two 9V batteries
* [Open Scope MZ](https://s3-us-west-2.amazonaws.com/digilent/resources/instrumentation/openscope-mz/digilent-openscope_workbook-final.pdf)

Note: I know that Digilent (the company that created Open Scope MZ) do not recommend that you buy it, because of negative feedback from users, but I haven't noticed any problems whatsover with the wave generation, oscilloscope and voltage supply functionalities, so I'll abstain from giving opinion here and stick to the facts: It works for me.

To most of the components in the BOM (Bill of materials), I have also attached the readings that I have referred to when I was troubleshooting. Read them and explore them as often as you need.

# Wiring

(diagram with the wiring)

# Circuit Schematic

![schematic](schematic.png)

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

# ADC, Raspberry Pi and Open Scope MZ

Now comes the time when you have to setup the connection between the Raspberry Pi and the ADC and understnad how to work with Open Scope MZ. As a quick reminder, the ADC turns the amplified and filtered analog signal into a digital one, so that the RPI can understand it. Open Scope MZ can do many things, but what we'll focus on is wave generation and the oscilloscopes.

## Raspberry Pi 3B+

Before we start I'd like to mention several things regarding handling PCB's such as Raspberry Pi and Open Scope MZ:

* Don't hold the RPI (same goes for ADC and Open Scope MZ) in a way that you apply pressure to the components. Hold it always from the side so that you don't touch any sensitive parts.
* Don't turn off the RPI directly from the power supply cable. Always turn it off by the terminal or the GUI.
* Don't leave the RPI on wet, sticky, or dirty surfaces.
* Avoid touching the Raspberry too much when it's powered on.

There are several ways one can set up a Raspberry Pi, but what I will describe here will suffice for Windows 10. What you will need is a monitor and a mouse. A keyboard is also helpful, but not needed. The very first thing you will want to do is install an operating system for the Raspberry Pi. 

You will do that by installing Raspberry Pi Imager for your main computer from here - https://www.raspberrypi.com/software/. Follow the instructions from the website, it should be pretty straightforward, but if there's any problem whatsover you can contact raspberry support or email me (in case you're using Windows 10).

Then upload the OS to the SD card and supply it to the Raspberry Pi. Connect the monitor and mouse and start navigating yourself in the GUI. Explore it a bit if you haven't operated before with Raspberry Pi. Also, find the IP of your RPI by typing "hostname -I" on the terminal of your Raspberry Pi. You will need it later for controlling the Raspberry from your laptop. If you don't have a keyboard then this get's a little more complicated, but still doable. What you will want to do is activate the mobile hotspot on your phone, set a password to it, navigate yourself to a file named wpa_supplicant.conf that's on the SD card and add this text on the very end of the file: 

network={
   ssid="Test Wifi Network"
   psk="SecretPassWord"
}

Then get the SD card out of your laptop and plug it back in the Raspberry. Upon booting, your Raspberry should automatically connect to your mobile hotspot.

Now that your computer and Raspberry are connected to the same network, you can access the Raspberry terminal from your laptop by typing: ssh@pi (the IP address of the Raspberry - should be the same as the one for your computer).

The username is the default - raspberry.
The password is the default - pi

You can change those later if you wish.

I hope this goes without saying, but if there's any problems with what I've mentioned so far, don't be afraid to email me. You can find my email at my Github profile.

Now you have full access to the Raspberry, but you still don't see the GUI. To see the GUI from your laptop screen you have to install VNC Viewer from here: https://www.realvnc.com/en/connect/download/viewer/

Upon installation, type the IP address of your Raspberry and you will connect. Note that your laptop and the Raspberry should be connected to the same network.

I'd also recommend downloading a virtual keyboard as a package on your Raspberry so that you could always use it to its fullest potential with only a monitor, mouse and a phone.

## ADC
If you bought a brand new ADS1015 from Adafruit, then it will come with legs that are not soldered. If you're experienced with soldering, you know the drill.
If you're not though, I DO NOT recommend that you do this yourself. Either experiment and learn how to make precise solder connections (which wouldnt take more than 1-2 days in my opinion) or let someone else do it.

When connecting the ADC to the RPI you will notice several things. The power supply to the ADC is 5 volts. This is because Our final signal will vary between 2.3 and 4.3 Volts, and we should not feed voltages to our ADC that are higher that the supply voltage or permanent damage to the ADC could occur. Next, when executing our python code, we must have several libraries installed one of which is specific for the ADS that we are using - ADS1015. Let's install them now.

Navigate yourself to the terminal of the Raspberry Pi (You should be able to ssh it through the command prompt of your main computer, connecting to the RPI with VNC Viewer and navigating yourself with the GUI directly on the screen on the laptop or using just the Raspberry Pi with a monitor, mouse and a keyboard. If you can't do all of these, then you have not done something right in the Raspberry Pi section).

Type the following code:

sudo pip3 install adafruit-circuitpython-ads1x15
sudo pip3 install numpy
sudo pip3 install time


## Open Scope MZ

If you've bought a brand new Open Scope MZ, then you will receive the PCB and many female to female cables. I do not recommend using them, because you will need 6 at most.So just take 6 female to female cables from your nearest electronics shop and go with those, to avoid confusion.

What you will want to do is connect the wave generator with a power cable to your computer and open http://waveformslive.com

Add a device > Agent > ...

If it doesnt work on your search engine, try on another. It didnt work on Google Chrome but worked on Opera for me.

Explain Open Scope

# Circuit Debugging

*There's no dark magics involved in electronics and programming. The circuit and code do exactly what you told them to do.*

Having this said here's some practical tips for troubleshooting:

* Test with measuring tools (multimeter, oscilloscope) while building the circuit so that you can minimize troubleshooting as much as possible when it's all built.
* Open Scope MZ is clunky, but in my experience, it's not buggy. Try to understand it's logic as much as possible so that you are not confused by the results.
* I've tried my best in explaining why I do what I have described here, but if there's anything, absolutely anything that is not clear to you, I strongly advise you to consult yourself with other people or search engines and find out the missing piece, because it's very likely that it will backfire later on, with much higher impact.
* Before using measuring tools, test whether the tools themselves function properly with a simple test.

# Biggest challenges I faced and ways I overcame them
1. I had a lot of trouble finding the components listed here. I was lingering on this for 2-3 days until I found them all from 4 different distributors. What I would recommend to someone with the same problem is list at least 10 different distributors that match your needs (price, shipping time), search through all of them before you search for alternatives. I started searching for alternatives and lost about 2 days when I stumbled upon a website that had the exact component that I needed. Let searching for alternatives really be your last option.

2. In the start of the project I struggled to understand nearly everything, because I am still a novice in programming, electronics and digital signal processing. What I thought would be a solution to my lack of knowledge would be to just copy everything on the Github of the physics undergrads that helped me in this project (mentioned in the acknowledgements). Big mistake. I found myself solving about 20 different problems per day even though I copied everything. You can't get around the process of continuous improvement. Accept that your main task IS solving problems, rather than trying to avoid them. Learn what you don't understand, and most of all remember that the improvement in your skills is a function of how complex a problems seems to you after you solve it. Or you can just do what I did and copy everything. When you face a problem that you have to debug though, the emotional disbalance in you will be way higher, and eventually you will solve the problem because you are now forced to do your homework and understand what you did.

3. Setting up the Raspberry. Boy, was this a struggle. From getting electrocuted to writing oomplete shenanigans in the text files provided by installing the OS, I nearly experinced it all. Somehow I successfully connected the Raspberry Pi to my laptop's screen, keyboard and mouse which was the goal. Primarily with the help of Google (Fun fact: I have 338 search results starting with "How" in Google from the interval of the start of the project until the end)

4. Circuit problems - connecting everything at once is not a good practice. What seemed a good way to approach this circuit was to initiliaze a wave and connect one component at a time, and moving the oscillator at the end of that component to see whether the wave is moving through the circuit properly.

5. Coding problems - the codes provided by the physics undergrads was really confusing to me. I think the main lesson I learned here was don't be afraid in respecting your own ideas. From the start of the project I thought that their code must be the way to do this and I shouldnt change it, mainly because I'm not that experienced yet, even though I was always unsure whether the complexity was needed to achieve the goal. One day I just got so mad at myself that I still can't understand it and I erased it and started from scratch. I didnt know how to code, but my thinking process was the following: **Think about what you want the code to do and google until you found out how to write it in Python**. It turned out that this thinking process is very good! Im happy that with this thinking process I can turn my vision in code and achieve goals in my own unique way.

6. There were many times when I thought that Open Scope MZ was not functioning properly, because my hypotheses were almost always contradicted until I found out that my grounding was terrible. I've tried my best in explaining what I learned regarding grounding in this repository under the *** section.

# Acknowledgement

Many good people helped me in this project:

* **Ryan Lopez and Hak Zhang** - physics undergrads at UCSB. They were my main inspiration for this project - you can check their version of the project here: https://github.com/ryanlopezzzz/EEG/blob/main/README.md. Many thanks to them for the continuous email support throughout the project, and I strongly hope that our paths cross again in future initiatives! :)
* **Anton Atanasov** - cybersecurity student at Naval Academy "N. Vaptsarov" in Varna - met him at Space Challenges Bootcamp 2021, one of the brightest people I've ever met. He helped me with writing my own version of the python codes.
* **Victor Danchev** - CTO at Endurosat, PhD candidate in Astrophysics at Sofia University - he was the main lecturer at Space Challenges Bootcamp 2021 and is also a very bright individual. He helped me with understanding the differences between components when I was considering buying alternatives.
* **Simeon Baltadzhiev** - Robotics student at Ruse University - met him at Space Challenges Bootcamp 2021, Mony is an expert in my eyes when it comes to electronics. He helped me with soldering the ADC.
* **Dimitriy Georgiev** - Electrical Engineering graduate and intern at EnduroSat - met him at Space Challenges Bootcamp 2021, Dimitryi is also very experienced with electronics. He helped me with understanding how the components worked and some main circuit principles.
* **Dimitar Yordanov** - High schooler - met him at Space Challenges Bootcamp 2021, Dimitar is experieneced with Python and Raspberry Pi. He helped me set up my Raspberry.
* **My family** - They have been amazing in supporting me throughout this project. They also provided me with the capital needed for the hardware.











