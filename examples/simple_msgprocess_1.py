# need register version of CLE
#  envmsg -> MsgPreProcess(innermsgset) -> Msg1Process(msg2) -> Msg2Process(outmsg) -> MsgOutputProcess
#
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

# This is an example, each data has a Time property
MsgObjectSpace = Service.PCDataBase.CreateType('MsgObjectSpace')
MsgObjectSpace.CreateProperty('LastTime',libstarpy.TYPE_INT64,0)

################################################################ define datatype EnvInMsg
class RawEnvInMsg :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineTypeEx(MsgObjectSpace,'EnvInMsg',RawEnvInMsg)

################################################################ define datatype InnerMsgSet
dataset = MsgObjectSpace.GetDataSetBase()
InnerMsgSet = dataset.CreateType('InnerMsgSet',None)

################################################################ define datatype InnerMsg2
class RawInnerMsg2 :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineTypeEx(MsgObjectSpace,'InnerMsg2',RawInnerMsg2)

################################################################ define datatype EnvOutMsg
class RawEnvOutMsg :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineTypeEx(MsgObjectSpace,'EnvOutMsg',RawEnvOutMsg)

################################################################ define datatype MsgContext
class RawMsgContext :
  def __init__(self, MsgId, MsgInfo):
    self.MsgId = MsgId
    self.MsgInfo = MsgInfo
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   
pydata.DefineTypeEx(MsgObjectSpace,'MsgContext',RawMsgContext)


################################################################ Define procedure type MsgPreProcess
@pyproc.DefineProc('MsgPreProcess',EnvInMsg,InnerMsgSet)
def Execute(self,EnvInMsg) :  
  Context = self.Context  #  first must save Context in local variable
  #--find the msg context, corresponding to input msg id
  realm = Context['Realm']
  id = EnvInMsg.value().MsgId
  msgcontext = realm.FindCache(id)
  if msgcontext == None :
    # create msg context
    msgcontext = MsgContext(RawMsgContext(id,'msg context'))
    realm.SetCache(id,msgcontext)
    print('create msgcontext for :  ',id)
  else :
    print('find msgcontext for :  ',id)
  msgset = InnerMsgSet.Create(msgcontext,EnvInMsg)  
  return (0,1,msgset)
  
################################################################ Define procedure type Msg1Process
@pyproc.DefineProc('Msg1Process',InnerMsgSet,InnerMsg2)
def Execute(self,set1) :  
  Context = self.Context  #  first must save Context in local variable
  #--find the msg context, corresponding to input msg id
  datalist = set1.GetData()
  msgcontext = pydata.UnWrap(datalist[0])
  msg1 = pydata.UnWrap(datalist[1])
  return (0,1,InnerMsg2(RawInnerMsg2(msgcontext.value().MsgId,msg1.value().MsgInfo + '  ' + msgcontext.value().MsgInfo)))  
  
################################################################ Define procedure type Msg2Process
@pyproc.DefineProc('Msg2Process',InnerMsg2,EnvOutMsg)
def Execute(self,msg2) :  
  Context = self.Context  #  first must save Context in local variable
  #--find the msg context, corresponding to input msg id
  return (0,1,EnvOutMsg(RawEnvOutMsg(msg2.value().MsgId,'output  :  '+msg2.value().MsgInfo)))    
  
################################################################ Define procedure type MsgOutputProcess
@pyproc.DefineProc('MsgOutputProcess',EnvOutMsg,None)
def Execute(self,outmsg) :  
  Context = self.Context  #  first must save Context in local variable
  print(outmsg.value().MsgInfo)
  return (0,1,None)  

################################################################ Create Cell, add Proc
cell = Service.PCCellBase._New()
cell.AddProc(MsgPreProcess,Msg1Process,Msg2Process,MsgOutputProcess)
realm.AddCell(cell)

#create a msg, add it to realm
msg1 = EnvInMsg(RawEnvInMsg(1,'wwwwwww'))
msg1.Wrap().LastTime = Service._ServiceGroup._TickCount()
realm.AddEnvData(msg1)
realm.Execute()

msg2 = EnvInMsg(RawEnvInMsg(1,'tttttttttttttt'))
msg2.Wrap().LastTime = Service._ServiceGroup._TickCount()
realm.AddEnvData(msg2)
realm.Execute()

#--Build and using ProcChain
chain = realm.BuildProcChain(MsgOutputProcess,EnvInMsg)
newrealm = realm._New()
newrealm.AddProc(chain[1])
newrealm.AddProc(chain[1])
msg1 = EnvInMsg(RawEnvInMsg(1,'wwwwwww'))
msg1.Wrap().LastTime = Service._ServiceGroup._TickCount()
newrealm.AddEnvData(msg1)
newrealm.Execute()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
print('the app will insert node to neo4j, run carefully')
from py2neo import Graph,Node,Relationship
from py2neo import NodeMatcher
from py2neo import RelationshipMatcher

graph = Graph('http://localhost:7474',username='neo4j',password='970511')
matcher = NodeMatcher(graph)
rel_matcher = RelationshipMatcher(graph)
#graph.delete_all()

def insert_to_neo4j(t) :
  #--find node by name, and label
  c_type = t.GetTagLabel()
  c_tag = t.GetTag()
  node = matcher.match(c_type, name=c_tag).first()
  if node == None :
    print('insert node  ',c_type,'   :  ',c_tag)
    node = Node(c_type,name=c_tag)
    graph.create(node)
  #--t's class type exist?
  item_type = t.GetType()
  t_tag_label = item_type.GetTagLabel()
  t_tag = item_type.GetTag()
  c_node = matcher.match(t_tag_label, name=t_tag).first()
  if c_node == None :
    print('insert type  ',t_tag_label,'   :  ',t_tag)
    c_node = Node(t_tag_label,name=t_tag)
    graph.create(c_node)
  #--
  if c_node == node :
    pass
  else :
    is_inst = rel_matcher.match((c_node,node), r_type="istype").first()
    if is_inst == None :
      is_inst = Relationship(c_node,'istype',node)
      graph.create(is_inst)  
      
  #--create relations using source
  srcs = realm.GetSourceObject(t)      
  for src in srcs :
    src_type = src.GetTagLabel()
    src_tag = src.GetTag()
    src_node = matcher.match(src_type, name=src_tag).first()    
    if src_node == None :
      insert_to_neo4j(src)
      src_type = src.GetTagLabel()
      src_tag = src.GetTag()
      src_node = matcher.match(src_type, name=src_tag).first()      
          
    r_type_name = 'sourcedata'
    if realm.IsProc(src) == True :
      r_type_name = 'output'
      
    is_source = rel_matcher.match((src_node,node), r_type=r_type_name).first()
    if is_source == None :
      is_source = Relationship(src_node,r_type_name,node)
      graph.create(is_source)   
      
activeset = realm.GetActiveObject(None,1.0,0)
for t in activeset :
  insert_to_neo4j(t)  
  
'''  
  
# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 