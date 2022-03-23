# Microscope/Micro-Manager triggered song playback.

Waits for songs, and acquires data, with image + sound buffers.
Can be triggered to turn light on/off

Effectively a micromanager/national instruments interface.

Framestamps can be send to NI, as can raw audio, to allow matching between audio and video frames.

Video saved in multi-tiff;

Required micromanager set up to allow remote commands (Tools, Options-> RUN SERVER ON PORT 4827). 

requires:
 
PyQT5
pyqtgraph
pyaudio
nidaqmx
numpy
pycromanager

Set up your camera in micromanager, and set remote commands on. 
For the national instruments card, AI1 is the audio, AI2 is the frames from the camera (https://www.flirkorea.com/support-center/iis/machine-vision/application-note/configuring-synchronized-capture-with-multiple-cameras/)
Input lines to to AI2., for a 6-pin Hirose connectors. 

Digital Output (/dev1/linep/port1) goes to a trigger, if you want to trigger the light on/off for extended recordings that don't need pre-song data. 


 



