
from PyQt5 import QtGui, QtCore, QtWidgets
import wave
import audioop
from collections import deque
import os
import time
import math
import copy
from math import ceil
import pdb;
import pyaudio
import pycromanager
import pyqtgraph as pg
import numpy as np
import nidaqmx
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
from collections import deque
from nidaqmx.constants import AcquisitionType 
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.constants import TerminalConfiguration
from nidaqmx.constants import LineGrouping




global frameTrig
#global graph_win

import GlobalVars
global timer


CHUNK = 2048 # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16 #this is the standard wav data format (16bit little endian)s
MAX_DUR=60 #max dur in seconds
above_threshold=False;



def low_pass_filter_by_chunk(seg, cutoff, last_val):

    import array
    import math
    
    """
    # Forked from PyDub in order to keep the last values to avoid filter artefacats on chunked data
        cutoff - Frequency (in Hz) where higher frequency signal will begin to
            be reduced by 6dB per octave (doubling in frequency) above this point
    """
    RC = 1.0 / (cutoff * 2 * math.pi)
    dt = 1.0 / seg.frame_rate

    alpha = dt / (RC + dt)
    
    original = seg.get_array_of_samples()
    filteredArray = array.array(seg.array_type, original)
    
    frame_count = int(seg.frame_count())    
        
    for j in range(seg.channels):        # 1-# Chanes
        last_val[j] = last_val[j] + (alpha * (original[0] - last_val[j]))
        filteredArray[j] = int(last_val[j])
        
    #pdb.set_trace();
    for i in range(1, frame_count):
        for j in range(seg.channels):
            offset = (i * seg.channels) + j
            last_val[j] = last_val[j] + (alpha * (original[offset] - last_val[j]))
            filteredArray[offset] = int(last_val[j])

    
    return seg._spawn(data=filteredArray),last_val

def high_pass_filter_by_chunk(seg, cutoff, last_val,last_data):
    # Forked from PyDub in order to keep the last values to avoid filter artefacats on chunked data
    """
        cutoff - Frequency (in Hz) where lower frequency signal will begin to
            be reduced by 6dB per octave (doubling in frequency) below this point
    """
    import array
    import math
   # from PyDub import AudioSegment
    from pydub import AudioSegment
    from pydub.utils import get_min_max_value
    import pdb

    RC = 1.0 / (cutoff * 2 * math.pi)
    dt = 1.0 / seg.frame_rate

    alpha = RC / (RC + dt)

    minval, maxval = get_min_max_value(seg.sample_width * 8)
    
    original = seg.get_array_of_samples()
    filteredArray = array.array(seg.array_type, original)
    
    frame_count = int(seg.frame_count())
    #pdb.set_trace();
    
    for j in range(seg.channels):
        #filteredArray[i] = original[i]
        last_val[j] = alpha * (last_val[j] + original[0] - last_data[j])
        filteredArray[j] = int(min(max(last_val[j], minval), maxval))
    
    for i in range(1, frame_count):
        for j in range(seg.channels):
            offset = (i * seg.channels) + j
            offset_minus_1 = ((i-1) * seg.channels) + j

            last_val[j] = alpha * (last_val[j] + original[offset] - original[offset_minus_1])
            filteredArray[offset] = int(min(max(last_val[j], minval), maxval))

    for i in range(1, frame_count):
        for j in range(seg.channels):
            offset = (i * seg.channels) + j
            last_data[j]=original[offset];               
   # pdb.set_trace();
    return seg._spawn(data=filteredArray), last_val, last_data


def RescanInputs():
    import GlobalVars

   

import GlobalVars;
import pycromanager;
import numpy as np;
import pdb
import time;
import threading

           
def VidAcquisition():

        global imagestartbuffer
        global imagesaving
        global permwinimage
        global permwintimes;
        global startbuffertimes
        global activewintimes
        global starttime
        global frameTrig;    
        global vid_timer;
        global above_threshold;


            
        #if GlobalVars.core.is_sequence_running():
        while (GlobalVars.core.get_remaining_image_count()>0):             
                new_image = GlobalVars.core.pop_next_image()                
                new_image=new_image.reshape(GlobalVars.height,GlobalVars.width)
                #new_image = new_image.astype('float32')/new_image.max()*255.0
                #new_image = new_image.astype('uint8')
                permwinimage.append(new_image)
                newtime=time.time();
                permwintimes.append(float(newtime)-float(starttime))
              
                if (above_threshold==True):           #EG are we recording      
                    imagesaving.append(new_image)                            
                    activewintimes.append(float(newtime)-float(starttime))
                else:              
                    imagestartbuffer.append(new_image);                         
                    startbuffertimes.append(float(newtime)-float(starttime));
                            
        if (GlobalVars.isRunning):
            vidthread=threading.Timer(vid_timer,VidAcquisition)
            vidthread.start();
            
def TriggeredRecordAudio(ui):
    
 import threading
 import GlobalVars
 import array
 from pydub import AudioSegment
 import pycromanager;
 import pydub
 
 global imagestartbuffer
 global imagesaving
 global permwinimage
 global permwintimes;
 global startbuffertimes
 global activewintimes
 global starttime
 global frameTrig;
 global above_threshold
 global FrameTimesTracker
 global frameTrig
 global vid_timer

 GlobalVars.exposure=GlobalVars.core.get_exposure();
 GlobalVars.height=GlobalVars.core.get_image_height();
 GlobalVars.width=GlobalVars.core.get_image_width();
 
 vid_timer=(GlobalVars.exposure/1000)/2; #check regularly. 
 
 SILENCE_LIMIT = GlobalVars.buffertime;
 PREV_AUDIO = GlobalVars.buffertime;
 acq_timestamps=[]
 FrameTimesTracker=deque(maxlen=CHUNK);
 RATE=GlobalVars.SampleRate;
 print(RATE)
 rel = int((RATE/CHUNK)) #*2) #2 channels Rate in audio chunks. 
 MIN_DUR=((GlobalVars.buffertime*2)+2);#
 
 GlobalVars.fps=((1000/GlobalVars.exposure))   

 imagestartbuffer=deque(maxlen=int(GlobalVars.fps*PREV_AUDIO));
 permwinimage=deque(maxlen=int(GlobalVars.fps*PREV_AUDIO)); 
 startbuffertimes=deque(maxlen=int(GlobalVars.fps*PREV_AUDIO)); 
 permwintimes=deque(maxlen=int(GlobalVars.fps*PREV_AUDIO));
 
 
 imagesaving=[]
 activewintimes=[] 
 starttime=time.time();
 
 if GlobalVars.core.is_sequence_running():
     GlobalVars.core.stop_sequence_acquisition();
     
 GlobalVars.core.clear_circular_buffer();
 GlobalVars.core.start_continuous_sequence_acquisition(1) 
 
 InputTask=nidaqmx.Task()
 InputTask.ai_channels.add_ai_voltage_chan("Dev1/ai2",terminal_config = TerminalConfiguration.RSE)
 InputTask.ai_channels.add_ai_voltage_chan("Dev1/ai3",terminal_config = TerminalConfiguration.RSE)
 InputTask.timing.cfg_samp_clk_timing(RATE,sample_mode=AcquisitionType.CONTINUOUS,samps_per_chan=GlobalVars.SampleRate*20)
 InputTask.start()
 
 OutputTask=nidaqmx.Task();
 OutputTask.do_channels.add_do_chan('Dev1/port0/line1',line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
 OutputTask.start()
 OutputTask.write([False],auto_start=True)
 
 prev_audio = deque(maxlen=int(PREV_AUDIO * rel)) #prepend audio running buffer
 
 perm_win = deque(maxlen=int(PREV_AUDIO * rel)) 
 plot_win = deque(maxlen=int(0.5*rel))
 

 vidthread=threading.Timer(vid_timer,VidAcquisition)
 vidthread.start();
 time.sleep(0.01);
 
 fps=int(1/(GlobalVars.exposure/1000))
 

    
 ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
 audio2send = []

 started = False
 
 def updateGraph():        
       ui.GraphWidget.plot(plotarray, width=1, clear=True)       
       #ui.FPS_Label.setText(

 timer = pg.QtCore.QTimer()
 timer.timeout.connect(updateGraph)
 timer.start(500)
 count=1;


 oldret=0;           
 
 above_threshold=False;
 time.sleep(0.01); 
 
 while (GlobalVars.isRunning==1):
     
  newtime = time.time()
 
  data=InputTask.read(number_of_samples_per_channel=CHUNK);# CHUNK x 2.
  temparray=np.array(data); # CHUNK x 2.

  temparray=temparray*(32768/10);# so scale +/- 10 to +/- 32678
  temparray=temparray.astype('int16');# and shift to int16 for WAV writing later

  currdata = np.empty((2*CHUNK,), dtype=temparray.dtype) # array for interleaved bytes
  curraudio = np.empty((CHUNK,), dtype=temparray.dtype) # array for byte audio.
  
  curraudio = temparray[0,:];  
  currdata[0::2] = temparray[0,:];
  currdata[1::2] = temparray[1,:]
  
  cur_data=currdata.tobytes(); # and to bytes finally. 
  cur_audio=curraudio.tobytes();  
  
  count=count+1
  if (count>20):
      count=0
      QtWidgets.qApp.processEvents()
      
  plot_win.append(cur_audio)  
  perm_win.append(cur_audio)
  plotdata = b''.join(list(plot_win))
  plotarray = array.array("h",plotdata);
  
  if (len(permwintimes)>2):
      try:
          FPSDisplay=permwintimes[-1]-permwintimes[-2];
          FPSDisplay=(1/FPSDisplay)
          ui.FPS_Label.setText(str(FPSDisplay))
      except:
          pass
      
  

  
  if((sum([x > GlobalVars.threshold for x in plotarray])> 0) and len(audio2send)<(MAX_DUR*rel)):    
   if(not started):
    OutputTask.write([True],auto_start=True)
    temp=time.time();    
    ui.ListeningTextBox.setText('<span style="color:red">singing</span>')
    started = True
    above_threshold=True;
   audio2send.append(cur_data)
   #above_threshold=True;
  elif (started is True and len(audio2send)>(MIN_DUR*rel)):
   print("Finished")
   OutputTask.write([False],auto_start=True)
   alltimes=list(startbuffertimes)+list(activewintimes);
   above_threshold=False;
   print('total time:')
   print(time.time()-temp+PREV_AUDIO)
   filename = save_audio(list(prev_audio) + audio2send,imagestartbuffer,imagesaving,fps,alltimes,GlobalVars.Ch1DirPath,GlobalVars.Ch1fileName)
   started = False     
   prev_audio = copy.copy(perm_win)
   imagestartbuffer=copy.copy(permwinimage)  
   startbuffertimes=[float(x) - float(permwintimes[0]) for x in permwintimes]
   imagesaving=[]
   activewintimes=[]
   starttime = time.time()
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
   audio2send=[]
  elif (started is True):
   print('too short');
   print('total time:')
   print(time.time()-temp+PREV_AUDIO)
   #ui.ListeningTextBox.setText('too short')
   OutputTask.write([False],auto_start=True)
   started = False
   above_threshold=False;   
   prev_audio = copy.copy(perm_win)
   imagestartbuffer=copy.copy(permwinimage)   
   startbuffertimes=[float(x) - float(permwintimes[0]) for x in permwintimes]
   imagesaving=[]
   activewintimes=[]
   starttime = time.time()
   audio2send=[]
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
  else:
   prev_audio.append(cur_data)

   
 print("done recording")

 OutputTask.write([False],auto_start=True)     
 InputTask.stop();
 OutputTask.stop();
 InputTask.close();
 OutputTask.close();
 GlobalVars.core.stop_sequence_acquisition();
 
def save_audio(data, imagebuffer,imagedata,fps, timestamps,rootdir, filename):
 import GlobalVars
 import pdb;
 import pyaudio
 
 from libtiff import TIFF
 from PIL import Image
    
 """ Saves mic data to  WAV file. Returns filename of saved
 file """
# filename = GlobalVars.path+'_'+str(int(time.time()))
 # writes data to WAV and TIFF file
 T=time.localtime()
 outtime=str("%02d"%T[0])+str("%02d"%T[1])+str("%02d"%T[2])+str("%02d"%T[3])+str("%02d"%T[4])+str("%02d"%T[5])
 DatePath='/'+str("%02d"%T[0])+'_'+str("%02d"%T[1])+'_'+str("%02d"%T[2])+'/' 
 filename = rootdir+DatePath+filename+'_'+outtime
 
 if not os.path.exists(os.path.dirname(rootdir+DatePath)):
    try:
        os.makedirs(os.path.dirname(rootdir+DatePath))
    except:
        print('File error- bad directory?')

 data = b''.join(data)

 wf = wave.open(filename + '.wav', 'wb')
 wf.setnchannels(2);
 wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
 wf.setframerate(int(GlobalVars.SampleRate)) 
 wf.writeframes(data)
 print(len(data)/GlobalVars.SampleRate)
 
 wf.close()
 #pdb.set_trace();
 print('saving image');  
 tif = TIFF.open(filename+'.tif', mode = 'w')
 im = Image.fromarray(imagebuffer[1])
 imidx=2;
 #dtype=im.dtype
# pdb.set_trace()
 print('time in frames: ')
 print((len(imagebuffer)+len(imagedata))*(GlobalVars.exposure/1000))

 for i in range (len(imagebuffer)):
     im = Image.fromarray(imagebuffer[i])
     im = im.resize((int(GlobalVars.width),int(GlobalVars.height)), Image.ANTIALIAS) 
     tif.write_image(im, compression = None)
     
 for i in range (len(imagedata)):
     im = Image.fromarray(imagedata[i])
     im = im.resize((int(GlobalVars.width),int(GlobalVars.height)), Image.ANTIALIAS)
     try:
         tif.write_image(im, compression = None) #exception for too big a tiff file sometimes. 
     except:
         tif.close();  #close the old one
         tif = TIFF.open(filename+'_'+str(imidx)+'.tif', mode = 'w') #open a new one
         tif.write_image(im, compression = None) #write the offending image
         imidx=imidx+1; #this should never get about 2, but.... maybe?          

 tif.close(); #close tif files. 
 
 
 f = open(filename + 'timestamps.txt','a')
 for i in timestamps:
     reltime=float(i)-float(timestamps[0])-GlobalVars.buffertime;
     f.write(str(reltime)+'\n');
 f.close(); 
 return filename + '.wav'
 

