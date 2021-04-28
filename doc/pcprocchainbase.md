<h1 align="center">PCProcChainBase</h1>

The base classes for process management are PCProcBase, PCCellBase, PCProcChainBase, and PCProcRemoteBase. Usually use PCProcBase. 

**PCCellBase** and **PCProcRemoteBase** inherit the methods and properties of PCProcBase. PCProcRemoteBase is a remotely executed process class that is not fully supported in the current release. 

**PCProcChainBase** is a process chain consisting of multiple processes that contain a starting process and an ending process that are connected together to perform a specific function. A single process can also be used as a process chain. The process chain is the basis of scheduling. At runtime, the executable object Runner is created according to the process chain, and then the data object is assigned to the Runner, and each process in the Runner is executed in turn. 

*[The process chain should be placed in the Cell](#)*

Create instance of PCProcChainBase 
---

```python
chain = Service.PCProcChainBase._New()
or
chain = Service.PCProcChainBase()
```

Propertiess supported by PCProcChainBase
---

*[PCProcStart : VS_UUID(string)](#)*

ID of the first process

Functions supported by PCProcChain management objects
---

#### a. basic function

*[IsType](#)*

`VS_BOOL IsType()`

*[GetType](#)*

Get the type object of the process chain.

`void *GetType()`

*[GetTypeName](#)*

return type name.

`VS_CHAR *GetTypeName()`

*[GetTag](#)*

Return the string after the process chain object is stored.

Tag is a string of 40 characters

**[Objects with same type and same tag should be considered as the same object](#)**

`VS_CHAR *GetTag()`

*[GetTagLabel](#)*

return 'chain_PCProcChainBase'

`VS_CHAR *GetTagLabel()`

*[IsInstance](#)*

the data object is instance of input Type

`VS_BOOL IsInstance(void *Type)`

*[Wrap](#)*

This function returns itself, for compatibility with the pydata calling method.

`void *Wrap()`

*[FromParaPkg](#)*

Create a process chain in order according to the process objects in the package.
This function will clear the existing process objects in the process chain.

`VS_BOOL FromParaPkg(VS_PARAPKGPTR Para)`

*[FromPara](#)*

Create a process chain in order based on the input process object
This function will clear the existing process objects in the process chain.

`VS_BOOL FromPara(void *Proc0,void *Proc1,...)`

*[ToParaPkg](#)*

Get a list of process objects in the process chain.

`VS_PARAPKGPTR ToParaPkg()`

*[AddChildProcChain](#)*

Add a sub-process chain

`VS_BOOL AddChildProcChain(struct StructOfPCProcBase *PCProcParent,void *Child,struct StructOfPCProcBase *PCProcNext)`

> * PCProcParent : Parent process object, cannot be NULL
> * Child : Can be a process or process chain
> * PCProcNext : The next process pointed to by the process chain should not be NULL. Otherwise the output object of the sub-process chain will be placed in the environment

*[GetFirstProc](#)*

Get the first process in the process chain.

`struct StructOfPCProcBase *GetFirstProc()`

*[GetLastProc](#)*

Get the last process in the process chain.

`struct StructOfPCProcBase *GetLastProc()`

*[Append](#)*

Add process or process chain at the tail.

`VS_BOOL Append(void *ProcOrProcChain)`

**If ProcOrProcChain is a process chain, a cell will be created and encapsulate the process chain in the Cell.**

*[Equals](#)*

Determine if the two process chains are the same.

`VS_BOOL Equals(struct StructOfPCProcChainBase *PCProcChain)`

*[Find](#)*

The lookup process starts with FirstPCProc, the end process is the process chain of LastPCProc, and FirstPCProc and LastPCProc can be NULL.

`VS_PARAPKGPTR Find(struct StructOfPCProcBase *FirstPCProc, struct StructOfPCProcBase *LastPCProc)`


*[IsOnlyOneProc](#)*

This procchain has only one process.

`VS_BOOL IsOnlyOneProc()`

*[GetSignature](#)*

Reserved, used to verify identity of the process in the future

`VS_CHAR *GetSignature()`

*[RegCallBack](#)*

Set the callback, the currently supported callback is OnFreeCallback.

```python
freecallbackobj = Service._New()
@freecallbackobj._RegScriptProc_P('OnFreeCallback')
def func(CleObj,WhichObj) :
  print(str(WhichObj),'   ',str(WhichObj.GetTag()), '  isfreed')
Service.PCProcChainBase.RegCallBack(freecallbackobj);
```

`void RegCallBack(void *TargetObject)`

*[UnRegCallBack](#)*

Remove the callback

*[RecordReject](#)*

If Flag is true(default is false), the reject data will be recorded, and can be get using realm's GetReject function.

The return value is RecordRejectID.

`VS_CHAR *RecordReject(VS_BOOL Flag)`






