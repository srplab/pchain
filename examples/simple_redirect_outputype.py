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
pydata.DefineSubType(NumberClass,'IntegerClass')

# Define procedure types
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  return (4,1,NumberClass(val))

# Define procedure types
@pyproc.DefineProc('OutputProc',(IntegerClass,IntegerClass),None)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  print('sum = ', num1.value() + num2.value())
  Context['Cell'].Finish()
  return (0,1,None)

IntegerInputProc = InputProc.CreateSubType("IntegerInputProc",None)
IntegerInputProc.RedirectOutput(NumberClass,IntegerClass)
    
cell = Service.PCCellBase._New()
cell.AddProc(IntegerInputProc,OutputProc)

realm.AddCell(cell)
realm.Execute()


#--save & load
para = Service._ServiceGroup._NewParaPkg()
realm.SaveObject(para,cell)
print(para._ToJSon())

realm.RemoveCell(cell)

loadcells = realm.LoadObject(para,True)
print(loadcells[0])
realm.AddCell(loadcells[0])
realm.Execute()

print('modify cell output...')
realm.RemoveCell(loadcells[0])

subcell = Service.PCCellBase.Create(None,'SubCell',InputProc.GetType().InputQueueToParaPkg(),InputProc.GetType().OutputQueueToParaPkg())
subcell.AddProc(InputProc)
subcell.RedirectOutput(NumberClass,IntegerClass)

print('subcell    =    ',subcell.GetTag())
print('subcell inst 1  =    ',subcell._New().GetTag())
print('subcell inst 2  =    ',subcell._New().GetTag())

para = Service._ServiceGroup._NewParaPkg()
realm.SaveObject(para,subcell._New())
print(para._ToJSon())
loadcells = realm.LoadObject(para,True)
print('subcell loaded  =    ',loadcells[0].GetTag())

cell = Service.PCCellBase._New()
cell.AddProc(subcell,OutputProc)

print(cell.GetTag())

para = Service._ServiceGroup._NewParaPkg()
realm.SaveObject(para,cell)
print(para._ToJSon())

realm.AddCell(cell)
realm.Execute()

loadcells = realm.LoadObject(para,True)
print(loadcells[0].GetTag())

# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 