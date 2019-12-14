<h1 align="center">Interoperate with C language</h1>

This example defines a data class NumberClass, an input procedure InputProc, and a process for calculating the sum of two numbers. Among them NumberClass and InputProc use python language. The process of calculating the sum of two numbers is implemented in C language.

The complete example is in the directory: [examples/simple_c_process](../examples/simple_c_process.py)

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

Define the process CAddProcClass in C language
===

Create a base code with the starmodule tool and modify the code.

The command line is as follows:

```sh
starmodule CProcModule.CAddProcClass -c
```

CProcModule as a module. Generate a shared library after compilation. Create CAddProcClass when the load is initialized.

Proceed as follows:

* Create an instance of PCProcBase with the name changed to CAddProcClass

```c
void *PCProcBase = SRPInterface->GetObjectEx(NULL, "PCProcBase");
void *NumberClass = SRPInterface->GetObjectEx(NULL, "NumberClass");

CAddProcClass = SRPInterface -> MallocObjectL(SRPInterface->GetIDEx(PCProcBase),0,NULL);
SRPInterface -> SetName( CAddProcClass, "CAddProcClass");

* Define the input and output of CAddProcClass

```c
/*--create input and output*/
if ((VS_BOOL)SRPInterface->ScriptCall(CAddProcClass, NULL, "InputFrom", "(oo)z", NumberClass, NumberClass) == VS_FALSE) {
	SRPInterface->ProcessError(VSFAULT_WARNING, __FILE__, __LINE__, "load CProcModule failed, call function InputFrom failed");
	SRPInterface->FreeObject(CAddProcClass);
	SRPInterface->Release();
	CoreShellInterface->Release();
	return VS_FALSE;
}
if ((VS_BOOL)SRPInterface->ScriptCall(CAddProcClass, NULL, "OutputFrom", "(o)z", NumberClass) == VS_FALSE) {
	SRPInterface->ProcessError(VSFAULT_WARNING, __FILE__, __LINE__, "load CProcModule failed, call function OutputFrom failed");
	SRPInterface->FreeObject(CAddProcClass);
	SRPInterface->Release();
	CoreShellInterface->Release();
	return VS_FALSE;
}

```

* Write the Execute function of CAddProcClass

```c
static VS_INT32 CAddProcClass_ScriptCallBack( void *L )
{
    void *Object;
    VS_CHAR *ScriptName;
    
    ScriptName = SRPInterface -> LuaToString( SRPInterface -> LuaUpValueIndex(3) );
    Object = SRPInterface -> LuaToObject(1);
    /*first input parameter is started at index 2 */
    if( strcmp(ScriptName,"Execute") == 0 ){
   
    ...
    
    }
    return 0;
}
```

>  * Get two input data objects, return 2 if not present, wait for more data

```c
/*--get input*/
VS_PARAPKGPTR InputPara = (VS_PARAPKGPTR)SRPInterface->ScriptCall(Object, NULL, "InputToParaPkg", "()p");
if (InputPara == NULL) {
	/*--failed*/
	SRPInterface->LuaPushInt(-1);
	return 1;
}
void *InputData1 = InputPara->GetObject(0);
void *InputData2 = InputPara->GetObject(1);
if (InputData1 == NULL || InputData2 == NULL) {
	/*--request more data*/
	SRPInterface->LuaPushInt(2);
	return 1;
}
```

> * Since the data object is defined by python, you need to call the GetDataBuf function, which converts the data into a type of parapkg acceptable to other languages.

```c
VS_PARAPKGPTR InputData1_ParaPkg = (VS_PARAPKGPTR)SRPInterface->ScriptCall(InputData1, NULL, "GetDataBuf", "()p");
VS_PARAPKGPTR InputData2_ParaPkg = (VS_PARAPKGPTR)SRPInterface->ScriptCall(InputData2, NULL, "GetDataBuf", "()p");
VS_DOUBLE Result = InputData1_ParaPkg->GetFloat(0) + InputData2_ParaPkg->GetFloat(0);
```

> * The type of the output object is defined by python, you need to create its instance through the Create function.

```c
void *NumberClass = SRPInterface->GetObjectEx(NULL, "NumberClass");
void *OutputData = (void *)SRPInterface->ScriptCall(NumberClass, NULL, "Create", "(d)o", Result);
if(OutputData != NULL )
	SRPInterface->ScriptCall(Object, NULL, "AddOutputData", "(o)", OutputData);
```

> * Finally, accept the input data, set the Cell execution completion flag, and return

```c
SRPInterface->ScriptCall(Object, NULL, "AcceptInput", "(o)", NULL);
SRPInterface->ScriptCall(CellObject, NULL, "Finish", "()");
SRPInterface->LuaPushInt(0);
return 1;
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






