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

realm = Service.PCRealmBase()

# Define procedure types
@pyproc.DefineProc('HelloWorldProc',None,None)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  print('Hello world !')
  return (0,1,None)

#method1 :
HelloWorldProc.call()

#method2 :
proc = HelloWorldProc()
proc()

#method3 :
realm.RunProc(None,None,HelloWorldProc)

#method4 : add to cell, run
realm.AddProc(HelloWorldProc)
realm.Execute()

pchain.cleterm() 