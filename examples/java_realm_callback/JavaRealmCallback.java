///**********************************************************************
//  
//  JavaRealmCallback.java
//  
//  $Compile: javac JavaRealmCallback.java
//  created at: 2019-5-28, with tool starmodule
//  
//  Copyright (C) 2005-2019 srplab
//  
//***********************************************************************/
  
import com.srplab.www.starcore.*;
import java.util.Iterator;
	
public class JavaRealmCallback{
    public static void StarCoreScript_Init(String[] args){
        StarCoreFactory starcore= StarCoreFactory.GetFactory();
        StarSrvGroupClass SrvGroup = starcore._GetSrvGroup(0);
        final StarServiceClass Service = SrvGroup._GetService("","");
        
        final StarObjectClass PCRealmBase = Service._GetObject("PCRealmBase");
        final StarObjectClass JavaRealmClass_Obj=PCRealmBase._New("JavaRealmClass");
        JavaRealmClass_Obj._RegScriptProc_P("OnBeforeExecute", new StarObjectScriptProcInterface() {
            public Object Invoke(Object CleObject, Object[] EventParas)
            {
            	  StarObjectClass PCRealm = (StarObjectClass)CleObject;
            	  StarParaPkgClass EnvData = (StarParaPkgClass)PCRealm._Call("GetEnvDataQueue");
            	  
            	  StarObjectClass StringClass = (StarObjectClass)Service._GetObject("StringClass");
            	  StarObjectClass PCCellBase = (StarObjectClass)Service._GetObject("PCCellBase");
            	  StarObjectClass LengthProc = (StarObjectClass)Service._GetObject("LengthProc");
            	  for (Iterator iter = EnvData._Iterator(); iter.hasNext();) { 
            	  	Object data = iter.next();
            	  	if( StringClass._IsInst((StarObjectClass)data) == true ){
            	  	  StarObjectClass newcell = PCCellBase._New();
                    newcell._Call("CaptureEnvData",PCRealm,data); 
                    newcell._Call("AddProc",LengthProc);
                    PCRealm._Call("AddCell",newcell);
            	  	}
            	  }
                return null;
            }
        });
        JavaRealmClass_Obj._RegScriptProc_P("OnCellFinish", new StarObjectScriptProcInterface() {
            public Object Invoke(Object CleObject, Object[] EventParas)
            {
            	  StarObjectClass PCRealm = (StarObjectClass)CleObject;
            	  StarObjectClass PCCell = (StarObjectClass)EventParas[0];
            	  boolean IsSuccess = (boolean)EventParas[1];
            	  
            	  PCRealm._Call("ProcessCellEnvData",PCCell,IsSuccess);
            	  PCRealm._Call("RemoveCell",PCCell);
            	  return null;
            }
        });       
    }
}
