
global isRunning
global numdevices
global devicenumber
global inputdeviceindex
global SampleRate
global COM_PORT_Idx
global threshold
global buffertime
global path
global fps
global height;
global width;
global Ch1DirPath
global Ch1fileName
global Pin1;
global exposure;
global ShutterRecording;



def loadConfig(loadfilename):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    import serial
    from numpy import arange,array

    parser = SafeConfigParser()
    loadfilename=loadfilename.replace('/','\\')    

    if not parser.read(str(loadfilename)): #.replace('/','\\')):
        raise(IOError, 'cannot load')
        
    GlobalVars.inputdeviceindex=int(parser.get('main','GlobalVars.inputdeviceindex'))
    GlobalVars.threshold=float(parser.get('main','GlobalVars.threshold'))
    GlobalVars.buffertime=float(parser.get('main','GlobalVars.buffertime'))
    GlobalVars.Ch1DirPath=str(parser.get('main','GlobalVars.Ch1DirPath'))
    GlobalVars.Ch1fileName=str(parser.get('main','GlobalVars.Ch1fileName'))
    GlobalVars.exposure=float(parser.get('main','GlobalVars.exposure'))

    GlobalVars.ShutterRecording=bool(parser.getboolean('main','GlobalVars.ShutterRecording'))
    GlobalVars.Pin1=str(parser.get('main','GlobalVars.Pin1'))    
    GlobalVars.COM_PORT_Idx=int(parser.get('main','GlobalVars.COM_PORT_Idx'))
    GlobalVars.SampleRate=int(parser.get('main','GlobalVars.SampleRate'))
    GlobalVars.DeviceName=str(parser.get('main','GlobalVars.DeviceName'))

      

def saveConfig(savefilename):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    from numpy import array
             
    SaveFile= open((savefilename),'w')
    
    parser = SafeConfigParser()
    
    parser.add_section('main')

     
    parser.set('main','GlobalVars.inputdeviceindex',str(GlobalVars.inputdeviceindex))
    parser.set('main','GlobalVars.threshold',str(GlobalVars.threshold))
    parser.set('main','GlobalVars.buffertime',str(GlobalVars.buffertime))
    parser.set('main','GlobalVars.Ch1DirPath',str(GlobalVars.Ch1DirPath));    
    parser.set('main','GlobalVars.Ch1fileName',str(GlobalVars.Ch1fileName));
    parser.set('main','GlobalVars.exposure',str(GlobalVars.exposure));
    parser.set('main','GlobalVars.ShutterRecording',str(GlobalVars.ShutterRecording));
    parser.set('main','GlobalVars.Pin1',str(GlobalVars.Pin1));
    parser.set('main','GlobalVars.COM_PORT_Idx',str(GlobalVars.COM_PORT_Idx));
    parser.set('main','GlobalVars.SampleRate',str(GlobalVars.SampleRate));
    parser.set('main','GlobalVars.DeviceName',str(GlobalVars.DeviceName));        
    

      
    parser.write(SaveFile)    
    SaveFile.close()
##
def UpDateValues(ui):
    import GlobalVars
    from numpy import arange
    import pdb
##

    ui.ArduinoSelectioncomboBox.setCurrentIndex(GlobalVars.COM_PORT_Idx);
    GlobalVars.COM_PORT=ui.ArduinoSelectioncomboBox.currentText();
    #
    ui.SampleRatecomboBox.setCurrentIndex(GlobalVars.samplerate_Idx)
    print(samplerate_Idx)
    GlobalVars.samplerate=int(ui.SampleRatecomboBox.currentText());
    #pdb.set_trace();
    ui.Ch1FileNameLabel.setText(GlobalVars.Ch1fileName)
    ui.Ch1FileDirectoryLabel.setText(GlobalVars.Ch1DirPath);
    ui.ThresholdLineEdit.setText(str(GlobalVars.threshold))
    #ui.ExposureTimelineEdit.setText(str(GlobalVars.exposure));    
    ui.InputSelectioncomboBox.setCurrentIndex(GlobalVars.inputdeviceindex);
    
    ui.BufferTimeSpinBox.setValue(GlobalVars.buffertime);
    ui.ShutterRecordingcheckBox.setCheckState(GlobalVars.ShutterRecording)
    
