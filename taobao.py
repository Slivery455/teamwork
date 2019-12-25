import requests
import re
def getHTMLText(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'} #设置浏览器代理
        #用cookies伪装登陆
        coo = 't=bc762e1da427e1a56bf0087609b100ef; enc=zzIe4j5bWowbysKMtQG3o1E3jwUXWknHaMPXqJjZdA6IkXHPrVDdiIduump6Uzil5N7KRisvfksuavG1UMtWKw%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16f182a9b6c596-01192871067169-6353160-144000-16f182a9b6d29e; cna=Pr+sFfjD3V4CAWolza5t9UWe; uc3=id2=UNQ2kNNfq5zYeg%3D%3D&nk2=F451%2BF0K&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dByuqkagkpXUlx%2FGA%3D; lgc=tx1999; uc4=nk4=0%40FZRNSK5aM7YdH3jexY6yihQ%3D&id4=0%40UgP9q1rrnwUU2szglYrTU3iZ%2FOeJ; tracknick=tx1999; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=2_1; l=dBrEhAXqqdZQeQsGBOfwSuI8Li7TEKAb8sPzw4OGxICPOpCM5KENWZLsG_THCnGVnsE9R387PXqQBW8F2yC5syhmRAaZk_bxXdTh.; v=0; uc1=cookie14=UoTbm8FKt7D7jw%3D%3D; cookie2=1d24ca579de5a2f9f4c4fdcdd470e316; _tb_token_=3e577e8e3e1e; isg=BIqKaowd4z8ZBm-a0qN9OEJj23Ds0w-5iH9uMxTDf11oxyqB_Ate5dA10zMbN4Zt'
        cookies = {}
        for line in coo.split(';'):  # 浏览器伪装
            name, value = line.strip().split('=', 1)
            cookies[name] = value
        r = requests.get(url, cookies=cookies, headers=headers, timeout=30)
        r.raise_for_status()    #检测状态
        print(r.encoding)
        r.encoding = r.apparent_encoding    #更改网页编码模式，变成UTF-8
        return r.text           #返回网页信息
    except:
        return 'error1'
    #
    #     r=requests.get(url,timeout=30,headers=headers)
    #     r.raise_for_status()
    #     r.encoding=r.apparent_encoding
    #     print(r.encoding)
    #     return r.text
    # except:
    #     return ""

def parsePage(ilt,html):
    try:
        #用正则表达式提取爬取的信息
        plt=re.findall(r'"view_price":"[\d.]*"', html)
        sale=re.findall(r'"view_sales":".*?"', html)
        loc = re.findall(r'"item_loc":".*?"', html)
        tlt=re.findall(r'"raw_title":".*?"', html)
        shop = re.findall(r'"nick":".*?"', html)
        link = re.findall(r'"detail_url":".*?"', html)
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            sales=eval(sale[i].split(':')[1])
            location=eval(loc[i].split(':')[1])
            title=eval(tlt[i].split(':')[1])
            shopname=eval(shop[i].split(':')[1])
            links='http:'+eval(link[i].split(':')[1])       #加头套，使链接可访问
            ilt.append([price,sales,location,title,shopname,links])
    except:
        print("error2")

def getKey(x):
    return x[0]

def printGoodsList(ilt):
    result = sorted(ilt, key=getKey)
    tplt="{:^4}\t{:^8}\t{:^8}\t{:^16}\t{:^8}\t\t\t{:^16}\t{:^16}"                       #限制字数
    print(tplt.format("序号","价格","销量","地址","商品名称","店铺名","链接"))   #打印信息
    count =0
    for g in result:
        count=count+1
        print(tplt.format(count,g[0],g[1],g[2],g[3],g[4],g[5]))


def main():
    goods = '水果'                                        #设置搜索内容
    depth = 2                                             #设置搜索页数
    start_url = 'http://s.taobao.com/search?q=' + goods   #设置网页地址
    infoList = []                                         #储存爬取到的信息的列表

    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44*i)            #设置搜索的是第几页
            html = getHTMLText(url)                        #访问网页
            parsePage(infoList,html)                       #储存信息
        except:
            print("error")
    printGoodsList(infoList)                               #打印信息
main()