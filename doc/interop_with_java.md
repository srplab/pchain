<h1 align="center">Interoperate with java language</h1>

This example defines a data class NumberClass, an input procedure InputProc, and a process for calculating the sum of two numbers. Among them NumberClass and InputProc use python language. The process of calculating the sum of two numbers is implemented in java language.

The complete example is in the directory: [examples/simple_java_process](../examples/simple_java_process.py)

The code and description are as follows

Define the data type NumberClass in python language
===

```python
pydata.DefineType('NumberBaseClass')
class NumberClass(NumberBaseClass) :
  @staticmethod
  def Load(MetaData) :
    # MetaData maybe string or parapkg
    # raise Exception('Load function is not defined ')
    if type(MetaData) == type('') :
      return NumberClass(float(MetaData))
    else :
      return NumberClass(MetaData[0])
  def ToParaPkg(self,parapkg) :
    parapkg[0] = self.value()
    return True
  def Save(self) :
    return str(self.value())      
pydata.Register(NumberClass)  
```

Define the process InputProc in python
===

```python
@pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  val = input('input a number : ')
  if pchain.ispython2 == True :
    return (4,1,NumberClass(val))
  else :
    return (4,1,NumberClass(float(val)))
```

Define the process CAddProcClass in java language
===

Create a base code with the starmodule tool and modify the code.

The command line is as follows:

```sh
starmodule CProcModule.CAddProcClass --java
```

* Create an instance of PCProcBase with the name changed to CAddProcClass

```java
StarObjectClass PCProcBase = Service._GetObject("PCProcBase");
StarObjectClass NumberClass = Service._GetObject("NumberClass");
StarObjectClass CAddProcClass_Obj=PCProcBase._New("CAddProcClass");
```

* Define the input and output of CAddProcClass

```java
if( CAddProcClass_Obj._Callbool("InputFrom",NumberClass,NumberClass) == false )
    throw new Exception("failed");
if( CAddProcClass_Obj._Callbool("OutputFrom",NumberClass) == false )
    throw new Exception("failed");
```

* Write the Execute function of CAddProcClass

```c
CAddProcClass_Obj._RegScriptProc_P("Execute", new StarObjectScriptProcInterface() {
    public Object Invoke(Object In_CleObject, Object[] EventParas)
    {
    	  StarObjectClass CleObject = (StarObjectClass)In_CleObject;
      	  StarObjectClass RealmObject = (StarObjectClass)EventParas[0];
    	  StarObjectClass CellObject = (StarObjectClass)EventParas[1];

          ...
    }
});
```

>  * Get two input data objects, return 2 if not present, wait for more data

```java
/*--get input*/
StarParaPkgClass InputPara = (StarParaPkgClass)CleObject._Call("InputToParaPkg");
if( InputPara == null )
    return -1;
StarObjectClass InputData1 = (StarObjectClass)InputPara._Get(0);
StarObjectClass InputData2 = (StarObjectClass)InputPara._Get(1);
if( InputData1 == null || InputData2 == null )
    return 2;
```

> * Since the data object is defined by python, you need to call the GetDataBuf function, which converts the data into a type of parapkg acceptable to other languages.

```java
StarParaPkgClass InputData1_ParaPkg = (StarParaPkgClass)InputData1._Call("GetDataBuf");
StarParaPkgClass InputData2_ParaPkg = (StarParaPkgClass)InputData2._Call("GetDataBuf");
            	  
double Result = InputData1_ParaPkg._Getdouble(0) + InputData2_ParaPkg._Getdouble(0);
```

> * The type of the output object is defined by python, you need to create its instance through the Create function.

```java
StarObjectClass NumberClass = (StarObjectClass)Service._GetObject("NumberClass");
StarObjectClass OutputData = (StarObjectClass)NumberClass._Call("Create",Result);
            	  
if( OutputData != null )
    CleObject._Call("AddOutputData",OutputData);
```

> * Finally, accept the input data, set the Cell execution completion flag, and return

```java
CleObject._Call("AcceptInput");
CellObject._Call("Finish");
return 0;
```        

Add the process to the realm to execute
===

```python
# load c module
Service._DoFile('','./c_process/CProcModule.dll','')  # windows
cell = Service.PCCellBase._New()
cell.AddProc(InputProc(),Service.CAddProcClass)
realm.AddCell(cell)
result = realm.ExecuteForResult()
print(result[0])
```

Output result:

```
input a number : 1
input a number : 2
3
```






