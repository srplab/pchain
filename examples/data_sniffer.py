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

from PIL import Image

Service = pchain.cleinit()
import libstarpy

realm = Service.PCRealmBase._New()

pydata.DefineType('SizeClass',type(()))
pydata.DefineType('IntClass',type(int))
pydata.DefineType('ImageFileClass',type(''))
pydata.DefineType('ImageClass')
pydata.DefineType('ImageFormatClass',type(''))
pydata.DefineType('ImageHistogramClass',type([]))

@pyproc.DefineProc('ImageOpenProc',ImageFileClass,ImageClass)
def Execute(self,ImageFile) :  
  Context = self.Context  #  first must save Context in local variable
  im = Image.open(ImageFile.value())
  return (0,1,ImageClass(im))
  
@pyproc.DefineProc('ImageResizeProc',(ImageClass,SizeClass),ImageClass)
def Execute(self,InputImage,NewSize) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return (0,0,None)
  if Context['Cell'].IsFromOutSide(NewSize) == False :
    print( 'size   ',NewSize.value(),'  is from internal, reject it')
    Context['SelfObj'].RejectInput(NewSize)
    return (2,0,None)
  newim = InputImage.value().resize(NewSize.value())
  #--set source image
  Context['SelfObj'].AddOutputDataEx(ImageClass(newim),InputImage)
  return (0,1,None)

@pyproc.DefineProc('ImageSizeProc',ImageClass,SizeClass)
def Execute(self,InputImage) :  
  Context = self.Context  #  first must save Context in local variable
  return (0,1,SizeClass(InputImage.value().size))
 
@pyproc.DefineProc('ImageFormatProc',ImageClass,ImageFormatClass)
def Execute(self,InputImage) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return (0,0,None)  
  if InputImage.value().format == None :
    return (2,-1,None)  
  return (0,1,ImageFormatClass(InputImage.format))    
  
@pyproc.DefineProc('ImageHistogramProc',ImageClass,ImageHistogramClass)
def Execute(self,InputImage) :  
  Context = self.Context  #  first must save Context in local variable
  return (0,1,ImageHistogramClass(InputImage.value().histogram()))

result = realm.RunProc((ImageFileClass('pchain.png'),SizeClass((100,100))),None,ImageOpenProc,ImageResizeProc)
img = result

#----------------------------------------------------------------------------------------------------------------------
#first method    
#create reaml stub to check all data object created

'''
realmstub = Service.PCRealmStubBase._New()
@realmstub._RegScriptProc_P('OnOutputDataToEnv')
def OnOutputDataToEnv(SelfObj,Realm,PCCell,PCProc,DataList):
  for item in DataList :
    print('output  data    ',str(item))
realm.SetRealmStub(realmstub) 

result = realm.RunProc(img,('m',ImageHistogramClass,'m',SizeClass),ImageFormatProc,ImageSizeProc,ImageHistogramProc)
print(result)
'''

#----------------------------------------------------------------------------------------------------------------------
#second method    

@pyproc.DefineProc('MonitorDataProc',Service.PCDataBase,None)
def Execute(self,data) :  
  Context = self.Context  #  first must save Context in local variable
  if Context['Cell'].IsFromOutSide(data) == True :
    return (0,-1,None)
  print('output.................',data) 
  return (0,-1,None)   # this proc does not process input,so reject input
  
result = realm.RunProc(img,None,ImageFormatProc,ImageSizeProc,ImageHistogramProc,MonitorDataProc)
print(result)
#----------------------------------------------------------------------------------------------------------------------

pchain.cleterm() 