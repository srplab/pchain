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
print(result)
img = result

result = realm.RunProc(img,None,ImageFormatProc,ImageSizeProc,ImageHistogramProc)
print(result)

result = realm.RunProc(img,('m',ImageHistogramClass,'m',SizeClass),ImageFormatProc,ImageSizeProc,ImageHistogramProc)
print(result)

print('dynamic add proc......')

@realm._RegScriptProc_P('OnCellToBeFinish')
def OnCellToBeFinish(Realm,cell):
  print('ImageOpenProc  is executed?  ',cell.IsProcExecuted(ImageOpenProc))
  output = cell.GetCellMissingOutput()
  if output._Number == 0 :
    return False
  for item in output :
    if cell.IsCellOutputMustExist(item) == True :
      input = cell.GetEnvData()
      chain = Realm.BuildProcChain(output,input)
      if chain[0] == False :
        return False  # failed
      if cell.FindProc(chain[1]) == None :
        cell.AddProc(chain[1])
        return True
      else :
        return False
        
@realm._RegScriptProc_P('OnOutputDataToEnv')
def OnOutputDataToEnv(Realm,cell,proc,datalist):  
  print('output data  ',str(datalist))

print('+++++++++++++++++++++++++')
result = realm.RunProc(img,('m',ImageHistogramClass,'m',SizeClass),ImageFormatProc,ImageSizeProc)
print(result)

result = realm.RunProc(img,(ImageHistogramClass,SizeClass),ImageFormatProc,ImageSizeProc)
print(result)


print('source is   ',str(result[0].GetSource()[0]))

pchain.cleterm() 