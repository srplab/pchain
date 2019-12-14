# -*- coding: utf-8 -*-
"""
    main.py

    :package : {name}
    :date    : {date}
"""

import sys
import os
import pchain
from pchain import pydata
from pchain import pyproc
from pchain.pydata import PCPyDataClass
from pchain.pyproc import PCPyProcClass
import libstarpy

SrvGroup = libstarpy._GetSrvGroup(0)
Service = SrvGroup._GetService("","")

# define pcdata management type
pydata.DefineType('NumberClass') 

# define pcproc management type
@pyproc.DefineProc('NumberProc',(NumberClass),None)
def Execute(self,num) :
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return (0,0,None)  
  print(num.value())
  return (0,1,None)