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
class NumberClass(PCPyDataClass) :
  @staticmethod
  def Load(MetaData) :
    # MetaData maybe string or parapkg
    # raise Exception('Load function is not defined ')
    if type(MetaData) == type('') :
      return NumberClass(float(MetaData))
    else :
      return NumberClass(MetaData[0])
  def Save(self) :
    #raise Exception('Save function is not defined for '+str(self))   
    return str(self.num) 

  def ToParaPkg(self,parapkg) :
    parapkg[0] = self.num
    return True
pydata.Register(NumberClass)  

pydata.DefineSubType(NumberClass,'IntegerClass')
pydata.DefineSubType(IntegerClass,'SubIntegerClass')

# Define procedure types
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  if pchain.ispython2 == True :
    if type(val) == int :
      return (4,1,SubIntegerClass(val))
    else :
      return (4,1,NumberClass(val))
  else :    
    if type(eval(val)) == int :
      return (4,1,SubIntegerClass(eval(val)))
    else :
      return (4,1,NumberClass(eval(val)))

# Define procedure types
@pyproc.DefineProc('OutputProc',(NumberClass,IntegerClass),None)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  if num1 == None or num2 == None :
    return (2,0,None)
  print(num2.GetType())
  print(num2.Wrap().GetType())
  print(num2.Wrap().GetType()._Class)
  print(num2.Wrap().GetType()._Class._Class)
  print('sum = ', num1.value() + num2.value())
  Context['Cell'].Finish()
  return (0,1,None)

cell = Service.PCCellBase._New()
cell.AddProc(InputProc,OutputProc)

realm.AddCell(cell)
realm.Execute()

# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 