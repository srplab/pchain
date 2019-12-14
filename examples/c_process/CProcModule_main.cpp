/**********************************************************************
  
  CProcModule_main.cpp
  
  $Author: 
  created at: 2019-5-24, with tool starmodule
  
  Copyright (C) 2005-2019 srplab
  
***********************************************************************/
  
#include "vsopenapi.h"

static class ClassOfSRPInterface *SRPInterface;
static class ClassOfCoreShellInterface *CoreShellInterface;
static void *CAddProcClass;


static VS_INT32 SRPAPI CAddProcClass_ScriptCallBack( void *L );
static VS_BOOL SRPAPI CAddProcClass_LuaFuncFilter(void *Object,void *ForWhichObject,VS_CHAR *FuncName,VS_UWORD Para);
static VS_BOOL SRPAPI CAddProcClass_RegGetValue(void *Object,void *ForWhichObject,VS_CHAR *Name,VS_UWORD Para,VS_BOOL GetAllRawAttributeFlag);
static VS_BOOL SRPAPI CAddProcClass_RegSetValue(void *Object,void *ForWhichObject,VS_CHAR *Name,VS_INT32 Index,VS_UWORD Para);

/*--do not save StarCore,it maybe invalid after function return*/
extern "C" SRPDLLEXPORT VS_BOOL CProcModule_Init2(class ClassOfStarCore *StarCore, struct StructOfVSStarCoreInterfaceTable *InterfaceTable )
{
    class ClassOfBasicSRPInterface *BasicSRPInterface;
    class ClassOfSRPControlInterface *ControlInterface;
    
    //--init star core
    BasicSRPInterface = StarCore ->GetBasicInterface();
    SRPInterface = BasicSRPInterface ->GetSRPInterface(BasicSRPInterface ->QueryActiveService(NULL),"","");
    ControlInterface = BasicSRPInterface ->GetSRPControlInterface();
    CoreShellInterface = (class ClassOfCoreShellInterface *)ControlInterface ->GetCoreShellInterface();
    ControlInterface ->Release();
    
	void *PCProcBase = SRPInterface->GetObjectEx(NULL, "PCProcBase");
	void *NumberClass = SRPInterface->GetObjectEx(NULL, "NumberClass");
	if (PCProcBase == NULL || NumberClass == NULL) {
		SRPInterface->ProcessError(VSFAULT_WARNING, __FILE__, __LINE__, "load CProcModule failed, can not find class PCProcBase and NumberClass");
		SRPInterface->Release();
		CoreShellInterface->Release();
		return VS_FALSE;
	}

    CAddProcClass = SRPInterface -> MallocObjectL(SRPInterface->GetIDEx(PCProcBase),0,NULL);
    SRPInterface -> SetName( CAddProcClass, "CAddProcClass");
	/*--create input and output*/
	if ((VS_BOOL)SRPInterface->ScriptCall(CAddProcClass, NULL, "InputFrom", "(oo)z", NumberClass, NumberClass) == VS_FALSE) {
		SRPInterface->ProcessError(VSFAULT_WARNING, __FILE__, __LINE__, "load CProcModule failed, call function InputFrom failed");
		SRPInterface->FreeObject(CAddProcClass);
		SRPInterface->Release();
		CoreShellInterface->Release();
		return VS_FALSE;
	}
	if ((VS_BOOL)SRPInterface->ScriptCall(CAddProcClass, NULL, "OutputFrom", "(o)z", NumberClass) == VS_FALSE) {
		SRPInterface->ProcessError(VSFAULT_WARNING, __FILE__, __LINE__, "load CProcModule failed, call function OutputFrom failed");
		SRPInterface->FreeObject(CAddProcClass);
		SRPInterface->Release();
		CoreShellInterface->Release();
		return VS_FALSE;
	}
    SRPInterface -> RegLuaFunc( CAddProcClass, NULL, (void*)CAddProcClass_ScriptCallBack, (VS_UWORD)0 );
    SRPInterface -> RegLuaFuncFilter(CAddProcClass,CAddProcClass_LuaFuncFilter,(VS_UWORD)0);
    SRPInterface -> RegLuaGetValueFunc(CAddProcClass,CAddProcClass_RegGetValue,(VS_UWORD)0 );
    SRPInterface -> RegLuaSetValueFunc(CAddProcClass,CAddProcClass_RegSetValue,(VS_UWORD)0 );
    
    return VS_TRUE;
}

extern "C" SRPDLLEXPORT void CProcModule_Term2(class ClassOfStarCore *StarCore, struct StructOfVSStarCoreInterfaceTable *InterfaceTable)
{
    if( SRPInterface == NULL )
        return;
    SRPInterface -> FreeObject( CAddProcClass );
    SRPInterface -> Release();
    CoreShellInterface ->Release();
    return;
}
extern "C" SRPDLLEXPORT VS_FUNCTION_TABLE *CProcModule_GetExportFunctionTable( )
{
    static VS_FUNCTION_TABLE FuncPtr[3];

    strcpy(FuncPtr[0].FunctionName,"CProcModule_Init2");
    FuncPtr[0].FunctionAddr = (void *)CProcModule_Init2;
    strcpy(FuncPtr[1].FunctionName,"CProcModule_Term2");
    FuncPtr[1].FunctionAddr = (void *)CProcModule_Term2;
    FuncPtr[2].FunctionName[0] = 0;
    FuncPtr[2].FunctionAddr = NULL;
    return (VS_FUNCTION_TABLE *)FuncPtr;
}
static VS_BOOL SRPAPI CAddProcClass_LuaFuncFilter(void *Object,void *ForWhichObject,VS_CHAR *FuncName,VS_UWORD Para)
{
    if( strcmp(FuncName,"Execute") == 0 )
        return VS_TRUE;
    return VS_FALSE;
}
static VS_INT32 CAddProcClass_ScriptCallBack( void *L )
{
    void *Object;
    VS_CHAR *ScriptName;
    
    ScriptName = SRPInterface -> LuaToString( SRPInterface -> LuaUpValueIndex(3) );
    Object = SRPInterface -> LuaToObject(1);
    /*first input parameter is started at index 2 */
    if( strcmp(ScriptName,"Execute") == 0 ){
		void *RealmObject = SRPInterface->LuaToObject(2);
		void *CellObject = SRPInterface->LuaToObject(3);
        /*--get input*/
		VS_PARAPKGPTR InputPara = (VS_PARAPKGPTR)SRPInterface->ScriptCall(Object, NULL, "InputToParaPkg", "()p");
		if (InputPara == NULL) {
			/*--failed*/
			SRPInterface->LuaPushInt(-1);
			return 1;
		}
		void *InputData1 = InputPara->GetObject(0);
		void *InputData2 = InputPara->GetObject(1);
		if (InputData1 == NULL || InputData2 == NULL) {
			/*--request more data*/
			SRPInterface->LuaPushInt(2);
			return 1;
		}
		VS_PARAPKGPTR InputData1_ParaPkg = (VS_PARAPKGPTR)SRPInterface->ScriptCall(InputData1, NULL, "GetDataBuf", "()p");
		VS_PARAPKGPTR InputData2_ParaPkg = (VS_PARAPKGPTR)SRPInterface->ScriptCall(InputData2, NULL, "GetDataBuf", "()p");
		VS_DOUBLE Result = InputData1_ParaPkg->GetFloat(0) + InputData2_ParaPkg->GetFloat(0);

		void *NumberClass = SRPInterface->GetObjectEx(NULL, "NumberClass");
		void *OutputData = (void *)SRPInterface->ScriptCall(NumberClass, NULL, "Create", "(d)o", Result);
		if(OutputData != NULL )
			SRPInterface->ScriptCall(Object, NULL, "AddOutputData", "(o)", OutputData);

		SRPInterface->ScriptCall(Object, NULL, "AcceptInput", "(o)", NULL);

		SRPInterface->ScriptCall(CellObject, NULL, "Finish", "()");

		SRPInterface->LuaPushInt(0);
        return 1;
    }
    return 0;
}
static VS_BOOL CAddProcClass_RegGetValue(void *Object,void *ForWhichObject,VS_CHAR *Name,VS_UWORD Para,VS_BOOL GetAllRawAttributeFlag)
{
/*
    if( stricmp(Name, "Version" ) == 0 ){
        SRPInterface -> LuaPushString("1.0.0");
        return VS_TRUE;
    }
*/
    return VS_FALSE;
}
static VS_BOOL SRPAPI CAddProcClass_RegSetValue(void *Object,void *ForWhichObject,VS_CHAR *Name,VS_INT32 Index,VS_UWORD Para)
{
    return VS_FALSE;
}
