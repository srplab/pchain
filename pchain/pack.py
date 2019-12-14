def pack(ResultFolder) :
  import pchain
  import sys
  import os

  if os.path.exists('packageinfo.json') == False :
    print('file packageinfo.json" not existed')
    return False

  f = None
  if pchain.ispython2 == True :     
    f = open('packageinfo.json')
  else :
    f = open('packageinfo.json',encoding='utf-8')
  packagetxt = f.read()
  f.close()
        
  Service = pchain.cleinit()
  SrvGroup = Service._ServiceGroup;

  packageinfo = SrvGroup._NewParaPkg()
  if packageinfo._FromJSon(packagetxt) == False :
    SrvGroup._ClearService()
    libstarpy._ModuleExit()
    print('load packageinfo.json" failed')
    return False

  PackageLang = packageinfo["PackageLang"]
  if PackageLang != "python" and PackageLang != "python2" and PackageLang != "python3" and PackageLang != "c" and PackageLang != "c#" and PackageLang != "java" :
    print('PackageLang '+PackageLang+' is not defined or not supported')
    return False
    
  if PackageLang == "python" or PackageLang == "python2" or PackageLang == "python3":        
      try :
        print('try to create requirements.txt for python dependence, using \"pipreqs\"')
        from pipreqs import pipreqs
        pipreqs.init({'<path>':'./','--pypi-server':None,'--proxy':None,'--use-local':None,'--use-local':True,'--savepath':'./requirements.txt','--diff':None,'--clean':None,'--print':False})
        if os.path.exists("requirements.txt"):
            if os.path.getsize("requirements.txt") > 3 :
                print('create requirements.txt finish')
            else :
                os.remove("requirements.txt")
                print('no python dependence is needed')
            
      except Exception as exc:   
        print("failed, requirements.txt need to be created manually") 
  
  PackageEntry = packageinfo["PackageEntry"]  
  if PackageEntry == None or len(PackageEntry) == 0 :
    print('PackageEntry is not defined')
    return False

  print("begin update packageinfo.json ...")
  pchain.cleinit()

  #--save all object
  existedObjects = Service._AllObject()

  if PackageLang == "c" :
    Result = Service._DoFile("",PackageEntry,"");
  else :
    if PackageLang == "python" or PackageLang == "python2" or PackageLang == "python3":
      import sys
      sys.path.insert(0,os.getcwd())
      try :
        __import__(packageinfo['PackageName'])
        Result = [True,'']
      except Exception as exc:   
        import traceback
        traceback.print_exc()
        return False          
    else :
      Result = Service._DoFile(PackageLang,PackageEntry,"");

  if Result[0] == False :
    print(Result[1])
    return False

  createdObjects = Service._AllObject()

  def ObjectExist(which,obj):
    for val in obj._Iterator() :
      if val == which :
        return True
    return False

  newObjects = []
  for val in createdObjects._Iterator() :
    if ObjectExist(val,existedObjects) == False and \
      ( Service.PCDataBase._IsInst(val) == True or Service.PCProcBase._IsInst(val) == True ) :
      o_name = val._Name.split('.')
      if len(o_name) == 1 :
        pass
      elif len(o_name) == 2 :
        if o_name[0] == packageinfo["PackageName"] :
          pass
        else :
          print('failed, object '+val._Name+'  is in the package namespace')
          return False          
      else :
        print('failed, object '+val._Name+'  is in the package namespace')
        return False            
      newObjects.append(val)      
      print("new object captured : ",o_name[len(o_name)-1])

  ObjectList = SrvGroup._NewParaPkg()
  for i in range(len(newObjects)):
    o_name = newObjects[i]._Name.split('.')
    ObjectList[ObjectList._Number] = packageinfo["PackageName"] + "." + o_name[len(o_name)-1]

  packageinfo["ObjectList"] = ObjectList
  
  #Calculate md5 value without file packageinfo.json
  packageinfo["signature"] = getmd5()

  f = None
  if pchain.ispython2 == True :     
    f = open('packageinfo.json','w')
  else :
    f = open('packageinfo.json','w',encoding='utf-8')
  packagetxt = f.write(packageinfo._ToJSon())
  f.close()

  print("end update packageinfo.json ...")
  ZipPackageName = packageinfo["PackageName"] + "-" + packageinfo["PackageLang"].lower() + "." + packageinfo["PackageVersion"]

  pchain.cleterm()

  print("start packing ...")
  import zipfile

  def zippackag(ZipPackageName):
    file_news = ZipPackageName +'.zip'
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk("."):
      fpath = dirpath.replace(".",'')
      fpath = fpath and fpath + os.sep or ''
      for filename in filenames:
        if filename == file_news :
          pass
        else :
          z.write(os.path.join(dirpath, filename),fpath+filename)
    z.close()
  zippackag(ResultFolder+os.sep+ZipPackageName)

  print("finish ...")
  return True
  

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