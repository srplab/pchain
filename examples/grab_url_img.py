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

from grab_url_img_module import UrlClass
from grab_url_img_module import HtmlClass
from grab_url_img_module import ImageUrlClass
from grab_url_img_module import ImageClass
from grab_url_img_module import DownloadHtmlProc
from grab_url_img_module import ParseImageUrlProc
from grab_url_img_module import DownloadImageProc

realmstub = Service.PCRealmStubBase._New()
@realmstub._RegScriptProc_P('OnException')
def OnException(SelfObj,level,Info):
  if level == 0 or level == 6 :
    pass    
  else :
    print(Info)
realm.SetRealmStub(realmstub)

'''
#--first method
procs = realm.BuildProcChain(ImageClass,UrlClass)
result = realm.RunProc(UrlClass('http://www.srplab.com/en/index.html'),(0,ImageClass),procs[1])
print(result)
'''

#--second method
result = realm.RunProc(UrlClass('http://www.srplab.com/en/index.html'),(0,ImageClass),DownloadHtmlProc,ParseImageUrlProc,DownloadImageProc)
print(result)

'''
#--third method
procs = realm.BuildProcChain(ImageClass,UrlClass)
parapkg = Service._ServiceGroup._NewParaPkg()
realm.SaveObject(parapkg,procs[1])

proc_str = parapkg._ToJSon()

result = realm.RunString(UrlClass('http://www.srplab.com/en/index.html'),None,proc_str)
print(result)
'''

print(realmstub.GetPerformanceData(False))

pchain.cleterm() 