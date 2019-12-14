def do(parameter) :
  import sys
  import os
  ppath = os.getcwd()
  ppath = os.path.join(ppath,'../')
  sys.path.insert(0,ppath)
  import pchain
  from pchain import pack

  currentpath = os.getcwd()
  packagepath = os.path.join(currentpath,parameter)
  if os.path.exists(packagepath) == False :
    print(packagepath + ' not exist')
    return
  os.chdir(packagepath)
  pack.pack(currentpath)
  os.chdir(currentpath)

if __name__ == '__main__':
  import sys
  if len(sys.argv) != 2 :
    print('usage : python pack.py packagefolder')
  else :
    do(sys.argv[1])
