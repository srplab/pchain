# -*- coding: utf-8 -*-
"""
    main.py

    :project : testsum
    :date    : 2019-02-25 09:49:21
"""

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

#define number
class NumberClass(PCPyDataClass) :
  @staticmethod
  def Load(MetaData) :
    #print('load................',MetaData)
    #raise Exception('Load function is not defined ')
    aa = NumberClass(float(MetaData))
    return aa
  def Save(self) :
    #raise Exception('Save function is not defined for '+str(self))    
    return str(self.num)
pydata.Register(NumberClass)  

class StringClass(PCPyDataClass) :
  pass
pydata.Register(StringClass) 


#define proc
class NumberToStringProc(PCPyProcClass) :
  def Execute(self,num) :
    return (0,1,StringClass(str(num.value())))
pyproc.Register(NumberToStringProc,(NumberClass),(StringClass))

class StringToNumberProc(PCPyProcClass) :
  def Execute(self,strv) :
    return (0,1,NumberClass(float(strv.value())))
pyproc.Register(StringToNumberProc,(StringClass),(NumberClass))

class StringToNumberProc1(PCPyProcClass) :
  def Execute(self,strv) :
    return (0,1,NumberClass(float(strv.value())))
pyproc.Register(StringToNumberProc1,(StringClass),(NumberClass))


print('build procchain...')
result = realm.BuildProcChain(NumberClass,NumberClass)
print(result)
print(result[1].ToParaPkg())
print('build procchain...end')

print('build procchain...')
result = realm.BuildProcChain(NumberClass,NumberClass)
print(result)
print(result[1].ToParaPkg())
print('build procchain...end')

print('assign output type....')
run_result = realm.RunProc(NumberClass(4.3),NumberClass,result[1])
print(run_result[0])

#define OnProcPriority callback
stub = Service.PCRealmStubBase()
@stub._RegScriptProc_P("OnProcPriority")
def OnProcPriority(CleObj,ProcessSet, OutputPriority) :
  print(ProcessSet)
  OutputPriority._Clear()
  for i in range(ProcessSet._Number) :
    OutputPriority[i] = i * 4 + 1.0
realm.SetRealmStub(stub)     

result = realm.BuildProcChain(NumberClass,NumberClass)
print(result[1].ToParaPkg())