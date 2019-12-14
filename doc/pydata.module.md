<h1 align="center">Define and Use Data Object with Python</h1>

The data processed by pchain is all objects, and the object class is a subclass derived from PCPyDataClass. This subclass may override these functions: Load, Save, ToString, ToParaPkg, Dup and Equals. Where Load is used to recover from a string, the method must be defined as a static method of the subclass; Save is used to store the data object as a string; "Dup" function returns a copy; ToString returns a string for display; ToParaPkg change data to parapkg; Equals returns True if two instance's value are equal.

PCPyDataClass encapsulates a python object (which can be an integer, a string, an instance of a class, etc.), provided when the instance is created, and gets the wrapped python object via the value() function.

```python
class PCPyDataClass :
  def __init__(self,val) :
    self.val = val
    
  ...
  
  def value(self) :
    return self.val    
```

After the data class is defined, you need to call the pydata.Register function to register. When registering, you can specify the namespace of the data class. The namespace is an instance of StarObjectSpace, which can be created by StarObjectSpace._New (the name of the namespace).
The object passed to the pchain needs to be encapsulated into a cle object, which is returned by the data object's function Wrap.

Define Data Class
---

Define a subclass of PCPyDataClass and then register it, for example:

```python
from pchain import pydata
from pchain.pydata import PCPyDataClass

class NumberClass(PCPyDataClass) :
  pass
pydata.Register(NumberClass)  

```

* using NumberClass.GetType() to get the correspoding cle type object 
* using GetType() to get the correspoding cle type object of instance

**[Another method : Using DefineType/DefineTypeEx/DefineSubType](#)**

> * DefineType : DefineType(tpname,rawtype=None), rawtype is a python type or class
> * DefineSubType : DefineSubType(parenttype,tpname,rawtype = None), rawtype is a python type or class
> * DefineTypeEx : DefineType(datatype,tpname,rawtype=None), rawtype is a python type or class. datatype is the data base type which has properties 

```python
pydata.DefineType('DiskPathClass',None)
pydata.DefineType('Rawlass',type(''))

class myclass :
  pass 
class mysubclass(myclass) :
  pass  
  
pydata.DefineType('RawMyClass',myclass)
pydata.DefineSubType(RawMyClass,'RawMySubClass',mysubclass)

inst = RawMySubClass(mysubclass())
```

```python
newtype = Service.PCDataBase.CreateType('DataHasProperty')
newtype.CreateProperty('Attr1',libstarpy.TYPE_CHARPTR,'')
pydata.DefineTypeEx(newtype,'NumberClass')

re = NumberClass(val)
re.Wrap().Attr1 = 'From input'
```

The data management type defined by this method, using the following template

```python
class {0}(PCPySimpleDataClass) :
    rawtype = pyrawtype
    
    def __init__(self,val) :
      if self.rawtype == None :
        self.val = val
      else :
        import inspect
        if (inspect.isclass(self.rawtype) == True and isinstance(val,self.rawtype)) or (type(val) == self.rawtype) :
          self.val = val
        else :     
          raise Exception('create data instance failed, input ',val,'is not instance of ',self.rawtype)          
                      
pydata._Register({0},StarNameSpace) 
```

**The data management type defined by this method does not support ToParaPkg and Load, therefore it can not access from other language. [You can override these two functions dynamically](#)**

**[Note: Save function must be add corresponding to Load](#)**

for example,

```python
pydata.DefineType('NumberBaseClass',None)
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

Using Data Object
---

Create an instance of the data class, obtain the associated CLE object through the Wrap function, and the application needs to record the returned CLE object to ensure that the object is not garbage collected within the valid range. The returned CLE object can be passed to the pchain.
Through the pydata.UnWrap function, you can get an instance of the data class associated with the CLE object.

For Example,

```python
d1 = NumberClass(-2).Wrap()
d2 = NumberClass(4).Wrap()
d3 = NumberClass(-8).Wrap()

```

