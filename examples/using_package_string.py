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

from pchain import loader
grab_url_img_package = loader.loadfolder("grab_url_img_package")

proc_str = r'''{"PackageInfo":[{"PackageName":"grab_url_img_package","PackageVersion":"1.0.0","PackageUrl":"https://xxxx"}],"ObjectList":[{"Type":"PCProcChain","PCProcBase":[{"ClassName":"grab_url_img_package.DownloadHtmlProc","ObjectID":"7de8b486-22aa-42c1-b3da-f2a899133d0c","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_package.UrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_package.HtmlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_package.ParseImageUrlProc","ObjectID":"12d8dbdb-fe9e-46b6-9080-3be1fa1bbf41","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_package.HtmlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_package.ImageUrlClass"}],"Type":"PCProc"},{"ClassName":"grab_url_img_package.DownloadImageProc","ObjectID":"48bc33b7-d41e-45f9-93e5-7ac1edeccb24","InputQueue":[{"RequestNumber":1,"DataBaseName":"grab_url_img_package.ImageUrlClass"}],"OutputQueue":[{"DataBaseName":"grab_url_img_package.ImageClass"}],"Type":"PCProc"}]}]}'''
pkg = Service._ServiceGroup._NewParaPkg()
pkg._FromJSon(proc_str)
loadobjects = realm.LoadObject(pkg,False)
print(loadobjects[0].GetTag())
print(loadobjects[0].GetTagLabel())

UrlClass = pydata.UnWrap(grab_url_img_package.UrlClass)
result = realm.RunString(UrlClass('http://www.srplab.com/en/index.html'),None,proc_str)
print(result)

pchain.cleterm() 