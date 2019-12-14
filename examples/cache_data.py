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

pydata.DefineType('NumberClass')

# Define procedure types
@pyproc.DefineProc('TestProcClass',None,PersonClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  return (0,1,None)


data = PersonClass(Person(name='aaaa',age=15))
d2 = NumberClass(1234.5)

print(data.SetCache(TestProcClass,d2))
cd = data.GetCache(TestProcClass)

print(d2.GetTag())
print(cd.GetTag())

print(d2)
print(cd)

myset = Service.PCDataSetBase.CreateType("myset",NumberClass)
print(myset)
print(myset.GetTag())

set1 = myset.Create(d2,cd)
print(set1)
print(set1.GetTag())

set2 = myset.Create(d2,data)
print(set2)