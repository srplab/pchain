# -*- coding: utf-8 -*-
"""
    pyproc.py

    :project : pchain
    :date    : 2019-04-09 09:49:21
"""

pyprocypemap = {}

'''    
class PCPyProcResult :
  def __init__(self,returnvalue,processinput,result) :
    self.returnvalue = returnvalue
    self.processinput = processinput
    self.result = result  
'''    
    
PCDataBaseClass = None 
PCProcBaseClass = None 

def _processresult(SelfObj,procname,result,libstarpy,PCPyDataClass) :
  if result == None :
    return -1
  #process output  
  if type(result) == type(()) or type(result) == type([]) : 
    for item in result :
      if isinstance(item,PCPyDataClass) :        
        SelfObj.AddOutputData(item.Wrap())
      else :
        if type(item) == libstarpy.ObjectClass and PCDataBaseClass._IsInst(item) :
          SelfObj.AddOutputData(item)
        else :
          raise Exception('Call '+ procname + ' failed, the output is not subtype of PyDataBaseClass')
          #return -1  #returns type error
  else :
    if isinstance(result,PCPyDataClass) :
      cledata = result.Wrap()
      SelfObj.AddOutputData(cledata)
    else :
      if type(result) == libstarpy.ObjectClass and PCDataBaseClass._IsInst(result) :
        SelfObj.AddOutputData(result)
      else :
        raise Exception('Call '+ procname + ' failed, the output is not subtype of PyDataBaseClass')
        #return -1  #returns type error  

class PCPyProcClass(object) :
  def __init__(self) :
    self.IsType = self._IsType
    self.Wrap = self._Wrap 
    
  def Dup(self) :
    return self.__class__() 
    
  def __getattr__(self, name):
    if name == 'Tag' :
      cle_self = self.Wrap()
      return cle_self.GetTag() 
    elif name == 'TagLabel' :
      cle_self = self.Wrap()
      return cle_self.GetTagLabel()    
    elif name == '_ID' :
      cle_self = self.Wrap()
      return cle_self._ID
    else:
      return self.__getattribute__(name)
    
  @classmethod
  def GetTag(cls) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.GetTag()    
    
  @classmethod
  def GetTagLabel(cls) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.GetTagLabel() 
    
  @classmethod
  def Wrap(cls) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc         
  
  def _Wrap(self) :
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")   
    if Service == None :
      return None        
    if hasattr(self,'cleobjid') == True :
      retobj = Service._GetObject(self.cleobjid)
      if retobj == None :
        pass # restore corresponding cle pcproc object
      else :
        return retobj
  
    cleproc = pyprocypemap.get(self.__class__)  
    if cleproc == None :
      raise Exception('Wrap '+ self.__class__.__name__ + ' failed, it is not registered')
    
    # find the pcproc  
    cleobj = Service._New()
    cleobj._AttachRawObject(self,False)      
    
    newproc = cleproc._New()
    newproc.SetAttachObject(cleobj)

    self.cleobjid = newproc._ID
    
    return newproc

  @classmethod
  def GetType(cls) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc
           
  @classmethod
  def IsPChainRawInstance(cls,which) :
    if isinstance(which,PCPyProcClass) :
      return True
    return False      
    
  def __call__(self, *args):
    return self.__class__.call(*args)
    
  @classmethod    
  def call(cls, *args):
    # call execute? no
    import libstarpy
    import inspect
    from pchain import pydata
    from pchain.pydata import PCPyDataClass
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")  
    
    newin = []
    for item in args :
            
      if type(item) == libstarpy.ObjectClass  :
        if PCDataBaseClass._IsInst(item) == True :
          rawitem = pydata.UnWrap(item)
          if rawitem == None :
            rawitem = item
        else :
          if item._HasRawContext() == True :
            rawitem = item._GetRawObject()
            if isinstance(rawitem,PCPyDataClass) == True :
              pass
            else :
              rawitem = item
          else :
            rawitem = item
      else :
        rawitem = item
      if isinstance(rawitem,PCPyDataClass) :
        newin.append(rawitem.Wrap())
      else :
        if type(rawitem) == libstarpy.ObjectClass and PCDataBaseClass._IsInst(rawitem) == True :
          newin.append(rawitem) 
        else :
          if rawitem == None :
            newin.append(rawitem) 
          else :
            raise Exception('call '+ cls.__name__ + ' failed, input args must be cle object or instance of PCPyDataClass')
    #   
    self_cleobj = cls.GetType()
    result = Service.PCRealmBase.RunProc(newin,self_cleobj.GetOutputType(),self_cleobj)
    if result._Number == 0 :  #failed
      raise Exception('call '+ cls.__name__ + ' failed, RunProc function returns false')
      return None
    else :
      ReturnValue = result
      if SrvGroup._IsParaPkg(ReturnValue) == False :
        if isinstance(ReturnValue,PCPyDataClass) :
          return ReturnValue
        else : 
          if type(ReturnValue) == libstarpy.ObjectClass :
            if PCDataBaseClass._IsInst(ReturnValue) and ReturnValue.HasDataTypeClass() :            
              return pydata.UnWrap(ReturnValue)
            else :
              return ReturnValue
          else :
            if ReturnValue == None :
              return ReturnValue
            else : 
              raise Exception('call '+ cls.__name__ + ' failed, output must be None, or cle object or instance of PCPyDataClass')        
      else :
        if ReturnValue._Number == 0 :
          return None
        else :
          returntuple = []
          for item in ReturnValue._Iterator() :
            if isinstance(item,PCPyDataClass) :
              returntuple.append(item)
            else :
              if type(item) == libstarpy.ObjectClass :
                if PCDataBaseClass._IsInst(item) and item.HasDataTypeClass() :            
                  returntuple.append(pydata.UnWrap(item))
                else :
                  returntuple.append(item)
              else :
                if item == None :
                  returntuple.append(item)
                else : 
                  raise Exception('call '+ cls.__name__ + ' failed, output must be None, or cle object or instance of PCPyDataClass')
          if len(returntuple) == 1 :
            return returntuple[0]
          else :
            return tuple(returntuple)    
    #==end 
    
  @classmethod  
  def DefineMethod(cls,MethodName) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('DefineMethod '+ cls.__name__ + ' failed, it is not registered')
    def CreateDecorator(func):
      cleproc._RegScriptProc_P(MethodName,func)
    return CreateDecorator               

  def GetLocalBuf(self) :
    cle_self = self.Wrap()
    return cle_self.GetLocalBuf()

  def GetSignature(self) :
    cle_self = self.Wrap()
    return cle_self.GetSignature()

  def RejectInput(self,DataObject) :
    cle_self = self.Wrap()
    cle_self.RejectInput(DataObject)

  def AcceptInput(self,DataObject) :
    cle_self = self.Wrap()
    cle_self.AcceptInput(DataObject)

  def RecordReject(self,Flag) :
    cle_self = self.Wrap()
    return cle_self.RecordReject(Flag)    
            
  @classmethod
  def InputQueueToParaPkg(cls) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.InputQueueToParaPkg()

  @classmethod
  def GetInputNumber(cls) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.GetInputNumber()

  @classmethod
  def GetRequestNumber(cls,Index) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.GetRequestNumber(Index)
                    
  def IsFromInternal(self,Index) :
    cle_self = self.Wrap()
    return cle_self.IsFromInternal(Index)    
    
  @classmethod
  def IsSlave(cls,Index) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.IsSlave(Index)      
    
  @classmethod
  def IsMustExist(cls,Index) :
    cleproc = pyprocypemap.get(cls)  
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.IsMustExist(Index)

  @classmethod
  def _to_pydata(cls,returnval) :
    if returnval == None :
      return None  
    from pchain import pydata  
    from pchain.pydata import PCPyDataClass
    val = pydata.UnWrap(returnval)  
    if isinstance(val,PCPyDataClass) == True :      
      return val
    else :
      return returnval

  @classmethod
  def _to_pydatatype(cls,returnval) :
    if returnval == None :
      return None  
    from pchain import pydata  
    from pchain.pydata import PCPyDataClass
    val = pydata.UnWrap(returnval)  
    import libstarpy
    if val == None or type(val) == libstarpy.ObjectClass :
      return returnval
    if val == PCPyDataClass or issubclass(val,PCPyDataClass) == True :   
      return val
    else :
      return returnval

  @classmethod
  def _to_pyproc(cls,returnval) :
    if returnval == None :
      return None
    val = pyproc.UnWrap(returnval)  
    if isinstance(val,PCPyProcClass) == True :      
      return val
    else :
      return returnval  

  def GetMasterInput(self,Index) :
    cle_self = self.Wrap()
    returnval = cle_self.GetMasterInput(Index) 
    if returnval == None :
      return returnval
    return self._to_pydata(returnval)  
    
  def GetMasterInputType(self,Index) :
    cle_self = self.Wrap()
    returnval = cle_self.GetMasterInputType(Index) 
    if returnval == None :
      return returnval
    return self._to_pydatatype(returnval)    

  @classmethod
  def GetInputType(cls,Index) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    returnval = cleproc.GetInputType(Index)
    if returnval == None :
      return returnval
    return cls._to_pydatatype(returnval)

  @classmethod
  def SetInputType(cls,Index,val) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.SetInputType(Index,val)
    
  def IsEnough(self,Index) :
    cle_self = self.Wrap()
    return cle_self.IsEnough(Index)   

  @classmethod
  def GetInputTypeEx(cls,Index,val) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    result = cleproc.GetInputTypeEx()
    returnval = []
    for item in result :
      returnval.append(cls._to_pydatatype(item))
    return returnval
 
  def DataCanBeAsInput(self,PCData,IncludeCellProcChain) :
    cle_self = self.Wrap()
    return cle_self.DataCanBeAsInput(PCData,IncludeCellProcChain)   
            
  def DataCanBeAsOutput(self,PCData,IncludeCellProcChain) :
    cle_self = self.Wrap()
    return cle_self.DataCanBeAsOutput(PCData,IncludeCellProcChain) 
    
  def ProcCanBeAsInput(self,PCProc) :
    cle_self = self.Wrap()
    return cle_self.ProcCanBeAsInput(PCProc) 

  def OutputToParaPkg(self) :
    cle_self = self.Wrap()
    result = cle_self.OutputToParaPkg() 
    returnval = []
    for item in result :
      returnval.append(self._to_pydata(item))
    return returnval

  @classmethod
  def GetOutputNumber(cls) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.GetOutputNumber()

  @classmethod
  def OutputQueueToParaPkg(cls) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.OutputQueueToParaPkg()

  @classmethod
  def OriginOutputQueueToParaPkg(cls) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.OriginOutputQueueToParaPkg()

  @classmethod
  def GetOutputType(cls) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    result = cleproc.GetOutputType()
    returnval = []
    for item in result :
      returnval.append(cls._to_pydatatype(item))
    return returnval

  @classmethod
  def GetOriginOutputType(cls) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    result = cleproc.GetOriginOutputType()
    returnval = []
    for item in result :
      returnval.append(cls._to_pydatatype(item))
    return returnval

  def ClearOutputData(self,DataClass) :
    cle_self = self.Wrap()
    return cle_self.ClearOutputData(DataClass)  
    
  def AddOutputData(self,*args) :
    cle_self = self.Wrap()
    return cle_self.AddOutputData(*args)      
    
  def AddOutputDataEx(self,DataObject,*SourceData) :
    cle_self = self.Wrap()
    return cle_self.AddOutputDataEx(DataObject,*SourceData)  
    
  def GetCell(self) :
    cle_self = self.Wrap()
    return cle_self.GetCell()     
    
  def Suspend(self) :
    cle_self = self.Wrap()
    cle_self.Suspend()        
    
  def Resume(self) :
    cle_self = self.Wrap()
    cle_self.Resume()     

  def Continue(self,Delay) :
    cle_self = self.Wrap()
    cle_self.Continue(Delay)     

  def GetRootProc(self) :
    cle_self = self.Wrap()
    result = cle_self.GetRootProc()    
    return self._to_pyproc(result)
    
  def GetPrevProc(self) :
    cle_self = self.Wrap()
    result = cle_self.GetPrevProc() 
    returnval = []
    for item in result :
      returnval.append(self._to_pyproc(item))
    return returnval
    
  def GetNextProc(self) :
    cle_self = self.Wrap()
    result = cle_self.GetNextProc()    
    return self._to_pyproc(result)    
    
  def IsPrevProcFinish(self,PrevPCProc,PCDataClass) :
    cle_self = self.Wrap()
    return cle_self.IsPrevProcFinish(PrevPCProc,PCDataClass)        
    
  def IsCurrent(self) :
    cle_self = self.Wrap()
    return cle_self.IsCurrent()           
	
  @classmethod    
  def IsType(cls) :
    return True 
  def _IsType(self) :
    cle_self = self.Wrap()
    return cle_self.IsType()        

  @classmethod
  def GetTypeName(cls) :
    cleproc = pyprocypemap.get(cls)
    if cleproc == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cleproc.GetTypeName()
    
  def Equals(self,PCProc) :
    cle_self = self.Wrap()
    return cle_self.Equals(PCProc)   

  def IsInstance(self,PCProc) :
    cle_self = self.Wrap()
    return cle_self.IsInstance(PCProc)

  def RegCallBack(self,TargetObject) :
    cle_self = self.Wrap()
    cle_self.RegCallBack(TargetObject) 

  def UnRegCallBack(self,TargetObject) :
    cle_self = self.Wrap()
    cle_self.UnRegCallBack(TargetObject)

def GetCleType(tp):
  cleproc = pyprocypemap.get(tp)  
  if cleproc == None :
    raise Exception('Wrap '+ tp.__name__ + ' failed, it is not registered')
  return cleproc
  
def Register(tp,InputQueue,OutputQueue) :   
  from pchain import pydata
  from pchain.pydata import PCPyDataClass
  import libstarpy
  import inspect
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  

  global PCDataBaseClass
  if PCDataBaseClass == None :
    PCDataBaseClass = Service.PCDataBase
  global PCProcBaseClass
  if PCProcBaseClass == None :
    PCProcBaseClass = Service.PCProcBase
    
  import inspect
  f = inspect.stack()[1][0]  
  _m_name = f.f_locals['__name__']
  StarNameSpace = None
  if _m_name == None :
    pass
  elif _m_name == '__main__' :
    pass
  else :
    _m_name = _m_name.replace('.','_')
    StarNameSpace = Service._GetObject(_m_name)
    if StarNameSpace == None :
      StarNameSpace = Service.StarObjectSpace._New(_m_name)
    else :
      if Service.StarObjectSpace._IsInst(StarNameSpace) == True : 
        pass
      else :
        raise Exception('Register '+tp.__name__+' failed, there has cle object which is not instance of StarNameSpace named '+_m_name)    
  return _Register(tp,StarNameSpace,InputQueue,OutputQueue)
            
def _Register(tp,StarNameSpace,InputQueue,OutputQueue) :   
  from pchain import pydata
  from pchain.pydata import PCPyDataClass
  import libstarpy
  import inspect
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  

  global PCDataBaseClass
  if PCDataBaseClass == None :
    PCDataBaseClass = Service.PCDataBase
  global PCProcBaseClass
  if PCProcBaseClass == None :
    PCProcBaseClass = Service.PCProcBase
        
  if StarNameSpace == None :
    _allobject = SrvGroup._NewParaPkg()
    Service._GetObjectEx3(tp.__name__,_allobject)
    starspaceobject = Service.StarObjectSpace
    for item in _allobject :
      if starspaceobject.FindSpace(item) == None :
        if item._Name == tp.__name__ :
          _allobject._Free()
          raise Exception('Register '+tp.__name__+' failed, it had been registered before.')
    _allobject._Free()  
  else :
    if type(StarNameSpace) == libstarpy.ObjectClass and Service.StarObjectSpace._IsInst(StarNameSpace) :
      if StarNameSpace.GetObject(tp.__name__) == None :
        pass
      else :
        raise Exception('Register '+tp.__name__+' failed, it had been registered before.')
    else :
      raise Exception('Register '+tp.__name__+' failed, '+str(StarNameSpace)+' is not instance of StarObjectSpace')
  cleproc = pyprocypemap.get(tp)    
  if cleproc == None :
    cleproc = Service.PCProcBase._New(tp.__name__)
    cleproc._LockGC()  # do not free
    #input 
    if InputQueue == None :
      pass
    else :
      if type(InputQueue) == type(()) :
        newin = []
        for item in InputQueue :
          if inspect.isclass(item) and issubclass(item,PCPyDataClass) :
            newin.append(pydata.GetCleType(item))
          else :
            newin.append(item) 
        if len(newin) == 0 :
          pass
        else :          
          cleproc.InputFrom(tuple(newin)) 
      else :
        if inspect.isclass(InputQueue) and issubclass(InputQueue,PCPyDataClass) :
          cleproc.InputFrom(pydata.GetCleType(InputQueue)) 
        else :
          cleproc.InputFrom(InputQueue)
    #--output
    if OutputQueue == None :
      pass
    else :
      if type(OutputQueue) == type(()) :
        newin = []
        for item in OutputQueue :
          if inspect.isclass(item) and issubclass(item,PCPyDataClass) :
            newin.append(pydata.GetCleType(item))
          else :
            newin.append(item)   
        if len(newin) == 0 :
          pass
        else :        
          cleproc.OutputFrom(tuple(newin)) 
      else :
        if inspect.isclass(OutputQueue) and issubclass(OutputQueue,PCPyDataClass) :
          cleproc.OutputFrom(pydata.GetCleType(OutputQueue)) 
        else :
          cleproc.OutputFrom(OutputQueue)
    #register function
    @cleproc._RegScriptProc_P('Execute')
    def cleproc_Execute(SelfObj,Realm,Cell,Runner) :
      from pchain import pydata
      pythonobj = UnWrap(SelfObj)  
      in1 = SelfObj.InputToParaPkg()
      SrvGroup = libstarpy._GetSrvGroup(0)
      pythonobj.Context = {'SelfObj':SelfObj,'Realm':Realm,'Cell':Cell,'Runner':Runner}
      para = []
      for item in in1._Iterator() :        
        if type(item) == libstarpy.ObjectClass and PCDataBaseClass._IsInst(item) and item.HasDataTypeClass() :
          para.append(pydata.UnWrap(item))        
        else :
          if SrvGroup._IsParaPkg(item) == True :
            subitem = []
            for ii in item._Iterator() :
              if type(ii) == libstarpy.ObjectClass and PCDataBaseClass._IsInst(ii) and ii.HasDataTypeClass() :
                subitem.append(pydata.UnWrap(ii)) 
              else :   
                subitem.append(ii)       
            para.append(tuple(subitem))                 
          else :
            para.append(item)
      #call class function
      result = pythonobj.Execute(*para)
      if isinstance(result,tuple) :
        if len(result) == 3 and type(result[0]) == int and type(result[1]) == int :
          if result[1] < 0 :
            SelfObj.RejectInput(None)
          else :
            if result[1] > 0 :
              SelfObj.AcceptInput(None)
        else :
          isresultvalid = True
          for item in result :
            if isinstance(item,PCPyDataClass) :                
              pass
            else :
              isresultvalid = False
          if isresultvalid == False :
            raise Exception('result from proc '+pythonobj.__class__.__name__+' must be tuple (returnvalue,processinput,result)')
          else :
            SelfObj.AcceptInput(None)
            result = (0,1,result)                     
      else :        
        if isinstance(result,PCPyDataClass) :
          SelfObj.AcceptInput(None)          
          result = (0,1,result)
        else :
          if result == None :
            SelfObj.AcceptInput(None)
            result = (0,1,result)          
          else :
            raise Exception('result from proc '+pythonobj.__class__.__name__+' must be tuple (returnvalue,processinput,result)')
      if result[0] < 0 :
        return -1
      else :  
        _processresult(SelfObj,tp.__name__,result[2],libstarpy,PCPyDataClass)
      if result[0] == 0 or result[0] == 1 or result[0] == 2 or result[0] == 3 :
        return result[0]
      else :
        return SelfObj.Continue(result[0]-4)   
      
    #register function
    @cleproc._RegScriptProc_P('_StarCall')
    def cleproc_StarCall(SelfObj,*Args) :
      import libstarpy
      import inspect
      from pchain import pydata
      from pchain.pydata import PCPyDataClass
      SrvGroup = libstarpy._GetSrvGroup(0)
      Service = SrvGroup._GetService("","")  
        
      pythonobj = UnWrap(SelfObj)       
      returntuple = pythonobj(*Args)
      if type(returntuple) == type(()) or type(returntuple) == type([]) :
        ParaPkg = SrvGroup._NewParaPkg()
        for item in returntuple :
          if isinstance(item,PCPyDataClass) :
            ParaPkg[ParaPkg._Number] = item.Wrap()
          else :
            ParaPkg[ParaPkg._Number] = item
        return ParaPkg
      else :
        if isinstance(returntuple,PCPyDataClass) :
          return returntuple.Wrap()
        else :
          return returntuple
        return returntuple
        
    # set attach object
    attach_cleobj = Service._New()
    attach_cleobj._AttachRawObject(tp(),False)      
    cleproc.SetAttachObject(attach_cleobj)
        
    pyprocypemap[tp] = cleproc
    
    if StarNameSpace == None :
      pass
    else :
      StarNameSpace.SetObject(cleproc)  
        
    cleproc.Notify()
    
  return tp
    
def UnWrap(cleobj) :
  import libstarpy
  if type(cleobj) == libstarpy.ObjectClass :
    if PCProcBaseClass._IsInst(cleobj) :
      pass
    else :  #for some case, cle object attach raw data directly
      rawinst = cleobj._GetRawObject()
      return rawinst
  else :
    return None
  if cleobj.TypeFlag == True :
    localobj = cleobj.GetAttachObject()
    if localobj == None :
      return None    
    return localobj._GetRawObject()   
  else :
    #has attach pyproc
    localobj = cleobj.GetAttachObject()   
    if localobj == None :
      pass
    else :
      return localobj._GetRawObject() 
    #create new pyproc
    cleobjtype = cleobj.GetType()
    localobj = cleobjtype.GetAttachObject()
    if localobj == None :
      return None    
    rawproc = localobj._GetRawObject()   
    if rawproc == None :
      return None  
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")        
    newrawproc = rawproc.__class__()
    attach_cleobj = Service._New()
    attach_cleobj._AttachRawObject(newrawproc,False)      
    cleobj.SetAttachObject(attach_cleobj)
    newrawproc.cleobjid = cleobj._ID
    return newrawproc    

def _DefineType(globaltbl,localtbl,tpname,InputDataType,OutputDataType,RawInputOutput,IsAsync,PyFunc = None) :
  if PyFunc == None :
    def CreateDecorator(func):
      DefineType(tpname,StarNameSpace,InputDataType,OutputDataType,RawInputOutput,IsAsync,func)
    return CreateDecorator 
    
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  

  global PCDataBaseClass
  if PCDataBaseClass == None :
    PCDataBaseClass = Service.PCDataBase     
  global PCProcBaseClass
  if PCProcBaseClass == None :
    PCProcBaseClass = Service.PCProcBase    
  
  StarNameSpace = None
  _m_name = globaltbl.get('__name__')
  if _m_name == None :
    pass
  elif _m_name == '__main__' :
    pass
  else :
    _m_name = _m_name.replace('.','_')
    StarNameSpace = Service._GetObject(_m_name)
    if StarNameSpace == None :
      StarNameSpace = Service.StarObjectSpace._New(_m_name)
    else :
      if Service.StarObjectSpace._IsInst(StarNameSpace) == True : 
        pass
      else :
        raise Exception('Register '+tpname+' failed, there has cle object which is not instance of StarNameSpace named '+_m_name)    
      
  proc_class_rawtext = '''
from pchain import pydata
from pchain.pydata import PCPyDataClass  
from pchain.pydata import PCPySimpleDataClass  
from pchain import pyproc
from pchain.pyproc import PCPyProcClass

class {0}(PCPyProcClass) :
  def Execute(self,*args) :  
    Context = self.Context  #  first must save Context in local variable
    
    from pchain import pydata
    from pchain.pydata import PCPyDataClass  
    from pchain.pydata import PCPySimpleDataClass  
    
    WrapCallResult = None
    if RawInputOutput == True :
      if type(args) == type(()) : 
        callargs = []
        for item in args :  
          if item == None :
            callargs.append(None)
          else :
            callargs.append(item.value())
        if len(callargs) == 0 :  
          WrapCallResult = WrapPyFunc()
        else :
          WrapCallResult = WrapPyFunc(*callargs)
      else :
        callargs = args.value()
        WrapCallResult = WrapPyFunc(callargs)    
      if WrapCallResult == None :
        return (0,0,None)
      if RetPyType == None :
        return (0,0,None)
      else :
        return (0,0,RetPyType(WrapCallResult))
    else :
      WrapCallResult = WrapPyFunc(self,*args)
      return WrapCallResult
        
pyproc._Register({0},StarNameSpace,InputPyType,RetPyType)
{0}.GetType().IsAsync = IsAsync
globaltbl['{0}'] = {0}
localtbl['{0}'] = {0}
'''      

  local_env = {}
  local_env['StarNameSpace'] = StarNameSpace
  local_env['InputPyType'] = InputDataType
  local_env['RetPyType'] = OutputDataType
  local_env['WrapPyFunc'] = PyFunc
  local_env['RawInputOutput'] = RawInputOutput
  local_env['globaltbl'] = globaltbl
  local_env['localtbl'] = localtbl
  local_env['IsAsync'] = IsAsync
  
  exec(str.format(proc_class_rawtext,tpname),local_env)
  return globaltbl[tpname]

def DefineProc(tpname,InputDataType,OutputDataType,PyFunc = None) :
  import inspect
  f = inspect.stack()[1][0]  
  if PyFunc == None :
    def CreateDecorator(func):
      _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,False,False,func)
    return CreateDecorator 
  return _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,False,False,PyFunc)
  
def DefineRawProc(tpname,InputDataType,OutputDataType,PyFunc = None) :
  import inspect
  f = inspect.stack()[1][0]  
  if PyFunc == None :
    def CreateDecorator(func):
      _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,True,False,func)
    return CreateDecorator 
  return _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,True,False,PyFunc)  
  
def DefineAsyncProc(tpname,InputDataType,OutputDataType,PyFunc = None) :
  import inspect
  f = inspect.stack()[1][0]  
  if PyFunc == None :
    def CreateDecorator(func):
      _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,False,True,func)
    return CreateDecorator 
  return _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,False,True,PyFunc)
  
def DefineAsyncRawProc(tpname,InputDataType,OutputDataType,PyFunc = None) :
  import inspect
  f = inspect.stack()[1][0]  
  if PyFunc == None :
    def CreateDecorator(func):
      _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,True,True,func)
    return CreateDecorator 
  return _DefineType(f.f_globals,f.f_locals,tpname,InputDataType,OutputDataType,True,True,PyFunc)   