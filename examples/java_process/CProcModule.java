///**********************************************************************
//  
//  CProcModule.java
//  
//  $Compile: javac CProcModule.java
//  created at: 2019-5-25, with tool starmodule
//  
//  Copyright (C) 2005-2019 srplab
//  
//***********************************************************************/
  
import com.srplab.www.starcore.*;
	
public class CProcModule{
    public static void StarCoreScript_Init(String[] args) throws Exception{
        StarCoreFactory starcore= StarCoreFactory.GetFactory();
        StarSrvGroupClass SrvGroup = starcore._GetSrvGroup(0);
        final StarServiceClass Service = SrvGroup._GetService("","");
        
        StarObjectClass PCProcBase = Service._GetObject("PCProcBase");
        StarObjectClass NumberClass = Service._GetObject("NumberClass");
        StarObjectClass CAddProcClass_Obj=PCProcBase._New("CAddProcClass");
        /*--create input and output*/
        if( CAddProcClass_Obj._Callbool("InputFrom",NumberClass,NumberClass) == false )
            throw new Exception("failed");
        if( CAddProcClass_Obj._Callbool("OutputFrom",NumberClass) == false )
            throw new Exception("failed");
        
        CAddProcClass_Obj._RegScriptProc_P("Execute", new StarObjectScriptProcInterface() {
            public Object Invoke(Object In_CleObject, Object[] EventParas)
            {
            	  StarObjectClass CleObject = (StarObjectClass)In_CleObject;
            	  StarObjectClass RealmObject = (StarObjectClass)EventParas[0];
            	  StarObjectClass CellObject = (StarObjectClass)EventParas[1];
            	  
            	  StarParaPkgClass InputPara = (StarParaPkgClass)CleObject._Call("InputToParaPkg");
            	  if( InputPara == null )
            	    return -1;
            	  StarObjectClass InputData1 = (StarObjectClass)InputPara._Get(0);
            	  StarObjectClass InputData2 = (StarObjectClass)InputPara._Get(1);
            	  if( InputData1 == null || InputData2 == null )
            	      return 2;
            	  StarParaPkgClass InputData1_ParaPkg = (StarParaPkgClass)InputData1._Call("GetDataBuf");
            	  StarParaPkgClass InputData2_ParaPkg = (StarParaPkgClass)InputData2._Call("GetDataBuf");
            	  
            	  double Result = InputData1_ParaPkg._Getdouble(0) + InputData2_ParaPkg._Getdouble(0);
            	  
            	  CleObject._Call("ClearOutputData");
            	  StarObjectClass NumberClass = (StarObjectClass)Service._GetObject("NumberClass");
            	  StarObjectClass OutputData = (StarObjectClass)NumberClass._Call("Create",Result);
            	  
            	  if( OutputData != null )
            	      CleObject._Call("AddOutputData",OutputData);
            	  CleObject._Call("AcceptInput");
            	  
            	  CellObject._Call("Finish");
            	  
                return 0;
            }
        });
    }
}
