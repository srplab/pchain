<h1 align="center">PCBufDataBase</h1>

The base classes for data management are PCDataBase,PCDataSetBase,PCObjectDataBase and PCBufDataBase. PCDataSetBase and PCObjectDataBase inherits the methods in PCDataBase.   

PCBufDataBase is used to hold a parapkg.

**Note: The PCBufDataBase should be got via any PCDataBase instance.**

define buf data anagement type
------

```python
bufdataclass = Service.PCDataBase.GetBufDataBase().CreateType('bufdataclass')
```

create buf data management instance
------

```python
parapkg = Service._ServiceGroup._NewParaPkg(12,'22222')
d1 = bufdataclass.Create(parapkg)
or
d1 = bufdataclass(parapkg)
# create instance of instance
e = d1()
```

Functions supported by buf data management object
------

*[Create](#)*

create a new buf data instance

`void *Create(VS_PARAPKGPTR ParaPkg)`







