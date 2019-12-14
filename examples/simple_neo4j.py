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
pydata.DefineType('NumberClass')

# Define procedure types
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  return (4,1,NumberClass(val))

# Define procedure types
@pyproc.DefineProc('OutputProc',(NumberClass,NumberClass),None)
def Execute(self,num1,num2) :  
  Context = self.Context  #  first must save Context in local variable
  print('sum = ', num1.value() + num2.value())
  Context['Cell'].Finish()
  return (0,1,None)
    
cell = Service.PCCellBase._New()
cell.AddProc(InputProc,OutputProc)

realm.AddCell(cell)
realm.Execute()

activeset = realm.GetActiveObject(None,1.0,0)
activesetTag = realm.GetTagEx(activeset)
print(activesetTag)

#--we add it to neo4j
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
    insert_to_neo4j(src)

    src_type = src.GetTagLabel()
    src_tag = src.GetTag()
    src_node = matcher.match(src_type, name=src_tag).first()    
    if src_node == None :
      pass
    else : 
      is_source = rel_matcher.match((src_node,node), r_type="issource").first()
      if is_source == None :
        is_source = Relationship(src_node,'issource',node)
        graph.create(is_source)      

for t in activeset :
  insert_to_neo4j(t)    


# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 