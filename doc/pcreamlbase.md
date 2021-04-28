<h1 align="center">PCRealmBase</h1>

PCRealm manages environment data and Cell. It is itself a cle object, providing Execute, ExecuteOnce, ExecuteForResult, and ExecuteUntil function. Performing the allocation of environmental data in Realm, Cell scheduling, provides a single-step execution, storage and recovery process and process chain. According to the state of the current execution, the callback pcrealm function executes the policy set by the app.

Realm manages the processing of environmental data. Put the environment data to be processed into the realm environment data queue, and then call Execute, ExecuteOnce or ExecuteUntil to start the processing of the environment data. When the state is stable, that is, the cell cannot continue processing, no new process or data is added, the execution finished.

Create instance of PCRealmBase 
---

```python
realm = Service.PCRealmBase._New()
or
realm = Service.PCRealmBase()
```

Propertiess supported by PCRealmBase
---

*[TraceFlag : bool](#)*

The default value is false. If equal to true, the following callback function is called at the execution of each process.

> * OnRunnerBeforeExecuted : Called before Runner executed
> * OnRunnerProcBeforeExecuted : Called before the process in runner is executed
> * OnRunnerProcExecuted : Called after the process in runner is executed
> * OnRunnerExecuted : Called after Runner executed

*[ExecuteStage : int](#)*

The execution of realm is divided into four phases: EXECUTEPREPARE(0)，EXECUTE(1)，IDLEPREPARE(2)，IDLE(3)

**[Note : Do not modify this property](#)**

*[ScheduleTickCount : int64](#)*

Schedule count, plus 1 for each schedule

*[ErrorCount : int](#)*

The number of errors that occurred during the processing.
Automatically set to 0 before each execution

*[InitialLiveCount : int](#)*

Initial LiveCount value for data objects.

Default value is 64

*[PCCellQueue : object](#)*

Cell queue to run. Do not modify it directly.

*[PCCellLibrary : object](#)*

The queue used to store the Cell. Do not modify it directly.

*[MaxUnAllocatedData : int](#)*

The default is 128. The maximum number of environmental data objects produced by the process run in the Cell, or number of output data by pcproc or cell. When the number is exceeded, a callback "OnMoreUnAllocatedData" is generated for the Realm to which the Cell or proc belongs. The Realm determines whether there is an exception. Default stops the running.

*[MaxSourceDataLength : int](#)*

The default is 64. The maximum length of the source data chain, if exceeded, triggers the OnLongSourceData event.

*[MaxLoopCount : VS_INT32](#)*

The number of times for a process returns continue but does not produce an output, which exceeds the threshold, triggering the OnLongLoop callback

*[MaxSuspendTickCount : VS_INT64](#)*

If the process suspends beyond this threshold, the OnLongSuspend event is fired

default value is 1000(ms)

Functions supported by realm
---

#### a. basic function

*[GetLocalBuf](#)*

Get the local buffer of Realm, the buffer may be used by the app to store data

`VS_PARAPKGPTR GetLocalBuf()`

*[SetLocalBuf](#)*

Set the local buffer of Realm, the buffer may be used by the app to store data

`void SetLocalBuf(VS_PARAPKGPTR Buf)`

*[SaveToJSonPkg](#)*

Convert the input package to a package that can be stored as a json string

`VS_PARAPKGPTR SaveToJSonPkg(VS_PARAPKGPTR Buf)`

*[LoadFromJSonPkg](#)*

The parameter package converted from the json string is restored to the original parameter package.

`VS_PARAPKGPTR LoadFromJSonPkg(VS_PARAPKGPTR JSonPkg)`

*[BuildDepends](#)*

The input parameters contain Proc, Cell, ProcChain and data object, which returns their classes.

The output is a string in the format:

{"ClassName":"CaptureBoolProc","ClassName":"BoolClass"}

`VS_CHAR *BuildDepends(VS_PARAPKGPTR Input)`

*[IsDependsExist](#)*

The input parameter is the ParaPkg converted from the Json string output by BuildDepends.

`VS_BOOL IsDependsExist(VS_PARAPKGPTR DependsClass)`

*[GetSystemPackageInfo](#)*

Get system package information.

`VS_PARAPKGPTR GetSystemPackageInfo()`

*[FindSystemPackage](#)*

Find packages that define data types or process types

`VS_CHAR *FindSystemPackage(void *DataOrProcType)`

*[SaveObject/SaveObjectString](#)*

Save the object to ParaPkg and convert it to a JSon string. Saveable objects are PCProc, PCCell, PCProcChain,PCData. multiple objects can be saved at once.

`VS_BOOL SaveObject(VS_PARAPKGPTR Buf,void *Object1,...)`

`VS_CHAR *SaveObjectString(void *Object1, ...)`

*[LoadObject/LoadObjectString](#)*

Loading objects from ParaPkg converted from json. The result is ParaPkg. If it fails, the number of objects in ParaPkg is 0.

`VS_PARAPKGPTR LoadObject(VS_PARAPKGPTR Buf,VS_BOOL IsNotStrictMatch)`

`VS_PARAPKGPTR LoadObjectString(VS_CHAR *SaveInfo, VS_BOOL IsNotStrictmatch)`

> If IsNotStrictMatch is equal to false, the input and output of each procedure must be identical.
Otherwise, the type and number of input data, and the type of output data must be consistent

*[FindProcForOutput](#)*

Find the matching process based on the type of output data.

`VS_PARAPKGPTR FindProcForOutput(struct StructOfPCDataBase *PCDataClass)`

*[FindProcChainForOutput](#)*

Find the matching process chain based on the type of output data.

`VS_PARAPKGPTR FindProcChainForOutput(struct StructOfPCDataBase *PCDataClass)`

*[FindProcForInput](#)*

Find the matching process based on the type of input data. Multiple input data must all meet.

`VS_PARAPKGPTR FindProcForInput(struct StructOfPCDataBase *PCDataClass,VS_INT32 RequestNumber,...)`

RequestNumber can be omitted, the default is 1  

*[FindProcChainForInput](#)*

Find the matching process chain based on the type of input data. Multiple input data must all meet.

`VS_PARAPKGPTR FindProcChainForInput(struct StructOfPCDataBase *PCDataClass,VS_INT32 RequestNumber,...)`

RequestNumber can be omitted, the default is 1  

*[FindProc](#)*

Find the matching process based on the type of input and output data. Multiple input data must all meet.

`VS_PARAPKGPTR FindProc(struct StructOfPCDataBase *OutputPCDataClass, struct StructOfPCDataBase *InputPCDataClass,VS_INT32 RequestNumber, ...)`

RequestNumber can be omitted, the default is 1  

*[FindProcChain](#)*

Find the matching process chain based on the type of input and output data. Multiple input data must all meet.

`VS_PARAPKGPTR FindProcChain(struct StructOfPCDataBase *OutputPCDataClass, struct StructOfPCDataBase *InputPCDataClass,VS_INT32 RequestNumber, ...)`

RequestNumber can be omitted, the default is 1  

*[GetCellForInput](#)*

Get the Cells in Realm that can process this data. May return multiple cells

`VS_PARAPKGPTR GetCellForInput(struct StructOfPCDataBase *PCDataClass)`

*[BuildProcChain](#)*

The process chain is built based on the type of output data. There are two ways : to indicate the maximum number of steps or to indicate the possible type of input data type or proc.

> * OutputDataOrProc: Output data or process type, may be data or process type or parapkg for multiple data types. Cannot be NULL.
> * InputDataOrProc: Possible input data types or procs, may be multiple or parapkg, Can be NULL.

The returned result contains two items:

> * 0: bool, true for successful.
> * 1: If the build is successful, the process chain is returned; if fails, and this entry is not empty, then there is no process can create output data of the corresponding type

`VS_PARAPKGPTR BuildProcChain(void *OutputDataOrProc,void *InputDataOrProc,...)`

**[Note : This function randomly returns a process chain each time it is called.The returned process chain will be freed with ParaPkg. If you don't want it to be freed, you need to save the process chain to a variable](#)**

**[Note2: If a RealmStub object is set, you can set a callback function OnProcPriority, which returns the priority of the process and affects the selection of the process](#)**

```python
stub = Service.PCRealmStubBase()
@stub._RegScriptProc_P("OnProcPriority")
def OnProcPriority(CleObj,ProcessSet, OutputPriority) :
  print(ProcessSet)
  OutputPriority._Clear()
  for i in range(ProcessSet._Number) :
    OutputPriority[i] = i * 4 + 1.0
realm.SetRealmStub(stub)     

result = realm.BuildProcChain(NumberClass,NumberClass)
print(result[1].ToParaPkg())
```

*[FindProcChainEx](#)*

The lookup process starts with FirstPCProc, the end process is the process chain of LastPCProc, and FirstPCProc and LastPCProc can be NULL.

`VS_PARAPKGPTR FindProcChainEx(struct StructOfPCProcBase *FirstPCProc, struct StructOfPCProcBase *LastPCProc)`

*[FindByTag](#)*

Find objects based on Tag, which can be Proc or Data. If it does not exist, call the Stub callback function “OnFindByTag”

`void *FindByTag(VS_CHAR *Tag)`

*[RequestProcChain](#)*

This function calls realm's callback function OnRequestProcChain for processing. The app is responsible for how to handle it.

VS_PARAPKGPTR RequestProcChain(void *OutputDataOrProc, void *InputDataOrProc, ...)

If you need to request the process chain from the internet, it is a time-consuming operation, and the process of calling the function should be an asynchronous process.

> * OutputDataOrProc: Output data or process type, may be data or process type or parapkg for multiple data types. Cannot be NULL.
> * InputDataOrProc: Possible input data types or procs, may be multiple or parapkg, Can be NULL.

```
@pyproc.DefineAsyncProc('xxxx',UrlClass,WebPageClass)
def Execute(self,url) :
  Context = self.Context  #  first must save Context in local variable
  SelfObj = Context["SelfObj"]
  
  chain = Context["Realm"].RequestProcChain(xxx,xxx)
```

*[Reset](#)*

If in ExecuteUntil, the error count is cleared.

If in step debug, the error count is cleared.

Otherwise, 
> for a running Cell,
>> * Generate OnCellFinish event
>> * Clear the current state of the Cell, release the Cell and Runner, and set IsReady=false
> 
> * Clear error count
> * Clear environmental data
> * Reset execution phase

`void Reset()`

**[This function does not clear Realm's local buffer](#)**

*[Clear](#)*

Clear data, cell, and localbuf

`void Clear(VS_BOOL ClearPrivateBuf)`

*[GetLastNewTypeTickCount](#)*

Get the TickCount(ms) when the new type was last added

`VS_INT64 GetLastNewTypeTickCount()`

*[RegCallBack](#)*

Set the callback, the currently supported callback is OnFreeCallback.
``` TargetObject.OnFreeCallback(CleObj,PCRealm) ```

`void RegCallBack(void *TargetObject)`

*[UnRegCallBack](#)*

Remove the callback

`void UnRegCallBack(void *TargetObject)`

*[GetTag](#)*

Returns a tag of a group of objects

`VS_PARAPKGPTR GetTag(void *InputObject1,...)`

*[GetTagEx](#)*

Returns a tag of a group of objects

`VS_PARAPKGPTR GetTagEx(VS_PARAPKGPTR InputObjectList)`

*[FormatChanged](#)*

For the two sets of data, the data is decomposed into new, removed and changed data, returning ParaPkg, each item is a child ParaPkg, containing 4 items:

0:Tag, 1: (0,remove,1:changed,2:add), 2: Previous Object(is existed) or Empty, 3: Current Object(is existed) or Empty

`VS_PARAPKGPTR FormatChanged(VS_PARAPKGPTR PreviousDataSet, VS_PARAPKGPTR CurrentDataSet)`

*[IsData](#)*

input is pcdata instance

`VS_BOOL IsData(void *Object)`

*[IsProc](#)*

input is pcproc instance

`VS_BOOL IsProc(void *Object)`

*[IsCell](#)*

input is pccell

`VS_BOOL IsCell(void *Object)`

*[IsChain](#)*

input is procchain

`VS_BOOL IsChain(void *Object)`

*[IsDataType](#)*

input is pcdata type

`VS_BOOL IsDataType(void *Object)`

*[IsProcType](#)*

input is pcproc

`VS_BOOL IsProcType(void *Object)`

*[IsPChainObject](#)*

input object defined in pchain or is instance of pchain

`VS_BOOL IsPChainObject(void *Object)`

*[SetLog](#)*

Can be integers, floats, booleans, strings, parameter packages, and objects

`void SetLog(...)`

*[ClearLog](#)*

Clear logs

`void ClearLog()`

*[GetLog](#)*

Get logs

`VS_PARAPKGPTR GetLog()`

*[SetNodeSet](#)*

Set NodeSet Object, which is instance of NodeSetBase of cnode module for network graph computing

`void SetNodeSet(void *CNodeSet)`

*[GetNodeSet](#)*

Get NodeSet Object

`void *GetNodeSet()`


#### b. Environmental data management

*[AddEnvData](#)*

Add environment data to the Realm, you can add multiple at the same time
input parameter may be data objects or parapkg which holds multiple data object

`void AddEnvData(void *Data,...)`

**This function generate an instance of the input data object and add the instance to the Realm**

*[RemoveEnvData](#)*

Remove environment data from the Cell, you can remove multiple at the same time

`void RemoveEnvData(...)`

Input parameters can be parameter packages (Parapkg) or multiple data objects

*[ClearEnvData](#)*

Clear the environment data belonging to the DataClass instance. If the DataClass is equal to NULL, clear all the environment data.

`void ClearEnvData(struct StructOfPCDataBase *DataClass)`

*[EnvDataToCell](#)*

Assign the environment data to the running Cell, if not, assign it to the Cell in the CellLibrary, and move the cell to running cell queue.
Otherwise return false.

`VS_BOOL EnvDataToCell(void *data)`

**This function also removes the data object from the realm**

*[EnvDataToProc](#)*

Assign one or multiple environment data to the Cell. The cell is created based on input proc. If input proc is a cell, using it, or else, create a new cell, add input procs to the cell, and then add the cell to realm.

`VS_BOOL EnvDataToProc(void *DataOrParaPkg,void *Proc1,...)`

**This function also removes the data object from the realm**

*[GetEnvData](#)*

Obtain the environment data queue of the PCDataBase instance created when executing. If PCDataBase is equal to NULL, all the environment data is returned.

`VS_PARAPKGPTR GetEnvData(void *PCDataBase)`

*[GetNewEnvData](#)*

Obtain the environment data queue of the PCDataBase instance. If PCDataBase is equal to NULL, all the environment data is returned.

`VS_PARAPKGPTR GetNewEnvData(void *PCDataBase)`

*[IsFromOutSide](#)*

The environment data is from outside of the realm

`VS_BOOL IsFromOutSide(void *PCDataBase)`

*[ProcessCellEnvData](#)*

If the Cell runs successfully, the unprocessed environment data and the dynamically generated environment data are rolled back to Realm. If the Cell does not run successfully, only the non-dynamically generated environment data is rolled back to Realm.

`void ProcessCellEnvData(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell, VS_BOOL IsSuccess)`

*[ProcessCellEnvDataEx](#)*

Process the same as ProcessCellEnvData. The difference with ProcessCellEnvData in that the function returns the data output by the Cell at the same time, or the dynamically generated unprocessed data.

`VS_PARAPKGPTR ProcessCellEnvDataEx(struct StructOfPCRealmBase *PCRealm, struct StructOfPCCellBase *Cell, VS_BOOL IsSuccess)`

#### c. Cell management

*[AddCell](#)*

Add Cell to Cell Queue.

`void AddCell(struct StructOfPCCellBase *PCCell)`

*[AddProc](#)*

Enter one or more processes or process chains. This function automatically creates a cell, adds the input process or process chain to it, and then places the cell in the realm.

`VS_BOOL AddProc(void *ProcOrChain, ...)`


*[AddCellLibrary](#)*

Add Cell to Cell Library.

`void AddCellLibrary(struct StructOfPCCellBase *PCCell)`

*[RemoveCellLibrary](#)*

Remove Cell from Cell Library.

`void RemoveCellLibrary(struct StructOfPCCellBase *PCCell)`

*[GetCell](#)*

Get the list of cells in the Cell Queue.

`VS_PARAPKGPTR GetCell()`

*[MoveToCellLibrary](#)*

*[GetCellLibrary](#)*

Get the list of cells in the Cell Library.

`VS_PARAPKGPTR GetCellLibrary()`

*[MoveToCellLibrary](#)*

if cell is in CellQueue, then move it to CellLibrary, or else, Add it to CellLibary

`void MoveToCellLibrary(struct StructOfPCCellBase *PCCell)`

*[MoveToCellQueue](#)*

if cell is in CellLibary, then move it to CellQueue, or else, Add it to CellLibary

`void MoveToCellQueue(struct StructOfPCCellBase *PCCell)`

*[RemoveCell](#)*

Remove cell from the realm

`void RemoveCell(struct StructOfPCCellBase *PCCell)`

#### d. Execute related functions

*[Execute](#)*

Run Realm.

`void Execute()`

> 1. Call Realm's callback function OnBeforeExecute. In the callback function, the app can generate new Cells according to the environment data, add the Cells to the Realm's Cell queue, and assign the env data to the Cell.
> 2. Schedule each Cell in the Cell queue, once per Cell. **If the status of all the cells does not change, the execution is completed.**
> 3. call the callback function OnAfterExecute
> 4. Change realm's ExecuteStage to IDLEPREPARE

*[ResetExecuteOnce](#)*

Set the execution phase to EXECUTEPREPARE. This function should be called first before calling ExecuteOnce

`void ResetExecuteOnce()`

*[ExecuteOnce](#)*

Execute once. If the return value is equal to true, it means that during the execution phase, if it returns false, it means the execution is completed, in the Idle stage.

if realm's ExecuteStage is IDLEPREPARE, then call the callback function OnIdle.

`VS_BOOL ExecuteOnce()`

*[ExecuteForResult](#)*

This function is the same as Execute except that does not call callback function OnFrameData. After the execution is completed, the dynamically generated environment data in Realm is returned as the result.

The return value is ParaPkg. If there is no element, the execution fails.

`VS_PARAPKGPTR ExecuteForResult()`

*[ExecuteUntil](#)*

Continue execution. After calling this function, it enters the loop and does not exit until FinishExecuteUntil is called.

The function should be called in a separate thread

`void ExecuteUntil(VS_BOOL DebugMode)`

This function first schedules cells, then enter idle phase, and then repeat again.

There are several functions related to it

> *[SuspendExecuteUntil](#)*
>
> Suspend the current execution loop.
>    
> `void SuspendExecuteUntil(VS_BOOL ForAddEnvData)`
>    
> Can only suspend in the Idle phase. If ForAddEnvData is true, all current environment data is cleared and the execution phase is set to the Execute phase. Otherwise, it simply suspend
>
> *[ResumeExecuteUntil](#)*
>
> Resume
>
> void ResumeExecuteUntil()
>
> *[FinishExecuteUntil](#)*
>
> End execution
>
> `void FinishExecuteUntil()`

If **DebugMode** is equal to true, then stepping into the single step. Call `BreakOnProcContinue` to execute the next step. or call `CancelBreakOnProc`

```python
import threading
class Realm_ExecuteThread(threading.Thread): 
    def __init__(self, realm):
        threading.Thread.__init__(self)
        self.realm = realm
    def run(self):                 
        libstarpy._SRPLock()
        #self.realm.ExecuteUntil(True)
        self.realm.ExecuteUntil(False)
        libstarpy._SRPUnLock()

thread1 = Realm_ExecuteThread(realm)
thread1.start()
...
pchain.cleloop()
pchain.cleterm()
```

#### e. Debug related functions

*[BreakOnProc](#)*

Set the breakpoint before the running of a process in the cell , or after a process in the cell returns 0. The execution will pause until CallOnProcContinue is called.

`void BreakOnProc(struct StructOfPCCellBase *PCCell)`

If PCCell is NULL, any Cell in Realm is suspended before execution.

*[BreakOnProcContinue](#)*

Continue execution

`VS_BOOL BreakOnProcContinue()`

*[CancelBreakOnProc](#)*

Cancel single-step execution

`void CancelBreakOnProc()`

*[GetStatus](#)*

Get the state of the object, return ParaPkg, can be converted to json string by _ToJSon () function

`VS_PARAPKGPTR GetStatus(void *Object)`

*Input parameter Object is cell or NULL. if object is NULL, return status of all cells in the realm*

#### f. Callback function about Runner

*[OnRunnerBeforeExecuted](#)*

Called before Runner executes, Realm's TraceFlag must be true

`void OnRunnerBeforeExecuted(struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner)`

*[OnRunnerProcBeforeExecuted](#)*

Called before the execution of a process in runner, Realm of TraceFlag must be true

`void OnRunnerProcBeforeExecuted(struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner,struct StructOfPCProcBase *Proc,VS_INT32 Condition)`

> Condition
> * Condition ==0, can be executed  
> * ==1,has output data allocated to next proc  
> * ==2 has output data can be allocated to next proc  
> * ==3 is suspend

*[OnRunnerProcExecuted](#)*

Called after the execution of a process in runner, Realm of TraceFlag must be true

`void OnRunnerProcExecuted(struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner,struct StructOfPCProcBase *Proc,VS_INT32 ExecuteResult)`

*[OnRunnerExecuted](#)*

Called after Runner executes, Realm's TraceFlag must be true

`void OnRunnerBeforeExecuted(struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner)`

#### g. Callback Function about Realm and Cell

*[OnBeforeExecute](#)*

Called before the run loop of Realm. In the callback function, new Cells can be created according to the environment data in Realm and added to the Cell queue.

`void OnBeforeExecute()`

example,

```python
@realm._RegScriptProc_P('OnBeforeExecute')
def realm_OnBeforeExecute(CleObj):
  envdata = CleObj.GetEnvData()
  if envdata._Number == 0 :
    return
  #find the proc, allocate data
  for data in envdata :  
    if CleObj.EnvDataToCell(data) == False :
      procs = CleObj.FindProcForInput(data,False)
      if procs._Number == 0 :
        pass
      else :      
        newcell = Service.PCCellBase._New()
        for proc in procs:
          newcell.AddProc(proc._New())    
        CleObj.AddCell(newcell)
        CleObj.EnvDataToCell(data)
  return  
```

If no callback function is defined, the default processing is as follows:

```python
envdata = CleObj.GetEnvData()
if envdata._Number == 0 :
  return
#allocate the data to cell
for item in envdata :    
  cells = CleObj.GetCellForInput(item)
  for c in cells :
   c.AddEnvData(CleObj,item)
CleObj.RemoveEnvData(envdata)
```


*[OnAfterExecute](#)*

Called after the loop of exectution.

`VS_BOOL OnAfterExecute()`

If the callback returns false, the realm's execution ends, otherwise the scheduling continues.

*[OnMoreUnAllocatedData](#)*

If the cell generates a large amount of environment data and exceeds the threshold MaxUnAllocatedData, the callback function is called.

`VS_INT32  OnMoreUnAllocatedData(void *PCProc)`

> * Returns 0, execution error, terminate the execution (default)
> * Returns 1, normal, no processing required, at this time the Cell's MaxUnAllocatedData threshold is increased by 64 to prevent the event from being generated too quickly.

*[OnLongLoop](#)*

The process loops multiple times, exceeding the threshold.

`VS_BOOL OnLongLoop(void *PCCell, void *PCProc,VS_INT32 LoopCount)`

> * Returns false, execution error, terminate the execution (default)
> * Returns true, continue.

*[OnLongSuspend](#)*

The process suspend time expired,

Returns true by default, indicating that it should continue to wait

`VS_BOOL OnLongSuspend(void *PCCell, void *PCProc, VS_INT64 SuspendTick)`

*[OnInputInvalid](#)*

There is input data, but the LiveCount of the input data equals to 0, then the callback function is called. The function returns true, indicating that execution is required, false(default) to terminates.

`VS_BOOL OnInputInvalid(void *PCCell, void *PCProc)`

*[OnLongSourceData](#)*

Returns true, indicating that the data is valid, false, the data is invalid.

`VS_BOOL OnLongSourceData(void *PCCell, void *PCData)`

*[OnOutputDataToEnv](#)*

In the callback function, the data object output to the environment can be corrected. After the function returns, the data object is added to the cell environment.

`void OnOutputDataToEnv(void *PCCell, void *PCProc, VS_PARAPKGPTR DataList)`

*[OnCellToBeFinish](#)*

Called before the end of the Cell's execution.

`VS_BOOL OnCellToBeFinish(struct StructOfPCCellBase *Cell)`

This callback can add a new process chain, new data, and can set IsSuspend equal to true.

**[In the callback function, app can call GetEnvDataUnHandled to get the environment data that can not be processed, and, call GetMissingEnvDataProc/GetCellMissingOutput/IsCellOutputMustExist to get the process that cannot be executed due to missing input.](#)**


If IsSuspend is false, and the function returns false, then an OnCellFinish callback will be called, and the Cell schedule ends.

If the function returns true and IsSuspend is equal to false, the Cell continues to schedule. And does not call the OnCellFinish callback function

*[OnCellFinish](#)*

Called at the end of the Cell's execution.

`void OnCellFinish(struct StructOfPCCellBase *Cell,VS_BOOL IsSuccess)`

For the Cell in Realm (`if cell._Parent == realm`), call `ProcessCellEnvData` to process the environment data before the callback function returns; and call `MoveToCellLibrary` to move the Cell to the Cell Library of the realm.

*[OnStartIdle](#)*

Call this fallback function before entering the Idle phase

`void OnStartIdle()`

*[OnIdle](#)*

`void OnIdle()`

*[OnStopIdle](#)*

Call this fallback function before exiting the Idle phase

`void OnStopIdle()`

*[OnRemoteExecute](#)*

Call this callback function for processing when the remote process executes.

`void OnRemoteExecute(struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner,struct StructOfPCProcRemoteBase *Proc)`

this function check the proc locates on remote or not, if at remote, then pack input data and send to remote, suspend and wait for result

**[This function is reserved and has not been implemented yet.]()**

*[OnRequestProcChain](#)*

Call this callback function for get a processchain.

VS_PARAPKGPTR OnRequestProcChain(VS_PARAPKGPTR OutputDataOrProc, VS_PARAPKGPTR InputDataOrProc)

> OutputDataOrProc : output data or proc type
> InputDataOrProc : input data or process set

#### h. Process or process chain execute function

*[RunProc](#)*

`VS_PARAPKGPTR RunProc(void *InputData, void *OutputDataClass, void *ProcOrProcs,...)`

Pchain automatically creates a Cell, adds the input process to the Cell, then passes the Cell to the realm, and then executes.

This function uses the context in which the realm is called. You can create a new realm and call it with the new realm

> * InputData: can be NULL, PCData, or ParaPkg (multiple data)
> * OutputDataClass: can be NULL, PCDataClass, or ParaPkg. **if parameter 'ProcOrProcChain' is a Cell, then OutputDataClass is ignored**
> * The return value is ParaPkg. If there is no element, the execution fails.

ProcOrProcs: Can be PCProc, PCProcChain. Maybe multiple. The relationship between multiple processes is parallel.

For example,

```python
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
    
Result = realm.RunProc(UrlClass('http://www.srplab.com'),None,DownLoadUrlProc)
print(Result)    
```

For input argument number,
```python
@pyproc.DefineAsyncProc('ListFileClass',DiskPathClass,FileNameClass)
def Execute(self,DiskPath) :
  Context = self.Context
    
  localbuf = Context['SelfObj'].GetLocalBuf()
  if Context['SelfObj'].Status == 0 :
    import os
    listfile = os.listdir(DiskPath.value())      
    localbuf[0] = listfile
    localbuf[1] = 0
    
    Context['SelfObj'].Status = 1
    
  Index = localbuf[1]
  if Index >= localbuf[0]._Number :
    return (0,0,None)
    
  Result = localbuf[0][Index]
  localbuf[1] = Index + 1
  return (4,0,FileNameClass(Result))

# return one FileName
result = realm.RunProc(DiskPathClass('e:\\'),FileNameClass,ListFileClass)
print(result)

# return more FileName
result = realm.RunProc(DiskPathClass('e:\\'),(0,FileNameClass),ListFileClass)
print(result)
```

**Note : This function uses Realm's LocalBuf and Cache, but it does not change them and the state of Realm except append log information generated during execution**

*[RunProcEx](#)*

`VS_PARAPKGPTR RunProcEx(void *InputData, void *OutputDataClass, void *ProcOrProcs, ...)`

ProcOrProcs: Can be PCProc, PCProcChain. Maybe multiple. If there are multiple, multiple processes form a process chain in order. Then call the process chain

**Note : This function uses Realm's LocalBuf and Cache, but it does not change them and the state of Realm except append log information generated during execution**

*[RunString](#)*

Execute process or process chain,which are strings in json format.

`VS_PARAPKGPTR RunString(void *InputData, void *OutputDataClass, VS_CHAR *ProcOrProcChain)`

> * InputData: can be NULL, PCData, or ParaPkg (multiple data)
> * OutputDataClass: can be NULL, PCDataClass, or ParaPkg. if parameter 'ProcOrProcChain' is a Cell, then OutputDataClass is ignored
> * The return value is ParaPkg. If there is no element, the execution fails.
> * ProcOrProcChain: Is json string, may be PCProc, PCProcChain

example,

```python
result = realm.RunString(None,None,False,'''{"PackageInfo":[],"ObjectList":[{"ClassName":"BoolProc","ObjectID":"efe388c8-ad13-4156-a15d-2fea3cf727e0","OutputQueue":
[{"DataBaseName":"BoolClass"}],"Type":"PCProc"}]}''')
print(result)
```

**Note : This function uses Realm's LocalBuf and Cache, but it does not change them and the state of Realm except append log information generated during execution**

*[RunStringEx](#)*

`VS_PARAPKGPTR RunStringEx(void *InputData, void *OutputDataClass, VS_PARAPKGPTR ProcOrProcChainPkg)`

ProcOrProcChainPkg is a package converted from json string

**Note : This function uses Realm's LocalBuf and Cache, but it does not change them and the state of Realm except append log information generated during execution**

*[SyncFrom](#)*

Synchronize ScheduleTickCount, and other parameters

`VS_BOOL SyncFrom(struct StructOfPCRealmBase *SourceRealm)`

*Note : This function does not synchronize realm's local buf*


#### k. Object Cache

Used to store objects. Not affected by the Reset function. The SyncFrom function will synchronize the stored object to the current Realm

*[SetCache](#)*

Adding objects to the cache.

`void SetCache(void *Object)`

*[ClearCache](#)*

If the input object is not equal to NULL, the object is removed from the cache. Otherwise, delete all objects in the cache.

`void ClearCache(void *Object)`

*[GetCache](#)*

If the input object class is not equal to NULL, get all instances of the object class. Otherwise, get all objects in the cache.

`VS_PARAPKGPTR GetCache(void *Class)`

*[FindCache](#)*

Find objects by ID.

`void *FindCache(VS_CHAR *UuidString)`

#### L. pchain native version

*[GetVersion](#)*

`VS_PARAPKGPTR GetVersion()`

[Major,Minor,Patch]

*[GetVersionInfo](#)*

`VS_CHAR *GetVersionInfo()`

#### M. Get reject data

*[GetReject](#)*

Get the reject data. The RecordRejectID is the return value of function "RecordReject" of PCProc/PCCell/PCProcChain

`VS_PARAPKGPTR GetReject(VS_CHAR *RecordRejectID);`

*[ClearReject](#)*

Clear the reject data record. The RecordRejectID is the return value of function "RecordReject" of PCProc/PCCell/PCProcChain

If RecordRejectID is NULL or empty string, clear all records.

`void ClearReject(VS_CHAR *RecordRejectID);`

#### M. pchain native version

*[GetPerformanceData](#)*

Get statistics

`VS_PARAPKGPTR GetPerformanceData(VS_BOOL ResetFlag)`

#### N. Capture exception

*[PrintInfo](#)*

`void PrintInfo(VS_CHAR *Info)`

*[PrintException](#)*

`void PrintException(VS_CHAR *Info)`

*[OnException](#)*

Define this callback function. When the realm is executed, the exception information or the information that needs attention is generated by pchain.

Need to call SetRealmStub to receive callbacks

`void OnException(VS_INT32 AlarmLevel,VS_CHAR *Info)`

```python
cleobj = Service.PCRealmStubBase._New()
@cleobj._RegScriptProc_P('OnException')
def cleobj_OnException(SelfObj,AlarmLevel,Info) :
  print(Info)
realm.SetRealmStub(cleobj) 
```

AlarmLevel :
```
1 : Warning
0 : Information
```

*[SetRealmStub](#)*

This function can only be called once, and subsequent calls will failed.

Input parameters can be NULL, or instance of PCRealmStubBase.

`VS_BOOL SetRealmStub(struct StructOfPCRealmStubBase *RealmStubBase)`

This object handles the following callback functions of any realm:

> * void OnException(VS_INT32 AlarmLevel,VS_CHAR *Info);
> * VS_INT32  OnMoreUnAllocatedData(struct StructOfPCRealmBase *PCRealm,void *PCProc);
> * VS_BOOL OnLongLoop(struct StructOfPCRealmBase *PCRealm,void *PCCell, void *PCProc,VS_INT32 LoopCount);
> * VS_BOOL OnLongSuspend(struct StructOfPCRealmBase *PCRealm,void *PCCell, void *PCProc, VS_INT64 SuspendTick);
> * VS_BOOL OnInputInvalid(struct StructOfPCRealmBase *PCRealm,void *PCCell, void *PCProc);
> * VS_BOOL OnLongSourceData(struct StructOfPCRealmBase *PCRealm,void *PCCell, void *PCData);
> * void OnCreateData/OnDestroyData(void *PCData), this callback is called when new data type or instance(call CaptureCreateData with flag true) is created or destroyed
> * void OnCreateProc/OnDestroyProc(void *PCProc), this callback is called when new proc type is defined or instance(call CaptureCreateData with flag true) is created or destroyed
> * void *OnFindByTag(VS_CHAR *Tag)

For other realm callback functions, if the realm is not defined, but the stub is defined, it is handled by the stub object.

> * void OnRunnerBeforeExecuted(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner);
> * void OnRunnerProcBeforeExecuted(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner,struct StructOfPCProcBase *Proc,VS_INT32 Condition);
> * void OnRunnerProcExecuted(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner,struct StructOfPCProcBase *Proc,VS_INT32 ExecuteResult);
> * void OnRunnerExecuted(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner,VS_BOOL WillBeFree);

> * void OnBeforeExecute(struct StructOfPCRealmBase *PCRealm); 
> * void OnOutputDataToEnv(struct StructOfPCRealmBase *PCRealm,void *PCCell, void *PCProc, VS_PARAPKGPTR DataList)
> * VS_BOOL OnCellToBeFinish(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell);
> * void OnCellFinish(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell,VS_BOOL IsSuccess);
> * VS_BOOL OnAfterExecute(struct StructOfPCRealmBase *PCRealm);

> * void OnStartIdle(struct StructOfPCRealmBase *PCRealm);
> * void OnIdle(struct StructOfPCRealmBase *PCRealm);
> * void OnStopIdle(struct StructOfPCRealmBase *PCRealm);

> * void OnRemoteExecute(struct StructOfPCRealmBase *PCRealm,struct StructOfPCCellBase *Cell,struct StructOfPCProcRunnerBase *Runner,struct StructOfPCProcRemoteBase *Proc)

> * VS_PARAPKGPTR OnRequestProcChain(struct StructOfPCRealmBase *PCRealm,VS_PARAPKGPTR OutputPCDataSet, VS_PARAPKGPTR InputDataOrProc)
> * void OnProcPriority(VS_PARAPKGPTR ProcessSet, VS_PARAPKGPTR OutputPriority). ProcessSet contains multiple items, each of which is a ParaPkg, consisting of multiple processes. This callback function calculates the overall priority of multiple processes as a floating point number. The result is returned in OutputPriority. The number of items must be the same as the number of items in ProcessSet.


**[PCRealmStubBase](#)** has following attributes,

> * InitialLiveCount
> * MaxUnAllocatedData
> * MaxSourceDataLength
> * MaxLoopCount
> * MaxSuspendTickCount

> *[GetPerformanceData](#)*
> Returns performance statistics, which is a list of triplets, each of which represents the process type, the sum of the performance values, the number of runs, and the number of error runs
> `VS_PARAPKGPTR GetPerformanceData(VS_BOOL ResetFlag)`

> *[FindSystemPackage](#)*
> Find packages that define data types or process types
> `VS_CHAR *FindSystemPackage(void *DataOrProcType)`


*[GetRealmStub](#)*

`void *GetRealmStub()`

*[SetNodeSet](#)*

Set NodeSet Object, which is instance of NodeSetBase of cnode module for network graph computing

`void SetNodeSet(void *CNodeSet)`

*[GetNodeSet](#)*

Get NodeSet Object

`void *GetNodeSet()`

*[CaptureCreateData](#)*

`void CaptureCreateData(VS_BOOL Flag)`

Set the flag to true, when the data object (not the data type) is created and destroyed, the OnCreateData / OnDestroyData event is generated.

Default value is false.

*[CaptureCreateProc](#)*

`void CaptureCreateProc(VS_BOOL Flag)`

Set the flag to true, when the proc object (not the proc type) is created and destroyed, the OnCreateProc/OnDestroyProc event is generated.

Default value is false.

Create instance of PCRealmStubBase 
---

```python
stub = Service.PCRealmStubBase._New()
or
stub = Service.PCRealmStubBase()
```



















