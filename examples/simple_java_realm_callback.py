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

# Define data types
pydata.DefineType('StringClass')
pydata.DefineType('NumberClass')

@pyproc.DefineProc('LengthProc',StringClass,NumberClass)
def Execute(self,strobj) :
  Context = self.Context
  val = len(strobj.value())
  return (0,1,NumberClass(val))

@pyproc.DefineProc('ToIntProc',StringClass,NumberClass)
def Execute(self,strobj) :
  Context = self.Context
  val = 0
  try:
    val = int(strobj.value())
    return (0,1,NumberClass(val))
  except :
    return (0,-1,None)

realm = Nonerealm = Service.PCRealmBase._New()

'''
note : we define callback funtion with java

realm = Service.PCRealmBase._New()

#define callback of realm
@realm._RegScriptProc_P('OnBeforeExecute')
def realm_OnBeforeExecute(CleObj):
  NewEnvData = CleObj.GetEnvData()
  for data in NewEnvData :
    if StringClass.GetType()._IsInst(data) == True :
      newcell = Service.PCCellBase._New()
      newcell.AddEnvData(CleObj,data) 
      newcell.AddProc(LengthProc)   
      CleObj.AddCell(newcell)
  CleObj.RemoveEnvData(NewEnvData)       
  return  

@realm._RegScriptProc_P('OnCellFinish')
def realm_OnCellFinish(CleObj,cell,IsSuccess):
  CleObj.ProcessCellEnvData(cell,IsSuccess);
  CleObj.RemoveCell(cell)
  
'''
# libstarpy._SetScript('java','','jvm=C:\\Program Files\\Java\\jdk-10.0.2\\bin\\server\\jvm.dll')
Result = Service._DoFile('java','./java_realm_callback/JavaRealmCallback.class','')
print(Result)

realm = Service.JavaRealmClass._New()
  
realm.AddEnvData(StringClass('qqqwwweee'),StringClass('qqqwwweee888888888888888888'),StringClass('length'))
result = realm.ExecuteForResult()
print(str(result[0]),str(result[1]))

realm.AddEnvData(StringClass('qqqwwweeesdfasdfasdfasdf'),StringClass('length'))
result = realm.ExecuteForResult()
print(result[0])

pchain.cleterm() 