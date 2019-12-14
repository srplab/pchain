<h1 align="center">PCDataSetBase</h1>

The base classes for data management are PCDataBase,PCDataSetBase and PCObjectDataBase. PCDataSetBase inherits the methods in PCDataBase.  

PCDataSetBase is used to manage a set of data objects

**Note: The PCDataSetBase should be got via any PCDataBase instance.**

define data set management type
------

```python
datasettype = Service.PCDataBase.GetDataSetBase().CreateType('datasetclass',None)
```

create data set management instance
------

```python
set1 = datasettype.Create(...)
or
set1 = datasettype(...)
# create instance of instance
a = set1()
```

Input parameter may be parapkg which is list of data objects, or multiple data objects.

Functions supported by data set management object
------

*[AddData](#)*

Add a new data object in the dataset.

`void AddData(struct StructOfPCDataBase *PCData)`

example,
`set1.AddDataObject(xxx)`


*[RemoveData](#)*

Remove data objects from the dataset

`void RemoveData(struct StructOfPCDataBase *PCData)`

*[GetData](#)*

The data object in the dataset must belong to realm, otherwise the function returns an empty dataset. This function returns a list of data objects in the order they appear in the realm.

`VS_PARAPKGPTR GetData()`

*If you don't care about the order, you can use GetDataBuf to get a list of data objects.*

*[IsSubSet](#)*

The input dataset is equal to this dataset, or is a subset of it

`VS_BOOL IsSubSet(void *PCDataSet)`

*[GetDataBase](#)*

Get the data type stored in the set

`void *GetDataBase()`

*[Create](#)*

Create an instance, the input can be a parapkg or multiple data objects. If the collection has a DataBase set, the type of the input data object must be DataBase

`void *Create(...)`

*[CreateType](#)*

Create a collection type, the input parameters are the name of the type and the data type, where the data type can be NULL

`void *CreateType(VS_CHAR *TypeName,void *DataBase)`

*[RunString](#)*

Each data in the set is used as input to execute the process string. If there are multiple output results, only the first one is returned. For more complicated, please use RunString of Realm.

Returns ParaPkg, the number of results contained is the same as the number and order of objects in the collection. If an error occurs, ParaPkg does not contain any objects.

`VS_PARAPKGPTR RunString(VS_CHAR *ProcOrProcChain)`

*[RunProc](#)*

Each data in the set is used as input to execute the process. If there are multiple output results, only the first one is returned. For more complicated, please use RunProc of Realm.

Returns ParaPkg, the number of results contained is the same as the number and order of objects in the collection. If an error occurs, ParaPkg does not contain any objects.

`VS_PARAPKGPTR RunProc(void *ProcOrProcChain)`





