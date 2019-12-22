from Store import Store
from Fruit import Fruit
from Trendency import Trend
from Error import ParamError
from TianMaoReader import TianMaoReader
import xml.etree.ElementTree as xtree
from threading import Thread
import threading
import os

#This class is main class,now it does not contains online work,it works by reading a XML(HTML) I have stored in file named "page.html"
#and this file is searching "苹果".
#You can see how the list of store is been sorted and Print.

class Analysis:
    #@staticmethod
    def main(self):

        #Check if the XML file exists.A Error would be thrown if file is missing.
        if(os.path.exists('NutritionList.xml')==False):
            print('Error:Missing XML FILE(NutritionList)')
            return
        if(os.path.exists('Fruit.xml')==False):
            print('Error:Missing XML FILE(Fruit)')
            return
        #Collecting the kind of nutrition
        dom = xtree.parse('NutritionList.xml').getroot()
        root = xtree.parse("Fruit.xml").getroot()
        #Compare the version of two XML file
        if(dom.attrib.get('version') != root.attrib.get('version')):
            print('Dismatch the version with NutritionList.xml(',dom.attrib.get('version'),
                  ') and Fruit.xml(',root.attrib.get('version'),').')
            return
        fruits = []
        fruitkeys = []
        try:
            for item in dom.getchildren():
                fruitkeys.append(item.attrib.get('id'))
            #Getting class and its instance from XML.
            for fruit in root:
                fruits.append(Fruit(fruit.tag,fruit.attrib))
        except BaseException as e:
            for i in e.args:
                print(i,end='')
            return
        #Pretending the trendency is already figured out.
        customervalue = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
        trend = Trend(fruitkeys, customervalue)
        for fruit in fruits:
            fruit.Calculate(trend)
        fruits = sorted(fruits,key = lambda fruit:fruit.attr['score'])
        #This result is sorted,you can use it directly.
        #storelist = TianMaoReader.Reading(fruits[0])
        storelist = self.Searching(fruits)
        try:
            #Display!!!
            if storelist == None:
                print("Searching is failure,please try again.")
                return
            for item in storelist:
               item.Print()
        except ParamError as e :
            for i in e.args:
                print(i,end = '')
    #@classmethod
    def Searching(self,fruits):
        if isinstance(fruits,list) == False:
            raise ParamError("Threads need a list.")
            return None
        con = threading.Condition()
        warp = []
        storage = []
        storage.append([])
        storage.append([])
        t1 = Thread(target = TianMaoReader.Reading,args = (fruits[0],con,warp,storage[0]))
        t2 = Thread(target = TianMaoReader.Reading,args = (fruits[1],con,warp,storage[1]))
        t1.run()
        t2.run()
    #    con.acquire()
    #    while warp.__len__() < 2:
    #        print(warp.__len__())
    #        con.wait()
    #    con.release()
        result = []
        for re in storage:
            for item in re:
                result.append(item)
        return result
ana = Analysis()
ana.main()