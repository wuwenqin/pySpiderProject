import tkinter as tk
from tkinter import messagebox
import tkinter.messagebox as msg

import pymysql
from PIL import Image, ImageTk

from pySpder import pySpiderGui


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
    connect_sql(user,pwd)   # 查询数据库用户信息是否存在

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



def exit_register():#跳转至注册界面
    root.destroy()
    global root2
    root2 = tk.Tk()
    root2.wm_attributes('-topmost', 1)
    root2.title('管理员注册')
    root2.geometry('500x300')

    lable1 = tk.Label(root2, text='账号：', font=25).place(x=100, y=50)
    lable2 = tk.Label(root2, text='密码：', font=25).place(x=100, y=100)
    lable2 = tk.Label(root2, text='确认密码：', font=25).place(x=80, y=150)

    global entry_name, entry_key, entry_confirm
    name = tk.StringVar()
    key = tk.StringVar()

    confirm = tk.StringVar()
    entry_name = tk.Entry(root2, textvariable=name, font=25)
    entry_name.place(x=180, y=50)
    entry_key = tk.Entry(root2, textvariable=key, font=25, show='*')
    entry_key.place(x=180, y=100)
    entry_confirm = tk.Entry(root2, textvariable=confirm, font=25, show='*')
    entry_confirm.place(x=180, y=150)
    # 百度：tkinter要求由按钮（或者其它的插件）触发的控制器函数不能含有参数,若要给函数传递参数，需要在函数前添加lambda：
    button1 = tk.Button(root2, text='确定', height=2, width=10, command=lambda: id_write(name,key)).place(x=210, y=200)
    button2=tk.Button(root2,text='返回',height=2,width=10,command=return_login).place(x=280,y=200)
    # manager.frame()
    root.mainloop()  # 必须要有这句话，你的页面才会动态刷新循环，否则页面不会显示

# 返回登录界面
def return_login():
    root2.destroy()
    frame()
    root.mainloop()


# 数据库查看是否存在该用户，用户存在进入爬虫界面，不存在返回登录界面
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
        db.close()
        pySpiderGui.pySpiderFrameInit()
    else:
        msg._show(title='失败！', message='账户不存在！')
        db.close()
        root.mainloop()
        frame()

if __name__ == '__main__':
    frame()
