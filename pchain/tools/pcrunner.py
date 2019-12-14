def do(arg1,arg2='') :
  import sys
  import os
  ppath = os.getcwd()
  ppath = os.path.join(ppath,'../')
  sys.path.insert(0,ppath)
  import pchain
  from pchain import runner

  if len(arg2) == 0 :
    runner.run(os.path.join(os.getcwd(),arg1))
  else :
    if arg1.lower() == "--debug" :  
      runner.run(os.path.join(os.getcwd(),arg2),True)
    if arg1.lower() == "--develop" : 
      pchain.webpath = os.path.join(pchain.path + '/../pcconsole/pcconsole')
      runner.run(os.path.join(os.getcwd(),arg2),True)
      
if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2 :
    print('usage : python pcrunner.py [--DEBUG|--DEVELOP] xxx.py')
  else :
    if len(sys.argv) == 2 :
      do(sys.argv[1])
    else :
      do(sys.argv[1],sys.argv[2])