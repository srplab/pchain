<h1 align="center">PCRuleBase</h1>

The base classes for rule management are PCRuleBase. 

The rule object is used to record and describe a rule. The core of the rule is to store the buffer related to the rule. The buffer can store the underlying data type, such as: integer, bool type, string, etc., and can also store data objects. Object and process chain objects.
The structure of the rule object store is defined by rules
Rule objects can be converted to json strings, or json strings can be converted to rule objects.

*[The properties of the rule object and the functions provided are still in the early stages and are still under study.](#)*

Define new type or create instance of PCRuleBase 
---

```python

#define new type
myruletype = Service.PCRuleBase.CreateType('myruletype')
myruletype_sub = myruletype.CreateType('myruletype_sub')

#create instance
rule = myruletype.Create() / myruletype.Create(uuid)
or
rule = myruletype() / myruletype(uuid)
```

Functions supported by rule management objects
---

#### a. basic function

*[GetRuleBuf](#)*

Get the buffer of the rule.

`VS_PARAPKGPTR GetRuleBuf()`

*[SaveTo](#)*

Save the rule to the parameter package, which can be converted to a json string by the _ToJSon() function.

`VS_BOOL SaveTo(VS_PARAPKGPTR ValueBuf)`

The json string contains both PackageInfo and Value.
PackageInfo is a dependent package, and Value is a numeric value.

```text
{
	"PackageInfo": [],
	"Value": [
		{
			"Type": 4,
			"Value": "wwwee"
		},
		{
			"Type": 2,
			"Value": 56.678
		},
		{
			"Type": 7,
			"BaseClass": "PCDataBaseClass",
			"Value": {
				"ClassName": "MyData",
				"IsClass": false,
				"Value": [
					{
						"Type": 4,
						"Value": "234"
					},
					{
						"Type": 2,
						"Value": 5567.76
					}
				]
			}
		},
		{
			"Type": 7,
			"BaseClass": "PCDataBaseClass",
			"Value": {
				"ClassName": "PCDataBase",
				"IsClass": true
			}
		},
		[
			"Type",
			7,
			"BaseClass",
			"PCProcBaseClass",
			"Value",
			{
				"ClassName": "NumberProc3Proc",
				"ObjectID": "b3bdf405-e043-48d4-91a2-9d1a2ba3ff20",
				"InputQueue": [
					{
						"RequestNumber": 1,
						"IsOnlyDirect": false,
						"IsSlave": false,
						"DataBaseName": "NumberClass"
					}
				],
				"Type": "PCProc"
			}
		],
		{
			"Type": 7,
			"BaseClass": "PCDataBaseClass",
			"Value": {
				"ClassName": "NumberClass",
				"IsClass": false,
				"Value": "77777.8888"
			}
		}
	]
}

```

*[LoadFrom](#)*

Restore the rules from the parameter package, the contents of the parameter package from the json string, through the _FromJSon (str) function

`void *LoadFrom(VS_PARAPKGPTR ValueBuf)`

*[This function does not process PackageInfo and requires an external procedure to handle it.](#)*
Load the package using the loaderpackage function of the loader

```python
  Result = ProcChainPkg._FromJSon(PackageJSon)
  
  from pchain import loader
  loader.loadobjectpackage(ProcChainPkg)
```  

*[SaveToJSonPkg](#)*

Store a parameter package as a parameter package that can be converted to a json string

`VS_PARAPKGPTR SaveToJSonPkg(VS_PARAPKGPTR Buf)`

*[LoadFromJSonPkg](#)*

The parameter package converted from the json string is restored to the original parameter package.

`VS_PARAPKGPTR LoadFromJSonPkg(VS_PARAPKGPTR JSonPkg)`

*[Equals](#)*

Return true if the two rules are equal, false otherwise.

`VS_BOOL Equals(struct StructOfPCRuleBase *PCRule)`

*[OnApproved](#)*

Callback function, this rule is validated by PCData or PCProc

`void OnApproved(void *ByPCDataOrProc)`

*[OnDisapproved](#)*

Callback function, this rule is invalidated by PCData or PCProc

`void OnDisapproved(void *ByPCDataOrProc)`

*[OnBeforeFree](#)*

Callback function, before free

`void OnBeforeFree()`

*[Create](#)*

Create an instance of the rule, you can specify the ID of the rule instance

The input parameter ObjectID can be NULL or ""

`void *Create(VS_CHAR *ObjectID)`

*[CreateType](#)*

Create a rule type

`void *CreateType(VS_CHAR *TypeName)`

*[GetRuleType](#)*

Get the type object of the rule

`void *GetRuleType())`

*[CollectType](#)*

Get a list of rules with IsType true. Usually a direct instance of PCRuleBase, IsType is true.

`VS_PARAPKGPTR CollectType()`











