# -*- coding: utf-8 -*-
"""
    main.py

    :project : {name}
    :date    : {date}
"""

import sys
import os
import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

Service = pchain.cleinit()
import libstarpy

realm = Service.PCRealmBase()

# define pcdata management type
pydata.DefineType('NumberClass')

# define pcproc management type
@pyproc.DefineProc('NumberProc',(NumberClass),None)
def Execute(self,num) :
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return (0,0,None)    
  print(num.value())
  return (0,1,None)
         
# create cell, add proc or procchain
# cell = Service.PCCellBase()
# cell.AddProc(NumberProc.GetType())
# 
# add cell to realm  
# realm.AddCell(cell)

# handle realm's callback
realmstub = Service.PCRealmStubBase()
@realmstub._RegScriptProc_P('OnException')
def realmstub(SelfObj,AlarmLevel,Info) :
  if AlarmLevel == 1 :
    print(Info)  
realm.SetRealmStub(realmstub)  


# handle realm's callback
@realm._RegScriptProc_P('OnBeforeExecute')
def realm_OnBeforeExecute(CleObj):
  return
  
@realm._RegScriptProc_P('OnCellToBeFinish')
def realm_OnCellToBeFinish(CleObj,cell):
  return False
   
@realm._RegScriptProc_P('OnCellFinish')
def realm_OnCellFinish(CleObj,cell,IsSuccess):
  return
   
@realm._RegScriptProc_P('OnAfterExecute')
def realm_OnAfterExecute(CleObj):
  return False

realm.Execute()

# from pchain import debug
# debug.start()

# enter loop
pchain.cleloop()

# finish
pchain.cleterm() 
