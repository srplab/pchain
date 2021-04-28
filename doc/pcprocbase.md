<h1 align="center">PCProcBase</h1>

The base classes for process management are PCProcBase, PCCellBase, PCProcChainBase, and PCProcRemoteBase. Usually use PCProcBase. 

**PCCellBase** and **PCProcRemoteBase** inherit the methods and properties of PCProcBase. PCProcRemoteBase is a remotely executed process class that is not fully supported in the current release. 

**PCProcChainBase** is a process chain consisting of multiple processes that contain a starting process and an ending process that are connected together to perform a specific function. A single process can also be used as a process chain. The process chain is the basis of scheduling. At runtime, the executable object Runner is created according to the process chain, and then the data object is assigned to the Runner, and each process in the Runner is executed in turn. 

**PCCellBase** is an independent and schedulable unit. PCCell can contain multiple process chains. It can assign data objects to the process chain. When scheduling, create an execution object Runner according to the process chain in Cell.

define process management type
----

There are two ways to create process types and process instances:

#### a. Using function "Create" 

```python
@Service.PCProcBase.Create(None,"MyNumberProc",(NumberClass),(NumberStepClass))
def Execute(SelfObj,Realm,Cell,Runner) :
  #get input
  in1 = SelfObj.InputToParaPkg()  
  ...
  #   create output 
  SelfObj.AddOutputData(NumberStepClass.Create(xxx))
  SelfObj.AcceptInput() 
  return 0
NumberProc = Service.MyNumberProc
```

The third parameter of the "Create" function is a tuple, or None, which indicates the type of the input data type. There are several forms:

> + One data object, at which point you do not need to specify the number of data objects, for example:
`(NumberClass,NumberClass)`
The process has two inputs, each of which is NumberClass.
> + Indicate the number of instances of the input object, for example
`(2,NumberClass,0,NumberClass)`
The process has two inputs, The first input receives two NumberClass, and the second input receives all instances of NumberClass. Note: The number 0 indicates all
> + Specify dependent data objects, for example, 
`(NumberClass,'s',NumberClass)`
The process has two inputs,The first input is a NumberClass, The second input is a NumberClass and it's source is the first data object.
**'s'** flag cannot be applied to the first input.
The source data must be a unique source, and if the data object has multiple source objects, it does not meet the criteria as input
> + Optional input, for example, 
`(NumberClass,'o',NumberClass)`
The second input may be not existed.

The fourth parameter of the "Create" function is a tuple, or None, which indicates the type of the output.

#### b. define python class and register it to pchain 

```python
import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

pchain.cleinit()

class MyNumberProc(PCPyProcClass) :
  def Execute(self,Value) :  
    Context = self.Context  #  first must save Context in local variable
    ...
    return (0,1,NumberStepClass(xxx))
pyproc.Register(MyNumberProc,(NumberClass),(NumberStepClass))
NumberProc = MyNumberProc.GetType()
```

For more information about PCPyProcClass, please refer to [pyproc.module](./pyproc.module.md)

If the data management type is created using the [second method](./pcdatabase.md), the process management type also recommends using the second method.

Using this method to define the process management type, the number of input parameters of the Execute function corresponds to the number of input parameters specified in Register, and the input parameters are python objects, not data management objects.

The type of the output data object should be within the range of the output data type specified by the Register function. The number of output data objects is not limited, but should not be much.

> **return values**
> The return value may be a triple: (x, y, z) or z or None. if result is z or None, it equals to (0,1,z).
> Where **x** is the state of the process execution:
>> < 0   : failed
>> == 0  : finish
>> == 1  : suspend
>> == 2  : need more input
>> == 3  : wait new input
>> 4,..  : continue, delay. the delay time is (x-4)ms

> **y** indicates how to process input data
>> -1   : Reject All input
>> 0    : Do nothing
>> 1    : Accept All input

> If you reject or accept some inputs other than all input, you need to call `Context['SelfObj'].AcceptInput(xxx)`, or `Context['SelfObj'].RejectInput(xxx)`. When returning in this case, y is set to 0.

> The **z** value is a data object as output, which can be a data object or a tuple of multiple data objects

> **Context**
> Context is the context object for the process. It is a dict and contains the following four items. **Context can't store any data, pchain will create a new Context for each time**
>> + 'SelfObj': CLE object corresponding to this process
>> + 'Realm' : the current Reaml object
>> + 'Cell': current Cell object. **[may be NULL](#)**
>> + 'Runner': Current Runner object. **[may be NULL](#)**

#### c. Using pyproc.DefineProc or pyproc.DefineRawProc

These two functions support "@"

```python
pyproc.DefineProc(tpname,InputDataType,OutputDataType,PyFunc)
pyproc.DefineRawProc(tpname,InputDataType,OutputDataType,PyFunc)
```

> tpname : string, is proc type name
> StarNameSpace : cle object
> InputDataType : Tuple of input data types, please refer to 'InputFrom'
> OutputDataType : output data type. For DefineRawProc, only one type is supported, and the type must be defined with pydata.DefineType. For DefineProc, the OutputDatatype maybe a tuple
> PyFunc : python function to be called

for example,

**DefineRawProc/DefineAsyncRawProc**

```python
pydata.DefineType('PythonNumberClass')

def PyFun(a,b,c) :
  print('input :',a,b,c)      
  val = a + b + c
  return val

pyproc.DefineRawProc('PyFuncProc',(PythonNumberClass,PythonNumberClass,PythonNumberClass),PythonNumberClass,PyFun)
```

or

```python
pydata.DefineType('PythonNumberClass')

@pyproc.DefineRawProc('PyFuncProc',(PythonNumberClass,PythonNumberClass,PythonNumberClass),PythonNumberClass)
def PyFun(a,b,c) :
  print('input :',a,b,c)      
  val = a + b + c
  return val
```

This method can only encapsulate simple python functions and can only output one result. Every execution must be completed.

**DefineProc/DefineAsyncProc**

```
pydata.DefineType('PythonNumberClass')

@pyproc.DefineProc('PyFuncProc',(PythonNumberClass,PythonNumberClass,PythonNumberClass),PythonNumberClass)
def PyFun(self,a,b,c) :  
    Context = self.Context  #  first must save Context in local variable
    print('input :',a.value(),b.value(),c.value())      
    val = a.value() + b.value() + c.value()
    return PythonNumberClass(val)
```    

#### d. Define the process of asynchronous execute

Using DefineAsyncProc and DefineAsyncRawProc. These two functions set the process object's property IsAsync to true.

For asynchronous execution, refer to the description of the property IsAsync


Propertiess supported by process management object
---

*[ErrorCount : int](#)*

Count of errors that occurred during the execution

*[Status : int](#)*

The state of the execution, -1, 0, 0x7FFFFFFF are reserved, others are defined by the process itself

> + -1 : The process execution is terminated, the internal storage should be cleaned, and then returns 0.
> + 0  : first schedule
> + 0x7FFFFFFF : Process is not scheduled for the first time

*[IsSuspend : bool](#)*

Equal to true, the process is suspended, otherwise it is in normal execution state

*[RunnerID : VS_UUID(string)](#)*

The ID of the Runner object to which the process instance belongs. For scripting languages, this property is a string.

*[RootProcID : VS_UUID(string)](#)*

The ID of the process class corresponding to the process instance. This ID is valid when the process is in Runner. For scripting languages, this property is a string.

*[PCProcChild : PCProcChainBase](#)*

Sub-process chain.

*[IsAsync : bool](#)*

A flag for asynchronous execution. If equal to true, the process needs to run in a separate thread.

Procedures created with DefineAsyncProc and DefineAsyncRawProc will automatically set this property to true

For example,

```python
pydata.DefineType("UrlClass")
pydata.DefineType("WebPageClass")

# this proc will be blocked
@pyproc.DefineAsyncProc('DownLoadUrlProc',UrlClass,WebPageClass)
def Execute(self,url) :
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]

  try:    
    libstarpy._SRPUnLock()  # release cle lock, before enter wait
    import urllib2
    req = urllib2.Request(url.value())
    fd = urllib2.urlopen(req)
    result = fd.read()
    libstarpy._SRPLock()    # capture cle lock,
    return (0,1,WebPageClass(result))         
  except Exception as exc:
    libstarpy._SRPLock()    # capture cle lock,
    return (0,1,None)   

print(DownLoadUrlProc.GetType().IsAsync)
Result = DownLoadUrlProc()(UrlClass('http://www.srplab.com'))
print(Result)
```

**[Asynchronous execution using separate threads, before entering the time-consuming operation, you need to call _SRPUnLock to unlock, and then call _SRPLock after exiting.](#)**

Functions supported by process management objects
---

#### a. basic function

*[GetLocalBuf](#)*

Get the local buffer of the process, the buffer type is ParaPkg, which can store the basic type and cle object. When the process is completed, the contents of the buffer are cleared by pchain.
This function should be called in the Execute function of the process

`procbuf = xxx.GetLocalBuf()`

*[GetSignature](#)*

Reserved, used to verify identity of the process in the future

`VS_CHAR *GetSignature()`

*[Notify](#)*

Create OnNewProc callback of realm stub object to notify outside. **If the type is defined not using DefineProc/DefineRawProc/DefineRawProc/DefineAsyncRawProc, this function should be called.**

The new object may be new proc instance or proc type, which can be judged by Realm's function IsProc or IsProcType

`VS_BOOL Notify()`

*[IsType](#)*

`VS_BOOL IsType()`

*[IsRootType](#)*

The object is PCProcBase, PCProcRemoteBase, or PCCellBase

`VS_BOOL IsRootType()`

*[GetType](#)*

Get the type object of the process.

`void *GetType()`

*[GetTypeName](#)*

return type name.

`VS_CHAR *GetTypeName()`

*[GetTag](#)*

Tag is a string of 'proc_'+namespace+process type name

**[Objects of the same tag should be considered as the same object](#)**

`void *GetTag()`

*[GetTagLabel](#)*

Get tag label, format is "proc_"+namespace+type name.

`VS_CHAR *GetTagLabel()`

*[Equals](#)*

two process object are equal or not

`VS_BOOL Equals(struct StructOfPCProcBase *PCProc)`


*[IsCurrent](#)*

The process object has been assigned a data object, is executing or waiting to be executed

`VS_BOOL IsCurrent()`

*[IsInstance](#)*

the data object is instance of input Type

`VS_BOOL IsInstance(void *Type)`

*[EqualDataSet](#)*

Divide the input data list into multiple equal data sets. At least 2 data objects per data set

`VS_PARAPKGPTR EqualDataSet(VS_PARAPKGPTR DataList)`

```
[1,2,3,4,2,3,2,1]
result:
[1,1],[2,2,2],[3,3]
```

*[EqualDataSetEx](#)*

Divide the input data list into multiple equal data sets. At least 2 data objects per data set

`VS_PARAPKGPTR EqualDataSetEx(void *Data1,...)`

*[SplitDataSet](#)*

The function divides the objects in the DataList into two groups according to the objects in the FirstSetRef, one group is the object related to FirstSetRef, and the other is another group. If AddNotExistObject is equal to true, then a data object or process object that has relations with FirstSetRef which not in the DataList will be added.

`VS_PARAPKGPTR SplitDataSet(VS_PARAPKGPTR DataList, VS_PARAPKGPTR FirstSetRef,VS_BOOL AddNotExistObject)`

The result is ParaPkg:[parapkg1,parapkg2].

Parapkg1 is a related object set; parapkg2 is another object set.

*[CollectType](#)*

Get a list of process object with IsType true. Usually a direct instance of PCProcBase or PCProcRemoteBase or PCCellBase, IsType is true.

`VS_PARAPKGPTR CollectType()`

*[Wrap](#)*

This function returns the corresponding cleobject, for compatibility with the pyproc method.

`void *Wrap()`

*[RegCallBack](#)*

Set the callback, the currently supported callback is OnFreeCallback.

```python
freecallbackobj = Service._New()
@freecallbackobj._RegScriptProc_P('OnFreeCallback')
def func(CleObj,WhichObj) :
  print(str(WhichObj),'   ',str(WhichObj.GetTag()), '  isfreed')
Service.PCProcBase.RegCallBack(freecallbackobj);
```

`void RegCallBack(void *TargetObject)`

*[UnRegCallBack](#)*

Remove the callback

#### b. Input and output data object type management

*[InputFrom](#)*

Input data object type definition for the process

`VS_BOOL InputFrom(Args,...)`

Parameters can be quantity, dependency flags, and data type objects. The quantity and dependency flags are valid for the data type objects that follow, and can be omitted. In this case, the default value is [1](#). When the number is equal to [0](#), it means that the input accepts all data objects of this type in the current Cell as input. The dependency flag is the string ["s"](#) or ["o"](#), which can be omitted. When present: 
> "s" : the source data of the following input is the previous data object.
> "o" : the following input is optional.

*[The input object can be a data type or a data instance, and if it is an instance, it matches as follows:](#)*

> a. If it is a PCDataBase instance, the input data object must be equal to it
> b. If it is a PCDataSetBase instance, the input data object must be a subset of it

for example, 

```python
NumberProc1.InputFrom(NumberClass,"s",NumberStepClass)
NumberProc2.InputFrom("o",NumberClass)
```

*[InputQueueToParaPkg](#)*

The returned result is consistent with the format of the InputFrom input.

`VS_PARAPKGPTR InputQueueToParaPkg()`

*[CollectInputDataClass](#)*

Returns a list of input data types.

`VS_PARAPKGPTR CollectInputDataClass()`

*[GetInputNumber](#)*

Get the number of inputs

`VS_INT32 GetInputNumber()`

*[GetRequestNumber](#)*

Get the number data instance required of inputs

`VS_INT32 GetRequestNumber(VS_INT32 Index)`

*[IsFromInternal](#)*

Whether the input comes from the previous process

`VS_BOOL IsFromInternal(VS_INT32 Index)`

*[IsSlave](#)*

Whether the input is an attribute of the previous input data

`VS_BOOL IsSlave(VS_INT32 Index)`

*[IsMustExist](#)*

Whether the input must exist

`VS_BOOL IsMustExist(VS_INT32 Index)`

*[GetMasterInput](#)*

Get input data that is not an attribute before. Valid when the process is in Runner

`void *GetMasterInput(VS_INT32 Index)`

*[GetMasterInputType](#)*

Get input data type that is not an attribute before. 

`void *GetMasterInputType(VS_INT32 Index)`

*[GetInputType](#)*

Get the data type of the input

`void *GetInputType(VS_INT32 Index)`

*[SetInputType](#)*

Usually used to create new processes based on existing processes, modify the input data types of new processes, and optimize the scheduling of new processes.

Input type must be a subclass of the original type

`VS_BOOL SetInputType(VS_INT32 Index,void *PCDataType)`

*[IsEnough](#)*

Whether the input data already exists. Valid when the process is in Runner

`VS_BOOL IsEnough(VS_INT32 Index)`

*[GetInputTypeEx](#)*

Get list of data type object corresponding to each input, the item number equals to number of input

`VS_PARAPKGPTR GetInputTypeEx()`

*[OutputFrom](#)*

Output data object type definition.

Parameters can be "m" or, and data type objects.

> "m : the following output must be generated.

`VS_BOOL OutputFrom(arg1,...)`

**["m" can only be used when the proc is a PCCell](#)**

**If the proc is not cell, then for each output data type, pchain automatically defines new data types, whose name is the original {type name}_P{number}**

*[GetOutputNumber](#)*

Return the number of output data type

`VS_INT32 GetOutputNumber()`

*[GetOutputType/GetOriginOutputType](#)*

Return the output data type object list

`VS_PARAPKGPTR GetOutputType()`

`VS_PARAPKGPTR GetOriginOutputType()`

*[OutputQueueToParaPkg/OriginOutputQueueToParaPkg](#)*

The returned result is consistent with the format of the OutputFrom's input.

`VS_PARAPKGPTR OutputQueueToParaPkg()`

`VS_PARAPKGPTR OriginOutputQueueToParaPkg()`

#### c. Input and output data object management

*[GetInput](#)*

Get an input data object

`void *GetInput(VS_INT32 Index)`

The result returned is the data object assigned to the process, or ParaPkg for multiple data objects.

*[InputToParaPkg](#)*

Get all input data object

`VS_PARAPKGPTR InputToParaPkg()`

Returns the data objects assigned to each input of the process instance in turn, or multiple data objects (returned via ParaPkg). The function returns a result of ParaPkg, and each item corresponds to an input.

*[RejectInput](#)*

The data object is rejected as input. The data object is assigned to the instance of the process by pchain. There may be an incorrect allocation. The input is judged in the Execute function of the process. If it is wrong, the data object is rejected as an input.

`void RejectInput(void *DataObject)`

If the input parameter DataObject is NULL, reject all data objects currently assigned to the process

*[RecordReject](#)*

If Flag is true(default is false), the reject data will be recorded, and can be get using realm's GetReject function.

The return value is RecordRejectID.

`VS_CHAR *RecordReject(VS_BOOL Flag)`

*[AcceptInput](#)*

The data object is accepted as input. The data object is assigned to the instance of the process by pchain. After calling this function, the process instance can allocate new data objects again

`void AcceptInput(void *DataObject)`

If the input parameter DataObject is NULL, accept all data objects currently assigned to the process

*[OutputToParaPkg](#)*

Get all output data object

`VS_PARAPKGPTR OutputToParaPkg()`

Returns the data objects assigned to each output of the process instance, or multiple data objects (returned via ParaPkg). The function returns a result of ParaPkg, and each item corresponds to an output item.

*[AddOutputData](#)*

Add an output data object, you can add more than one at a time. Pchain sets all input data objects to the source object of the output object

If there is already equal output data, it will be added again. 

`VS_BOOL AddOutputData(void *DataObject1,void *DataOject2,...)`

**[Note: If it is a cell and the output data type is not defined, put it in EnvData. This happens when you customize the Cell's Execute procedure.](#)**

*[AddOutputDataEx](#)*

Add an output data object and set it's source.

`VS_BOOL AddOutputDataEx(void *DataObject, void *SourceData,...)`

Data objects in SourceData are arranged in order.

**[Note: If it is a cell and the output data type is not defined, put it in EnvData. This happens when you customize the Cell's Execute procedure.](#)**

*[UpdateOutputData](#)*

Update the output object, which must have been added to the output object of the process instance. This function sets the change flag of the output object. 

`VS_BOOL UpdateOutputData(void *PCData)`

#### d. Execute related functions

*[DataCanBeAsInput](#)*

Whether the data object can be used as the input data object. 

`VS_BOOL DataCanBeAsInput(struct StructOfPCDataBase *PCData)`

*[DataCanBeAsOutput](#)*

Whether the data object is output of the process. 

`VS_BOOL DataCanBeAsOutput(struct StructOfPCDataBase *PCData)`

*[ProcCanBeAsInput](#)*

Whether the outputof the process can be used as input. 

`VS_INT32 ProcCanBeAsInput(struct StructOfPCProcBase *PCProc)`

*[GetCell](#)*

Get the cell to which the process belongs to. It is valid when the process is in a Runner. 

`struct StructOfPCCellBase *GetCell()`

*[Suspend](#)*

Suspend the process, valid when the process belongs to a runner. If in the Execute function of the process, do not call this function, but returns result value 1 

`void Suspend()`

*[Resume](#)*

Resume the process, valid when the process belongs to a runner. 

`void Resume()`

*[Continue](#)*

Format the return result for continue execution. The input parameter of the function is the interval of the next execution, the unit is ms. 

`VS_INT32 Continue(VS_INT32 Delay)`

*[GetRootProc](#)*

For proc in Runner, get the corresponding proc in cell's procchain.

`void *GetRootProc()`

*[GetPrevProc](#)*

Get the previous process in the same process. This function is valid in the Execute function of the process.There may be more than one process, this function returns ParaPkg

`VS_PARAPKGPTR GetPrevProc()`

*[GetNextProc](#)*

If it is equal to NULL, it is represented as the last process in the process chain, and its output will be placed in the environment queue of the cell.

`void *GetNextProc()`

*[IsPrevProcFinish](#)*

Return true if previous process has output instance of PCDataClass, and the output has been allocated to this proc. If the output data type of previous process has no related with PCDataClass, the function also returns true.

PrevPCProc maybe NULL, in this case, all previous proc must meet above condition

`VS_BOOL IsPrevProcFinish(void *PrevPCProc,void *PCDataClass)`

*[NumberOfRunner](#)*

Called in the Execute function of the procedure. Get the number of execution instances. If WithSameProcChain is equal to true, then the number of running instances of this process chain is obtained. If equal to false, the number of running instances that are not the chain of this process is obtained.

`VS_INT32 NumberOfRunner(struct StructOfPCProcBase *PCProc,VS_BOOL WithSameProcChain)`

*[NumberOfEnvData](#)*

If InputIndex<0, all inputs are calculated, otherwise the specified input is calculated, and based on the input DataClass, it gets the number of instances of DataClass that can be assigned to PCProc.

This function retrieves the instance of the EnvDataQueue that belongs to the DataClass in turn, and determines whether ExcludeProc already contains PCProc. If not included, it means that it can be assigned. Count the number that can be assigned. If IncludeConnectedData is equal to false, the data already assigned to the process is not calculated, otherwise it is counted

`VS_INT32 NumberOfEnvData(struct StructOfPCProcBase *PCProc,VS_INT32 InputIndex,VS_BOOL IncludeConnectedData)`

#### e. process chain management

*[ChildToParaPkg](#)*

Get a list of sub-process chains

`VS_PARAPKGPTR ChildToParaPkg()`

#### f. direct call

Process instances can be called directly, for example:

```python
pydata.DefineType('NumberClass')
pyproc.DefineProc('InputProc',None,NumberClass)
def Execute(self) :  
  val = input('input a number : ')
  return NumberClass(val)
```

There are two ways to call the above procedure:

* Create an instance of the procedure and call it directly

```python
try :
  result = InputProc()()
  print(result.value())
  
  or
  
  result = InputProc.call()
  print(result.value())
```

If there is no error or no output, an exception will be triggered.

If the result is one, return directly; if there are multiple, return the tuple

* Called via CLE object

```python
try :
  result = InputProc().Wrap()()
  print(result)
```

Input parameters and output parameters are CLE objects. The encapsulated python object can be obtained via pydata.UnWrap

If the result is one, return directly; if there are multiple, return the parapkg

**[note: If the process is executed unsuccessfuly, an exception will be generated. Need to use try capture]**

Functions supported for python instances corresponding to cle objects 
---

* GetLocalBuf
* GetSignature
* GetTag
* GetTagLabel
* RejectInput
* AcceptInput
* RecordReject
* InputQueueToParaPkg
* GetInputNumber
* GetRequestNumber
* IsFromInternal
* IsSlave
* IsMustExist
* GetMasterInput
* GetMasterInputType
* GetInputType
* SetInputType
* IsEnough
* GetInputTypeEx
* DataCanBeAsInput
* DataCanBeAsOutput
* ProcCanBeAsInput
* OutputQueueToParaPkg
* OriginOutputQueueToParaPkg
* GetOutputNumber
* GetOutputType
* GetOriginOutputType
* ClearOutputData
* AddOutputData
* AddOutputDataEx
* GetCell
* Suspend
* Resume
* Continue
* GetRootProc
* GetPrevProc
* GetNextProc
* IsPrevProcFinish
* IsCurrent
* IsType
* GetType
* GetTypeName
* Equals
* IsInstance
* RegCallBack
* UnRegCallBack

Properties supported for python instances corresponding to cle objects 
---

* _ID
* Tag
* TagLabel






