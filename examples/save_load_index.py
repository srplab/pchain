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
pydata.DefineType('NumberClass',float)

# Define procedure types
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  return (4,1,NumberClass(val))

# Define procedure types
@pyproc.DefineProc('OutputProc',(NumberClass,NumberClass),None)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  print('sum = ', num1.value() + num2.value())
  Context['Cell'].Finish()
  return (0,1,None)


#save & load data
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

data = PersonClass(Person(name='aaaa',age=15))

print('')
print('')
print('')
print('')

pkg = Service._ServiceGroup._NewParaPkg()
data.SaveTo(pkg)
print('save data ....')
print(pkg._ToJSon())

newdata = Service.PCDataBase.LoadFrom(pkg)

print('data tag =  ',data.GetTag())
print('load data tag =  ',newdata.GetTag())
print('data == load data  : ',data.Equals(newdata))
print('data issame load data  : ',data.IsSame(newdata))

print('')
print('')
print('')
print('')
data.SetSignature('sssssssssssssssssssssssssssssssssssssssssssssssss')

data.SaveTo(pkg)
print('save data with signature ....')
print(pkg._ToJSon())

newdata = Service.PCDataBase.LoadFrom(pkg)

print('data tag =  ',data.GetTag())
print('load data tag =  ',newdata.GetTag())
print('data == load data  : ',data.Equals(newdata))
print('data issame load data  : ',data.IsSame(newdata))