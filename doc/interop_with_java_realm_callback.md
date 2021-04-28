<h1 align="center">Handling callback with java language</h1>

This example creates a new Realm instance that defines the instance's callback functions OnBeforeExecute and OnCellFinish.

The complete example is in the directory: [examples/simple_java_realm_callback](../examples/simple_java_realm_callback.py)

The code and description are as follows

Define the data types in python language
===

```python
pydata.DefineType('StringClass')
pydata.DefineType('NumberClass')
```

Define the process LengthProc and ToIntProc in python
===

```python
@pyproc.DefineProc('LengthProc',StringClass,NumberClass)
def Execute(self,strobj) :
  Context = self.Context
  val = len(strobj.value())
  return (0,1,NumberClass(val))

@pyproc.DefineProc('ToIntProc',StringClass,NumberClass)
def Execute(self,strobj) :
  Context = self.Context
  val = 0
  try:
    val = int(strobj.value())
    return (0,1,NumberClass(val))
  except :
    return (0,-1,None)
```

Create an instance of realm using java
===

Create a base code with the starmodule tool and modify the code.

The command line is as follows:

```sh
starmodule JavaRealmCallback.JavaRealmClass --java
```

* Create an instance of PCRealmBase with the name changed to JavaRealmClass

```java
final StarObjectClass PCRealmBase = Service._GetObject("PCRealmBase");
final StarObjectClass JavaRealmClass_Obj=PCRealmBase._New("JavaRealmClass");
```

* Define callback function "OnBeforeExecute"

```java
JavaRealmClass_Obj._RegScriptProc_P("OnBeforeExecute", new StarObjectScriptProcInterface() {
    public Object Invoke(Object CleObject, Object[] EventParas)
    {
    	  StarObjectClass PCRealm = (StarObjectClass)CleObject;
          StarObjectClass PCRealm = (StarObjectClass)CleObject;
          StarParaPkgClass EnvData = (StarParaPkgClass)PCRealm._Call("GetEnvData");
            	  
    	  StarObjectClass StringClass = (StarObjectClass)Service._GetObject("StringClass");
    	  StarObjectClass PCCellBase = (StarObjectClass)Service._GetObject("PCCellBase");
    	  StarObjectClass LengthProc = (StarObjectClass)Service._GetObject("LengthProc");
    	  for (Iterator iter = EnvData._Iterator(); iter.hasNext();) { 
    	  	  Object data = iter.next();
    	  	  if( StringClass._IsInst((StarObjectClass)data) == true ){
              	  StarObjectClass newcell = PCCellBase._New();
                  newcell._Call("AddEnvData",PCRealm,data); 
                  newcell._Call("AddProc",LengthProc);
                  PCRealm._Call("AddCell",newcell);
              }
    	  }
          return null;
    }
});
```

* Define callback function "OnCellFinish"

```java
JavaRealmClass_Obj._RegScriptProc_P("OnCellFinish", new StarObjectScriptProcInterface() {
    public Object Invoke(Object CleObject, Object[] EventParas)
    {
    	  StarObjectClass PCRealm = (StarObjectClass)CleObject;
    	  StarObjectClass PCCell = (StarObjectClass)EventParas[0];
    	  boolean IsSuccess = (boolean)EventParas[1];
            	  
    	  PCRealm._Call("ProcessCellEnvData",PCCell,IsSuccess);
    	  PCRealm._Call("RemoveCell",PCCell);
    	  return null;
    }
});
```

Create an instance of JavaRealmClass using python, add data, execute
===

* Load java module

```python
Service._DoFile('java','./java_realm_callback/JavaRealmCallback.class','')
```

* Create an instance of JavaRealmClass

```python
realm = Service.JavaRealmClass._New()
```

* Add data object

```python
realm.AddEnvData(StringClass('qqqwwweee'),StringClass('qqqwwweee888888888888888888'),StringClass('length'))
```

* Execute

```python
result = realm.ExecuteForResult()
print(str(result[0]),str(result[1]))
```

*Output result:

the output is the length of two strings

```
('9', '27')
```






