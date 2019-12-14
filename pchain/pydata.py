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

class PCPyDataClass :
  def __init__(self,val) :
    self.val = val
       
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
  
  def Wrap(self) :
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
    
  def SetRuleAttach(self,PCRule) :
    cle_self = self.Wrap()
    return cle_self.SetRuleAttach(PCRule)
    
  def GetRuleAttach(self) :
    cle_self = self.Wrap()
    result = cle_self.GetRuleAttach()
    val = []
    for item in result :
      val.append(item)
    return val
    
  def HasRuleAttach(self) :
    cle_self = self.Wrap()
    return cle_self.HasRuleAttach()
    
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
        
  def GetTag(self) :
    cle_self = self.Wrap()
    return cle_self.GetTag()   
    
  def GetTagLabel(self) :
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
    
  def IsProperty(self,val) :
    cle_self = self.Wrap()
    return cle_self.IsProperty(val) 
    
  def HasProperty(self) :
    cle_self = self.Wrap()
    return cle_self.HasProperty() 
    
  def GetDataSetBase(self) :
    cle_self = self.Wrap()
    return cle_self.GetDataSetBase()                   

  def GetObjectDataBase(self) :
    cle_self = self.Wrap()
    return cle_self.GetObjectDataBase()                   

  def GetBufDataBase(self) :
    cle_self = self.Wrap()
    return cle_self.GetBufDataBase()                   
        
def GetCleType(tp):
  cledata = pydatatypemap.get(tp)
  if cledata == None :
    raise Exception('Wrap '+ tp.__name__ + ' failed, it is not registered')
  return cledata    
  
def O_Register(datatype,tp) :
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  
  
  global PCDataBaseClass
  if PCDataBaseClass == None :  
    PCDataBaseClass = Service.PCDataBase  
  
  import sys
  f = list(sys._current_frames().values())[0] 
  StarNameSpace = None
  _m_name = f.f_back.f_back.f_globals.get('__name__')
  if _m_name == None :
    pass
  elif _m_name == '__main__' :
    pass
  else :
    StarNameSpace = Service._GetObject(_m_name)
    if StarNameSpace == None :
      StarNameSpace = Service.StarObjectSpace._New(_m_name)
    else :
      if Service.StarObjectSpace._IsInst(StarNameSpace) == True : 
        pass
      else :
        raise Exception('Register '+tp.__name__+' failed, there has cle object which is not instance of StarNameSpace named '+_m_name)
  return _Register(datatype,tp,StarNameSpace)
  
def Register(tp) :  
  return O_Register(None,tp)
  
def RegisterEx(datatype,tp) :  
  return O_Register(datatype,tp)
    
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
      if isinstance(rawinst,PCPyDataClass) == True :
        rawinst.RestoreDataObjectProperity = CleObjectProperty 
      else :
        return
                      
    pydatatypemap[tp] = cledata   
  if StarNameSpace == None :
    pass
  else :
    StarNameSpace.SetObject(cledata)
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
  if cleobj.IsType == True :
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

def _DefineType(globaltbl,datatype,tpname,pyrawtype) :
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  
  
  global PCDataBaseClass
  if PCDataBaseClass == None :  
    PCDataBaseClass = Service.PCDataBase    
  
  StarNameSpace = None
  _m_name = globaltbl.get('__name__')
  if _m_name == None :
    pass
  elif _m_name == '__main__' :
    pass
  else :
    StarNameSpace = Service._GetObject(_m_name)
    if StarNameSpace == None :
      StarNameSpace = Service.StarObjectSpace._New(_m_name)
    else :
      if Service.StarObjectSpace._IsInst(StarNameSpace) == True : 
        pass
      else :
        raise Exception('Register '+tpname+' failed, there has cle object which is not instance of StarNameSpace named '+_m_name)  
  
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
'''  
  
  local_env = {}
  local_env['StarNameSpace'] = StarNameSpace
  local_env['pyrawtype'] = pyrawtype
  local_env['globaltbl'] = globaltbl
  local_env['datatype'] = datatype
  exec(str.format(data_class_rawtext,tpname),local_env)
  return globaltbl[tpname]
  
class PCPySimpleDataClass(PCPyDataClass) :  
  pass
     
def DefineType(tpname,rawtype=None) :  
  import sys
  f = list(sys._current_frames().values())[0] 
  return _DefineType(f.f_back.f_globals,None,tpname,rawtype)  
  
def DefineTypeEx(datatype,tpname,rawtype=None) :  
  import sys
  f = list(sys._current_frames().values())[0] 
  return _DefineType(f.f_back.f_globals,datatype,tpname,rawtype)   
  
#--subtype
def _DefineSubType(globaltbl,parenttype,tpname,pyrawtype) :
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  Service = SrvGroup._GetService("","")  

  global PCDataBaseClass
  if PCDataBaseClass == None :  
    PCDataBaseClass = Service.PCDataBase  
    
  StarNameSpace = None
  _m_name = globaltbl.get('__name__')
  if _m_name == None :
    pass
  elif _m_name == '__main__' :
    pass
  else :
    StarNameSpace = Service._GetObject(_m_name)
    if StarNameSpace == None :
      StarNameSpace = Service.StarObjectSpace._New(_m_name)
    else :
      if Service.StarObjectSpace._IsInst(StarNameSpace) == True : 
        pass
      else :
        raise Exception('Register '+tpname+' failed, there has cle object which is not instance of StarNameSpace named '+_m_name)
  
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
'''  
  
  local_env = {}
  local_env['StarNameSpace'] = StarNameSpace
  local_env['pyrawtype'] = pyrawtype
  local_env['globaltbl'] = globaltbl
  local_env['parenttype'] = parenttype
  exec(str.format(data_class_rawtext,tpname),local_env)

  return globaltbl[tpname]
    
def DefineSubType(parenttype,tpname,rawtype = None) :  
  import sys
  f = list(sys._current_frames().values())[0] 
  return _DefineSubType(f.f_back.f_globals,parenttype,tpname,rawtype)    