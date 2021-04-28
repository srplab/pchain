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
  return (4,1,NumberClass(val))

#-----------------------------------------------------------------
import uuid

print('create data object : ',str(NumberClass(123)))

datasettype = Service.PCDataBase.GetDataSetBase().CreateType('datasetclass',None)
set1 = datasettype(NumberClass(123).Wrap())
print(set1)

objectdataclass = Service.PCDataBase.GetObjectDataBase().CreateType('objectdataclass')
d1 = objectdataclass(datasettype)
print(d1)
 
bufdataclass = Service.PCDataBase.GetBufDataBase().CreateType('bufdataclass')
parapkg = Service._ServiceGroup._NewParaPkg(12,'22222')
d1 = bufdataclass(parapkg)
print(d1)

print('create procchain object : ',str(Service.PCProcChainBase()))
print('create pccell object : ',str(Service.PCCellBase()))
print('create PCRealmStubBase object : ',str(Service.PCRealmStubBase()))
print('create PCRealmBase object : ',str(Service.PCRealmBase()))

# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 