# -*- coding: utf-8 -*-
"""
    main.py

    :project : {name}
    :date    : {date}
"""

import sys
import os
import pchain

Service = pchain.cleinit()
import libstarpy

realm = Service.PCRealmBase()
realmstub = Service.PCRealmStubBase()
@realmstub._RegScriptProc_P('OnException')
def realmstub(SelfObj,AlarmLevel,Info) :
  if AlarmLevel == 1 :
    print(Info)  
realm.SetRealmStub(realmstub)  

# define pcdata management type
 
NumberClass = Service.PCDataBase.CreateType("NumberClass")
# data = NumberClass.Create(234.55)


# define pcproc management type
 
@Service.PCProcBase.Create(None,"NumberProc",(NumberClass),(NumberClass,NumberStepClass))
def NumberProc_Execute(SelfObj,Realm,Cell,Runner) :
  #get input
  in1 = SelfObj.InputToParaPkg()
  if in1[0] == None :
    return 2
  SelfObj.AcceptInput()  

  #   create output 
  SelfObj.AddOutputData(in1[0])
  return 0

# create cell, add proc or procchain
# cell = Service.PCCellBase()
# cell.AddProc(NumberProc)
# 
# add cell to realm  
# realm.AddCell(cell)

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
