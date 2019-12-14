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
pydata.DefineType('NumberBaseClass')
class NumberClass(NumberBaseClass) :
  @staticmethod
  def Load(MetaData) :
    # MetaData maybe string or parapkg
    # raise Exception('Load function is not defined ')
    if type(MetaData) == type('') :
      return NumberClass(float(MetaData))
    else :
      return NumberClass(MetaData[0])
  def ToParaPkg(self,parapkg) :
    parapkg[0] = self.value()
    return True
  def Save(self) :
    return str(self.value())     
pydata.Register(NumberClass)  

# Define procedure types
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  if pchain.ispython2 == True :
    return (4,1,NumberClass(val))
  else :
    return (4,1,NumberClass(float(val)))

# load c module
Service._DoFile('','./c_process/CProcModule.dll','')
  
cell = Service.PCCellBase._New()
cell.AddProc(InputProc,Service.CAddProcClass)

realm.AddCell(cell)
result = realm.ExecuteForResult()
print(result[0])

# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 