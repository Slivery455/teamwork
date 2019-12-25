from Store import Store
from Food import Food
from Trendency import Trend
from Error import ParamError
from TianMaoReader import TianMaoReader
import xml.etree.ElementTree as xtree
from threading import Thread
from FoodFactory import FFactory
import threading
import os

#This class is main class,now it does not contains online work,it works by reading a XML(HTML) I have stored in file named "page.html"
#and this file is searching "苹果".
#You can see how the list of store is been sorted and Print.

class Analysis:

    def main(self):
        #Check if the XML file exists.A Error would be thrown if file is missing.
        rlist = self.XMLReader()
        dom = rlist[0]
        root = rlist[1]

        food = []
        fruitkeys = []
        try:
            for item in dom.getchildren():
                fruitkeys.append(item.attrib.get('id'))
            #Getting class and its instance from XML.
            for fruit in root:
                food.append(Food(fruit.tag, fruit.attrib))
        except BaseException as e:
            for i in e.args:
                print(i,end='')
            return
        #Pretending the trendency is already figured out.
        customervalue = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
        trend = Trend(fruitkeys, customervalue)
        for item in food:
            item.Calculate(trend)
        food = sorted(food,key = lambda food:food.attr['score'],reverse = True)

        #This result is sorted,you can use it directly.
        #storelist = TianMaoReader.Reading(food[0])
        storelist = self.Searching(food)
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

    def Searching(self, food):
        if isinstance(food, list) == False:
            raise ParamError("Threads need a list.")
            return None
        con = threading.Condition()
        warp = []
        storage = []
        storage.append([])
        storage.append([])
        t1 = Thread(target = TianMaoReader.Reading, args = (food[0], con, warp, storage[0]))
        t2 = Thread(target = TianMaoReader.Reading, args = (food[1], con, warp, storage[1]))
        t1.run()
        t2.run()
        #Threads synchronization
        con.acquire()
        while warp.__len__() < 2:
            print(warp.__len__())
            con.wait()
        con.release()
        result = []
        for re in storage:
            for item in re:
                result.append(item)
        result.sort(key=lambda Store: Store.attr['score'], reverse=True)
        return result

    def XMLReader(self):
        foodfilename = 'Nutrition.xml'
        keyfilename = 'Food.xml'
        if (os.path.exists(foodfilename) == False):
            BaseException('Error:Missing XML FILE(',foodfilename,')')
            return None
        if (os.path.exists(keyfilename) == False):
            BaseException('Error:Missing XML FILE(',keyfilename,')')
            return None
            # Collecting the kind of nutrition
        dom = xtree.parse('Nutrition.xml').getroot()
        root = xtree.parse("Food.xml").getroot()
        # Compare the version of two XML file
        if (dom.attrib.get('version') != root.attrib.get('version')):
            raise BaseException('Dismatch the version with NutritionList.xml(', dom.attrib.get('version'),
                  ') and Food.xml(', root.attrib.get('version'), ').')
            return None
        rlist = [dom,root]
        return rlist

ana = Analysis()
ana.main()
#rt = ana.XMLReader()
#dom = rt[0]
#root = rt[1]
#for item in dom.getchildren():
#    print(item.attrib)
#for item in root.getchildren():
#   print(item.tag,item.attrib)
