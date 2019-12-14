# python 2.7

import sys
import os
try:
  import pchain
except Exception as exc:
  pchain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../')
  sys.path.insert(0,pchain_path)
  import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

Service = pchain.cleinit()
import libstarpy

from data_and_proc_type import StringClass
from data_and_proc_type import UrlClass
from data_and_proc_type import WebPageClass

from data_and_proc_type import DownLoadUrlProc
from data_and_proc_type import StringToUrlProc


print('string \"download\" tag is   :',StringClass('download').GetTag())
print('DownLoadUrlProc tag is   :',DownLoadUrlProc.GetType().GetTag())
print('StringClass tag is   :',StringClass.GetType().GetTag())


#space = Service.StarObjectSpace._New("TestSpace")   
#pydata.DefineSubType(StringClass,'SubStringClass')
#print('SubStringClass tag is   :',SubStringClass.GetType().GetTag())

#print('SubStringClass(sss) tag is   :',SubStringClass('sss').GetTag())
#print('SubStringClass(sss) taglabel is   :',SubStringClass('sss').GetTagLabel())

#bb = SubStringClass('sss')
#bb.SetSignature('sdsfsdfsdf')
#print('bb tag is   :',bb.GetTag())
#print('bb taglabel is   :',bb.GetTagLabel())

#print(bb.IsInstance(StringClass))