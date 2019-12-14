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
pydata.DefineType('IntegerClass',int)

# Define procedure types
@pyproc.DefineProc('StringLengthProc',StringClass,IntegerClass)
def Execute(self,input_str) :  
  Context = self.Context  #  first must save Context in local variable
  return (0,1,IntegerClass(len(input_str.value())))

d2 = StringClass("aaaa")
print(d2.RunProc(StringLengthProc))

d3 = StringClass("sssssssssssss")
set1 = Service.PCDataSetBase.Create(d2,d3)
print(set1.RunProc(StringLengthProc))

pkg = Service._ServiceGroup._NewParaPkg()
set1.SaveTo(pkg)
print(pkg._ToJSon())

ld_set = Service.PCDataBase.LoadFrom(pkg)
print(ld_set.RunProc(StringLengthProc))

print(ld_set.GetTag())
print(set1.GetTag())
print(ld_set)

pkg._Clear()
realm.SaveObject(pkg,set1,d2)
print(pkg._ToJSon())

loads = realm.LoadObject(pkg,False)
print(loads)
