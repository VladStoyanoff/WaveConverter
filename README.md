# WaveConverter
This project builds an EEG device that measures brain waves to determine if the user is concentrating or relaxed. An EEG uses electrodes placed on the user's scalp to measure the voltage difference between brain regions. These voltage differences oscillate and represent synchronized activity over a network of neurons. Depending on the electrode placements, brain waves have different characteristic frequency, magnitude, and are related to different brain activities. In our project, we measure alpha waves originating from the occipital lobe because they are one of the strongest EEG signals. Alpha waves have a signature frequency in the range of 8-12 HZ. It reflects activities of the visual cortex: their magnitude is increased with closed eyes and relaxation, and decreased with open eyes and concentration.

In our project, we use a circuit to amplify the electrode signals from the brain, and uses a number of high pass, low pass, and notch filters to filter out frequencies outside of 8-12 HZ. Then, we take data with a raspberry pi 4 and post-process the data using digital filters and analyze it with statistical methods. In the end, we successfully captured alpha waves and observed that its magnitude varies significantly between a concentrated and relaxed state. Furthermore, we came up with three applications that utilize our EEG device:

1st application: use EEG to play "EEG bird" (modeled after flappy bird).

https://youtu.be/KFIHE_fInmM
2nd application: use EEG to monitor child attention level. We had fun making this video!!

https://youtu.be/HQ8krHOXocc
3rd application: brain-to-text communication, in hope to help paralyzed people communicate.

https://youtu.be/74iM_w6vFuU
We based our project on the guidance of an amazing article instructables.com/DIY-EEG-and-ECG-Circuit/. However, we created our own circuit design, wrote our own code for data-taking and analysis, and included unique and fun applications. We hope this Github Repository can help people implement and debug their own EEG circuit. Make sure to check out the circuit debugging tips section if you are working on a similar project and your circuit doesn't work!
