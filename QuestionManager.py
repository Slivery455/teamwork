from tkinter import *
import tkinter.ttk
import tkinter.messagebox
import xml.etree.ElementTree as xt
import os
from Error import ParamError
from Trendency import Trend

class Answer():
    def __init__(self,this,attr):
        if isinstance(attr,dict) == False or ('no' in attr == False) or ('text' in attr == False) or (isinstance(this,int) == False):
            raise ParamError('Error Param for initializing Answer.')
        self.no = int(attr['no'])
        self.this = this
        self.next = int(attr['next'])
        self.text = attr['text']

class Question():
    def __init__(self,no,text):
        if isinstance(no,int)== False or isinstance(text,str) == False:
            raise ParamError('Error Param for initializing Question.')
        self.no = no
        self.text = text

class QuestionManager():
    questions = []
    answers = []
    history = []
    chosen = []
    #obj is using for Single Pattern
    obj = None
    def __init__(self):
        if self.obj == None:
            done = True
            obj = self
            if (os.path.exists('questionnaire.xml') == False):
                print('Error:Missing XML FILE(questionnaire)')
                return
            questions = list(xt.parse("questionnaire.xml").getroot().getchildren())
            end = questions[-1].attrib['no']

            for question in questions:
                self.questions.append(Question(int(question.attrib['no']),question.attrib['text']))
                for answer in question.getchildren():
                    #print(answer.attrib)
                    self.answers.append(Answer(int(question.attrib['no']),answer.attrib))
                if question.attrib['no'] == end:
                   break
        else:
            self = self.obj

    def store(self,no,qno,ano):
        if no > self.history.__len__() or no > self.chosen.__len__():
            raise BaseException("Data Error!")
        elif no == self.history.__len__() and no == self.chosen.__len__():
            self.history.append(qno)
            self.chosen.append(ano)
        elif self.history.__len__() == self.chosen.__len__() and no >= 0:
            for i in range(no+1,self.history.__len__()-1):
                self.history.pop(-1)
                self.chosen.pop(-1)
            self.history.append(qno)
            self.chosen.append(ano)
        else:
            raise BaseException("Unknown Error(1).")

    def getQuestion(self,num):
        #Supposed to throw a Exception.
        if num >= self.questions.__len__():
            return None
        return self.questions[num]

    def getAnswer(self,num):
        result = []
        for answer in self.answers:
           if answer.this == num:
                result.append(answer)
        return result
    def getLastQuestion(self,num):
        if num <= 0:
            raise BaseException("Unknown Error(2).")
        result = {'question':self.getQuestion(self.histroy[num-1]),'Answer':self.getAnswer(self.history[num-1]),'Chosen':self.chosen[num-1]}
        return result

qm = QuestionManager()
print(qm.getQuestion(1).no,qm.getQuestion(2).text)
for result in qm.getAnswer(1):
    print(result.no,result.text,result.next)
for result in qm.getAnswer(2):
    print(result.no,result.text,result.next)
qm.store(0,2,3)
qm.store(1,1,6)
qm.store(2,5,2)
qm.store(0,1,4)
qm.store(1,3,1)
qm.store(2,5,5)
for i in range(0,3):
    print(qm.history[i],qm.chosen[i])
