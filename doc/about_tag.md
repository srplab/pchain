<h1 align="center">About Object Tag</h1>

  Data, process, cell, and chain objects has tag and taglabel, which can be obtained by GetTag and GetTabLabel function. Tag is type name or a string of 40 characters. 
  
  Two objects are identical if they have the same tag. The two objects are equal (compared by the function Equals), then their tags must be the same. However, for data object, if the two data objects have the same tag, they are not necessarily equal.
  
  Data objects can be set to signature. The same type, two data objects with the same signature are the same, in this case they have the same Tag.
  
Data, cell, process, and chain can be stored as json strings, or restored from strings. The restored objects are equal to the stored objects and have the same tag.
  
  **[The Tag of the data object may be different for python2 and python3. Need to choose programming using python2 or python3, Or define the Save method for each data management object type.](#)**
  
```python
class Person :
  hair = 'black'
  def __init__(self, name = 'Charlie', age=8):
    self.name = name
    self.age = age
  def say(self, content):
    print(content)
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False   

pydata.DefineType('PersonClass',Person)

# Define procedure types
@pyproc.DefineProc('TestProcClass',None,PersonClass)
def Execute(self) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return None
  return (0,1,None)


data = PersonClass(Person(name='aaaa',age=15))
print('data tag =  ',data.GetTag())
print('data tag label =  ',data.GetTagLabel())

pkg = Service._ServiceGroup._NewParaPkg()
data.SaveTo(pkg)
newdata = Service.PCDataBase.LoadFrom(pkg)

print('load data tag =  ',newdata.GetTag())
print('load data tag label =  ',newdata.GetTagLabel())
print('data == load data ? ',data.Equals(newdata))

TestProc = TestProcClass().Wrap()
print('proc tag =  ',TestProc.GetTag())
print('proc tag label =  ',TestProc.GetTagLabel())


cell1 = Service.PCCellBase._New()
cell1.AddProc(TestProcClass)
print('cell1 tag =  ',cell1.GetTag())
print('cell1 tag label =  ',cell1.GetTagLabel())

cell2 = Service.PCCellBase._New()
cell2.AddProc(TestProcClass)
print('cell2 tag =  ',cell2.GetTag())
print('cell2 tag label =  ',cell2.GetTagLabel())

realm.SaveObject(pkg,cell1)
print(pkg._ToJSon())
load_pkg = realm.LoadObject(pkg,False)
print('load cell1 tag =  ',load_pkg[0].GetTag())
print('load cell1 tag label =  ',load_pkg[0].GetTagLabel())
print('cell1 == load cell1 ? ',cell1.Equals(load_pkg[0]))
print('cell2 == load cell1 ? ',cell2.Equals(load_pkg[0]))
```

output:

```sh
('data tag =  ', '9b952f6fc293cc28f113fcedaad7ab9630f65f49')
('data tag label =  ', 'data_global_PersonClass')
('load data tag =  ', '9b952f6fc293cc28f113fcedaad7ab9630f65f49')
('load data tag label =  ', 'data_global_PersonClass')
('data == load data ? ', True)
('proc tag =  ', 'proc_global_TestProcClass')
('proc tag label =  ', 'proc_global_TestProcClass')
('cell1 tag =  ', '10bb6393d8fd1f4e7914e7320235ff9bbfa2a38f')
('cell1 tag label =  ', 'cell_global_PCCellBase')
('cell2 tag =  ', '10bb6393d8fd1f4e7914e7320235ff9bbfa2a38f')
('cell2 tag label =  ', 'cell_global_PCCellBase')
{"PackageInfo":[],"ObjectList":[{"ClassName":"PCCellBase","ObjectID":"864416da-0cbc-4df7-83d9-6d017d043834","Type":"PCCell","ProcChainQueue":[{"Type":"PCProcChain","PCProcBase":[{"ClassName":"TestProcClass","ObjectID":"f78d1978-f570-4895-8bb6-8d5cda4e3d91","OutputQueue":[{"DataBaseName":"PersonClass"}],"Type":"PCProc"}]}]}]}
('load cell1 tag =  ', '10bb6393d8fd1f4e7914e7320235ff9bbfa2a38f')
('load cell1 tag label =  ', 'cell_global_PCCellBase')
('cell1 == load cell1 ? ', True)
('cell2 == load cell1 ? ', True)
```
  







