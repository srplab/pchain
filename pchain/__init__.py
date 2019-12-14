import os
import sys

ispython2 = False
is64Bit = False
isUbuntuOs = False
def CheckPythonVersion() :
  import platform
  version = platform.python_version().split('.')  
  if( version[0] == '2' and version[1] == '7' ):
    global ispython2
    ispython2 = True
  if platform.architecture()[0] == '64bit' :
    global is64Bit
    is64Bit = True
  osinfo = platform.platform().lower()
  global isUbuntuOs
  if osinfo.find('ubuntu') == -1 and osinfo.find('deepin') == -1 :
    isUbuntuOs = False
  else :
    isUbuntuOs = True

CheckPythonVersion()

path = os.path.dirname(os.path.abspath(__file__))
nativepath = ""
nativename = ""
webpath = path + '/webpage'
templatepath = path + '/template'
platform = ""
if sys.platform.startswith("win32") :
  if is64Bit == True :
    nativepath = path + '/windows/64'
  else :
    nativepath = path + '/windows/32'
  nativename = "star_pchain.dll"
  platform = 'windows'
elif sys.platform.startswith("linux") : 
  if isUbuntuOs == True :
    nativepath = path + '/linux/ubuntu'
  else :
    nativepath = path + '/linux'
  nativename = "libstar_pchain.so"
  platform = 'linux'
elif sys.platform.startswith("darwin") :   
  nativepath = path + '/darwin'
  nativename = "libstar_pchain.dylib"
  platform = 'darwin'
else :
  nativepath = path

userpath = os.path.expanduser("~")
if os.path.exists(userpath+"/.pchain") == False :
  os.makedirs(userpath+"/.pchain")
userpath = userpath+"/.pchain"  
if os.path.exists(userpath+"/packages") == False :
  os.makedirs(userpath+"/packages")
packagepath = userpath+"/packages"  

import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename=userpath + '/pchain.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

SystemPackageInfo = None
IsInitCLE = False
IsRunFromPChain = False
IsInitPChain = False

def cleinstall() :
  import pchain
  import urllib 
  import os
  import sys
  import logging

  if ispython2 == True :
    import urllib2 
  else :
    from urllib.request import urlretrieve

  def report(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("\r%d%%" % percent + ' complete')
    sys.stdout.flush()

  try :
    import requests
  except Exception as exc:
    print("can not import python module 'requests', install it")
    import sys
    import subprocess
    Result = subprocess.call([sys.executable, "-m", "pip", "install", "requests"])    
    if Result != 0 :
      print("install requests failed")
      return False
    else :
      print("install requests finish")
        
  if pchain.platform == 'windows' :
    clefile = ''
    if pchain.is64Bit == True :
      clefile = 'starcore_x64.3.7.2.exe'
    else :
      clefile = 'starcore_win32.3.7.2.exe'
    print('download '+clefile+' from https://github.com/srplab/starcore_for_windows')
    import tempfile
    f, output_filename = tempfile.mkstemp(suffix='.exe')
    os.close(f)        
        
    try :
      url = 'https://github.com/srplab/starcore_for_windows/raw/master/'+clefile
      print('begin download '+url)
      if ispython2 == True :
        urllib.urlretrieve(url, output_filename,report)
      else :
        urlretrieve(url, output_filename,report)
      print('\nfinish download '+url)
          
      os.system(output_filename)
      os.remove(output_filename)
          
      print('install finish')
      return True
          
    except Exception as exc:
      print(exc)
      return False 
      
  if pchain.platform == 'linux' :
    clefile = ''
    if pchain.is64Bit == True :
      if isUbuntuOs == True :
        clefile = 'starcore-ubuntu_3.7.2-2_amd64.deb'
      else :
        clefile = 'starcore-3.7.2-1.x86_64.rpm'
    else :
      print('please install 32bit version manually')
      return False
    print('download '+clefile+' from https://github.com/srplab/starcore_for_linux')
    import tempfile
    f, output_filename = tempfile.mkstemp(suffix='.deb')
    os.close(f)        
        
    try :
      url = 'https://github.com/srplab/starcore_for_linux/raw/master/'+clefile
      print('begin download '+url)
      if ispython2 == True :
        urllib.urlretrieve(url, output_filename,report)
      else :
        urlretrieve(url, output_filename,report)
      print('\nfinish download '+url)
      
      if isUbuntuOs == True :    
        os.system('sudo dpkg -i '+output_filename)
      else :
        os.system('sudo rpm -i --force '+output_filename)
      os.remove(output_filename)
          
      print('install finish')
      return True

    except Exception as exc:
      print(exc)
      return False 

  if pchain.platform == 'darwin' :
    clefile = ''
    if pchain.is64Bit == True :
      clefile = 'starcore_macos-3.7.2.x86_64.tar.gz'
    else :
      print('32bit version is not supported')
      return False
    print('download '+clefile+' from https://github.com/srplab/starcore_for_macos')
    import tempfile
    f, output_filename = tempfile.mkstemp(suffix='.gz')
    os.close(f)        
        
    try :
      url = 'https://github.com/srplab/starcore_for_macos/raw/master/'+clefile
      print('begin download '+url)
      if ispython2 == True :
        urllib.urlretrieve(url, output_filename,report)
      else :
        urlretrieve(url, output_filename,report)
      print('\nfinish download '+url)
      
      print(output_filename)

      cur_path = os.getcwd()
      path = os.path.dirname(output_filename)
      os.chdir(path)
      os.system('tar -zxf '+output_filename)
      os.chdir('starcore.install')
      os.system('./install.sh')
      os.chdir(cur_path)
      
      os.remove(output_filename)
          
      print('install finish')
      return True
          
    except Exception as exc:
      print(exc)
      return False 
            
  return False
      
def cleinit() :
  global IsInitPChain
  if IsInitPChain == True :
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    return SrvGroup._GetService('','')
    
  import platform
  import os
  import sys
  import pchain
  version = platform.python_version().split('.')
  modulename = ""
  
  #set current path for starcore
  savedcwd = os.getcwd()
  os.chdir(pchain.nativepath)
  #put it first path
  try :
    index=sys.path.index(pchain.nativepath)    
  except Exception as exc:       
    sys.path.insert(0,pchain.nativepath)
  
  try:
    if( version[0] == '2' and version[1] == '7' ):
      import libstarpy
      modulename = 'python'
    elif version[0] == '3' and version[1] == '5' :
      import libstar_python35
      modulename = 'python35'
    elif version[0] == '3' and version[1] == '6' :
      import libstar_python36
      modulename = 'python36'
    elif version[0] == '3' and version[1] == '7' :
      import libstar_python37
      modulename = 'python37'
    else :
      print('python ' + version + ' not supported')
      os.chdir(savedcwd)
      return None
        
  except Exception as exc:   
    print('cle init failed, may be it not installed, auto install it !')
    if cleinstall() == False :   
      os.chdir(savedcwd)   
      return None
    else :
      print('please run app again')
      os.chdir(savedcwd)
      return None      
      
  os.chdir(savedcwd)
  
  global IsInitCLE
  IsInitCLE = False
  import libstarpy
  SrvGroup = libstarpy._GetSrvGroup(0)
  if SrvGroup != None and SrvGroup._GetService('','') != None:
    IsInitCLE = True

  Service = None
  if IsInitCLE == False :
    import libstarpy
    Service=libstarpy._InitSimple("test","123",0,0);
    SrvGroup = Service._ServiceGroup;
    CleVer = libstarpy._Version()
    if CleVer[0] < 3 or ( CleVer[0] == 3 and CleVer[1] < 114 ) :
      print('pchain initialize failed, starcore version must be equal or higher than 3.7.2')
      SrvGroup._ClearService()
      libstarpy._ModuleExit()      
      return None  
    Result = Service._DoFile("",nativepath+"/"+nativename,"");
    if Result[0] == False :
      print(Result[1])    
      SrvGroup._ClearService()
      libstarpy._ModuleExit()      
      return None  
    IsInitPChain = True
  else :
    CleVer = libstarpy._Version()
    if CleVer[0] < 3 or ( CleVer[0] == 3 and CleVer[1] < 114 ) :
      print('pchain initialize failed, starcore version must be equal or higher than 3.7.2')
      return None  
    Service = SrvGroup._GetService("","")
    Result = Service._DoFile("",nativepath+"/"+nativename,"");
    if Result[0] == False :
      print(Result[1])
      return None  
    IsInitPChain = True
      
  @Service.PCProcBase._RegScriptProc_P('Create')
  def PCProcBase_Create(CleObj,StarSpaceObject,ProcName,InputQueue,OutputQueue):
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")
    Proc = Service.PCProcBase._New(ProcName)
    #--input
    if InputQueue == None :
      pass
    else :
      Proc.InputFrom(InputQueue)
    #--output
    if OutputQueue == None :
      pass
    else :
      Proc.OutputFrom(OutputQueue)
    if StarSpaceObject == None :
      pass
    else :
      StarSpaceObject.SetObject(Proc)  
    def CreateDecorator(func):
      Proc._RegScriptProc_P('Execute',func)
    return CreateDecorator
      
  @Service.PCCellBase._RegScriptProc_P('Create')
  def PCProcBase_Create(CleObj,StarSpaceObject,ProcName,InputQueue,OutputQueue):
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")
    Proc = Service.PCCellBase.CreateType(ProcName)
    #--input
    if InputQueue == None :
      pass
    else :
      Proc.InputFrom(InputQueue)
    #--output
    if OutputQueue == None :
      pass
    else :
      Proc.OutputFrom(OutputQueue)
    if StarSpaceObject == None :
      pass
    else :
      StarSpaceObject.SetObject(Proc)  
    return Proc
    
  @Service.PCRealmBase._RegScriptProc_P('LoadPackage')
  def PCRealmBase_LoadPackage(CleObj,PackageList):
    PackageInfo = PackageList['PackageInfo']
    if PackageInfo == None or PackageInfo._Number == 0 :
      return
    from pchain import loader
    LoadResult = True
    for item in PackageInfo._Iterator() :  
      url = item['PackageUrl']
      if len(url) == 0 :
        if loader.load(item['PackageName'],item['PackageVersion']) == False :
          print('package ',item['PackageName'],' has no url and not installed, can not load')
          LoadResult = False
      else :
        if loader.loadurl(url) == False :
          LoadResult = False
    return LoadResult
          
  return Service
  
def cleloop() : 
  import libstarpy
  print('enter loop, [ESC] to exit')
  @libstarpy._MsgLoop()
  def ExitProc() :
    if libstarpy._KeyPress() == 27 : 
      return True
    return False 
        
def cleterm() :
  global IsInitCLE
  if IsInitCLE == False :
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)  
    SrvGroup._ClearService()
    libstarpy._ModuleExit()
