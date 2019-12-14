import sys
import os
try:
  import pchain
except :  
  pchain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../')
  sys.path.insert(0,pchain_path)
  import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

Service = pchain.cleinit()
import libstarpy

realm = Service.PCRealmBase()

stub = Service.PCRealmStubBase()
@stub._RegScriptProc_P('OnException')
def stub_OnException(SelfObj,AlarmLevel,Info) :
  print('++++++++++++++++++',Info)
  
@stub._RegScriptProc_P('OnBeforeExecute')
def stub_OnBeforeExecute(CleObj,Realm):
  print('--------------------------',str(Realm))
  return  
    
realm.SetRealmStub(stub)  

# Define data types
pydata.DefineType('PythonNumberClass')

# Define procedure types
@pyproc.DefineProc('PyFuncProc',(PythonNumberClass,PythonNumberClass,PythonNumberClass),PythonNumberClass)
def Execute(self,a,b,c) :  
    Context = self.Context  #  first must save Context in local variable
    print('input :',a.value(),b.value(),c.value())      
    val = a.value() + b.value() + c.value()
    return PythonNumberClass(val)

'''
func = PyFuncProc()
result = func(PythonNumberClass(1.0),PythonNumberClass(2.0),PythonNumberClass(3.0))
'''

result = PyFuncProc.call(PythonNumberClass(1.0),PythonNumberClass(2.0),PythonNumberClass(3.0))
print(result)
print(result.Wrap().GetSource())
print(result.Wrap().GetOwnerProc())

# finish
pchain.cleterm() 