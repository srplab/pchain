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

# Define procedure types
@pyproc.DefineProc('TestProcClass',None,PersonClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  return (0,1,None)


data = PersonClass(Person(name='aaaa',age=15))
print('data tag =  ',data.GetTag())
print('data tag label =  ',data.GetTagLabel())

pkg = Service._ServiceGroup._NewParaPkg()
data.SaveTo(pkg)
newdata = Service.PCDataBase.LoadFrom(pkg)

print('load data tag =  ',newdata.GetTag())
print('load data tag label =  ',newdata.GetTagLabel())
print('data == load data ? ',data.Equals(newdata))

TestProc = TestProcClass().Wrap()
print('proc tag =  ',TestProc.GetTag())
print('proc tag label =  ',TestProc.GetTagLabel())


cell1 = Service.PCCellBase._New()
cell1.AddProc(TestProcClass)
print('cell1 tag =  ',cell1.GetTag())
print('cell1 tag label =  ',cell1.GetTagLabel())

cell2 = Service.PCCellBase._New()
cell2.AddProc(TestProcClass)
print('cell2 tag =  ',cell2.GetTag())
print('cell2 tag label =  ',cell2.GetTagLabel())

realm.SaveObject(pkg,cell1)
print(pkg._ToJSon())
load_pkg = realm.LoadObject(pkg,False)
print('load cell1 tag =  ',load_pkg[0].GetTag())
print('load cell1 tag label =  ',load_pkg[0].GetTagLabel())
print('cell1 == load cell1 ? ',cell1.Equals(load_pkg[0]))
print('cell2 == load cell1 ? ',cell2.Equals(load_pkg[0]))
