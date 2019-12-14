#install clipspy with python 36 64bits

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

# Define data types
class StringClass(PCPyDataClass) :
  pass
pydata.Register(StringClass)  

class NumberClass(PCPyDataClass) :
  pass
pydata.Register(NumberClass) 

class LengthProc(PCPyProcClass) :
  def Execute(self,strobj) :
    Context = self.Context
    val = len(strobj.value())
    return (0,1,NumberClass(val))
pyproc.Register(LengthProc,StringClass,NumberClass)

class ToIntProc(PCPyProcClass) :
  def Execute(self,strobj) :
    Context = self.Context
    val = 0
    try:
      val = int(strobj.value())
      return (0,1,NumberClass(val))
    except :
      return (0,-1,None)
pyproc.Register(ToIntProc,StringClass,NumberClass)

#----------------------------------------------------------
# init clips

import clips
env = clips.Environment()

# inject classes to clips
for item in Service.PCDataBase.CollectType() :
  class_string = '(defclass ' + item.GetTag() + ' (is-a USER) (slot Value) (slot Realm))'
  env.build(class_string)
  
for item in Service.PCProcBase.CollectType() :
  class_string = '(defclass ' + item.GetTag() + ' (is-a USER) (slot Value) (slot Realm))'
  env.build(class_string)

# create router to capture output from clips
class MyLoggingRouter(clips.Router):
  def query(self, _name):
    if _name == "stdout" :
      return True
    else :
      return False
    
  def print(self, name, message):
    if len(message) == 0 :
      pass
    else :  
      # print(message)    
      lists = message.split()
      if len(lists) == 0 :
        return
      if lists[0] == 'createproc' :
        l_realm = Service._GetObjectEx(lists[1])
        l_proc = Service._GetObject(lists[2])
        l_data = Service._GetObjectEx(lists[3])
        
        newcell = Service.PCCellBase._New()
        newcell.AddEnvData(l_realm,l_data) 
        l_realm.RemoveEnvData(l_data) 
        newcell.AddProc(l_proc._New())   
        l_realm.AddCell(newcell)
                
rou = MyLoggingRouter('myrouter',0)
rou.add_to_environment(env)
rou.activate()
 
# define rule
rule = str.format("""
(defrule my-rule
  ?f1 <- (object (is-a {0}) (name ?name1) (Realm ?realm1) (Value ?x1 & ~"{1}"))
  ?f2 <- (object (is-a {0}) (name ?name2) (Realm ?realm2) (Value ?x2 & "{1}"))
  =>
  (unmake-instance ?f1) 
  (format t "createproc %s LengthProc %s" ?realm1 ?name1)
 )
""",StringClass.GetType().GetTag(),StringClass('length').GetTag())
env.build(rule)  

#define callback of realm
@realm._RegScriptProc_P('OnBeforeExecute')
def realm_OnBeforeExecute(CleObj):
  env.reset()
  NewEnvData = CleObj.GetEnvDataQueue()
  # inject envdata to clips
  for item in NewEnvData :
    datatype = item.GetType()
    cls = None
    try :
      cls = env.find_class(datatype.GetTag())
    except Exception :
      class_string = '(defclass ' + datatype.GetTag() + ' (is-a USER) (slot Value) (slot Realm))'
      env.build(class_string)
      cls = env.find_class(datatype.GetTag())
    inst = cls.new_instance(item._ID)
    inst['Value'] = item.GetTag()
    inst['Realm'] = CleObj._ID
  env.run()
  return  

@realm._RegScriptProc_P('OnCellFinish')
def realm_OnCellFinish(CleObj,cell,IsSuccess):
  CleObj.ProcessCellEnvData(cell,IsSuccess);
  CleObj.RemoveCell(cell)
  
realm.AddEnvData(StringClass('qqqwwweee'),StringClass('qqqwwweee888888888888888888'),StringClass('length'))
result = realm.ExecuteForResult()
print(str(result[0]),str(result[1]))

realm.AddEnvData(StringClass('qqqwwweeesdfasdfasdfasdf'),StringClass('length'))
result = realm.ExecuteForResult()
print(result[0])

pchain.cleterm() 