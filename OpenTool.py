#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on '2018/7/13'
__author__ = 'caochaobin'

import tkinter as tk
from tkinter import messagebox
# from tkinter.font import families
from tkinter import *
from pypinyin import Style
import pypinyin
import webbrowser
import json

FONT_1 = ('微软雅黑', 14, 'normal')
FONT_2 = ('Arial', 12, 'normal')


# 点击添加按钮，弹出输入窗口
class PopupDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        sw = self.winfo_screenwidth()  # 得到屏幕宽度
        sh = self.winfo_screenheight() - 100  # 得到屏幕高度
        ww = 400
        wh = 110
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.geometry("%dx%d+%d+%d" % (ww, wh, x, y))  # 居中显示
        self.resizable(0, 0)  # 禁止缩放窗口
        # self.attributes("-toolwindow", 1)
        # self.attributes('-disabled', 1)

        self.title('添加路径')
        self.transient(parent)
        self.parent = parent  # 显示式地保留父窗口
        frame = tk.Frame(self)
        frame.grid()

        self.grab_set()  # 使焦点聚焦到新窗口，根窗口失效
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # 第一行
        # frame = tk.Frame(self)
        # row1.pack(fill=X)
        tk.Label(frame, text='名称：').grid(row=0, column=0, sticky=E, pady=8)
        self.name = tk.StringVar()
        # 横跨四列
        self.entry1 = tk.Entry(frame, textvariable=self.name, width=50)
        self.entry1.grid(row=0, column=1, columnspan=4, sticky=W, pady=8)
        # 第二行
        tk.Label(frame, text='路径：').grid(row=1, column=0, sticky=E)
        self.url = tk.StringVar()
        tk.Entry(frame, textvariable=self.url, width=50).grid(row=1,
                                                              column=1, columnspan=4, sticky=W)
        # 第三行
        tk.Button(frame, text="确定", command=self.ok).grid(row=2, column=2, sticky=S, pady=10)
        tk.Button(frame, text="取消", command=self.cancel).grid(row=2, column=3, sticky=S, pady=10)

        self.entry1.focus_set()

        # 事件处理
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def ok(self, event=None):
        urlname = self.name.get().strip()
        url = self.url.get().strip()

        if urlname == '' or url == '':
            messagebox.showwarning('警告', '输入不能为空！')
            return

        # if self.parent.urllist.has_key(self.parent.name): # has_key() 方法
        if urlname in self.parent.urllist:
            if messagebox.askyesno('提示', '名称 ‘%s’ 已存在，将会覆盖，是否继续？' % urlname):
                pass
            else:
                return

        # 顯式地更改父窗口參數
        # self.parent.name = urlname
        # self.parent.url = url

        self.parent.urllist[urlname] = url

        # 重新加载列表
        self.parent.listbox.delete(0, END)
        for item in self.parent.urllist:
            self.parent.listbox.insert(END, item)
        self.destroy()  # 銷燬窗口

    def cancel(self, event=None):
        self.destroy()


# 主窗体
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.pack()

        # 获取列表
        self.urllist = self.readUrlList()
        if self.urllist:
            self.createWidgets()
            self.mainloop()
        else:
            messagebox.showinfo('Error', '读取地址列表失败！请查看openlist.json文件是否存在并且格式正确。')

    def readUrlList(self):
        try:
            with open('openlist.json', 'r', encoding='utf-8') as f_obj:
                urllist = json.load(f_obj)
                # for name,url in urllist.items():
                #     print(name,url)
            return urllist
        except FileNotFoundError:
            return None

    def savaUrllist(self):
        with open('openlist.json', 'w', encoding='utf-8') as f:
            json.dump(self.urllist, f, ensure_ascii=False, indent=2)

        print('文件保存成功。')

    def createWidgets(self):
        # 创建搜索框
        self.frame1 = tk.Frame()
        self.frame1.pack(side=TOP, fill=X)
        self.lb = Label(self.frame1, text='搜索：', font=FONT_2)
        self.lb.pack(side=LEFT)
        self.keywdbox = Entry(self.frame1, font=FONT_2)
        self.keywdbox.pack(side=LEFT, fill=X, expand=YES)

        self.keywdbox.focus_set()  # 打开应用时光标定位到搜索框

        # 创建列表框
        self.frame2 = tk.Frame()
        self.frame2.pack(side=TOP, fill=X, pady=5)
        self.scrolly = Scrollbar(self.frame2, )
        self.scrolly.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.frame2, width=60, height=15, font=FONT_1,
                               yscrollcommand=self.scrolly.set)  # 列表框
        # self.listbox = Listbox(self.frame2, height=18, selectmode = EXTENDED,
        #                      yscrollcommand=self.scrolly.set)  # 列表框
        self.listbox.pack(fill=BOTH, expand=YES)
        self.scrolly.config(command=self.listbox.yview)

        # 创建添加、删除按钮
        self.frame3 = tk.Frame()
        self.frame3.pack(side=TOP, fill=BOTH, pady=10)
        Label(self.frame3, width=20).pack(side=LEFT, expand=YES)  # 增加空标签，为了调整按钮位置
        self.btnadd = Button(self.frame3, text='添加', command=self.additem)
        self.btnadd.pack(side=LEFT, expand=YES)
        self.btndel = Button(self.frame3, text='删除', command=self.deleteitem)
        self.btndel.pack(side=LEFT, expand=YES)
        Label(self.frame3, width=20).pack(side=RIGHT, expand=YES)

        # 加载地址列表
        for item in self.urllist:
            self.listbox.insert(END, item)  # 从尾部插入

        # 添加事件处理
        self.doevent()

    def doevent(self):
        # self.keywdbox.bind("<Return>", self.showlist)  # 按回车键，显示搜索结果
        self.keywdbox.bind("<KeyRelease>", self.showlist)  # 实时显示搜索结果
        # self.keywdbox.bind("<BackSpace>", self.showlistAll)
        self.listbox.bind('<Double-Button-1>', self.openurl)  # 双击打开地址
        self.listbox.bind('<Return>', self.openurl)  # 按Enter键打开地址

        self.listbox.bind('<Left>', lambda e: self.keywdbox.focus_set())  # 返回搜索框
        # self.listbox.bind('<Right>', lambda e: self.keywdbox.focus_set())  # 返回搜索框
        self.keywdbox.bind("<Down>", self.jump_to_listbox)  # 按DOWN键，跳到列表中

    def additem(self):
        pw = PopupDialog(self)
        # self.master.attributes('-disabled', 1)    # 使主窗口失效
        self.wait_window(pw)  # 這一句很重要！！！
        # self.master.attributes('-disabled', 0)    # 激活主窗口

        # 如果要获取一个输入值，采用下面方法
        # r = simpledialog.askstring('Python Tkinter', 'Input String',
        #                            initialvalue='Python Tkinter')

    def deleteitem(self):
        index = self.listbox.curselection()
        try:
            item = self.listbox.get(index)
        except TclError:
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

        # for item in index:
        #     print(self.listbox.get(item))
        #     self.listbox.delete(item)
        # print(index)
        # urlname = self.listbox.get(self.listbox.curselection())
        # print(urlname)

    def openurl(self, event):
        urlname = self.listbox.get(self.listbox.curselection())
        url = self.urllist[urlname]  # 根据key值获取对应url值

        if url is not None and url != '':
            webbrowser.open(url)
        else:
            messagebox.showinfo('Error !', '打开地址失败！地址为空。')

    def jump_to_listbox(self, event):
        if self.listbox.size():
            self.listbox.select_clear(0, END)
            self.listbox.select_set(0)
            self.listbox.activate(0)
            # print(self.listbox.curselection())
            self.listbox.focus_set()

    def showlistAll(self, event):
        keywd = self.keywdbox.get().strip()
        # 退格清空文本框时，重新显示列表
        if len(keywd) == 1:
            self.listbox.delete(0, END)
            for item in self.urllist:
                self.listbox.insert(END, item)  # 从尾部插入

    def showlist(self, event):
        keywd = self.keywdbox.get().strip()
        if keywd:
            self.listbox.delete(0, END)
            # print(urllist)
            for item in self.urllist:
                cond_1 = keywd.lower() in item.lower()
                cond_2 = keywd.lower() in pypinyin.slug(item.lower(), separator='')
                cond_3 = keywd.lower() in pypinyin.slug(item.lower(), style=Style.FIRST_LETTER, separator='')
                if any([cond_1, cond_2, cond_3]):
                    self.listbox.insert(END, item)  # 加载搜索结果
        else:
            self.listbox.delete(0, END)
            for item in self.urllist:
                self.listbox.insert(END, item)  # 空字符时，加载所有列表


if __name__ == '__main__':
    root = Tk()  # 构造窗体
    root.title('Open Everything')
    root.iconbitmap('opentool.ico')

    root.resizable(0, 0)  # 固定窗口大小
    app = Application(master=root)
    # app.mainloop()

    # 关闭窗口后重新保存文件
    if app.urllist:
        app.savaUrllist()
