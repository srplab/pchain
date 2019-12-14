<h1 align="center">PChain & Clips</h1>

Clips is a rule-based expert system. The project **[clipspy, python3](https://pypi.org/project/clipspy/)** provides a python interface that can be called via python. When the pchain is executed, the realm first generates a callback event OnBeforeExecute, which carries a new list of environment data. This event is used to generate the process of processing the data and add the process to the realm to process the data object. In this process, a rule-based approach can be employed. 

The data type, process type, process chain base class, pccell base class defined in pchain, can be used as classes in clips, and instances of corresponding classes are used as instances in clips.

The complete example is in the directory: [work_with_clipspy/simple.py](../work_with_clipspy/simple.py)

This example is relatively simple, just explaining the interaction between pchain and clips.

* Define two data types: string and number

```python
class StringClass(PCPyDataClass) :
  pass
pydata.Register(StringClass)  

class NumberClass(PCPyDataClass) :
  pass
pydata.Register(NumberClass) 
```

* Two procedures are defined: one is to calculate the length of the string, the other is to convert the string to an integer

```python
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
```

Define classes for clips corresponding to pchain types
------

According to the type in the pchain, the corresponding class is established in the clips. Each pchain type has a label that can be used as the name of the class in the clips, which is obtained by the GetTag function.

```python
import clips
env = clips.Environment()

# inject classes to clips
for item in Service.PCDataBase.CollectType() :
  class_string = '(defclass ' + item.GetTag() + ' (is-a USER) (slot Value) (slot Realm))'
  env.build(class_string)
  
for item in Service.PCProcBase.CollectType() :
  class_string = '(defclass ' + item.GetTag() + ' (is-a USER) (slot Value) (slot Realm))'
  env.build(class_string)
```

Only the name of the class is needed here. If you already know which classes are available, you need not use the function above to get the class name. You can create the class directly in the clips by using the class name.

Define rules & actions
------

This example is to enter two string data, if a string is length, use the LengthProc procedure to calculate the length of another string.

To achieve this, a rule is defined here, as follows:

```python
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
```

Currently, clippsy does not support python callback functions. Therefore, when the rule is triggered, Python is notified to perform the corresponding action by printing the string information.

In order to receive print information from clips, you need to create a router. After receiving the information, if it is the agreed information format, create a Cell and LengthProc instance, put the LengthProc instance into the Cell, put the environment data into the Cell, and finally submit the Cell to Realm, which is executed by Realm.

```python
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
```  

Handling the OnBeforeExecute callback function
------

In the callback function, an instance of the corresponding class is generated as a fact in clips according to the environment data of the realm.

Then execute the clips. If 'length' and other strings exist in the environment data, the rules of the clips are executed, creating a process for processing the data.

Each pchain object has an ID that can be used as the name of the corresponding clips's instance. The object's label can be used as the value of an instance. The object tag is obtained by GetTag and is a string. For complex objects, the string may be long.

```python
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
```      

**Output result:**

```python
realm.AddEnvData(StringClass('qqqwwweee'),StringClass('length'))
result = realm.ExecuteForResult()
print(result[0])

realm.AddEnvData(StringClass('qqqwwweeesdfasdfasdfasdf'),StringClass('length'))
result = realm.ExecuteForResult()
print(result[0])
```

```
9
24
```






