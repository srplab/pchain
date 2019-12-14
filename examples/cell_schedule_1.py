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
pydata.DefineType('NumberClass')

# Define procedure types
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  return (4,1,NumberClass(float(val)))

# Define procedure types
@pyproc.DefineProc('OutputProc',(NumberClass,NumberClass),NumberClass)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  print('sum = ', num1.value() + num2.value())
  return (0,1,NumberClass(num1.value() + num2.value()))
    
@pyproc.DefineProc('PrintProc',NumberClass,NumberClass)
def Execute(self,dat) :  
  Context = self.Context  #  first must save Context in local variable
  print('output result  =  ',dat.value())
  return (0,0,dat)
      
#create cell type & execute self    
mycell = Service.PCCellBase.Create(None,"mycell",None,NumberClass)
@mycell._RegScriptProc_P("Execute")
def Execute(cleobj,realm,cell,runner) :
  newin1 = InputProc.call()
  newin2 = InputProc.call()
  result = OutputProc.call(newin1,newin2)
  cleobj.ClearEnvData()
  cleobj.AddOutputData(result)
  return 0

result = realm.RunProcEx(None,None,mycell,PrintProc)
print(result)

# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 