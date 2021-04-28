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

result = realm.LoadObjectString(r'''{"PackageInfo":[],"ObjectList":[{"Type":"PCProcChain","PCProcBase":[{"ClassName":"grab_url_img_module.DownloadHtmlProc","ObjectID":"219f2b01-2aa3-469b-84e3-0edf538632e9","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_module.UrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_module.HtmlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_module.ParseImageUrlProc","ObjectID":"05357823-edc5-48ba-9aa7-5b1080911752","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_module.HtmlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_module.ImageUrlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_module.DownloadImageProc","ObjectID":"408c6658-13f3-42fb-bc1d-ade88914234b","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_module.ImageUrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_module.ImageClass"}],"Type":"PCProc"}]}]}''', False)
print(result[0].ToParaPkg())

result = realm.RunString(UrlClass('http://www.srplab.com/en/index.html'),None,r'''{"PackageInfo":[],"ObjectList":[{"Type":"PCProcChain","PCProcBase":[{"ClassName":"grab_url_img_module.DownloadHtmlProc","ObjectID":"219f2b01-2aa3-469b-84e3-0edf538632e9","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_module.UrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_module.HtmlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_module.ParseImageUrlProc","ObjectID":"05357823-edc5-48ba-9aa7-5b1080911752","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_module.HtmlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_module.ImageUrlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_module.DownloadImageProc","ObjectID":"408c6658-13f3-42fb-bc1d-ade88914234b","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_module.ImageUrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_module.ImageClass"}],"Type":"PCProc"}]}]}''')
print(result)


pchain.cleterm() 