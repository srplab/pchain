def PrintUsage() :
  print('usage : python -m pchain --pack packagefolder')
  print('usage : python -m pchain --project projectname')
  print('usage : python -m pchain --package packagename')
  print('usage : python -m pchain --install xxx.1.0.0.zip')

import sys
if len(sys.argv) < 3 :
  PrintUsage()
else :
  if sys.argv[1] == '--pack' :
    from pchain.tools import pcpack  
    pcpack.do(sys.argv[2])
  elif sys.argv[1] == '--project' :
    from pchain.tools import pcmanager 
    pcmanager.do('--project',sys.argv[2])
  elif sys.argv[1] == '--package' :
    from pchain.tools import pcmanager 
    pcmanager.do('--package',sys.argv[2])    
  elif sys.argv[1] == '--install' :
    from pchain.tools import pcpackinstall 
    pcpackinstall.do(sys.argv[2])        
  else :  
    PrintUsage()
  