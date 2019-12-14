def return_internal(Result,PackageName) :
    if Result == True :
      import libstarpy
      SrvGroup = libstarpy._GetSrvGroup(0)
      Service = SrvGroup._GetService("","")        
      return Service._GetObject(PackageName)
    else :
      return None
      
def getmd5() :
  import os
  import hashlib
  fileMd5 = hashlib.md5()
  for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
      whichf = os.path.join(dirpath, filename)
      if filename == 'packageinfo.json' :
        continue
      fileOpen = open(whichf, 'rb')
      fileMd5.update(fileOpen.read())
      fileOpen.close()
  return fileMd5.hexdigest()      

def load(PackageName,PackageVersion='',PrintFlag=True) :
  try:
    import os
    import pchain
    
    if pchain.SystemPackageInfo == None :
      import libstarpy
      SrvGroup = libstarpy._GetSrvGroup(0)
      Service = SrvGroup._GetService("","")        
    
      query = SrvGroup._NewQueryRecord()      
      realmobj = Service.PCRealmBase._FirstInst(query)
      Service.PCRealmBase._QueryClose(query) 
      if realmobj == None :
        if PrintFlag == True :
          print('PCRealmBase instance is not created')
        return None
      else :
        pchain.SystemPackageInfo = realmobj.GetSystemPackageInfo()   
            
    if pchain.SystemPackageInfo != None :
      for loadedpackage in pchain.SystemPackageInfo._Iterator() :
        if loadedpackage["PackageName"] == PackageName :
          if len(PackageVersion) == 0 :
            return return_internal(True,PackageName)
          elif PackageVersion <= loadedpackage["PackageVersion"] :
            return return_internal(True,PackageName)
          else :
            if PrintFlag == True :
              print('the request package "'+PackageName+'['+PackageVersion+']" had been loaded with another version ['+loadedpackage["PackageVersion"]+']')
            return None
    
    PackageName_WithExt = None
    if True :
      dirList = []
      ext_name = None
      if pchain.ispython2 == True : 
        ext_name = '-python2'
      else :
        ext_name = '-python3'
      files = os.listdir(pchain.packagepath)
      for f in files:
        if os.path.isdir(pchain.packagepath + '/' + f) == True and f.startswith(PackageName+'-python.') == True :
          dirList.append(f)
        elif os.path.isdir(pchain.packagepath + '/' + f) == True and f.startswith(PackageName+ext_name+'.') == True :
          dirList.append(f)
      if len(dirList) == 0 :
        if PrintFlag == True :
          print(PackageName + ' is not installed')
        return None
      # find the highest 
      installed_package_version = ""
      for f in dirList :
        thisver = f[f.index('.')+1:]      
        if len(installed_package_version) == 0 :
          if len(PackageVersion) == 0 :
            installed_package_version = thisver
            PackageName_WithExt = f
          elif installed_package_version >= PackageVersion :
            installed_package_version = thisver
            PackageName_WithExt = f
        else :
          if installed_package_version < thisver :
            installed_package_version = thisver
            PackageName_WithExt = f
      if len(installed_package_version) == 0 :
        if PrintFlag == True :
          print(PackageName + ' version '+PackageVersion+' is not installed')
        return None      
      PackageVersion = installed_package_version
    
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")      
    
    f = None
    if pchain.ispython2 == True :      
      f = open(pchain.packagepath+'/'+PackageName_WithExt + "/packageinfo.json")
    else :
      f = open(pchain.packagepath+'/'+PackageName_WithExt + "/packageinfo.json",encoding='utf-8')
    packagetxt = f.read()
    f.close()
    
    packageinfo = SrvGroup._NewParaPkg()
    if packageinfo._FromJSon(packagetxt) == False :  
      if PrintFlag == True :
        print('invalid format "packageinfo.json" for package '+PackageName )
      return None
    Result = loadinternal(packageinfo["PackageName"],packageinfo["PackageLang"],packageinfo["PackageEntry"],pchain.packagepath+'/'+PackageName_WithExt)
    if Result == True and pchain.SystemPackageInfo != None :
      pchain.SystemPackageInfo[pchain.SystemPackageInfo._Number] = packageinfo
    return return_internal(Result,packageinfo["PackageName"])
          
  except Exception as exc:   
    if PrintFlag == True :
      print(repr(exc))
    return None         

def loadurl(url) :
  try :
    import urllib 
    import os
    import sys
    import logging
    import pchain

    if pchain.ispython2 == True : 
      import urllib2 
      from urllib import ContentTooShortError
    else :
      from urllib.request import urlretrieve
      from urllib.error import ContentTooShortError
    
    try :
      import requests
    except Exception as exc:
      print("can not import python module 'requests', install it")
      import sys
      import subprocess
      Result = subprocess.call([sys.executable, "-m", "pip", "install", "requests"])    
      if Result != 0 :
        print("install requests failed")
        return None
      else :
        print("install requests finish")
          
    fname = url.split('/')[-1]
    if fname.endswith(".zip") == False :
      print('package file must be a zip compressed file and end with .zip')
      return None  
    #extrace package name and version
    flist = fname.split('.')
    if len(flist) == 5 :
      pass
    else :
      print('invalid package name, must be xxxx.x.x.x.zip')
      return None  
    PackageName = flist[0][:flist[0].rindex('-')]    
    if load(PackageName,flist[1]+'.'+flist[2]+'.'+flist[3],False) == None :
      #print(PackageName + ' had been installed before')
      pass
    else :
      return return_internal(True,PackageName)    
    
    import tempfile
    f, output_filename = tempfile.mkstemp(suffix='.zip')
    os.close(f)
    
    def report(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      if percent > 100 :
        percent = 100
      sys.stdout.write("\r%d%%" % percent + ' complete')
      sys.stdout.flush()

    print('begin download '+url)
    if pchain.ispython2 == True : 
      urllib.urlretrieve(url, output_filename,report)
    else :
      urlretrieve(url, output_filename,report)
    print('\nfinish download '+url)
    Result = loadzip_internal(output_filename,url,True)
    os.remove(output_filename)
    return Result
    
  except ContentTooShortError:
    loadurl(url)
  except Exception as exc:   
    print('download ['+url+'] failed, '+repr(exc))
    return None     

def loadzip(zipfilename,installIgnoreVersion = False) :
  return loadzip_internal(zipfilename,'',installIgnoreVersion)

# if call without packagepath, the package will be installde
def loadzip_internal(zipfilename,url,installIgnoreVersion) :
  import zipfile
  import os
  import pchain
  try:
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")  
    
    destfolder = pchain.packagepath
    if installIgnoreVersion == False :
      tempname = zipfilename.replace("\\","/")
      fname = tempname.split('/')[-1]
      flist = fname.split('.')
    
      if len(flist) == 5 :
        pass
      else :
        print('invalid package name, must be xxxx.x.x.x.zip')
        return None      
      PackageName = flist[0][:flist[0].rindex('-')]
      if load(PackageName,flist[1]+'.'+flist[2]+'.'+flist[3],False) == None :
        pass
      else :
        return return_internal(True,PackageName)     
    myzip = zipfile.ZipFile(zipfilename)
    f = None
    if pchain.ispython2 == True : 
      f = myzip.open("packageinfo.json")
    else :
      f = myzip.open("packageinfo.json")
    packagetxt = f.read()
    f.close()
    
    if pchain.ispython2 == False :     
      packagetxt = packagetxt.decode(encoding='utf-8')
    
    packageinfo = SrvGroup._NewParaPkg()
    if packageinfo._FromJSon(packagetxt) == False :  
      print('"packageinfo.json" invalid format' )
      return None
    fpath = os.path.join(destfolder,packageinfo["PackageName"] + "-" + packageinfo["PackageLang"].lower()+"."+packageinfo["PackageVersion"])
    if os.path.exists(fpath) == False : 
      os.makedirs(fpath)
      
    # print('begin uncompress...')
    for file in myzip.namelist():
      myzip.extract(file,fpath)
    myzip.close() 
    
    # check signature
    currentpath = os.getcwd()
    os.chdir(fpath)
    package_signature = getmd5()
    os.chdir(currentpath)
    
    if package_signature == packageinfo["signature"] :
      pass
    else :
      print(packageinfo["PackageName"]+'singature check failed.')
      return None       
    
    PackageLang = packageinfo["PackageLang"]
    if PackageLang != "python" and PackageLang != "python2" and PackageLang != "python3" and PackageLang != "c" and PackageLang != "c#" and PackageLang != "java" :
      print('PackageLang '+PackageLang+' is not defined or not supported')
      return None    
    
    if PackageLang == "python" or PackageLang == "python2" or PackageLang == "python3":
      if os.path.exists(fpath+"/requirements.txt") == True and os.path.getsize(fpath+"/requirements.txt") > 3 \
        and (pchain.platform == 'windows' or pchain.platform == 'linux' or pchain.platform == 'darwin' ): 
        print("find requirements.txt, processing it")
        import sys
        import subprocess
        Result = subprocess.call([sys.executable, "-m", "pip", "install", "-r", fpath+"/requirements.txt"])    
        if Result != 0 :
           print("install requirements.txt failed")
        else :
          print("install requirements.txt finish")     
  
    PackageEntry = packageinfo["PackageEntry"]  
    if PackageEntry == None or len(PackageEntry) == 0 :
      print('PackageEntry is not defined')
      return None
    
    Result = loadinternal(packageinfo["PackageName"],PackageLang,PackageEntry,fpath)

    #update url  
    if len(url) == 0 :
      if pchain.SystemPackageInfo == None :
        query = SrvGroup._NewQueryRecord()      
        realmobj = Service.PCRealmBase._FirstInst(query)
        Service.PCRealmBase._QueryClose(query) 
        if realmobj == None :
          print('PCRealmBase instance is not created')
          return None
        else :
          pchain.SystemPackageInfo = realmobj.GetSystemPackageInfo()   
            
      if Result == True and pchain.SystemPackageInfo != None :
        pchain.SystemPackageInfo[pchain.SystemPackageInfo._Number] = packageinfo
    else :
      if Result == True :
        f = None
        if pchain.ispython2 == True :     
          f = open(os.path.join(fpath+'/packageinfo.json'))
        else :
          f = open(os.path.join(fpath+'/packageinfo.json'),mode='r',encoding='utf-8')
        packagetxt = f.read()
        f.close()
        
        packageinfo = SrvGroup._NewParaPkg()
        if packageinfo._FromJSon(packagetxt) == True :
          packageinfo['PackageUrl'] = url
          if pchain.ispython2 == True :     
            f = open(os.path.join(fpath+'/packageinfo.json'),'w')
          else :
            f = open(os.path.join(fpath+'/packageinfo.json'),mode='w',encoding='utf-8')
          packagetxt = f.write(packageinfo._ToJSon())
          f.close()
          
          if Result == True and pchain.SystemPackageInfo != None :
            pchain.SystemPackageInfo[pchain.SystemPackageInfo._Number] = packageinfo
            
    return return_internal(Result,packageinfo["PackageName"]) 

  except Exception as exc:   
    print(exc)
    return None 

def loadfolder(Folder,PrintFlag=True) :
  import os
  try:
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")  
    import pchain

    if os.path.exists(Folder + '/packageinfo.json' ) == False : 
      if PrintFlag == True :
        print(Folder + '/packageinfo.json is not found')
      return None
          
    f = None
    if pchain.ispython2 == True : 
      f = open(Folder + "/packageinfo.json")
    else :
      f = open(Folder + "/packageinfo.json",encoding='utf-8')
    packagetxt = f.read()
    f.close()
    
    packageinfo = SrvGroup._NewParaPkg()
    if packageinfo._FromJSon(packagetxt) == False :  
      if PrintFlag == True :
        print('invalid format "packageinfo.json"' )
      return None
    Result = loadinternal(packageinfo["PackageName"],packageinfo["PackageLang"],packageinfo["PackageEntry"],Folder)
    if pchain.SystemPackageInfo == None :
      query = SrvGroup._NewQueryRecord()      
      realmobj = Service.PCRealmBase._FirstInst(query)
      Service.PCRealmBase._QueryClose(query) 
      if realmobj == None :
        print('PCRealmBase instance is not created')
        return None
      else :
        pchain.SystemPackageInfo = realmobj.GetSystemPackageInfo()    
    if Result == True and pchain.SystemPackageInfo != None :
      pchain.SystemPackageInfo[pchain.SystemPackageInfo._Number] = packageinfo
    return return_internal(True,packageinfo["PackageName"]) 
    
  except Exception as exc:   
    if PrintFlag == True :
      print(repr(exc))
    return None      
    
def loadinternal(PackageName,PackageLang,PackageEntry,Folder) :
  import os
  try:
    import libstarpy
    SrvGroup = libstarpy._GetSrvGroup(0)
    Service = SrvGroup._GetService("","")  
    import pchain
      
    if PackageLang != "python" and PackageLang != "python2" and PackageLang != "python3" and PackageLang != "c" and PackageLang != "c#" and PackageLang != "java" :
      print('PackageLang '+PackageLang+' is not defined or not supported')
      return False
  
    if PackageEntry == None or len(PackageEntry) == 0 :
      print('PackageEntry is not defined')
      return False
    
    if PackageLang == "python" or PackageLang == "python2" or PackageLang == "python3": 
      if pchain.ispython2 == True :  
        if PackageLang == "python" or PackageLang == "python2" :
          pass
        else :
          print('PackageLang '+PackageLang+' is not supported, must be python or python2 ')
          return False
      else :
        if PackageLang == "python" or PackageLang == "python3" :
          pass
        else :
          print('PackageLang '+PackageLang+' is not defined or not supported, must be python or python3')
          return False

    #--save all object
    existedObjects = Service._AllObject()

    if PackageLang == "c" :
      Result = Service._DoFile("",Folder+"/"+PackageEntry,"");
    else :
      if PackageLang == "python" or PackageLang == "python2" or PackageLang == "python3" :
        import sys
        sys.path.insert(0,Folder)
        try :
          __import__(PackageName)
          Result = [True,'']
        except Exception as exc:   
          import traceback
          traceback.print_exc()
          return False          
      else :
        Result = Service._DoFile(PackageLang,Folder+"/"+PackageEntry,"");

    if Result[0] == False :
      print(Exception(Result[1]))
      return False    
    return True  
  except Exception as exc:   
    print(exc)
    return False     
    
def loadobjectpackage(parapkg) :
  packageinfo = parapkg["PackageInfo"]
  if packageinfo == None or packageinfo._Number == 0 :
    return True
  for i in range(packageinfo._Number) :
    eachpackage = packageinfo[i]
    if load(eachpackage["PackageName"],eachpackage["PackageVersion"],False) == None :
      if loadurl(eachpackage["PackageUrl"]) == None :
        print("package "+eachpackage["PackageName"]+"."+eachpackage["PackageVersion"]+" can not load")
        return False
  return True         
    
if __name__ == '__main__':
  #--test
  import sys
  import os
  ppath = os.getcwd()
  sys.path.insert(0,os.path.join(ppath,"../"))
  import pchain
  
  import platform
  version = platform.python_version().split('.')
  modulename = ""
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
    raise Exception('not supported')  
  Service=libstarpy._InitSimple("test","123",0,0);
  SrvGroup = Service._ServiceGroup;

  pchain.cleinit()
  loadurl('http://localhost:4000/test.1.0.0.zip')