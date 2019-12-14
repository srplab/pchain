def do(parameter) :
  import sys
  import os
  ppath = os.getcwd()
  ppath = os.path.join(ppath,'../')
  sys.path.insert(0,ppath)
  import pchain
  from pchain import loader

  Service=pchain.cleinit()
  SrvGroup = Service._ServiceGroup;

  realm = Service.PCRealmBase()  
  Result = loader.loadzip(parameter,True)
  pchain.cleterm()
  
  if Result == None :
    print('install failed')    
  else :
    print('install finish')

if __name__ == '__main__':
  import sys
  if len(sys.argv) != 2 :
    print('usage : python pcpackinstall.py xxx.1.0.0.zip')
  else :
    do(sys.argv[1])
