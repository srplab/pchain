<h1 align="center">Learning which procedure is 'length'</h1>

This is a simple example of learning which process is associated with the string 'length' by the relationship between the data objects. This example has some specificities, and the method is effective only for this purpose, and is not a widely applicable example. The study of relationships and rules is complex and requires further study of simple methods. 

A set of data objects of the execution process is analyzed. The type of the data object is PCRealmFrameData, which is generated and maintained by pchain. Pchain puts the object generated in the process into the PCRealmFrameData instance. After the pchain processes the input data object, it dispatches the data object to run.

The complete example is in the directory: [examples/studylen_proc.py](../examples/studylen_proc.py)

* Define two data objects: string and integer

```python
pydata.DefineType('StringClass',str)
pydata.DefineType('NumberClass',int)
```

* Two procedures are defined: one is to calculate the length of the string, the other is to convert the string to an integer

```python
@pyproc.DefineProc('MyProc1',StringClass,NumberClass)
def Execute(self,strobj) :
  Context = self.Context
  val = len(strobj.value())
  return (0,1,NumberClass(val))

@pyproc.DefineProc('MyProc2',StringClass,NumberClass)
def Execute(self,strobj) :
  Context = self.Context
  val = 0
  try:
    val = int(strobj.value())
    return (0,1,NumberClass(val))
  except :
    return (0,-1,None)
```

The programmer knows which process is 'length', but how does the computer know? One way is to learn which process is related to 'length' by analyzing the relationship between the data.

The data used for learning is two sets of strings:

```
['qqqwwweee','length','9']
['tttttttt','length','8']
```

Define procedure to process the PCRealmFrameData data object
------

```python
@pyproc.DefineProc('EqualRuleProc',Service.PCRealmFrameData,())
def Execute(self,FrameData) :
    Context = self.Context
    ...
```

Create an instance of the process, join the Cell, and put the Cell into the realm.

```python
cell = Service.PCCellBase._New()
cell.AddProc(MyProc1,MyProc2)
realm.AddCellLibrary(cell)
```

Define the realm callback function 'OnBeforeExecute'. In this callback function, the executed cell will be set according to the data object. If the data object is an instance of PCRealmFrameData at this time, the process instance created above will be executed.

```python
@realm._RegScriptProc_P('OnBeforeExecute')
def realm_OnBeforeExecute(CleObj):
  envdata = CleObj.GetEnvDataQueue()
  for data in envdata :  
    CleObj.EnvDataToCell(data)
  return  
```  

EqualRuleProc processing
------

#### a. step 1

According to the data object in the input dataset, equal objects are grouped into sets, and only dynamically generated data objects are retained in each group.

```python
    sameset = Context['SelfObj'].EqualDataSet(FrameData.ToParaPkg())
    
    #--only handle dynamic generated data object
    sameset_clean = [t for t in sameset if len([x for x in t if x.IsDynamic()]) >= 2]
    if len(sameset_clean) == 0 :
      return None      
```      

#### b. step 2


* Divide all current objects into two groups, one for other process objects and data objects related to equal data objects in the collection, and one for the context object.

```python
#--for simple, here only process sameset_clean[0]
dataset = Context['SelfObj'].SplitDataSet(FrameData.ToParaPkg(),sameset_clean[0], True) 
```    

Related objects may be data objects or process objects. Here it is subdivided into two groups: one is a process object and the other is a data object.

```python
#--Remove redundant data object, If the data object is the output of a process object, the data object is redundant, and the data object is removed
   procset = [t for t in dataset[0] if Service.PCProcBase._IsInst(t)]
        
    #--find source data from output data and procs
    sourceset = []
    for t in dataset[0] :
      if Service.PCDataBase._IsInst(t) :
        for l in procset :
          if t.IsFromProc(l) == True :  # t is output data via proc t
            for m in dataset[0] :
              if Service.PCDataBase._IsInst(m) :
                if t.IsSource(m) :        # add source data of t
                  sourceset.append(m)
```

* For each procedure in the process collection, if a data object in the data collection is rejected as input, the process object is deleted. This method does not have universal significance, apply only to the example

```python
    #If a process rejects a data object as input, it is removed from the process group
    newprocset = []    
    for l in procset :
      IsReject = False
      for t in sourceset :
        if t.IsReject(l) :
          IsReject = True
      if IsReject == False :
        newprocset.append(l)
    procset = newprocset
```    

* The context data object cannot be the output of a procedure in the above procedure collection, and if so, the context data object is deleted

```python
    contextset = []
    for t in dataset[1] :
      if Service.PCDataBase._IsInst(t) :
        isoutputdata = False      
        for l in procset :          
          if t.IsFromProc(l) == True :
            isoutputdata = True
            break
        if isoutputdata == False :
          contextset.append(t)
      else :
        contextset.append(t) 
```        

[After the above processing, three object sets are generated according to the input data object: a process object set, a source data object set, and a context data object set.](#)

```
set1： [MyProc1],[9,qqqwwweee],[length]
set2:  [MyProc1],[8,tttttttt],[length]
```

#### c. step 3

Merged with the previous data set, for the same object, the count is incremented by 1, the average count for each set is calculated, and the object less than the average count is deleted.

If you want to view the code, please refer to the example

Output result:

```
find relation :  [context:length]source:StringClass -> process:MyProc1
```






