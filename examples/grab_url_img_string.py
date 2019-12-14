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

import grab_url_img_module
from grab_url_img_module import UrlClass

realmstub = Service.PCRealmStubBase._New()
@realmstub._RegScriptProc_P('OnException')
def OnException(SelfObj,level,Info):
  if level == 0 or level == 6 :
    pass    
  else :
    print(Info)
realm.SetRealmStub(realmstub)

result = realm.RunString(UrlClass('http://www.srplab.com/en/index.html'),None,r'''{"PackageInfo":[],"ObjectList":[{"Type":"PCProcChain","PCProcBase":[{"ClassName":"DownloadHtmlProc","ObjectID":"699b4409-cb56-4237-b360-5bec0cd81a6c","InputQueue":[{"RequestNumber":1,"DataBaseName":"UrlClass"}],"OutputQueue":[{"DataBaseName":"HtmlClass"}],"Type":"PCProc"},{"ClassName":"ParseImageUrlProc","ObjectID":"749696b3-8153-4b1a-be54-bc9e41cc7928","InputQueue":[{"RequestNumber":1,"DataBaseName":"HtmlClass"}],"OutputQueue":[{"DataBaseName":"ImageUrlClass"}],"Type":"PCProc"},{"ClassName":"DownloadImageProc","ObjectID":"bfaac82f-5da6-4931-9c5a-de6c951dbb98","InputQueue":[{"RequestNumber":1,"DataBaseName":"ImageUrlClass"}],"OutputQueue":[{"DataBaseName":"ImageClass"}],"Type":"PCProc"}]}]}''')
print(result)


pchain.cleterm() 