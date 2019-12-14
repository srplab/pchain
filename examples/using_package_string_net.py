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
realmstub = Service.PCRealmStubBase._New()
@realmstub._RegScriptProc_P('OnException')
def OnException(SelfObj,level,Info):
  if level == 0 or level == 6 :
    pass    
  else :
    print(Info)
realm.SetRealmStub(realmstub)

from pchain import loader

#load package first

proc_str = r'''{"PackageInfo":[{"PackageName":"grab_url_img_package","PackageVersion":"1.0.0","PackageUrl":"http://127.0.0.1/grab_url_img_package.1.0.0.zip"}],"ObjectList":[{"Type":"PCProcChain","PCProcBase":[{"ClassName":"grab_url_img_package.DownloadHtmlProc","ObjectID":"7de8b486-22aa-42c1-b3da-f2a899133d0c","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_package.UrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_package.HtmlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_package.ParseImageUrlProc","ObjectID":"12d8dbdb-fe9e-46b6-9080-3be1fa1bbf41","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_package.HtmlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_package.ImageUrlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_package.DownloadImageProc","ObjectID":"48bc33b7-d41e-45f9-93e5-7ac1edeccb24","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_package.ImageUrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_package.ImageClass"}],"Type":"PCProc"}]}]}'''
pkg = Service._ServiceGroup._NewParaPkg()
pkg._FromJSon(proc_str)
print(loader.loadobjectpackage(pkg))

print('load package   ',str(Service.grab_url_img_package))
print(Service.grab_url_img_package.DownloadHtmlProc)

#restore object
loadobjects = realm.LoadObject(pkg,False)

#call process
UrlClass = pydata.UnWrap(Service.UrlClass)
result = realm.RunProc(UrlClass('http://www.srplab.com/en/index.html'),None,loadobjects[0])
print(result)

pchain.cleterm() 