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

# Define procedure types
@pyproc.DefineProc('OutputProc',(NumberClass,NumberClass),NumberClass)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  print('sum = ', num1.value() + num2.value())
  Context['Cell'].Finish()
  return (0,1,NumberClass(num1.value() + num2.value()))

#each rule, may associate with a rule object which is an instance of PCRuleBase
rule = Service.PCRuleBase._New()
@rule._RegScriptProc_P('OnApproved')
def OnApproved(cleobj,dataorproc):
  print('OnApproved -------',dataorproc)
  print('source data    :   ',dataorproc.GetSource())
  print('owner proc     :   ',dataorproc.GetOwnerProc())

@rule._RegScriptProc_P('OnDisapproved')
def OnDisapproved(cleobj,dataorproc):
  print('OnDisapproved -------',dataorproc)    
  
@rule._RegScriptProc_P('OnBeforeFree')
def OnBeforeFree(cleobj):
  print('OnBeforeFree -------',cleobj)    
    
print('rule object  ',rule)    
cell = Service.PCCellBase._New()
cell.AddProcEx(rule,InputProc,OutputProc)

realm.AddCell(cell)
result = realm.ExecuteForResult()
print(result[0])

result[0].Approved()


pchain.cleterm() 