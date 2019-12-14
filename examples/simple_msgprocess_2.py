# need register version of CLE
#
#  envmsg -> MsgPreProcess
#         -> Msg1Process(msg2) -> Msg2Process(outmsg) -> MsgOutputProcess
#
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

Service = pchain.cleinit()
import libstarpy

realm = Service.PCRealmBase._New()

################################################################ define datatype EnvInMsg
class RawEnvInMsg :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineType('EnvInMsg',RawEnvInMsg)

################################################################ define datatype InnerMsg2
class RawInnerMsg2 :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineType('InnerMsg2',RawInnerMsg2)

################################################################ define datatype EnvOutMsg
class RawEnvOutMsg :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineType('EnvOutMsg',RawEnvOutMsg)

################################################################ define datatype MsgContext
class RawMsgContext :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineType('MsgContext',RawMsgContext)


################################################################ Define procedure type MsgPreProcess
@pyproc.DefineProc('MsgPreProcess',EnvInMsg,None)
def Execute(self,envmsg) :  
  Context = self.Context  #  first must save Context in local variable
  #--find the msg context, corresponding to input msg id
  if len(envmsg.GetSource()) == 0 :
    pass
  else :
    return (0,-1,None)
  realm = Context['Realm']
  id = envmsg.value().MsgId
  msgcontext = realm.FindCache(id)
  if msgcontext == None :
    # create msg context
    msgcontext = MsgContext(RawMsgContext(id,'msg context'))
    realm.SetCache(id,msgcontext)
    print('create msgcontext for :  ',id)
  else :
    print('find msgcontext for :  ',id)
  envmsg.AddSource(msgcontext)
  envmsg.ResetSchedule()  #--clear schedule info
  return (0,1,None)
  
################################################################ Define procedure type Msg1Process
@pyproc.DefineProc('Msg1Process',EnvInMsg,InnerMsg2)
def Execute(self,msg1) :  
  Context = self.Context  #  first must save Context in local variable
  if len(msg1.GetSource()) == 0 :
    return (0,-1,None)  # no source data, can not process
  else :
    pass
  msgcontext = msg1.GetSource()[0]
  return (0,1,InnerMsg2(RawInnerMsg2(msgcontext.value().MsgId,msg1.value().MsgInfo + '  ' + msgcontext.value().MsgInfo)))  
  
################################################################ Define procedure type Msg2Process
@pyproc.DefineProc('Msg2Process',InnerMsg2,EnvOutMsg)
def Execute(self,msg2) :  
  Context = self.Context  #  first must save Context in local variable
  #--find the msg context, corresponding to input msg id
  return (0,1,EnvOutMsg(RawEnvOutMsg(msg2.value().MsgId,'output  :  '+msg2.value().MsgInfo)))    
  
################################################################ Define procedure type MsgOutputProcess
@pyproc.DefineProc('MsgOutputProcess',EnvOutMsg,None)
def Execute(self,outmsg) :  
  Context = self.Context  #  first must save Context in local variable
  print(outmsg.value().MsgInfo)
  return (0,1,None)  

################################################################ Create Cell, add Proc
cell = Service.PCCellBase._New()
cell.AddProc(MsgPreProcess,Msg1Process,Msg2Process,MsgOutputProcess)
realm.AddCell(cell)

#create a msg, add it to realm
msg1 = EnvInMsg(RawEnvInMsg(1,'wwwwwww'))
realm.AddEnvData(msg1)
realm.Execute()

msg2 = EnvInMsg(RawEnvInMsg(1,'tttttttttttttt'))
realm.AddEnvData(msg2)
realm.Execute()

#--Build and using ProcChain
chain = realm.BuildProcChain(MsgOutputProcess,EnvInMsg)
newrealm = realm._New()
newrealm.AddProc(chain[1],MsgPreProcess)
newrealm.AddProc(chain[1],MsgPreProcess)
msg1 = EnvInMsg(RawEnvInMsg(1,'wwwwwww'))
newrealm.AddEnvData(msg1)
newrealm.Execute()

  
# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 