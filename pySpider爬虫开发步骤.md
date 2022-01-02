# 							pySpider爬虫步骤记录

## 1.创建工程项目

​	通过**PyCharm软件**进行创建。

​	点击 File->New Project 即可创建项目。

![创建项目](爬虫开发步骤图片存储/创建项目.jpg)



**创建数据库和数据库表信息**



爬虫数据存储表spiderdata

```mysql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for spiderdata
-- ----------------------------
DROP TABLE IF EXISTS `spiderdata`;
CREATE TABLE `spiderdata`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `keyword` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `publishedtime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `linkurl` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
```

用户信息表user

```mysql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `password` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `email` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;

```





## 2.创建pySpider包，并创建initialFrame初始化页面类。



initialFrame类中的代码如下：

```python
import tkinter as tk

import pymysql
from PIL import Image, ImageTk
from pySpder import pySpider


def frame():#初始界面
    global root
    root= tk.Tk()
    root.geometry('500x400')
    root.title('爬虫系统')
    lable0=tk.Label(root,text='请先登录',bg='pink',font=('微软雅黑',50)).pack()#上

    tk.Label(root, text='用户名:', font=('微软雅黑', 10)).place(x=40, y=120) # 用户名
    text_user_default = tk.StringVar()
    username=tk.Entry(root, textvariable= text_user_default).place(x=120, y=120)

    tk.Label(root, text='密码:', font=('微软雅黑', 10)).place(x=40, y=160) # 密码
    text_password_default = tk.StringVar()
    password=tk.Entry(root, textvariable=text_password_default).place(x=120, y=160)

    lable1=tk.Label(root,text='请选择:',font=('微软雅黑',20)).place(x=40,y=320)#下
    tk.Button(root, text='登录',font=('微软雅黑',10),width=5, height=2,command=lambda:exit_spider(text_user_default,text_password_default)).place(x=140, y=320)
    tk.Button(root, text='注册',font=('微软雅黑',10),width=5, height=2,command=exit_register).place(x=200, y=320)

    root.mainloop()#必须要有这句话，你的页面才会动态刷新循环，否则页面不会显示

# 百度：tkinter要求由按钮（或者其它的插件）触发的控制器函数不能含有参数,若要给函数传递参数，需要在函数前添加lambda：
def exit_spider(username,password):#跳转至爬虫界面
    root.destroy()
    user=username.get()   # 获取用户
    pwd=password.get()  # 获取密码
    connect_sql(user,pwd)

def exit_register():#跳转至注册界面
    root.destroy()
    # manager.frame()

# 数据库查看是否存在该用户
def connect_sql(username,password):
    #连接数据库，root是数据库的用户名，应该是默认的是root，wuwenqin是数据库的密码，pythonspider是要连接的数据库名字
    db = pymysql.connect(host="localhost",user= "root", password= "wuwenqin", db="pythonspider")
    #建立游标cursor，这个游标可以类比指针，这样理解比较直观
    cursor = db.cursor()
    sql = "SELECT password FROM user WHERE username='%s' AND password='%s'" % (username,password)
    cursor.execute(sql) #sql语句被执行
    result = cursor.fetchone()#得到的结果返回给result数组
    # 检测账号密码是否存在
    if result: # 账户存在，进入爬虫界面
        print("账户存在")
        pySpider.pySpiderFrameInit()
    else:
        print("账户:"+username+"\t密码："+password+"输入错误")
        frame()

if __name__ == '__main__':
    frame()

```

初始化界面如图：

![](爬虫开发步骤图片存储/初始化界面.jpg)



## 3.连接数据库，查询是否有该用户，存在该用户即跳转到爬虫页面

```python

# 百度：tkinter要求由按钮（或者其它的插件）触发的控制器函数不能含有参数,若要给函数传递参数，需要在函数前添加lambda：
def exit_spider(username,password):#跳转至爬虫界面
    root.destroy()
    user=username.get()   # 获取用户
    pwd=password.get()  # 获取密码
    connect_sql(user,pwd)


# 数据库查看是否存在该用户
def connect_sql(username,password):
    #连接数据库，root是数据库的用户名，应该是默认的是root，wuwenqin是数据库的密码，pythonspider是要连接的数据库名字
    db = pymysql.connect(host="localhost",user= "root", password= "wuwenqin", db="pythonspider")
    #建立游标cursor，这个游标可以类比指针，这样理解比较直观
    cursor = db.cursor()
    sql = "SELECT password FROM user WHERE username='%s' AND password='%s'" % (username,password)
    cursor.execute(sql) #sql语句被执行
    result = cursor.fetchone()#得到的结果返回给result数组
    # 检测账号密码是否存在
    if result: # 账户存在，进入爬虫界面
        print("账户存在")
        pySpider.pySpiderFrameInit()
    else:
        print("账户:"+username+"\t密码："+password+"输入错误")
        frame()

```

p.s:

​	这期间遇到了个小bug：

```python
TypeError: init() takes 1 positional argument but 5 were given
```

一般出现这个问题都是参数传递错误，这个异常意思是：只有一个参数位置却给出了5个。

首先查看该方法的参数：pymysql.Connect()参数说明

```python
host(str):      MySQL服务器地址
port(int):      MySQL服务器端口号
user(str):      用户名
passwd(str):    密码
db(str):        数据库名称
charset(str):   连接编码

connection对象支持的方法
cursor()        使用该连接创建并返回游标
commit()        提交当前事务
rollback()      回滚当前事务
close()         关闭连接

cursor对象支持的方法
execute(op)     执行一个数据库的查询命令
fetchone()      取得结果集的下一行
fetchmany(size) 获取结果集的下几行
fetchall()      获取结果集中的所有行
rowcount()      返回数据条数或影响行数
close()         关闭游标对象

```

```
# 修改如下：指定对应的参数即可
db=pymysql.connect(host="localhost",user= "root", password= "wuwenqin", db="pythonspider")
```

​	

## 4.注册账户，若账户不存在则将注册信息存入数据库中



```python

# 注册账号
def id_write(name,key):
    name1 = name.get()
    key1 = key.get()
    db = pymysql.connect(host="localhost",user= "root", password= "wuwenqin", db="pythonspider")
    #建立游标cursor，这个游标可以类比指针，这样理解比较直观
    cursor = db.cursor()
    sql = "SELECT `username` FROM user WHERE `username`='%s'  " % name1
    cursor.execute(sql) #sql语句被执行
    result = cursor.fetchone()#得到的结果返回给result数组
    if result:#如果查询到了账号存在
          msg._show(title='存在用户',message='换个账号') #
    else:#没有账号
        register_sql="insert into user (username,password) values ('%s','%s')" % (name1,key1)
        cursor.execute(register_sql)
        db.commit()
        msg._show(title='成功！',message='注册成功！')
    db.close()#查询完一定要关闭数据库啊

```

p.s: 这里需要注意到 通过数据库进行的**查询不需要提交commit()的操作，但写、删、改要进行数据提交的操作**，否则**Mysql数据库会默认该次事务不成功**。(为什么不成功？ 这是因为数据库Mysql默认的事务隔离级别是 **可重复读**)





## 5.本次爬虫，主要是根据传入关键字和所需爬取数量进行爬虫，故先简单开发爬虫功能。但由于CSDN不能进行page下一页，而是通过滑动到最下端点击“加载更多”进行信息的加载，每次加载大概30条数据

​	功能接口Web(keyWord,spiderNum)：根据传入关键字和所需爬取数量进行爬虫

```python
# keyWord关键字搜索， spiderNum爬取数量
def Web(keyWord,spiderNum)  :
    # 创建web-打开-登录-切换-输入-爬取
    web = Chrome()  # 创建谷歌浏览器窗口；此处不适合用无头浏览器，因为这个网页最坑的就是登陆后要是没退出，一直会提醒那在其他地方登陆，这个又要重新打开，所以每次爬取完信息，都要自己手动关闭一下这个页面，否则下一次必定报错，需要手动把登陆信息给删除掉；
    baseUrl="https://so.csdn.net/so/search?q="+keyWord +"&t=blog&u=&tm=365&urw=" # 拼接要查询的关键字
    web.get(baseUrl)
    time.sleep(3)
    # Rolldown(web) # 滚动功能
    # Rolldown(web) # 滚动功能
    # RollClick(web)
    cultByNum(web,spiderNum) # 根据传入的爬取数量进行滚动
    # 通过xpath获取 与关键词相关的博客文章
    # list=web.find_elements(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/div')
    list=web.find_elements_by_class_name("list-item")
    len=0  # 目前有多少博客文章
    # try:
    # 通过链接，获取博客内的相关信息
    for data in list:
        href=data.find_element_by_class_name("block-title").get_attribute("href") # 获取链接
        #通过链接获取信息，需要传入链接href以及关键字keyWord，进行后面的存储
        Collect_information(href,keyWord)
        len=len+1
        print(href)
        print(len)
    writeIntoDataBase(datalist) # 写入数据库中
    # except(Exception):
    #     print(Exception.args)
    # time.sleep(10)

```

该功能相关对应的使用方法：

```python

# 根据传入的spiderNum爬取数量进行计算：需要滑动几次加载
def  cultByNum(web,spiderNum):
    initNum=30  # 一次加载大概30篇文章
    if spiderNum<initNum:
        pass
    else:
        needRoll=int(spiderNum/initNum)  # 向下取整
        if needRoll==1: # 只需滚动一次
            Rolldown(web)
        elif needRoll==2: # 两次
            Rolldown(web)
            Rolldown(web)
        else: # 根据needRoll的次数翻滚
            Rolldown(web)
            Rolldown(web)
            needRoll-=2
            while needRoll>0:
                needRoll-=1
                RollClick(web)

# 滚动到当前页面底部，一次加载30篇文章
def Rolldown(web):
    js = "window.scrollTo(0,document.body.scrollHeight)"
    web.execute_script(js)
    time.sleep(2)

# 滚动到底部，并点击加载更多按钮
def RollClick(web):
    Rolldown(web)  # 需要先滑动到底部，让加载按钮显示出来
    web_Loadmore=web.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[3]').click()
    time.sleep(3) # 休眠3秒，让数据能同步爬取

```



以及根据 博客链接进行 博客文章的作者、创作时间、内容、关键字、对应链接、题目 进行的数据爬虫功能：Collect_information(url,key)，这里使用的是requests模块进行的爬虫

```python


#根据传入的详细博客地址进行数据爬取，每次存储一个博客文章的数据到datalist中
def Collect_information(url,key):
    only_1_page_data=[]
    # title="" # 标题
    content="" # 内容
    # author="" # 作者
    keyword=key # 关键字，根据关键字进行的查询
    # createtime="" # 创作时间
    response=requests.get(url=url,headers=headers).text
    rtree=etree.HTML(response)
    title=rtree.xpath('//*[@id="articleContentId"]/text()') # 标题
    author= rtree.xpath('//*[@id="mainBox"]/main/div[1]/div[1]/div/div[2]/div[1]/div/a[1]/text()') # 作者
    print(title)
    createtime = rtree.xpath('//span[@class="time"]/text()')[0] # 创作时间
    contentList = rtree.xpath('//*[@id="article_content"]//text()')
    linkurl = url  # 链接地址
    contentList = [str(i) for i in contentList]
    # 转换成str字符串，否则还是list列表类型
    content=''.join(contentList)
    title=str(title)
    author=str(author)
    createtime=str(createtime)
    # 将only_1_page_data 存储到 datalist中
    only_1_page_data.append(title)
    only_1_page_data.append(author)
    only_1_page_data.append(content)
    only_1_page_data.append(keyword)
    only_1_page_data.append(createtime)
    only_1_page_data.append(linkurl)
    datalist.append(only_1_page_data)

```



## 6.数据存入数据库Mysql中

```python

#写入数据库操作
def writeIntoDataBase(datalist):
    db = pymysql.connect(host="localhost",user= "root", password= "wuwenqin", db="pythonspider") # 连接数据库
    cursor = db.cursor()
    for data in datalist:
        sql="INSERT INTO spiderdata (title,author,content,keyword,publishedtime,linkurl) values ('%s','%s','%s','%s','%s','%s')"%(pymysql.converters.escape_string(data[0]),pymysql.converters.escape_string(data[1]),pymysql.converters.escape_string(data[2]),pymysql.converters.escape_string(data[3]),pymysql.converters.escape_string(data[4]),pymysql.converters.escape_string(data[5]))
        cursor.execute(sql) #sql语句被执行
        # result = cursor.fetchone()# 得到的结果返回给result数组
        db.commit() # 写入数据，提交才能执行
    db.close()  # 查询完一定要关闭数据库

```



遇到的bug：

![存入数据库出现的bug](爬虫开发步骤图片存储/存入数据库出现的bug.png)

p.s:需要转换成对应的类型

```python
list = ['a', 1, 'b', 4, 'c', 5]
# 首先需要将列表的元素全部转换为str，以下两种方法

# 使用for循环
list1 = [str(i) for i in list]

# 使用map函数
list2 = map(str, list)

# 使用join将列表中的元素串起来
res1 = ''.join(list1)
res2 = ''.join(list2)
print(res1, res2)

```





```python
sqlalchemy.exc.DataError: (pymysql.err.DataError) (1366, “Incorrect string value: ‘\xE6\xA0\x87\xE5\x87\x86’ for column ‘name’ at row 1”)
```

原因：数据库的编码不是utf-8格式的

解决方法：使用navicat mysql直接在设计表中修改。







## 7.多进程与多线程

### 	①多进程:

​	判断传入的进程数量，根据线程数量判断是否开启多进程。

```python

# keyWord关键字搜索， spiderNum爬取数量,nb_jobs开启的线程数量
def Web(keyWord,spiderNum,savepath,nb_jobs)  :
    # 创建web-打开-登录-切换-输入-爬取
    web = Chrome()  # 创建谷歌浏览器窗口；此处不适合用无头浏览器，因为这个网页最坑的就是登陆后要是没退出，一直会提醒那在其他地方登陆，这个又要重新打开，所以每次爬取完信息，都要自己手动关闭一下这个页面，否则下一次必定报错，需要手动把登陆信息给删除掉；
    baseUrl="https://so.csdn.net/so/search?q="+keyWord +"&t=blog&u=&tm=365&urw=" # 拼接要查询的关键字
    web.get(baseUrl)
    time.sleep(3)
    # Rolldown(web) # 滚动功能
    # Rolldown(web) # 滚动功能
    # RollClick(web)
    cultByNum(web,spiderNum) # 根据传入的爬取数量进行滚动
    # 通过xpath获取 与关键词相关的博客文章
    # list=web.find_elements(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/div')
    list=web.find_elements_by_class_name("list-item")
    len=0  # 目前有多少博客文章

# 多线程，判定是否需要多进程
    if nb_jobs<2:
        pass
    else:
        mpool=Pool(nb_jobs if nb_jobs else cpu_count())
    # 通过链接，获取博客内的相关信息
    linkedurlList=[]
    for data in list:
        href=data.find_element_by_class_name("block-title").get_attribute("href") # 获取链接
        #通过链接获取信息，需要传入链接href以及关键字keyWord，进行后面的存储，在这里可以进行一个多线程
        linkedurlList.append(href)
        len = len + 1
        print(href)

    for url in linkedurlList:
        if nb_jobs<2:
            Collect_information(url,keyWord)
        else: # 多线程提交任务
            mpool.apply_async(Collect_information(url,keyWord))
        # print(len)
    # 多线程，记得关闭进程池
    if nb_jobs>=2:
        mpool.close()
        mpool.join()
    writeIntoDataBase(datalist,spiderNum) # 写入数据库中
    savedate(datalist,savepath,keyWord,spiderNum)   #  存储到特定位置，以xlsx文件存储
    return spiderNum

```

关键点：mpool.apply_async(Collect_information(url,keyWord))



关于进程池的学习链接：https://blog.csdn.net/weixin_43283397/article/details/104294890



```python
进程池pool中的apply方法与apply_async方法比较：
1. apply方法是阻塞的
   意思是等待当前子进程执行完毕后，再执行下一个进程。

2. apply_async是异步非阻塞的
   意思是不用等待当前进程执行完毕，随时根据系统调度来进行进程切换

applay达不到多进程效果，而apply_async属于异步，主进程和子进程同时跑，谁跑的快，谁先来。



```



### ②多线程

```python

# keyWord关键字搜索， spiderNum爬取数量,nb_jobs开启的线程数量
def Web(keyWord,spiderNum,savepath,nb_jobs)  :
    # 创建web-打开-登录-切换-输入-爬取
    web = Chrome()  # 创建谷歌浏览器窗口；此处不适合用无头浏览器，因为这个网页最坑的就是登陆后要是没退出，一直会提醒那在其他地方登陆，这个又要重新打开，所以每次爬取完信息，都要自己手动关闭一下这个页面，否则下一次必定报错，需要手动把登陆信息给删除掉；
    baseUrl="https://so.csdn.net/so/search?q="+keyWord +"&t=blog&u=&tm=365&urw=" # 拼接要查询的关键字
    web.get(baseUrl)
    time.sleep(3)
    # Rolldown(web) # 滚动功能
    # Rolldown(web) # 滚动功能
    # RollClick(web)
    cultByNum(web,spiderNum) # 根据传入的爬取数量进行滚动

    # 通过xpath获取 与关键词相关的博客文章
    # list=web.find_elements(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/div')
    list=web.find_elements_by_class_name("list-item")
    len=0  # 目前有多少博客文章

    # 通过链接，获取博客内的相关信息
    linkedurlList=[]
    for data in list:
        href=data.find_element_by_class_name("block-title").get_attribute("href") # 获取链接
        #通过链接获取信息，需要传入链接href以及关键字keyWord，进行后面的存储，在这里可以进行一个多线程
        linkedurlList.append(href)
        len = len + 1
        print(href)

# 线程池
    pool = ThreadPoolExecutor(max_workers=nb_jobs)
    for url in linkedurlList:
        if nb_jobs<2:
            Collect_information(url,keyWord)
        else: # 多线程提交任务
            pool.submit(Collect_information,url,keyWord)
    pool.shutdown(wait=True)
        # print(len)

    writeIntoDataBase(datalist,spiderNum) # 写入数据库中
    savedate(datalist,savepath,keyWord,spiderNum)   #  存储到特定位置，以xlsx文件存储
    return spiderNum

```

关键点：pool = ThreadPoolExecutor(max_workers=nb_jobs)   # 线程池创建

​				pool.submit(Collect_information,url,keyWord)  # 提交任务

​				pool.shutdown(wait=True)  # 关闭线程池，wait等待任务结束

线程池进行的提交任务操作。





## 8.计算运行时间

​	使用time()函数即可进行时间计算。

```python
from time import *

begin_time=time()
# 程序运行时间计算
end_time = time()
run_time = end_time - begin_time
```



## 补充：UI界面设计

1.这里比较熟悉pyqt5，故记录如何使用qtDesigner进行UI界面设计。

参考：https://blog.csdn.net/qq_34919792/article/details/88086095?ops_request_misc=&request_id=&biz_id=102&utm_term=python%E7%9A%84pyqt5%E4%BC%98%E7%BE%8E%E7%95%8C%E9%9D%A2&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~sobaiduweb~default-1-88086095.nonecase&spm=1018.2226.3001.4450

首先要去安装pyqt5，cmd命令窗口中输入：**pip install pyqt5**

再安装qtDesigner插件，  cmd命令窗口中输入：**pip install pyqt5-tools**

然后可以通过python的位置中找到:

```python
py37\Lib\site-packages\PyQt5\designer.exe
```

界面设计的操作可以在上面的链接进行学习。

主要是图标等要进行pyrcc以及pyuic的操作，将 qrc资源文件和ui文件转换为py文件。

pyrcc 命令如下：

```python
pyrcc5 -o     具体生成的位置/文件名.py  文件路径/资源名.qrc
```

pyuic的命令类似：

```python
pyuic -o   具体生成的位置/文件名.py  文件路径/ui界面.ui
```

生成对应的资源py文件以及ui对应的py文件。



ui对应的py文件可通过加载ui界面实现简单操作：(如注册界面)

```python

class Register(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("register.ui", self)
        self.setMinimumSize(295, 535)
        self.setMaximumSize(295, 535)
        self.regist_commit.clicked.connect(self.regist)
        self.regist_cancel.clicked.connect(self.cancel)

```

```python
if __name__ == '__main__':
    app = QApplication(sys.argv)
    register = Register()
    register.show()
    app.exec_()

```

即可使用。































