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

pydata.DefineType('PythonNumberClass')

@pyproc.DefineRawProc('PyFuncProc',(PythonNumberClass,PythonNumberClass,PythonNumberClass),PythonNumberClass)
def PyFun(a,b,c) :
  print('input :',a,b,c)      
  val = a + b + c
  return val

'''
func = PyFuncProc()
result = func(PythonNumberClass(1.0),PythonNumberClass(2.0),PythonNumberClass(3.0))
'''

result = PyFuncProc.call(PythonNumberClass(1.0),PythonNumberClass(2.0),PythonNumberClass(3.0))
print(result)
print(result.value())
print(result.GetSource())
print(result.GetOwnerProc())

# finish
pchain.cleterm() 