import sys
import os
try:
  import pchain
except Exception as exc:
  pchain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../')
  sys.path.insert(0,pchain_path)
  import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

Service = pchain.cleinit()
import libstarpy

realm = Service.PCRealmBase._New()
realm_stub = Service.PCRealmStubBase._New()
@realm_stub._RegScriptProc_P('OnException')
def realm_stub_OnException(SelfObj,AlarmLevel,Info) :
  if AlarmLevel == 1 :
    print(Info)
realm.SetRealmStub(realm_stub) 

# Define data types
pydata.DefineType('PC_ButtonNameClass',str)  #--save button name
pydata.DefineType('PC_EventClass',str)  #save event 

# Define procedure types
@pyproc.DefineProc('ButtonClickHandlerProc',PC_EventClass,None)
def Execute(self,event) :  
  Context = self.Context  #  first must save Context in local variable
  btn_name = event.GetSource()[0]
  Context['Realm'].GetLocalBuf()[0].numLabel.setText(btn_name.value()+' is clicked')
  return (0,1,None)

#define stub function to handle all ream's callback
@realm_stub._RegScriptProc_P('OnBeforeExecute')
def realm_stub_OnBeforeExecute(stub,CleObj):
  NewEnvData = CleObj.GetEnvDataQueue()
  if NewEnvData._Number == 0 :
    return
  CleObj.EnvDataToProc(NewEnvData[0],ButtonClickHandlerProc)
  
@realm_stub._RegScriptProc_P('OnFrameData')
def realm_stub_OnFrameData(stub,CleObj,FrameData):
  print('OnFrameData   ',FrameData.GetTag(),str(FrameData),FrameData.GetUniformTick())
  return 

@realm_stub._RegScriptProc_P('OnAfterExecute')
def realm_stub_OnAfterExecute(stub,CleObj):
  print('avtive object = ',str(CleObj.GetActiveObject(None,1.0,0)))
  return False

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(self.tr('Simple Qt Sample'))
        self.resize(400, 200)
        numLabel=QLabel(self.tr(''))
        button1=QPushButton(self.tr('start'))
        
        layout = QVBoxLayout()
        self.numLabel=QLabel(self.tr('sfsdfsdf'))
        self.button1=QPushButton(self.tr('button1'))
        self.button1.clicked.connect(self.on_button_click)
        self.button2=QPushButton(self.tr('button12'))
        self.button2.clicked.connect(self.on_button_click)        
        layout.addWidget(self.numLabel)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        main_frame = QWidget()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(layout)
        
        #set realm context
        realm.GetLocalBuf()[0] = self        
        
    def on_button_click(self):
        sender = self.sender()
        
        #1. create pchain data
        PC_Button = None
        PC_Event = None
        if sender == self.button1 :
          PC_Button = PC_ButtonNameClass('button1')
          PC_Event = PC_EventClass('click1')
        else : 
          PC_Button = PC_ButtonNameClass('button2')
          PC_Event = PC_EventClass('click2')
        PC_Event.AddSource(PC_Button)
        
        realm.Clear(False)        

        #3. method1
        realm.RunProc(PC_Event,None,None)
        
        '''
        #3. method2
        realm.AddEnvData(PC_Event)
        realm.Execute()
        '''
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

pchain.cleterm() 