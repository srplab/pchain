# python 2.7

import sys
import os
import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

#define data type
pydata.DefineType("StringClass",type(""))

pydata.DefineSubType(StringClass,"UrlClass",None)
pydata.DefineSubType(StringClass,"WebPageClass",None)

#define process type
# this proc will be blocked
@pyproc.DefineAsyncProc('DownLoadUrlProc',UrlClass,WebPageClass)
def Execute(self,url) :
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]
  
  import libstarpy
  try:    
    libstarpy._SRPUnLock()  # release cle lock, before enter wait
    import urllib2
    req = urllib2.Request(url.value())
    fd = urllib2.urlopen(req)
    result = fd.read()
    libstarpy._SRPLock()    # capture cle lock,
    return (0,1,WebPageClass(result))         
  except Exception as exc:
    libstarpy._SRPLock()    # capture cle lock,
    Context["Realm"].SetLog('download '+url.value()+'  failed')
    return (-1,1,None)   

# this proc will be blocked
@pyproc.DefineProc('StringToUrlProc',StringClass,UrlClass)
def Execute(self,in_str) :
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]
  
  if in_str.value().startswith('http://') or in_str.value().startswith('https://') :
    return (0,1,UrlClass(in_str.value()))
  else :
    return (0,-1,None)
