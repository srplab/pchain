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
    
#create cell type & execute self    
mycell = Service.PCCellBase.Create(None,"mycell",None,NumberClass)
@mycell._RegScriptProc_P("Execute")
def Execute(cleobj,realm,cell,runner) :
  inputdata = cleobj.GetEnvDataQueue()
  newin = InputProc.call()
  result = OutputProc.call(inputdata[0],newin)
  cleobj.ClearEnvData()
  cleobj.AddOutputData(result)
  return 0

# method1
cell = mycell._New()
cell.AddEnvData(realm,NumberClass(1.2))
realm.AddCell(cell)
realm.Execute()

# method2
result = realm.RunProc(NumberClass(1.2),None,mycell)
print(result)

# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 