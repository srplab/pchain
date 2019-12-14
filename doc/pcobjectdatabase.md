<h1 align="center">PCObjectDataBase</h1>

The base classes for data management are PCDataBase,PCDataSetBase,PCObjectDataBase and PCBufDataBase. PCDataSetBase and PCObjectDataBase inherits the methods in PCDataBase.   

PCObjectDataBase is used to hold an cle object, may be a proc, cell, or data.

**Note: The PCObjectDataBase should be got via any PCDataBase instance.**

define object data anagement type

------

```python
objectdataclass = Service.PCDataBase.GetObjectDataBase().CreateType('objectdataclass')
```

create object data management instance
------

```python
d1 = objectdataclass.Create(object)
or
d1 = objectdataclass(object)
# create instance of instance
a = d1()
```

Functions supported by object data management object
------

*[Create](#)*

create a new object data instance

`void *Create(void *Object)`

*[GetObject](#)*

get the cle object

`void *GetObject()`







