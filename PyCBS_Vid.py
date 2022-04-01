
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QSizeGrip
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "GUI2.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

##from PyRecordMenu import Ui_MainWindow
from AudioRecorderFunctions import *
import GlobalVars



def RescanInputsButtonPushed():
    
    import GlobalVars
    import pyaudio as pa
    import sys, serial
    from serial.tools import list_ports

    from nidaqmx.system.device import Device

    system = nidaqmx.system.System.local()
    NIDevices=system.devices.device_names

    ui.InputSelectioncomboBox.disconnect();
    ui.InputSelectioncomboBox.clear();
    
    for p in NIDevices:                              
              # temp = p[0]
               #print(temp)
               ui.InputSelectioncomboBox.insertItem(0,str(p))
               
    ui.InputSelectioncomboBox.setCurrentText(GlobalVars.DeviceName);    
    ui.InputSelectioncomboBox.currentIndexChanged.connect(InputSelectioncomboBoxChanged);    
    
    ui.DAQOutComboBox.disconnect()
    ui.DAQOutComboBox.clear();
    
    device = Device(GlobalVars.DeviceName)
    DAQPorts=device.do_lines.channel_names;    
    
    for p in DAQPorts:                              
              # temp = p[0]
               #print(temp)
               ui.DAQOutComboBox.insertItem(0,str(p))

    ui.DAQOutComboBox.setCurrentText(GlobalVars.Pin1);
    ui.DAQOutComboBox.currentIndexChanged.connect(Ch1TriggerChanged);
##
##
##    if (len(temp)>0):
##        GlobalVars.COM_PORT=(temp)
##    else:
##        print("No Teensy Serial Device")   
  
def StopPushButton():   
    import GlobalVars
    GlobalVars.isRunning=0
    
    ui.StopPushButton.setEnabled(False)    
    ui.StartPushButton.setEnabled(True)
    ui.RescanInputsPushButton.setEnabled(True)
    ui.ThresholdLineEdit.setEnabled(True)
    ui.InputSelectioncomboBox.setEnabled(True)    
    ui.BufferTimeSpinBox.setEnabled(True)
    ui.Ch1SaveDirPushButton.setEnabled(True)
    ui.ArduinoSelectioncomboBox.setEnabled(True)
    ui.SampleRatecomboBox.setEnabled(True)
    ui.InputSelectioncomboBox.setEnabled(True)
    ui.SelectROIPushButton.setEnabled(True)
    ui.BufferTimeSpinBox.setEnabled(True)
    ui.ShutterRecordingcheckBox.setEnabled(True);
    
    
    ui.ListeningTextBox.setText('')
    #GlobalVars.core.

def StartPushButton():

    import GlobalVars
    ui.StopPushButton.setEnabled(True)
    ui.StartPushButton.setEnabled(False)
    ui.RescanInputsPushButton.setEnabled(False)
  #  ui.ThresholdLineEdit.setEnabled(False)    
    ui.InputSelectioncomboBox.setEnabled(False)    
    ui.BufferTimeSpinBox.setEnabled(False)
    ui.Ch1SaveDirPushButton.setEnabled(False)
    ui.ArduinoSelectioncomboBox.setEnabled(False)
    ui.SampleRatecomboBox.setEnabled(False)
    ui.InputSelectioncomboBox.setEnabled(False)
    ui.SelectROIPushButton.setEnabled(False)
    ui.BufferTimeSpinBox.setEnabled(False)
    ui.ShutterRecordingcheckBox.setEnabled(False);    

    GlobalVars.isRunning=1
    TriggeredRecordAudio(ui)
    

def ThresholdLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.threshold=float(newvalue)  
    
def BufferTimeSpinBoxChanged(newvalue):
    import GlobalVars
    GlobalVars.buffertime=int(newvalue)

def SelectROIPushButtonPressed(ui):
    import cv2;
    import GlobalVars;
    import numpy as np
    import pdb

    GlobalVars.core.clear_roi();    
    GlobalVars.core.snap_image();
    image_array=(GlobalVars.core.get_image())    
  #  image_array = image_array.astype('float32')/image_array.max()*255.0
   # image_array = image_array.astype('uint8')
    image_array = image_array.reshape(GlobalVars.height,GlobalVars.width);
    roi=cv2.selectROI('Choose ROI - Enter to select, "c" to cancel',image_array)

    print(roi);
  #pdb.set_trace();
    GlobalVars.core.set_roi(roi[0], roi[1], roi[2]-roi[0], roi[3]-roi[1]);    
    #ui.ClearROIPushButton.setEnabled(True);
    GlobalVars.height=GlobalVars.core.get_image_height();
    GlobalVars.width=GlobalVars.core.get_image_width();
    cv2.destroyAllWindows()
    
def ClearROIButtonPressed(ui):
    import GlobalVars;

    GlobalVars.core.clear_roi();
    GlobalVars.height=GlobalVars.core.get_image_height();
    GlobalVars.width=GlobalVars.core.get_image_width();    

    
    
def InputSelectioncomboBoxChanged(newvalue):
    import GlobalVars
    import pyaudio
    import pdb

def Ch1SaveDirPushButtonpushButtonClicked():

    import os
    import GlobalVars
    import pdb
    
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch1DirPath, ''))
    GlobalVars.Ch1DirPath = QtWidgets.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch1fileName = QtWidgets.QFileInfo(savefilename[0]).fileName();
    
    ui.Ch1FileNameLabel.setText("Filename: "+GlobalVars.Ch1fileName)
    ui.Ch1FileDirectoryLabel.setText("Directory: "+GlobalVars.Ch1DirPath)

  
def BirdNameLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.filename=str(newvalue)
    
def Ch1TriggerChanged():
    import GlobalVars
    GlobalVars.Pin1 = str(ui.DAQOutComboBox.currentText());
    
def updateSampleRate():
    import GlobalVars
    import pdb

       
    GlobalVars.SampleRate=int(ui.SampleRatecomboBox.currentText())


def ShutterRecordingcheckBoxPressed():
    import GlobalVars;
    GlobalVars.ShutterRecording=ui.ShutterRecordingcheckBox.checkState();

def forceResetpushButtonPressed():
    import GlobalVars
    import pdb
    pdb.set_trace();
  
def loadConfig_ButtonPressed():
    import os
    import GlobalVars       
            
    loadfilename = (QtWidgets.QFileDialog.getOpenFileName(ui,'Open Config File', GlobalVars.Ch1DirPath,'*.TAFcfg'))
    GlobalVars.DirPath = QtWidgets.QFileInfo(loadfilename[0]).path();
    GlobalVars.loadConfig(loadfilename[0])
    GlobalVars.UpDateValues(ui)

def saveConfig_ButtonPressed():
    import GlobalVars    
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Save Config File', GlobalVars.Ch1DirPath, '.TAFcfg','.TAFcfg'))
    GlobalVars.DirPath = QtWidgets.QFileInfo(savefilename[0]).path();
    GlobalVars.saveConfig(savefilename[0])

def updateSampleRate():
    import GlobalVars
    GlobalVars.samplerate=int(ui.SampleRatecomboBox.currentText())    
    
 

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        from numpy import arange, array, zeros
        import GlobalVars;
        import pycromanager
        import pdb

        bridge = pycromanager.Bridge()
        
        #get object representing micro-manager core
        GlobalVars.core= bridge.get_core()
        GlobalVars.core.clear_roi();
        GlobalVars.height=GlobalVars.core.get_image_height();
        GlobalVars.width=GlobalVars.core.get_image_width();
        GlobalVars.exposure=GlobalVars.core.get_exposure();
        GlobalVars.fps=((1000/GlobalVars.exposure))
        self.ExposureTimelineEdit.setText(str(GlobalVars.exposure))
        
        GlobalVars.DeviceName='Dev1';
        GlobalVars.ShutterRecording=True;
        print(GlobalVars.height)
        print('x')
        print(GlobalVars.width)
        GlobalVars.Pin1 = 'Dev1/port0/line1';
        GlobalVars.buffertime=3        
        GlobalVars.threshold=500
        GlobalVars.SampleRate=44100;
        GlobalVars.Ch1fileName=''
        GlobalVars.Ch1DirPath=''        
        GlobalVars.isRunning=False;
        
        self.RescanInputsPushButton.clicked.connect(RescanInputsButtonPushed)
        self.StopPushButton.clicked.connect(StopPushButton)
        self.StartPushButton.clicked.connect(StartPushButton)        
        
        self.DAQOutComboBox.currentIndexChanged.connect(Ch1TriggerChanged);
        self.SelectROIPushButton.clicked.connect(SelectROIPushButtonPressed)
        self.ClearROIPushButton.clicked.connect(ClearROIButtonPressed);
        self.InputSelectioncomboBox.currentIndexChanged.connect(InputSelectioncomboBoxChanged);
        self.ShutterRecordingcheckBox.stateChanged.connect(ShutterRecordingcheckBoxPressed)
        self.forceResetpushButton.clicked.connect(forceResetpushButtonPressed);
        self.ThresholdLineEdit.textChanged.connect(ThresholdLineEditChanged)
        self.Ch1SaveDirPushButton.clicked.connect(Ch1SaveDirPushButtonpushButtonClicked)         
        self.BufferTimeSpinBox.valueChanged.connect(BufferTimeSpinBoxChanged)        
        self.SampleRatecomboBox.currentIndexChanged.connect(updateSampleRate);
        self.actionLoad_Config.triggered.connect(loadConfig_ButtonPressed);
        self.actionSave_Config.triggered.connect(saveConfig_ButtonPressed);    

if __name__ == "__main__":
    import GlobalVars
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    RescanInputsButtonPushed()
    ui.show()
    sys.exit(app.exec_())
    
    #window.show()
    #sys.exit(app.exec_())


