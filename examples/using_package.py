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

realmstub = Service.PCRealmStubBase._New()
@realmstub._RegScriptProc_P('OnException')
def OnException(SelfObj,level,Info):
  if level == 0 or level == 6 :
    pass    
  else :
    print(Info)
realm.SetRealmStub(realmstub)


procs = realm.BuildProcChain(grab_url_img_package.ImageClass,grab_url_img_package.UrlClass)
parapkg = Service._ServiceGroup._NewParaPkg()
realm.SaveObject(parapkg,procs[1])

proc_str = parapkg._ToJSon()
print(proc_str)

print(procs[1].GetTag())
print(procs[1].GetTagLabel())

UrlClass = pydata.UnWrap(grab_url_img_package.UrlClass)
result = realm.RunString(UrlClass('http://www.srplab.com/en/index.html'),None,proc_str)
print(result)

print(realmstub.GetPerformanceData(False))
print(realm.FindSystemPackage(UrlClass))
print(realmstub.FindSystemPackage(UrlClass))

pchain.cleterm() 