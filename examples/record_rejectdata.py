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

Service = pchain.cleinit()
realm = Service.PCRealmBase()

pydata.DefineType('NumberClass')

@pyproc.DefineProc('HelloWorldProc',NumberClass,NumberClass)
def Execute(self,indata) :  
  print(str(indata),'  is reject')
  return (0,-1,None)

data = NumberClass(123.4)
print(data._ID)
proc = HelloWorldProc()
print(proc._ID)
RecordID = proc.RecordReject(True)
realm.RunProc(data,None,proc)

print(realm.GetReject(RecordID)[0]._ID)
realm.ClearReject(RecordID)
print(realm.GetReject(RecordID))


#proc.AddOutputData(NumberClass(123.4),NumberClass(122222.4),NumberClass(123.4))
proc.AddOutputDataEx(NumberClass(123.4),NumberClass(122222.4),NumberClass(123.4))

print(proc.OutputToParaPkg()[0])

print(proc.IsInstance(HelloWorldProc))
print(proc.GetInputNumber())

print(proc.GetType())

print(proc.Tag)


pchain.cleterm() 