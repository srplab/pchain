# python 2.7

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

pydata.DefineType("UrlClass")
pydata.DefineType("WebPageClass")

# this proc will be blocked
@pyproc.DefineAsyncProc('DownLoadUrlProc',UrlClass,WebPageClass)
def Execute(self,url) :
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]

  try:    
    libstarpy._SRPUnLock()  # release cle lock, before enter wait
    result = None
    if pchain.ispython2 == True :
      import urllib2
      req = urllib2.Request(url.value())
      fd = urllib2.urlopen(req)
      result = fd.read()
    else :
      import urllib.request
      fd = urllib.request.urlopen(url.value())
      result = fd.read()
    libstarpy._SRPLock()    # capture cle lock,
    return (0,1,WebPageClass(result))         
  except Exception as exc:
    libstarpy._SRPLock()    # capture cle lock,
    return (0,1,None)   
    
@pyproc.DefineProc('PrintTimerProc',None,None)
def Execute(self) :    
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]
  
  if Context["Cell"].NumberOfRunner(SelfObj,False) == 0 :
    return (0,0,None);
  print(Service._ServiceGroup._TickCountUs())
  return (SelfObj.Continue(10),0,None)

realmStub = Service.PCRealmStubBase._New()
@realmStub._RegScriptProc_P('OnLongLoop')
def OnLongLoop(cleobj,realm,PCCell,PCProc,LoopCount) :
  if PCProc.GetType() == PrintTimerProc.GetType() :
    print('###################',LoopCount)
    return True
  return False
realm.SetRealmStub(realmStub)

Result = realm.RunProc(UrlClass('http://www.srplab.com'),None,DownLoadUrlProc,PrintTimerProc)
print(Result)

# enter loop
pchain.cleloop()
# finish
pchain.cleterm() 