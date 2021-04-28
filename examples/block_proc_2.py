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

realmstub = Service.PCRealmStubBase._New()
@realmstub._RegScriptProc_P('OnLongSuspend')
def OnLongSuspend(SelfObj,Realm,PCCell, PCProc, SuspendTick):
  print(PCProc,'   is suspend ',SuspendTick)
  return True
realm.SetRealmStub(realmstub)

# this proc will be blocked
@pyproc.DefineAsyncProc('Parent_DownLoadUrlProc',UrlClass,WebPageClass)
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
    
#create sub proc type
ProcInst = Parent_DownLoadUrlProc()
result = realm.RunProc(UrlClass('http://www.srplab.com'),None,ProcInst)
print(result)

# enter loop
pchain.cleloop()
# finish
pchain.cleterm() 