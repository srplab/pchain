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

# Define data types
pydata.DefineType('StringClass',str)
pydata.DefineType('NumberClass',int)
pydata.DefineType('UpperStringClass',str)

# Define procedure types
@pyproc.DefineProc('LengthProc',StringClass,NumberClass)
def Execute(self,instr) :  
  Context = self.Context  #  first must save Context in local variable
  return (0,1,NumberClass(len(instr.value())))
  
@pyproc.DefineProc('ToUpperProc',StringClass,UpperStringClass)
def Execute(self,instr) :  
  Context = self.Context  #  first must save Context in local variable
  return (0,1,UpperStringClass(instr.value().upper()))  

@realm._RegScriptProc_P('OnBeforeExecute')
def realm_OnBeforeExecute(CleObj):
  envdata = CleObj.GetEnvData()
  if envdata._Number == 0 :
    return
  cell = Service.PCCellBase._New()
  cell.AddEnvData(CleObj,envdata[0])
  cell.AddProc(LengthProc)
  CleObj.AddCell(cell)
  
  cell = Service.PCCellBase._New()
  cell.AddEnvData(CleObj,envdata[0])
  cell.AddProc(ToUpperProc)
  CleObj.AddCell(cell)
  
  CleObj.RemoveEnvData(envdata)
  print(CleObj.GetEnvData()._Number)

realm.AddEnvData(StringClass('abcde'))
result = realm.ExecuteForResult()
print(result)

pchain.cleterm() 