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

import libstarpy

# Define data types
pydata.DefineType('UrlClass')
pydata.DefineType('HtmlClass')
pydata.DefineSubType(UrlClass,'ImageUrlClass')
pydata.DefineType('ImageClass')

# Define procedure types
@pyproc.DefineAsyncProc('DownloadHtmlProc',UrlClass,HtmlClass)
def Execute(self,url) :
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]
  
  try:    
    libstarpy._SRPUnLock()  # release cle lock, before enter wait
    import urllib2
    req = urllib2.Request(url.value())    
    fd = urllib2.urlopen(req)
    if fd.info()['Content-Type'] == 'text/html' :
      result = fd.read()
      fd.close()
      libstarpy._SRPLock()    # capture cle lock,
      print('download    ',url.value())
      return (0,1,HtmlClass(result))         
    else :
      fd.close()
      libstarpy._SRPLock()
      return (0,-1,None)
  except Exception as exc:
    libstarpy._SRPLock()    # capture cle lock,
    Context["Realm"].PrintException(str(exc))
    return (0,1,None)   

@pyproc.DefineProc('ParseImageUrlProc',HtmlClass,ImageUrlClass)
def Execute(self,page) :  
  Context = self.Context  #  first must save Context in local variable
  import re
  from urlparse import urljoin
  reg = r'src="(.+?\.png)"'
  reg_img = re.compile(reg)
  imglist = reg_img.findall(page.value())
  result = []
  url = page.GetSource()[0]
  for img in imglist:
    img_url = urljoin(url.value(),img)
    print(img_url)
    result.append(ImageUrlClass(img_url))
  return (0,1,tuple(result))


@pyproc.DefineAsyncProc('DownloadImageProc',ImageUrlClass,ImageClass)
def Execute(self,url) :
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]
  
  try:    
    libstarpy._SRPUnLock()  # release cle lock, before enter wait
    import urllib2
    req = urllib2.Request(url.value())    
    fd = urllib2.urlopen(req)
    if fd.info()['Content-Type'] == 'image/png' or fd.info()['Content-Type'] == 'image/jpeg' :
      result = fd.read()
      fd.close()
      libstarpy._SRPLock()    # capture cle lock,
      print('download    ',url.value())
      return (0,1,ImageClass(result))         
    else :
      fd.close()
      libstarpy._SRPLock()
      return (0,-1,None)
  except Exception as exc:
    libstarpy._SRPLock()    # capture cle lock,
    Context["Realm"].PrintException(str(exc))
    return (0,1,None)   