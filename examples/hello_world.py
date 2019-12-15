import pchain
from pchain import pyproc

Service = pchain.cleinit()
realm = Service.PCRealmBase()

@pyproc.DefineProc('HelloWorldProc',None,None)
def Execute(self) :  
  print('Hello world !')
  return (0,1,None)

realm.RunProc(None,None,HelloWorldProc)

pchain.cleterm() 