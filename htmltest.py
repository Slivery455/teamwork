from Store import Store
from Fruit import Fruit
from pyquery import PyQuery as pq
from selenium import webdriver as wd
import xml.dom.minidom as dom
import re


#
#This module is used for search stores with a concrete fruit and retrive a list of store WITH OR WITHOUT ASSERT.
#You are supposed to check the method "Calculate()" is used before you sort the list.
#Of course I will make it automatization soon.

class TianMaoReader :
    @classmethod
    def Reading(cls,fruit):
        #Commander of the browser(Chrome)
        browser = wd.Chrome()
        #Open the web page
        browser.get(
            'https://list.tmall.com/search_product.htm?q='+ fruit.attr['name'] +'水果&type=p&spm=a220m.1000858.a2227oh.d100&xl=%C6%BB%B9%FB_2&from=.list.pc_1_suggest')
        #Write the context of the page which we searched to html file
        html = browser.page_source
        root = pq(html).__str__()
        browser.close()
        file = open('TianMao.html', 'w', encoding='utf-8')
        file.write(root)
        #Open and decode the file we just stored
        root = dom.parse("TianMao.html")
        #Get root of the html
        sstmp2 = root.documentElement
        stmp2 = sstmp2.getElementsByTagName('div')
        i = 0
        #Prepare for initializing a store,the variable 'i' is not necessary.
        price = 0
        name = ''
        amount = 0.0
        sale = 0
        stores = []
        for item in stmp2:
            #This label contains the information about store.
            if item.getAttribute('class') != 'product-iWrap':
                continue
            children = item.getElementsByTagName('p')#item.childNodes
            for t in children:
                #Price for fruit
                if t.getAttribute('class') == 'productPrice':
                    em = t.getElementsByTagName('em')
                    for e in em:
                        price = e.getAttribute('title')
                elif t.getAttribute('class') == 'productTitle':
                    #Name of shops ,the amount of fruit is figured out here.
                    em = t.getElementsByTagName('a')
                    name = em[0].getAttribute('title')
                    stramount = re.findall('\d+斤',name)
                    if stramount.__len__() == 0:
                        #Maybe the weight of good is written by Chinese or not been written,
                        #I appoint it 500 gram in these scenarios
                        amount = 1
                    else:
                        #Fortunately we find the weight in title, and we figure out how much it is.
                        stramount = re.findall('\d+',stramount[0])
                        amount = float(stramount[0])
                    price = float(price)/amount
                elif t.getAttribute('class') == 'productStatus':
                    #How much this good is been saled per month?
                    em = t.getElementsByTagName('span')[0].getElementsByTagName('em')
                    str = em[0].childNodes[0].nodeValue
                    num = re.findall('\d+\.\d+',str)
                    if num.__len__() == 0:
                        num = re.findall("\d+",str)
                    #print(num)
                    if -1 != str.find('万'):
                        #Maybe they were written like "1.2万"?
                        sale = int(float(num[0])*10000)
                    else :
                        sale = int(num[0])
            #print(sale)
            children = item.getElementsByTagName('div')
            a = children[0].getElementsByTagName('a')
            url = 'http:'+a[0].getAttribute('href')
            stores.append(Store(name,price,0,sale,fruit,url))
            for shop in stores:
                shop.Calculate()
                shop.Print()
        return stores

apple = Fruit()
apple.Print()
apple.attr['name'] = '梨'
TianMaoReader.Reading(apple)
