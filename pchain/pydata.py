# -*- coding: utf-8 -*-
"""
    pydata.py

    :project : pchain
    :date    : 2019-04-09 09:49:21
    
    important:
    the app must not hold the instance of PCPyDataClass or it's child class.
        it should hold the object return from UnWrap
    ,and,
        use pydata.UnWrap to get the instance    
"""

pydatatypemap = {}

PCDataBaseClass = None

class PCPyDataClass(object) :
  def __init__(self,val) :
    self.val = val
    
    self.GetTag = self._GetTag
    self.GetTagLabel = self._GetTagLabel 
    self.IsType = self._IsType    
    self.Wrap = self._Wrap
       
  # need restore
  def __del__ (self):
    if hasattr(self,'RestoreDataObjectProperity') == True :
      if self.RestoreDataObjectProperity == None :    
        pass
      else :   
        try :
          import libstarpy
          SrvGroup = libstarpy._GetSrvGroup(0)
          if SrvGroup == None :
            return
          Service = SrvGroup._GetService("","")       
          if Service == None or Service.PCDataBase == None:
            return       
          Service.PCDataBase.ClearCleDataProperty(self.RestoreDataObjectProperity)
        except Exception as exc:
          pass
  
  '''
  @staticmethod
  def Load(MetaData) :
    #MetaData is a string
    raise Exception('Load function is not defined')
  '''    

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
    cledata = pydatatypemap.get(cls)
    if cledata == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cledata.GetTag()     
    
  @classmethod
  def GetTagLabel(cls) :
    cledata = pydatatypemap.get(cls)
    if cledata == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cledata.GetTagLabel()    
        
  def Save(self) :
    #raise Exception('Save function is not defined for '+str(self))   
    import pickle
    import base64    
    return base64.b64encode(pickle.dumps(self.val))

  def ToString(self) :
    return str(self.value())
  
  def __str__(self):
    return str(self.Wrap())
  
  def Dup(self) :
    return self.__class__(self.value())
    
  def Equals(self,inst) :
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    if SrvGroup == None :
      return False    
    Service = SrvGroup._GetService("","")       
    if Service == None :
      return False  
    l_val = None
    if isinstance(inst,PCPyDataClass) == True :
      l_val = inst.value()
    else :
      import libstarpy
      if type(inst) == libstarpy.ObjectClass and Service.PCDataBase._IsInst(inst) :
        rawinst = UnWrap(inst)
        if rawinst == None :
          return False
        else :
          return True
      else :
        return False
    if self.val == inst.val :
      return True
    else :
      return False     
      
  def ToParaPkg(self,parapkg) :
    raise Exception('ToParaPkg function is not supported ')      
    
  def value(self) :
    return self.val   
    
  @classmethod
  def Wrap(cls) :
    cledata = pydatatypemap.get(cls)
    if cledata == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cledata        

  def _Wrap(self) :
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    if SrvGroup == None :
      return None    
    Service = SrvGroup._GetService("","")       
    if Service == None :
      return None
    if hasattr(self,'cleobjid') == True :
      retobj = Service._GetObject(self.cleobjid)
      if retobj == None :
        # need restore
        if hasattr(self,'RestoreDataObjectProperity') == True :
          if self.RestoreDataObjectProperity == None : 
            raise Exception('Wrap '+ self.__class__.__name__ + " failed, it's corresponding cle object has been freed.")
          else :
            pass 
        else :
          raise Exception('Wrap '+ self.__class__.__name__ + " failed, it's corresponding cle object has been freed.")
      else :
        return retobj
    
    cledata = pydatatypemap.get(self.__class__)
    if cledata == None :
      raise Exception('Wrap '+ self.__class__.__name__ + ' failed, it is not registered')
    
    if hasattr(self,'classinst') == True :
      class_newdata = self.classinst.Wrap()
      newdata = class_newdata._New()
      self.cleobjid = newdata._ID
      return newdata
    
    # find the pcdata  
    cleobj = Service._New()
    cleobj._AttachRawObject(self,False)      
    newdata = cledata.Create(cleobj)
    
    # need restore
    if hasattr(self,'RestoreDataObjectProperity') == True :
      if self.RestoreDataObjectProperity == None :
        pass
      else :
        newdata.RestoreCleDataProperty(self.RestoreDataObjectProperity)
        newdata.ClearCleDataProperty(self.RestoreDataObjectProperity)
        self.RestoreDataObjectProperity = None
    
    #use newdata[0]._GetRawObject() to get the attach python object

    self.cleobjid = newdata._ID
    
    newdata.Notify()
    
    return newdata
  
  @classmethod
  def GetType(cls) :
    cledata = pydatatypemap.get(cls)
    if cledata == None :
      raise Exception('Wrap '+ cls.__name__ + ' failed, it is not registered')
    return cledata
            
  @classmethod
  def IsPChainRawInstance(cls,which) :
    if isinstance(which,PCPyDataClass) :
      return True
    return False  
    
  @classmethod  
  def DefineMethod(cls,MethodName) :
    cledata = pydatatypemap.get(cls) 
    if cledata == None :
      raise Exception('DefineMethod '+ cls.__name__ + ' failed, it is not registered')
    def CreateDecorator(func):
      cledata._RegScriptProc_P(MethodName,func)
    return CreateDecorator           

  '''              
  def GetType(self) :
    import libstarpy
    cle_self = self.Wrap()
    dt = cle_self.GetType()
    if type(dt) == libstarpy.ObjectClass :
      bufobj = dt.GetDataTypeClass()
      if bufobj == None : 
        return dt
      if bufobj._HasRawContext() == True :
        rawt = bufobj._GetRawObject()
        if issubclass(rawt,PCPyDataClass) == True :
          return rawt
        else :
          return dt
      return dt
    else :
      return None
  '''
      
  def SaveTo(self,ValueBuf) :
    cle_self = self.Wrap()
    return cle_self.SaveTo(ValueBuf)
    
  def SaveToString(self) :
    cle_self = self.Wrap()
    return cle_self.SaveToString()    
    
  @classmethod
  def LoadFrom(cls,ValueBuf) :
    cle_self = cls.GetType()
    bufobj = cle_self.LoadFrom(ValueBuf)
    if bufobj == None :
      return None
    val = UnWrap(bufobj)
    if isinstance(val,PCPyDataClass) == True :
      return val
    return bufobj
    
  @classmethod
  def LoadFromString(cls,ValueBuf) :
    cle_self = cls.GetType()
    bufobj = cle_self.LoadFromString(ValueBuf)
    if bufobj == None :
      return None
    val = UnWrap(bufobj)
    if isinstance(val,PCPyDataClass) == True :
      return val
    return bufobj    
        
  def AddSource(self,SourceData) :
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")  
      
    cle_self = self.Wrap()
    cle_SourceData = None
    if isinstance(SourceData,PCPyDataClass) == True :
      cle_SourceData = SourceData.Wrap()
    else :
      if type(SourceData) == libstarpy.ObjectClass and Service.PCDataBase._IsInst(SourceData) :
        cle_SourceData = SourceData
    if cle_SourceData == None or cle_self == None :
      return False
    return cle_self.AddSource(cle_SourceData)
  
  def IsChangedFrom(self,SourceData) :
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")  
      
    cle_self = self.Wrap()
    cle_SourceData = None
    if isinstance(SourceData,PCPyDataClass) == True :
      cle_SourceData = SourceData.Wrap()
    else :
      if type(SourceData) == libstarpy.ObjectClass and Service.PCDataBase._IsInst(SourceData) :
        cle_SourceData = SourceData
    if cle_SourceData == None or cle_self == None :
      return False
    return cle_self.IsChangedFrom(cle_SourceData)
    
  def GetSource(self) :
    cle_self = self.Wrap()
    result = cle_self.GetSource()
    if result == None :
      return []
    returnval = []
    for item in result :
      val = UnWrap(item)
      if isinstance(val,PCPyDataClass) == True :
        returnval.append(val)  
      else :
        returnval.append(item)  
    return returnval
    
  def GetOwnerProc(self) :
    cle_self = self.Wrap()
    result = cle_self.GetOwnerProc()
    if result == None :
      return None
    from pchain import pyproc
    from pchain.pyproc import PCPyProcClass
    val = pyproc.UnWrap(result)
    if isinstance(val,PCPyProcClass) == True :
      return val
    return result
    
  @classmethod    
  def IsType(cls) :
    return True 
  def _IsType(self) :
    cle_self = self.Wrap()
    return cle_self.IsType()     
    
  def IsSource(self,SourceData,MustDirect) :
    cle_self = self.Wrap()
    return cle_self.IsSource(SourceData,MustDirect)
    
  def IsSame(self,PCData) :
    cle_self = self.Wrap()
    return cle_self.IsSame(PCData)
    
  def IsInstance(self,PCDataType) :
    cle_self = self.Wrap()
    return cle_self.IsInstance(PCDataType)    
    
  def IsBefore(self,PCData) :
    cle_self = self.Wrap()
    return cle_self.IsBefore(PCData)   
    
  def IsAfter(self,PCData) :
    cle_self = self.Wrap()
    return cle_self.IsAfter(PCData)           
 
  # the same function defined in the corresponding cle object, may cause deadloop
  #def Equals(self,PCData) :
  #  cle_self = self.Wrap()
  #  return cle_self.Equals(PCData)
        
  def Approved(self) :
    cle_self = self.Wrap()
    cle_self.Approved()
    
  def Disapproved(self) :
    cle_self = self.Wrap()
    cle_self.Approved()  
    
  def IsReject(self,Proc) :
    cle_self = self.Wrap()
    return cle_self.IsReject(Proc)     
    
  def AddReject(self,Proc) :
    cle_self = self.Wrap()
    cle_self.AddReject(Proc)     
    
  def RemoveReject(self,Proc) :
    cle_self = self.Wrap()
    cle_self.RemoveReject(Proc)   
      
  def GetReject(self) :
    cle_self = self.Wrap()
    result = cle_self.GetReject()
    
    from pchain import pyproc
    from pchain.pyproc import PCPyProcClass   
    returnval = []
    for item in result :
      val = pyproc.UnWrap(item)
      if isinstance(val,PCPyProcClass) == True :
        returnval.append(val)
      else :
        returnval.append(item)
    return returnval      
    
  def IsAccept(self,Proc) :
    cle_self = self.Wrap()
    return cle_self.IsAccept(Proc)     
    
  def AddAccept(self,Proc) :
    cle_self = self.Wrap()
    cle_self.AddAccept(Proc)     
    
  def RemoveAccept(self,Proc) :
    cle_self = self.Wrap()
    cle_self.RemoveAccept(Proc)   
      
  def GetAccept(self) :
    cle_self = self.Wrap()
    result = cle_self.GetAccept()
    
    from pchain import pyproc
    from pchain.pyproc import PCPyProcClass   
    returnval = []
    for item in result :
      val = pyproc.UnWrap(item)
      if isinstance(val,PCPyProcClass) == True :
        returnval.append(val)
      else :
        returnval.append(item)
    return returnval   
    
  def ResetSchedule(self) :
    cle_self = self.Wrap()
    cle_self.ResetSchedule()       
       
  def IsFromProc(self,Proc) :
    cle_self = self.Wrap()
    return cle_self.IsFromProc(Proc) 
    
  def SetSignature(self,Signature) :
    cle_self = self.Wrap()
    cle_self.SetSignature(Signature)    
    
  def GetSignature(self) :
    cle_self = self.Wrap()
    return cle_self.GetSignature()       
   
  def _GetTag(self) :
    cle_self = self.Wrap()
    return cle_self.GetTag()   
    
  def _GetTagLabel(self) :
    cle_self = self.Wrap()
    return cle_self.GetTagLabel()      
    
  def SetUniformTick(self,Tick) :
    cle_self = self.Wrap()
    return cle_self.SetUniformTick(Tick)    
        
  def GetUniformTick(self) :
    cle_self = self.Wrap()
    return cle_self.GetUniformTick()  
    
  def SetCache(self,LabelUUID,CachedData) :
    cle_self = self.Wrap()
    result = cle_self.SetCache(LabelUUID,CachedData)
    return result
    
  def GetCache(self,LabelUUID) :
    cle_self = self.Wrap()
    result = cle_self.GetCache(LabelUUID)
    if result == None :
      return None
    val = UnWrap(result)
    if val == None :
      return result
    return val
    
  def ClearCache(self) :
    cle_self = self.Wrap()
    return cle_self.ClearCache()          
    
  def RunString(self,val) :
    cle_self = self.Wrap()
    return cle_self.RunString(val)        
    
  def RunProc(self,val) :
    cle_self = self.Wrap()
    return cle_self.RunProc(val)
    
  def GetDataSetBase(self) :
    cle_self = self.Wrap()
    return cle_self.GetDataSetBase()                   

  def GetObjectDataBase(self) :
    cle_self = self.Wrap()
    return cle_self.GetObjectDataBase()                   

  def GetBufDataBase(self) :
    cle_self = self.Wrap()
    return cle_self.GetBufDataBase()     

  @classmethod
  def DefineSubType(cls,SubTypeName) :
    cle_self = cls.GetType()
    return cle_self.DefineSubType(SubTypeName)

  @classmethod
  def CastFrom(cls,ParentDataType_Data) :
    cle_self = cls.GetType()
    return cle_self.CastFrom(ParentDataType_Data)
    
  def RegCallBack(self,TargetObject) :
    cle_self = self.Wrap()
    cle_self.RegCallBack(TargetObject) 

  def UnRegCallBack(self,TargetObject) :
    cle_self = self.Wrap()
    cle_self.UnRegCallBack(TargetObject)       
            
def GetCleType(tp):
  cledata = pydatatypemap.get(tp)
  if cledata == None :
    raise Exception('Wrap '+ tp.__name__ + ' failed, it is not registered')
  return cledata    
  
def Register(tp) :
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  
  
  global PCDataBaseClass
  if PCDataBaseClass == None :  
    PCDataBaseClass = Service.PCDataBase  
  
  import inspect    
  f = inspect.stack()[1][0]
  globaltbl = f.f_globals
  localtbl = f.f_locals
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
  _Register(None,tp,StarNameSpace)

  newtype = globaltbl[tp.__name__]
  newtype.cached_globaltbl = globaltbl
  newtype.cached_localtbl = localtbl
  return newtype
    
def _Register(datatype,tp,StarNameSpace=None) :
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  
  
  global PCDataBaseClass
  if PCDataBaseClass == None :  
    PCDataBaseClass = Service.PCDataBase  

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
  cledata = pydatatypemap.get(tp)
  if cledata == None :
    #not exist, create for it  
    cleobj = Service._New()
    cleobj._AttachRawObject(tp,True)
    cledata = None
        
    # the parent class
    basecls = None
    import pchain
    if pchain.ispython2 == True :
      basecls = tp.__bases__[0]
    else :
      basecls = tp.__base__
    if basecls == PCPyDataClass or basecls == PCPySimpleDataClass : 
      if datatype == None :
        cledata = Service.PCDataBase.CreateType(tp.__name__)
      else :
        cledata = datatype.CreateType(tp.__name__)
    else :
      parent_cledata = pydatatypemap.get(basecls)
      if parent_cledata == None :
        raise Exception('Register '+ basecls.__name__ + ' failed, it parent class is not registered')
      cledata = parent_cledata.CreateType(tp.__name__)
    cledata.SetDataTypeClass(cleobj)      
      
    @cleobj._RegScriptProc_P('ToString')
    def cleobj_ToString(cleobj,cledata) :
      rawinst = UnWrap(cledata)
      if rawinst == None :
        return None      
      return rawinst.ToString()
      
    @cleobj._RegScriptProc_P('IsRawInstance')
    def cleobj_IsInstance(cleobj,inst) :
      rawinst = inst._GetRawObject()
      if rawinst == None :
        pass
      else :
        return isinstance(rawinst,PCPyDataClass)
      rawinst = UnWrap(inst)
      if rawinst == None :
        return False
      return isinstance(rawinst,PCPyDataClass)
        
    @cleobj._RegScriptProc_P('Equals')
    def cleobj_Equals(cleobj,inst1,inst2) :
      rawinst1 = UnWrap(inst1)
      rawinst2 = UnWrap(inst2)
      if rawinst1 == None or rawinst2 == None :
        return False
      if rawinst1 == rawinst2 :
        return True
      if rawinst1.__class__ == rawinst2.__class__ :
        return rawinst1.Equals(rawinst2)
      else :
        return False      

    @cleobj._RegScriptProc_P('Dup')
    def cleobj_Dup(cleobj,inst,newtype_obj) :  # Dup function may change data type
      rawinst = UnWrap(inst)
      if rawinst == None :
        return None
      if newtype_obj == None :
        newinst = rawinst.Dup()
        if newinst == None :
          return None
        return newinst.Wrap()
      else :
        if newtype_obj._HasRawContext() == True :
          newtype = newtype_obj._GetRawObject()
          if issubclass(newtype,PCPyDataClass) == True :
            newinst = newtype(rawinst.value())
            return newinst.Wrap()
          else :
            return None            
        return None
      
    @cleobj._RegScriptProc_P('Save')
    def cleobj_Save(cleobj,cledata) :
      rawinst = UnWrap(cledata) 
      return rawinst.Save()
              
    @cleobj._RegScriptProc_P('Load')
    def cleobj_Load(cleobj,MetaData) :  # MetaData is a string
      rawinst = tp.Load(MetaData)
      if rawinst == None :
        return None
      return rawinst.Wrap()
      
    @cleobj._RegScriptProc_P('ToParaPkg')
    def cleobj_Save(cleobj,inst,parapkg) :
      rawinst = UnWrap(inst) 
      return rawinst.ToParaPkg(parapkg)
    
    # need save for restore  
    @cleobj._RegScriptProc_P('OnBeforeFree')
    def cleobj_OnBeforeFree(cleobj,rawobject,CleObjectProperty) :
      rawinst = rawobject._GetRawObject()   
      if rawinst == None :
        return
      try:
          if isinstance(rawinst,PCPyDataClass) == True :
            rawinst.RestoreDataObjectProperity = CleObjectProperty
          else :
            return
      except Exception as exc:
        pass
                      
    pydatatypemap[tp] = cledata  
    
    if StarNameSpace == None :
      pass
    else :
      StarNameSpace.SetObject(cledata)
    
    cledata.Notify()
    
  return tp
  
def UnWrap(cleobj) :
  import libstarpy
  if type(cleobj) == libstarpy.ObjectClass :
    if PCDataBaseClass._IsInst(cleobj) :
      pass
    else :  #for some case, cle object attach raw data directly
      rawinst = cleobj._GetRawObject()
      return rawinst
  else :
    return None
  if cleobj.TypeFlag == True :
    bufobj = cleobj.GetDataTypeClass()
    if bufobj == None :
      return None
    else :
      return bufobj._GetRawObject()
  else :
    bufobj = cleobj.GetObjectHasBuf()
    rawdata = bufobj[0]._GetRawObject()
    if rawdata == None :
      return None
    else :
      if rawdata.cleobjid == cleobj._ID :
        return rawdata
      else :
        newrawdata = rawdata.__class__(rawdata.value())
        newrawdata.cleobjid = cleobj._ID
        newrawdata.classinst = rawdata
        return newrawdata               

def _DefineType(globaltbl,localtbl,datatype,tpname,pyrawtype,StarNameSpaceIsValid,InputStarNameSpace) :
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  
  
  global PCDataBaseClass
  if PCDataBaseClass == None :  
    PCDataBaseClass = Service.PCDataBase    
  
  StarNameSpace = None
  if StarNameSpaceIsValid == False :
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
  else :
    StarNameSpace = InputStarNameSpace
  
  data_class_rawtext = '''
from pchain import pydata
from pchain.pydata import PCPyDataClass  
from pchain.pydata import PCPySimpleDataClass  
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
          
      self.GetTag = self._GetTag
      self.GetTagLabel = self._GetTagLabel 
      self.IsType = self._IsType    
      self.Wrap = self._Wrap        
          
    @staticmethod
    def Load(MetaData) :
      # MetaData maybe string or parapkg
      # raise Exception('Load function is not defined ')
      import pickle
      import base64
      if type(MetaData) == type('') :
        return {0}(pickle.loads(base64.b64decode(MetaData)))
      else :
        raise Exception('Load from ParaPkg is not supported ')
    def Save(self) :
      #raise Exception('Save function is not defined for '+str(self))   
      import pickle
      import base64    
      return base64.b64encode(pickle.dumps(self.val))                
                      
pydata._Register(datatype,{0},StarNameSpace)
globaltbl['{0}'] = {0}
localtbl['{0}'] = {0}
'''  
  
  local_env = {}
  local_env['StarNameSpace'] = StarNameSpace
  local_env['pyrawtype'] = pyrawtype
  local_env['globaltbl'] = globaltbl
  local_env['localtbl'] = localtbl
  local_env['datatype'] = datatype
  exec(str.format(data_class_rawtext,tpname),local_env)

  newtype = globaltbl[tpname]
  newtype.cached_globaltbl = globaltbl
  newtype.cached_localtbl = localtbl
  return newtype
  
class PCPySimpleDataClass(PCPyDataClass) :  
  pass
     
def DefineType(tpname,rawtype=None) :  
  import inspect
  f = inspect.stack()[1][0]
  return _DefineType(f.f_globals,f.f_locals,None,tpname,rawtype,False,None)
  
#--subtype
def _DefineSubType(globaltbl,localtbl,parenttype,tpname,pyrawtype,StarNameSpaceIsValid,InputStarNameSpace) :
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  

  global PCDataBaseClass
  if PCDataBaseClass == None :  
    PCDataBaseClass = Service.PCDataBase

  StarNameSpace = None
  if StarNameSpaceIsValid == False :
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
  else :
    StarNameSpace = InputStarNameSpace

  if pyrawtype == None : 
    pass
  else :
    if parenttype == None :
      raise Exception('Register '+tpname+' failed, its parent type '+parenttype.__name__+' is not found.')
    if parenttype.rawtype == None :
      raise Exception('Register '+tpname+' failed, rawtype must be None')
    else :
      if issubclass(pyrawtype,parenttype.rawtype) == False:
        raise Exception('Register '+tpname+' failed, rawtype is not subclass of its parent class') 
  
  data_class_rawtext = '''
from pchain import pydata
from pchain.pydata import PCPyDataClass  
from pchain.pydata import PCPySimpleDataClass  
class {0}(parenttype) :
  if pyrawtype == None :
    pass
  else :
    rawtype = pyrawtype
          
pydata._Register(None,{0},StarNameSpace)  
globaltbl['{0}'] = {0}
localtbl['{0}'] = {0}
'''  
  
  local_env = {}
  local_env['StarNameSpace'] = StarNameSpace
  local_env['pyrawtype'] = pyrawtype
  local_env['globaltbl'] = globaltbl
  local_env['localtbl'] = localtbl
  local_env['parenttype'] = parenttype
  exec(str.format(data_class_rawtext,tpname),local_env)

  newtype = globaltbl[tpname]
  newtype.cached_globaltbl = globaltbl
  newtype.cached_localtbl = localtbl

  return newtype
    
def DefineSubType(parenttype,tpname,rawtype = None) :
  import inspect
  f = inspect.stack()[1][0]  
  return _DefineSubType(f.f_globals,f.f_locals,parenttype,tpname,rawtype,False,None)

#this function is for __init__.py
def DefineSubType_WithSpace(parenttype,tpname,StarNameSpace,rawtype = None) :
  #import inspect
  #f = inspect.stack()[1][0]
  return _DefineSubType(parenttype.cached_globaltbl,parenttype.cached_localtbl,parenttype,tpname,rawtype,True,StarNameSpace)

#define default type
def pydata_Init() :
  import inspect
  f = inspect.stack()[0][0]
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("", "")
  StarNameSpace = Service.StarObjectSpace._New('pydata')
  _DefineType(f.f_globals,f.f_locals,None,'pint',int,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'pbool',bool,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'pfloat',float,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'pcomplex',complex,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'pstr',str,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'plist',list,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'pset',set,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'pdict',dict,True,StarNameSpace)
  _DefineType(f.f_globals,f.f_locals,None,'ptuple',tuple,True,StarNameSpace)