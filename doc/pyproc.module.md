<h1 align="center">Define and Use Proc Object with Python</h1>

The procedure class is exported from PCPyProcClass and defines the Execute function. The parameters of the function must be CLE objects or PCPyDataClass objects.

The result returned by the Execute function may be a triple (value, inputprocess, returnvalue) or returnvalue or None. if result is returnvalue or None, it equals to (0,1,returnvalue).
Where value is an int type, defined as follows

```python
<0 : failed
==0 : finish
==1 : suspend
==2 : need more input
==3 : need new input
>=4 : next execute delay time, the time is (value-4)ms
```

InputProcess is an integer defined as follows:

```python
-1 : Reject all Input
==0 : do nothing
1 : Accept all input
```

Result is the actual return value, which can be a single data, or a tuple (multiple data).
The result must be a Cle object, or an instance of PCPyDataClass and its subclasses.

The self object has properties 'Context', indicating the context of the currently executing. 

```python
SelfObj: CLE object corresponding to this process
Realm : the current Reaml object
Cell: current Cell object. **[may be NULL](#)**
Runner: Current Runner object. **[may be NULL](#)**

self.Context = {'SelfObj':SelfObj,'Realm':Realm,'Cell':Cell,'Runner':Runner}

if context is used, it should be saved with local variable, such as 

class NumberProc2(PCPyProcClass) :
  def Execute(self,num) : 
    Context = self.Context
```

After the process definition is completed, it must be registered by the pyproc.Register function. The first parameter is the class, the second parameter is the object namespace, and the third parameter is the tuple, which is used to describe the type of each input, and the input. Corresponding to the number, the fourth parameter is a tuple, which is used to describe the type of output.

Define Proc Class
---

**[First Method](#)**

Define a subclass of PCPyProcClass and then register it, for example:

```python
from pchain import pyproc
from pchain.pyproc import PCPyProcClass

class NumberProc2(PCPyProcClass) :
  def Execute(self,num) :  
    Context = self.Context
    if num.value() > 0 :  
      return (0,1,(NumberClass(num.value()),NumberStepClass(0)))
    else :
      return (0,1,(NumberStepClass(10)))
pyproc.Register(NumberProc2,(NumberClass),(NumberClass,NumberStepClass))

```

* using NumberProc2.GetType() to get the correspoding cle type object 
* using GetType() to get the correspoding cle type object of instance

**[Second Method](#)**

```python
pyproc.DefineProc("NumberProc2",(NumberClass),(NumberClass),PyFunc)
pyproc.DefineRawProc("NumberProc2",(NumberClass),(NumberClass),PyFunc)
```

This method can only encapsulate simple python functions and can only output one result. Every execution must be completed.


Using Proc Object
---

Obtain the corresponding CLE object via the Wrap function for pchain. You can also get the process object associated with a CLE object through the pyproc.UnWrap function.

For Example,

```python
proc1 = NumberProc2().Wrap()

```

Using local buf of proc instance
---

default value is None

```python
proc = NumberProc2()
proc.LocalBuf = []
```

for cle object which wrap the python proc instance

```python
cleobj = NumberProc2().Wrap()
proc = pyproc.UnWrap(cleobj)
proc.LocalBuf = []
```