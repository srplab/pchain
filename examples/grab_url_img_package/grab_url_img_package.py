# -*- coding: utf-8 -*-
"""
    main.py

    :package : grab_url_img_package
    :date    : 2019-08-17 16:04:46
"""

import sys
import os
import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass
import libstarpy

SrvGroup = libstarpy._GetSrvGroup(0)
Service = SrvGroup._GetService("","")

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
    fd = None
    if pchain.ispython2 == True :
      import urllib2
      req = urllib2.Request(url.value())
      fd = urllib2.urlopen(req)
    else :
      import urllib.request
      fd = urllib.request.urlopen(url.value())
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
  if pchain.ispython2 == True:
    from urlparse import urljoin
    reg = r'src="(.+?\.png)"'
    reg_img = re.compile(reg)
    imglist = reg_img.findall(page.value())
  else :
    from urllib.parse import urljoin
    reg = r'src="(.+?\.png)"'
    reg_img = re.compile(reg)
    imglist = reg_img.findall(page.value().decode('utf-8'))
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
    fd = None
    if pchain.ispython2 == True :
      import urllib2
      req = urllib2.Request(url.value())
      fd = urllib2.urlopen(req)
    else :
      import urllib.request
      fd = urllib.request.urlopen(url.value())
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