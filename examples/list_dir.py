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

realmStub = Service.PCRealmStubBase._New()
@realmStub._RegScriptProc_P('OnMoreUnAllocatedData')
def OnMoreUnAllocatedData(cleobj,realm,proc) :
  return 1
realm.SetRealmStub(realmStub)

# Define data types
pydata.DefineType('DiskPathClass')
pydata.DefineType('FileNameClass')

@pyproc.DefineAsyncProc('ListFileClass',DiskPathClass,FileNameClass)
def Execute(self,DiskPath) :
  Context = self.Context
    
  localbuf = Context['SelfObj'].GetLocalBuf()
  if Context['SelfObj'].Status == 0 :
    import os
    listfile = os.listdir(DiskPath.value())      
    localbuf[0] = listfile
    localbuf[1] = 0
    
    Context['SelfObj'].Status = 1
    
  Index = localbuf[1]
  if Index >= localbuf[0]._Number :
    return (0,0,None)
    
  Result = localbuf[0][Index]
  localbuf[1] = Index + 1
  return (4,0,FileNameClass(Result))

func = ListFileClass()
result = func(DiskPathClass('e:\\'))
print(result)

result = realm.RunProc(DiskPathClass('e:\\'),(0,FileNameClass),ListFileClass)
print(result)