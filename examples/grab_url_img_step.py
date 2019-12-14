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
from grab_url_img_module import ImageClass

realmstub = Service.PCRealmStubBase._New()
@realmstub._RegScriptProc_P('OnException')
def OnException(SelfObj,level,Info):
  if level == 0 or level == 6 :
    pass    
  else :
    print(Info)
realm.SetRealmStub(realmstub)    

@realm._RegScriptProc_P('OnCellToBeFinish')
def OnCellToBeFinish(Realm,cell):
  output = cell.GetCellMissingOutput()
  if output._Number == 0 :
    return False    
  input = cell.GetEnvDataQueue()
  
  print(Realm.QueryProcForInput(input[0]))
  print(Realm.QueryProcForOutput(output[0]))
  
  chain = Realm.BuildProcChain(output,input)
  if chain[0] == False :
    return False  # failed
  cell.AddProc(chain[1])
  return True
  
  

#--we insert proc in the callback
result = realm.RunProc(UrlClass('http://www.srplab.com/en/index.html'),(0,ImageClass))
print(result)

pchain.cleterm() 