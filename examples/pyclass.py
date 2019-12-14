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

#define a python class
class pyclass :
  def pyfunc(self,a,b,c) :
    return a+b+c

#define data management type
pydata.DefineType('PythonObjectClass',pyclass)
pydata.DefineType('PythonNumberClass')

#define proc management type
@pyproc.DefineRawProc('PyFuncProc',(PythonObjectClass,PythonNumberClass,PythonNumberClass,PythonNumberClass),PythonNumberClass)
def PyFun(obj,a,b,c) :
  print('input :',obj,a,b,c)      
  return obj.pyfunc(a,b,c)

'''
func = PyFuncProc()
result = func(PythonObjectClass(pyclass()),PythonNumberClass(1.0),PythonNumberClass(2.0),PythonNumberClass(3.0))
'''

result = PyFuncProc.call(PythonObjectClass(pyclass()),PythonNumberClass(1.0),PythonNumberClass(2.0),PythonNumberClass(3.0))
print(result.value())
print(result.Wrap().GetSource())
print(result.Wrap().GetOwnerProc())

# finish
pchain.cleterm() 