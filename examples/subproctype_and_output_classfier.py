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

print('please using python 2.7....')

pydata.DefineType('IndexClass',int)
pydata.DefineType('TotalClass',int)
pydata.DefineType('CapitalsClass',type({}))
pydata.DefineType('StatesClass',type([]))

pydata.DefineType('FileClass',file)
pydata.DefineSubType(FileClass,'QuizFileClass')
pydata.DefineSubType(FileClass,'AnswerKeyFileClass')

@pyproc.DefineProc('CreateIndexProc',(TotalClass,CapitalsClass),(IndexClass,CapitalsClass))
def Execute(self,Total,capitals) :
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return (0,0,None)
  if Context['SelfObj'].Status == 0 :
    Context['SelfObj'].GetLocalBuf()[0] = 0
    Context['SelfObj'].Status = 1
  index = Context['SelfObj'].GetLocalBuf()[0]
  Context['SelfObj'].GetLocalBuf()[0] = index + 1
  ret_index = IndexClass(index)
  ret_captial = CapitalsClass(capitals.value())
  ret_captial.AddSource(ret_index)
  if index + 1 >= Total.value() :
    return (0,1,(ret_index,ret_captial))
  else :
    return (4,0,(ret_index,ret_captial))

@pyproc.DefineProc('CreateTestFileProc',(IndexClass,'s',CapitalsClass),(StatesClass,FileClass))
def Execute(self,Index,capitals) :
  Context = self.Context  #  first must save Context in local variable
  if Context['SelfObj'].Status < 0 :
    return (0,0,None)  
  quizFile = open('capitalsquiz%s.txt' % (Index.value() + 1), 'w')
  answerKeyFile = open('capitalsquiz_answers%s.txt' % (Index.value() + 1), 'w')
  quizFile.write('Name:\n\nDate:\n\nPeriod:\n\n')
  quizFile.write((' ' * 20) + 'State Capitals Quiz (Form %s)' % (Index.value() + 1))
  quizFile.write('\n\n')
  
  import random
  states = list(capitals.value().keys())  
  random.shuffle(states)
  
  Context['SelfObj'].AcceptInput(Index)
  return (3,0,(StatesClass(states),FileClass(quizFile),FileClass(answerKeyFile)))

@pyproc.DefineProc('Parent_WriteContentFileProc',(IndexClass,'s',CapitalsClass,'s',StatesClass,'s',QuizFileClass,'s',AnswerKeyFileClass),None)
def Execute(self,Index,capitals,states,quizFile,answerKeyFile) :
  Context = self.Context  #  first must save Context in local variable
  
  print('WriteContentFileProc          ',str(quizFile))
  
  capitals = capitals.value()
  states = states.value()
  quizFile = quizFile.value()
  answerKeyFile = answerKeyFile.value()
  
  import random
  
  for questionNum in range(50):
    correctAnswer = capitals[states[questionNum]]
    wrongAnswers = list(capitals.values())
    del wrongAnswers[wrongAnswers.index(correctAnswer)]
    wrongAnswers = random.sample(wrongAnswers, 3)
    answerOptions = wrongAnswers + [correctAnswer]
    random.shuffle(answerOptions)
    
    quizFile.write('%s. What is the capital of %s?\n' % (questionNum + 1,states[questionNum]))
    for i in range(4):
      quizFile.write(' %s. %s\n' % ('ABCD'[i], answerOptions[i]))
    quizFile.write('\n')

    answerKeyFile.write('%s. %s\n' % (questionNum + 1, 'ABCD'[answerOptions.index(correctAnswer)]))
  
  return (0,1,None)

#create sub proc type
WriteContentFileProc = Parent_WriteContentFileProc.CreateSubType("WriteContentFileProc",None)  
  
@pyproc.DefineProc('CloseContentFileProc',(FileClass),None)
def Execute(self,ContentFile) :
  Context = self.Context  #  first must save Context in local variable
  #--when to close?  the ContentFile can not allocated to other procs
  if Context['Cell'].IsFinishExcept(ContentFile,Context['SelfObj']) == True :
    print('close file   -------------   ',str(ContentFile))
    ContentFile.value().close()
    return (0,1,None)
  else :
    return (4,0,None)
    
#  TestFile classfier
@pyproc.DefineProc('TestFileClassfierProc',(FileClass),(FileClass))
def Execute(self,TestFile) :
  Context = self.Context  #  first must save Context in local variable
  if TestFile.value().name.startswith('capitalsquiz_answers') :
    return (0,1,AnswerKeyFileClass(TestFile.value()))
  else :
    return (0,1,QuizFileClass(TestFile.value()))
    
#--create a new cell type to refine the output, put  TestFileClassfierProc and CreateTestFileProc into it
CreateTestFileCell = Service.PCCellBase.Create(None,'CreateTestFileCell',CreateTestFileProc.GetType().InputQueueToParaPkg(),(StatesClass,AnswerKeyFileClass,QuizFileClass))
CreateTestFileCell.AddProc(CreateTestFileProc,TestFileClassfierProc)
#CreateTestFileCell.ConnectProc(CreateTestFileProc,TestFileClassfierProc)

g_capitals = CapitalsClass({'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix','Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver','Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee','Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois':'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas':'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine':'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan':'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri':'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada':'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'NewMexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh','North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City','Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence','South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee':'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'WestVirginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'})
realm.RunProc((TotalClass(3),g_capitals),None,CreateIndexProc,CreateTestFileCell,WriteContentFileProc,CloseContentFileProc)

pchain.cleterm() 