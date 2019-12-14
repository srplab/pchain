# need register version of CLE
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

# Define data types, and property
newtype = Service.PCDataBase.CreateType('DataHasProperty')
newtype.CreateProperty('Attr1',libstarpy.TYPE_CHARPTR,'')
pydata.DefineTypeEx(newtype,'NumberClass')

# Define procedure types
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  re = NumberClass(val)
  re.Wrap().Attr1 = 'From input'
  return (4,1,re)

# Define procedure types
@pyproc.DefineProc('OutputProc',(NumberClass,NumberClass),None)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  print('sum = ', num1.value() + num2.value())
  Context['Cell'].Finish()
  return (0,1,None)
  
cell = Service.PCCellBase._New()
cell.AddProc(InputProc,OutputProc)

realm.AddCell(cell)
realm.Execute()

activeset = realm.GetActiveObject(None,1.0,0)
print(activeset)
activesetTag = realm.GetTagEx(activeset)
print(activesetTag)

for t in activeset :
  print( t.GetTagLabel())
  
for t in activeset :
  if realm.IsData(t) :
    print(t.Wrap().Attr1)
  
# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 