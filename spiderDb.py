# @Author:77
# -*- codeing = utf-8 -*-
# @TIME : 2022/4/25 16:00
# @File : spider.py
# @Software: PyCharm

#movie.douban.com/top250?start


from bs4 import BeautifulSoup
import re                   # 正则表达式，进行文字匹配
import urllib.request       #制定URL，获取网页数据
import xlwt                 #进行excel操作
import sqlite3             #进行SQLite 数据库操作

def main():
    baseurl="https://movie.douban.com/top250?start="
    #1,爬取网页
    datalist=getData(baseurl)
    # savepath="豆瓣电影Top250.xls"            #如果不加 ../的话就是加入本身的路径
    dbpath="douban.db"

    #2,逐一解析数据
    #3,保存数据
    # savaData(datalist,savepath)               #按住shirft键 快速定位

    savaData2DB(datalist,dbpath)


#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')    # 创建正则表达式对象，表示规则（字符串的模式）
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  #re.S 让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
#找到评价人数
findJudge =re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq =re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S) #不能少问号 不让会出现重复信息


#.*？ . 任何一个字符 *出现多次 ？整个出现的0次到多次  .s 忽略换行符
                                    #因为里面有双引号  所以 '' 表示的为一个字符串的意思
#爬取网页
def getData(baseurl):
    datalist=[]
    for i in range (0,10):           #调用获取页面信息的函数 10次
        url=baseurl+str(i*25)
        html=askURL(url)            #保存获取到的网页源码。
        #2.逐一解析数据 弄到一个网页解析一下

    # 2,逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):#查找符合要求的字符串，形成列表 #class 是一个类别 所以要加个下滑线
            #print(item)                    #测试：查看电影item 全部信息
            data=[]                         #保存一步电影# 所有信息
            item = str(item)                #把所有内容变为字符串

            #影片详情的链接
            link = re.findall(findLink,item)[0]#re库用来通过正则表达式查找指定的字符串
            data.append(link)#1添加电影详情链接

            imgSrc = re.findall(findImgSrc,item)[0] #取0是可能会碰到很多个
            data.append(imgSrc)             #2添加图片链接

            titles = re.findall(findTitle,item)  #3添加片名 片名可能只有中文名，没有外文名
            if(len(titles) ==2 ):           #如果存在2个电影名的话（中文名，外文名）
                ctitle = titles[0]          #添加中文名
                data.append(ctitle)         #添加外国名
                otitle = titles[1].replace("/","") #去掉无关的符号
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')            #留空

            rating = re.findall(findRating,item)[0]
            data.append(rating)             #4添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)           #5添加评价人数

            inq = re.findall(findInq,item)
            if len(inq) !=0:                #6添加概述 可能不存在概述
                inq = inq[0].replace("。","") #去掉句号
                data.append(inq)             #添加概述
            else:
                data.append(" ")             #留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)  #去掉<br>
            bd = re.sub(r'/xa0',' ',bd)                  #替换/
            data.append(bd.strip())                  #去掉前后的空格


            datalist.append(data)                     #把处理好的一步电影信息放入 datalist
    #print(datalist)  #这里输出查看一下信息

    return datalist



#得到指定一个URL的网页内容
def askURL(url):
    head = {                            #模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"
    }
                                        #用户代理，表示告诉豆瓣服务器，我们是什么类型的机器（浏览器）（本质上是告诉浏览器，我们可以接受什么水平的文件内容）
    request = urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:  #捕获一下错误
        if hasattr(e,"code"):           #将错误打印出来 hasattr 指示标签
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html   #注意要返回调用




#保存数据
def savaData(datalist,savepath):
    print("save..........")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True) #创建工作表
    col =('电影详情链接',"图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息") #定义了一下元组
    for i in range(0,8): #八个元组数据
        sheet.write(0,i,col[i])  #列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data =datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])



    book.save(savepath)   #保存




def savaData2DB(datalist,dbpath):
    init_db(dbpath)  #在保存之前先进行数据库操作 首先连接数据库
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()   #定义cur 为查询游标


    for data in datalist:
        for index in range(len(data)): #这里data是250行 8列的数据集
            # if index == 4 or index == 5 :
            #     continue
             data[index]='"'+data[index]+'"'
        sql ='''
                insert into movie250(
                info_link,pic_link,cname,ename,score,rated,introduction,info)
                values(%s) ''' %",".join(data) #把data这个列表，每一个毒药哦那个，连接起来
        # print(sql)
        cur.execute(sql) #调试的时候可以先不存
        conn.commit()
    cur.close()
    conn.close()


    print(".....")




#create table if not exists movie250
def init_db(dbpath):
    sql ='''
        create table if not exists movie250  
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link  text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        introduction text,
        info text
        )



    
    '''   #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()






















if __name__=="__main__": #当程序执行时


    #init_db("movietest.db")
    #调用函数
    main()
    print("爬取完毕：")