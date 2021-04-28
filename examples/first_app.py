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

realm = Service.PCRealmBase()

# Define data types
pydata.DefineType('NumberClass',int)

# Define procedure types
@pyproc.DefineProc('AddProc',(NumberClass,NumberClass),NumberClass)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  return (0,1,NumberClass(num1.value()+num2.value()))
    
cell = Service.PCCellBase()
cell.AddProc(AddProc)
cell.AddEnvData(realm,NumberClass(1),NumberClass(2))
realm.AddCell(cell)
result = realm.ExecuteForResult()
print(result[0])

result = realm.RunProc((NumberClass(1),NumberClass(2)),None,AddProc)
print(result[0])

# 1+2+3+4
result = realm.RunProc((NumberClass(1),NumberClass(2),NumberClass(3),NumberClass(4),NumberClass(5)),None,AddProc)
print(result[0])

pchain.cleterm() 