import sys
import os
try:
  import pchain
except Exception as exc:
  pchain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../')
  sys.path.insert(0,pchain_path)
  import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass

Service = pchain.cleinit()
import libstarpy

realm = Service.PCRealmBase._New()

# Define data types
pydata.DefineType('NumberClass',float)

realm.AddEnvData(NumberClass(1.2),NumberClass(3.4),NumberClass(4.5))
datas = realm.GetEnvData()
print(datas)

realm.RemoveEnvData(datas)
newdatas = realm.GetEnvData()
print(newdatas._Number)

realm.AddEnvData(datas)
datas = realm.GetEnvData()

realm.RemoveEnvData(datas[0])
print(realm.GetEnvData())
  
# enter loop
# pchain.cleloop()
# finish
pchain.cleterm() 