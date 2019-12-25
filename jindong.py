import requests
from lxml import etree
import re
def getHTMLText(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'} #设置浏览器代理
        #用cookies伪装登陆
        #coo = 't=bc762e1da427e1a56bf0087609b100ef; enc=zzIe4j5bWowbysKMtQG3o1E3jwUXWknHaMPXqJjZdA6IkXHPrVDdiIduump6Uzil5N7KRisvfksuavG1UMtWKw%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16f182a9b6c596-01192871067169-6353160-144000-16f182a9b6d29e; cna=Pr+sFfjD3V4CAWolza5t9UWe; uc3=id2=UNQ2kNNfq5zYeg%3D%3D&nk2=F451%2BF0K&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dByuqkagkpXUlx%2FGA%3D; lgc=tx1999; uc4=nk4=0%40FZRNSK5aM7YdH3jexY6yihQ%3D&id4=0%40UgP9q1rrnwUU2szglYrTU3iZ%2FOeJ; tracknick=tx1999; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=2_1; l=dBrEhAXqqdZQeQsGBOfwSuI8Li7TEKAb8sPzw4OGxICPOpCM5KENWZLsG_THCnGVnsE9R387PXqQBW8F2yC5syhmRAaZk_bxXdTh.; v=0; uc1=cookie14=UoTbm8FKt7D7jw%3D%3D; cookie2=1d24ca579de5a2f9f4c4fdcdd470e316; _tb_token_=3e577e8e3e1e; isg=BIqKaowd4z8ZBm-a0qN9OEJj23Ds0w-5iH9uMxTDf11oxyqB_Ate5dA10zMbN4Zt'
        #cookies = {}
        #for line in coo.split(';'):  # 浏览器伪装
        #    name, value = line.strip().split('=', 1)
        #    cookies[name] = value
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()    #检测状态
        print(r.raise_for_status())
        r.encoding = r.apparent_encoding    #更改网页编码模式，变成UTF-8
        html1 = etree.HTML(r.text)
        return html1           #返回网页信息
    except:
        return 'error1'

def parsePage(ilt,html):
    try:
        datas = html.xpath('//li[contains(@class,"gl-item")]')
        for data in datas:
            price=str(data.xpath('div/div[@class="p-price"]/strong/i/text()'))
            commit=str(data.xpath('div/div[@class="p-commit"]/strong/a/text()'))
            title=''.join(data.xpath('.//div[@class="p-name p-name-type-2"]//em//text()'))
            shop=data.xpath('.//div[@class="p-shop"]/span/a/text()')[0]
            links='https:' + data.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')[0]
            ilt.append([price,commit,title,shop,links])

    except:
        print("error2")

def getKey(x):
    return x[0]

def printGoodsList(ilt):
    result=sorted(ilt,key=getKey)
    tplt="{:^4}\t{:^8s}\t{:^8s}\t{:^32s}\t\t\t{:^16s}\t{:^16s}"                       #限制字数
    print(tplt.format("序号","价格","评论","商品名称","店铺名","链接"))   #打印信息
    count =0
    for g in result:
        count=count+1
        print(tplt.format(count,g[0],g[1],g[2],g[3],g[4]))


def main():
    goods = '水果'                                        #设置搜索内容
    depth = 2                                             #设置搜索页数
    start_url = 'https://search.jd.com/Search?keyword=' + goods +'&enc=utf-8'  #设置网页地址
    infoList = []                                         #储存爬取到的信息的列表

    for i in range(depth):
        try:
            url = start_url + '&page=' + str(2*i+1)            #设置搜索的是第几页
            html = getHTMLText(url)                        #访问网页
            parsePage(infoList,html)                       #储存信息
        except:
            print("error")
    printGoodsList(infoList)                               #打印信息
main()
#https://search.jd.com/Search?keyword=%E6%B0%B4%E6%9E%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=3&s=51&click=0
#https://search.jd.com/Search?keyword=%E6%B0%B4%E6%9E%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=5&s=101&click=0