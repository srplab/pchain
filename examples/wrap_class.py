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

#==
class Study:
  def __init__(self,name=None):
    self.name = name
  def say(self):
    print(self.name)
'''    
study = Study("xxxxxx")
study.say()
'''

# Define data types
pydata.DefineType('StringClass',type(''))
pydata.DefineType('StudyClass',Study)


@pyproc.DefineProc('Create_Study_Proc',StringClass,StudyClass)
def Execute(self,val) :  
  Context = self.Context  #  first must save Context in local variable
  return (0,1,StudyClass(Study(val.value())))

@pyproc.DefineProc('Study_Say_Proc',StudyClass,None)
def Execute(self,item) :  
  Context = self.Context  #  first must save Context in local variable
  item.value().say()
  return (0,1,None)

a = Create_Study_Proc.call(StringClass('xxxxxxxxx'))
Study_Say_Proc.call(a)

# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 