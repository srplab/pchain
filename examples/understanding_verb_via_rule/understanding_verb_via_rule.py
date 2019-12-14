# python 2.7

import sys
import os
try:
  import pchain
except Exception as exc:
  pchain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../')
  sys.path.insert(0,pchain_path)
  import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

Service = pchain.cleinit()
import libstarpy

import data_and_proc_type
from data_and_proc_type import StringClass

realm = Service.PCRealmBase._New()

# StringClass('download').GetTag()
rule = {'15e332107cd7a498553ab22a5ce04a2741fe0092':'DownLoadUrlProc'}

# Create an execution unit, according to the rules, obtain the process corresponding to the input, add it to the execution unit, and add other inputs as data to the execution unit.

@realm._RegScriptProc_P('OnBeforeExecute')
def realm_OnBeforeExecute(CleObj):
  envdata = CleObj.GetEnvDataQueue()  
  if envdata._Number == 0 : 
    return
  #--create a scheduler
  global rule
  Cell = Service.PCCellBase._New()
  for item in envdata : 
    tag = item.GetTag()    
    if (pchain.ispython2 == True and rule.has_key(tag) == False) or (pchain.ispython2 == False and (tag not in rule)):
      # is data
      Cell.AddEnvData(CleObj,item)
    else :
      proctype = rule[tag]
      proc = Service._GetObject(proctype)
      Cell.AddProc(proc)
  CleObj.AddCell(Cell)
  CleObj.RemoveEnvData(envdata);
  return  

# Remove execution unit when execution is complete
@realm._RegScriptProc_P('OnCellFinish')
def realm_OnCellFinish(CleObj,cell,IsSuccess):
  CleObj.RemoveCell(cell)

@realm._RegScriptProc_P('OnCellToBeFinish')
def OnCellToBeFinish(Realm,cell):
  procs = cell.GetMissingEnvDataProc()
  if procs._Number == 0 :
    envdata = cell.GetEnvDataUnHandled(None,0)
    # there is data not being processed, find a proc and add
    for item in envdata :
      tag = item.GetTag()    
      if (pchain.ispython2 == True and rule.has_key(tag) == False) or (pchain.ispython2 == False and (tag not in rule)):
        pass
      else :
        proctype = rule[tag]
        proc = Service._GetObject(proctype)
        cell.AddProc(proc) 
        return True  #--continue process     
    return False  # no procs waiting input
  else :
    envdata = cell.GetEnvDataQueue() 
    for item in procs :
      if cell.IsProcExecuted(item) == False :
        #the item is not execued, missing input
        for index in range(0,item.GetInputNumber()) :
          if item.IsFromInternal(index) == False and item.IsEnough(index) == False and item.IsMustExist(index) == True :
            chain = Realm.BuildProcChain(item.GetInputType(index),envdata)
            if chain[0] == False :  #--can not create input
              Realm.SetLog('proc  ['+str(item)+'] can not be execued due to no input')
              return False  # failed  
            if cell.FindProc(chain[1]) == None :
              cell.AddProc(chain[1])
              return True
            else :
              Realm.SetLog('proc  ['+str(item)+'] can not be execued due to no input')
              return False       
    return False     

#method 1  
realm.AddEnvData(StringClass('download'),StringClass('http://www.srplab.com'),StringClass('noise data'))
result = realm.ExecuteForResult()
print('download http://www.srplab.com ',str(result))

realm.AddEnvData(StringClass('download'),StringClass('noise data'))
result = realm.ExecuteForResult()
print(realm.GetLog())

#method 2
result = realm.RunProc((StringClass('http://www.srplab.com'),StringClass('noise data')),None,Service.DownLoadUrlProc) # StringClass('download'))
print(result)

result = realm.RunProc((StringClass('download'),StringClass('http://www.srplab.com')),None)
print(result)

print('------------------------------------------------')
print(realm.GetActiveObject(None,1.0,0))

# finish
pchain.cleterm() 