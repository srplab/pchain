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
class Person :
  hair = 'black'
  def __init__(self, name = 'Charlie', age=8):
    self.name = name
    self.age = age
  def say(self, content):
    print(content)
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   

pydata.DefineType('PersonClass',Person)

@pyproc.DefineProc('HelloWorldProc',None,None)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  print('Hello world !')
  return (0,1,None)

#--
myobjdataclass = Service.PCObjectDataBase.CreateType("myobjdataclass")

obj_data = myobjdataclass.Create(Service.PersonClass.GetType())
print(obj_data.GetObject())

obj_proc = myobjdataclass.Create(Service.HelloWorldProc.GetType())
print(obj_proc.GetObject())
print(obj_proc.GetTag())

savepara = Service._ServiceGroup._NewParaPkg()
obj_proc.SaveTo(savepara)
print(savepara._ToJSon())

ld = Service.PCDataBase.LoadFrom(savepara)
print(ld)

print(ld.GetTag())

#----------------
ParaPkg = Service._ServiceGroup._NewParaPkg(123.456,'dddddd',Service.HelloWorldProc)
buf_data = Service.PCBufDataBase.Create(ParaPkg)
print(buf_data)
print(buf_data.IsType)
print(buf_data.GetTag())

buf_data.SaveTo(savepara)
print(savepara._ToJSon())


ld = Service.PCDataBase.LoadFrom(savepara)
print(ld)
print(ld.GetTag())

print(ld.IsBufData())
print(ld.IsSame(buf_data))
print(ld.Equals(buf_data))


