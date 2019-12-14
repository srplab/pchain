def do(cmd,parameter) :
  import sys
  import os
  ppath = os.getcwd()
  ppath = os.path.join(ppath,'../')
  sys.path.insert(0,ppath)
  import pchain
  from pchain import runner

  if cmd.lower() == '--project' or cmd.lower() == '--raw_project' : # create project
    try :
      projectname = parameter
      print('create project '+projectname)
      cpath = os.getcwd()
      ppath = os.path.join(cpath,projectname)
      if os.path.exists(ppath) == False : 
        os.makedirs(ppath)
      #copy template
      srcfile = None
      if cmd.lower() == '--project' :      
        srcfile = os.path.join(pchain.templatepath,'project_main.py')
      else :
        srcfile = os.path.join(pchain.templatepath,'project_rawmain.py')
      desfile = os.path.join(ppath,'main.py')
      if os.path.exists(desfile) == True : 
        val = ''
        if pchain.ispython2 == True :
          val = raw_input(projectname+'/main.py has existed, overwrite it [Y]/N? ')
        else :
          val = input(projectname+'/main.py has existed, overwrite it [Y]/N? ')
        if val.lower() == 'n' :
          return False
      #-read file
      f = None
      if pchain.ispython2 == True :
        f = open(srcfile)
      else :
      	f = open(srcfile,encoding='utf-8')
      t = f.read()
      f.close()       
        
      import time
      key = {"name":projectname,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"pchain_path":os.path.join(pchain.path,'../')}
      outstr = t. format(**key)    

      f = None
      if pchain.ispython2 == True :     
        f = open(desfile,'w')
      else :
        f = open(desfile,'w',encoding='utf-8')
      f.write(outstr)
      f.close() 
       
      print('create project finish')
      return True
        
    except Exception as exc:   
      import traceback
      traceback.print_exc()
      return False  
        
  if cmd.lower() == '--package' or cmd.lower() == '--raw_package' : # create package
    try :
      packagename = parameter
      print('create package '+packagename)
      cpath = os.getcwd()
      ppath = os.path.join(cpath,packagename)
      if os.path.exists(ppath) == False : 
        os.makedirs(ppath)

      lang = '0'
      #if pchain.ispython2 == True :
      #  lang = raw_input('0-python,1-c/c++,2-c#,3-java, lang = [0]? ')
      #else :
      #  lang = input('0-python,1-c/c++,2-c#,3-java, lang = [0]? ')
      if len(lang) == 0 or lang.lower() == '0' :
        #copy template
        srcfile = None
        if cmd.lower() == '--package' :
          srcfile = os.path.join(pchain.templatepath,'package_main.py')
        else :
          srcfile = os.path.join(pchain.templatepath,'package_rawmain.py')
        desfile = os.path.join(ppath,packagename+'.py') # 'main.py')
        if copyfile(packagename,srcfile,desfile,True) == False :
          return False
      
        srcfile = os.path.join(pchain.templatepath,'packageinfo.json')
        desfile = os.path.join(ppath,'packageinfo.json')
        if os.path.exists(desfile) == True : 
          print('create package finish')
          return True
            
        #-read file
        f = None
        if pchain.ispython2 == True :
          f = open(srcfile)
        else :
          f = open(srcfile,encoding='utf-8')
        t = f.read()
        f.close()
          
        import json
        from collections import OrderedDict
        packageinfo = json.loads(t,object_pairs_hook=OrderedDict)
        packageinfo['PackageName'] = packagename
        packageinfo['PackageLang'] = 'python'
        packageinfo['PackageInfo'] = packagename + ' info'
        packageinfo['PackageEntry'] = packagename + '.py'
          
        f = None
        if pchain.ispython2 == True :     
          f = open(desfile,'w')
        else :
          f = open(desfile,'w',encoding='utf-8')
        f.write(json.dumps(packageinfo))
        f.close()    
           
        print('create package finish')
        return True     
          
      else : 
        print('lang '+lang+' may be supported in future')
        return False
        
    except Exception as exc:   
      import traceback
      traceback.print_exc()
      return False  
                
def copyfile(name,srcfile,desfile,promote) :
  try :
    import os
    import pchain
    if os.path.exists(desfile) == True and promote == True :
      val = ''
      if pchain.ispython2 == True :
        val = raw_input(desfile + ' has existed, overwrite it [Y]/N? ')
      else :
        val = input(desfile + ' has existed, overwrite it [Y]/N? ')
      if val.lower() == 'n' :
        return False
    #-read file
    f = None
    if pchain.ispython2 == True :
      f = open(srcfile)
    else :
      f = open(srcfile,encoding='utf-8')
    t = f.read()
    f.close()       
    
    import time
    key = {"name":name,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"pchain_path":os.path.join(pchain.path,'../')}
    outstr = t.format(**key)     

    f = None
    if pchain.ispython2 == True :     
      f = open(desfile,'w')
    else :
      f = open(desfile,'w',encoding='utf-8')
    f.write(outstr)
    f.close() 
        
    return True

  except Exception as exc:   
    import traceback
    traceback.print_exc()
    return False            
              
if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2 :
    print('usage : python pcmanager.py --project projectname')
    print('        python pcmanager.py --package packagename')
  else :
    do(sys.argv[1],sys.argv[2])