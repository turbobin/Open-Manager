# -*- coding: utf-8 -*-
import tkinter as tk
import json
import webbrowser
from tkinter import messagebox
from tkinter import *
import pypinyin
from pypinyin import Style
import threading
import time
import systemhotkey
import os
import base64
from icon import MYICO,ADDICO
FONT_1 = ('微软雅黑',10,'normal')
FONT_2 = ('Arial',10,'normal')

Win_Hide = False



# 主窗体
class Application(tk.Frame):
    def __init__(self,master = None): #顶层窗口master默认为空，应用中为root
        super().__init__()
        self.master = master
        self.pack() #放置到屏幕上
        #获取列表
        self.urllist = self.readUrlList()
        if self.urllist: #如果urllist不为空，创建窗口进入主循环
            self.creatWidgets()
            self.keywdbox.focus_set()
            self.mainloop()
        else:
            messagebox.showinfo('错误','读取地址列表失败，请查看openlist.json文件是否存在并且格式正确。')

    def readUrlList(self):
        try:
            with open('openlist.json','r',encoding='utf-8') as f_obj:
                urllist = json.load(f_obj) #使用json方法load json文件返回一个字典
            return urllist
        except Exception:
            return None

    def saveUrlList(self):
        with open('openlist.json','w',encoding='utf-8') as f:
            json.dump(self.urllist,f,ensure_ascii=False,indent=2) #导出列表到 json文件中，缩进2个空格
        #print("保存成功")

    def creatWidgets(self):
        #创建搜索框
        self.frame1 = tk.Frame()
        self.frame1.pack(side = TOP,fill=X)
        self.kwlb = tk.Label(self.frame1,text = '搜索：',font = FONT_2)
        self.kwlb.pack(side = LEFT)
        self.keywdbox = tk.Entry(self.frame1,font=FONT_2) #后面使用bind event来绑定事件  也可以用验证来实现
        #showlistCMD = self.frame1.register(self.showlist) #注册一个验证
        #self.keywdbox = tk.Entry(self.frame1,font=FONT_2,validate="key", validatecommand=(showlistCMD,'%P')) #后面使用 验证来绑定事件
        self.keywdbox.pack(side = LEFT,fill=X,expand = YES)
        tk.Label(self.frame1,width = 2).pack(side = RIGHT)#在最右侧添加一个空标签，占位对齐

        #创建列表框
        self.frame2 = tk.Frame()
        self.frame2.pack(side = TOP,fill = X,pady = 5)
        self.scrolly = tk.Scrollbar(self.frame2)
        self.scrolly.pack(side = RIGHT,fill = Y)
        self.listbox = tk.Listbox(self.frame2,width = 60,height = 15,font = FONT_1,yscrollcommand = self.scrolly.set)
        #创建列表框并设置右侧滚动条
        self.listbox.pack(fill=BOTH,expand=YES)
        self.scrolly.config(command = self.listbox.yview) #设置滚动条绑定listbox

        #创建添加、删除按钮
        self.frame3 = tk.Frame()
        self.frame3.pack(side = TOP,fill = BOTH,pady = 10)
        Label(self.frame3, width=20).pack(side=LEFT, expand=YES)  # 增加空标签，为了调整按钮位置
        self.btnadd = Button(self.frame3, text='添加', command=self.additem)
        self.btnadd.pack(side=LEFT, expand=YES) #expand使按钮左右有空白
        self.btnchange = Button(self.frame3, text='修改', command=self.changeitem)
        self.btnchange.pack(side=LEFT, expand=YES)
        self.btndel = Button(self.frame3, text='删除', command=self.deleteitem)
        self.btndel.pack(side=LEFT, expand=YES)
        Label(self.frame3, width=20).pack(side=RIGHT, expand=YES)

        #加载地址列表
        for item in self.urllist:
            self.listbox.insert(END,item) #从尾部插入项目

        #添加事件处理
        self.doevent()

    def additem(self):
        pw = Add_PopupDialog(self)
        self.wait_window(pw)  # 這一句很重要！！！

        # 如果要获取一个输入值，采用下面方法
        # r = simpledialog.askstring('Python Tkinter', 'Input String',
        #                            initialvalue='Python Tkinter

    def deleteitem(self):
        index = self.listbox.curselection()
        try:
            item = self.listbox.get(index)
        except Exception:
            messagebox.showinfo('提示', '请选择需删除的项目！')
            # messagebox.showwarning('警告','请选择需删除的项目！')
            return
        if messagebox.askyesno('删除', '删除 %s ？' % item):
            self.listbox.delete(index)
            del self.urllist[item]
            messagebox.showinfo('提示', '删除成功')
        else:
            # messagebox.showinfo('No', 'Quit has been cancelled')
            return

    def changeitem(self):
        index = self.listbox.curselection()
        try:
            urlname = self.listbox.get(index)
        except Exception:
            messagebox.showinfo('提示', '请选择需修改的项目！')
            return
        cw = Add_PopupDialog(self,'change',urlname)
        self.wait_window(cw)  # 這一句很重要！！！


    def doevent(self):
        #self.keywdbox.bind("<Return>",self.showlist) # 按回车键，显示搜索结果
        self.keywdbox.bind("<KeyRelease>",self.showlist) # 按任意键，显示搜索结果 一定要用keyrelease 否则字符还没有输入到Enter就进入了事件处理程序
        #self.keywdbox.bind("<BackSpace>",self.showlistAll)
        #self.keywdbox.bind("<Return>", lambda e: print('enter'))
        self.keywdbox.bind("<Delete>",self.showlistAll)
        self.listbox.bind("<Delete>", self.Rest)
        self.listbox.bind("<Escape>", self.Rest)
        self.keywdbox.bind("<Escape>",self.showlistAll)
        self.listbox.bind('<Double-Button-1>',self.openurl) # 双击打开地址
        self.listbox.bind('<Return>',self.openurl) # 按Enter键打开地址
        self.listbox.bind('<Left>', lambda e:self.keywdbox.focus_set())  # 返回搜索框
        #self.listbox.bind('<Delete>', lambda e: self.keywdbox.focus_set())  # 返回搜索框
        self.listbox.bind('<Right>', lambda e: self.keywdbox.focus_set())  # 返回搜索框
        self.keywdbox.bind("<Down>",self.jump_to_result)

    def Rest(self,event):
        self.keywdbox.focus_set()
        self.showlistAll(event)

    def openurl(self, event):
        self.listbox.focus_set()
        if self.listbox.curselection() == tuple():
            self.listbox.select_set(0,0)
            return
        urlname = self.listbox.get(self.listbox.curselection())
        url = self.urllist[urlname]  # 根据key值获取对应url值

        if url is not None and url != '':
            webbrowser.open(url)
        else:
            messagebox.showinfo('Error !', '打开地址失败！地址为空。')

    def jump_to_result(self,event):
        if self.listbox.size():
            self.listbox.select_clear(0,END)
            self.listbox.select_set(0)
            self.listbox.activate(0)
            #print(self.listbox.curselection())
            self.listbox.focus_set()

    def showlistAll(self, event):
        keywd = self.keywdbox.get().strip()
        # 退格清空文本框时，重新显示列表
        print(event.keycode)
        self.keywdbox.delete(0, END)
        for item in self.urllist:
            self.listbox.insert(END, item)  # 从尾部插入

    def showlist(self,event):
        keywd = self.keywdbox.get().strip()
        print(event.keycode,keywd)
        if event.keycode == 8:
            if len(keywd) == 1:
                self.listbox.delete(0, END)
                for item in self.urllist:
                    self.listbox.insert(END, item)  # 从尾部插入
        if keywd:
            self.listbox.delete(0, END)
            # print(urllist)
            for item in self.urllist:
                if (keywd.lower() in item.lower() )or (keywd.lower() in pypinyin.slug(item.lower(),separator = '') or(keywd.lower() in pypinyin.slug(item.lower(), style=Style.FIRST_LETTER,separator = ''))):
                    self.listbox.insert(END, item)  # 加载搜索结果
        else:
            self.listbox.delete(0, END)
            for item in self.urllist:
                self.listbox.insert(END, item)  # 空字符时，加载所有列表
    #
    # def showlist(self,content): #使用验证最后必须有一个return True
    #     #keywd = self.keywdbox.get().strip()
    #     #print(keywd)
    #     print(content)
    #     keywd = content.strip()
    #     if keywd:
    #         self.listbox.delete(0, END)
    #         # print(urllist)
    #         for item in self.urllist:
    #             if keywd.lower() in item.lower():
    #                 self.listbox.insert(END, item)  # 加载搜索结果
    #     else:
    #         self.listbox.delete(0, END)
    #         for item in self.urllist:
    #             self.listbox.insert(END, item)  # 空字符时，加载所有列表
    #     return True

#添加按钮的弹出窗口
class Add_PopupDialog(tk.Toplevel):
    def __init__(self,parent,add_or_change = 'new',aim_urlname = None):
        super().__init__()
        self.runmod = add_or_change
        self.aim_urlname = aim_urlname
        sw = self.winfo_screenwidth() #屏幕宽度
        sh = self.winfo_screenheight() - 100 #屏幕高度
        ww = 400 #窗口宽度
        wh = 120 #窗口高度
        x = (sw - ww) / 2  #计算窗口坐标点x
        y = (sh - wh) / 2  #计算窗口坐标点y
        self.geometry("%dx%d+%d+%d" %(ww,wh,x,y)) #设置窗口大小和布局位置
        self.resizable(0,0) #设置 x,y方向都不可以缩放

        tmp2 = open("tmp2.ico","wb")
        tmp2.write(base64.b64decode(ADDICO))
        tmp2.close()
        self.iconbitmap("tmp2.ico")
        #os.remove("tmp2.ico")
        
        #self.iconbitmap('add_new.ico')
        self.parent = parent #创建parent属性储存parent
        frame = tk.Frame(self) #创建一个frame
        frame.grid() #布置此frame
        #第一行  名称：[输入框]
        tk.Label(frame,text='名称：').grid(row = 0,column = 0,sticky = E,pady = 8) #0行0列左对齐，y方向8像素空格
        self.name = tk.StringVar() #创建name 字符串变量
        #输入框 横跨4列
        tk.Entry(frame,textvariable = self.name,width = 50).grid(row = 0,column = 1,columnspan = 4,sticky = W,pady=8)
        #输入框0行1列跨越4列，右对齐，y方向空格8像素

        #第二行  路径：[输入框]
        tk.Label(frame,text = '路径：').grid(row = 1,column = 0,sticky = E,pady = 8) #1行0列左对齐，y方向8像素空格
        self.url = tk.StringVar() #创建 url 字符串变量
        tk.Entry(frame,textvariable = self.url,width = 50).grid(row = 1,column = 1,columnspan = 4,sticky = W,pady = 8)

        #第三行 [确定]  [取消]
        tk.Button(frame, text="确定", command=self.ok).grid(row=2, column=2, sticky=W, pady=10) #确定按钮对应ok方法
        tk.Button(frame, text="取消", command=self.cancel).grid(row=2, column=3, sticky=S, pady=10) #取消按钮对应cancel方法

        if self.runmod == 'new':
            self.title('添加快捷路径')
        else:
            self.title('修改快捷路径')
            self.name.set(aim_urlname)
            self.url.set(self.parent.urllist[aim_urlname])


    def ok(self): #ok键按下
        urlname = self.name.get().strip() #从输入框中获得字符串，去掉头尾空格
        print(urlname)
        url = self.url.get().strip()
        if urlname == '' or url == '':
            messagebox.showwarning('提示','输入不能为空！')
            return
        if urlname in self.parent.urllist:
            if messagebox.askyesno('提示','名称‘%s’已经存在，将进行覆盖，是否继续？'%urlname):
                pass #pass是为了直接跳转到后面进行赋值操作，将url写入urllist字典中
            else:
                return
        #列表字典中添加或更新项目
        print(self.parent.urllist.pop(self.aim_urlname,None))
        self.parent.urllist[urlname] = url
        #重新加载列表字典
        self.parent.listbox.delete(0,END) #清空父窗口中listbox中的内容
        for item in self.parent.urllist:
            self.parent.listbox.insert(END,item) #循环添加项目到父窗口的listbox中
        self.destroy() #自己销毁自己窗口

    def cancel(self):
        self.destroy()

def show(root):
    """"""
    root.update()
    root.deiconify()
def hide(root):
    """"""
    root.withdraw()


class taskmain(threading.Thread):
    def __init__(self,root):
        super(taskmain,self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.root = root  # 构造窗体
        print("creat root")
    def run(self):
        self.root.title('我的快捷管理')
        # root.iconbitmap('Myshortcut.ico')
        self.root.resizable(0, 0)  # 固定窗口大小
        print("taskmain start")
        self.app = Application(master=self.root)
        #    self.bind("<Button-1>", lambda e: self.kwlb.focus_set)
        # 关闭窗口后重新保存文件
        if self.app.urllist:
            self.app.saveUrlList()
        print("taskmain end")


def action(arg):
    time.sleep(1)
    print('the arg is:%s\r' %arg)

EXITFLG = False
def hotkey():
    global EXITFLG
    while (EXITFLG == False):
        #print(EXITFLG)
        if systemhotkey.RUN == True:
            print(systemhotkey.RUN)
            if(root.winfo_viewable()):
                root.iconify()
            else:
                print(root.winfo_viewable())
                root.update()
                root.deiconify()
            systemhotkey.RUN = False
            print("hotkey run")
        time.sleep(0.1)




if __name__ == '__main__':
    root = tk.Tk()
    root.title('我的快捷管理')
    tmp = open("tmp.ico","wb")
    tmp.write(base64.b64decode(MYICO))
    tmp.close()
    root.iconbitmap("tmp.ico")
    #os.remove("tmp.ico")
    #root.iconbitmap('Myshortcut.ico')
    root.resizable(0, 0)  # 固定窗口大小
    print("taskmain start")
    print("init hotkey")
    hotkey_init = systemhotkey.Hotkey()
    hotkey_init.setDaemon(True)#设置守护进程模式
    hotkey_init.start()
    t1 = threading.Thread(target=hotkey)
    t1.setDaemon(True)#设置守护进程模式
    t1.start()

    print("hotkey run")
    print("hotkey start")
    app = Application(master=root)
    #    self.bind("<Button-1>", lambda e: self.kwlb.focus_set)
    # 关闭窗口后重新保存文件
    if app.urllist:
        app.saveUrlList()
    print("taskmain end")
    #EXITFLG = True
