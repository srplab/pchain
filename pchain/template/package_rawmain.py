# -*- coding: utf-8 -*-
"""
    main.py

    :package : {name}
    :date    : {date}
"""

import sys
import os
import pchain
import libstarpy
SrvGroup = libstarpy._GetSrvGroup(0)
Service = SrvGroup._GetService("","")

# define pcdata management type
NumberClass = Service.PCDataBase.CreateType("NumberClass")

# define pcproc management type

@Service.PCProcBase.Create(None,"NumberProc",(NumberClass),(NumberClass,NumberStepClass))
def NumberProc_Execute(SelfObj,Realm,Cell,Runner) :
  #get input
  in1 = SelfObj.InputToParaPkg()
  if in1[0] == None :
    return 2
  SelfObj.AcceptInput()  

  #   create output 
  SelfObj.AddOutputData(in1[0])
  return 0
