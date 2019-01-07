
工作了一段时间发现，电脑桌面上已经满屏的常用软件、常用项目文件夹的快捷方式，一大堆的常用文档，浏览器上收藏的工作网址更是有100+，通常想打开一个文档、网址要寻找半天，于是萌生了写一个工具集中管理这些地址的想法。

## 实现：Python - tkinter + webbrowser
效果如下：

![](https://i.imgur.com/vn7WO9d.png)
![](https://i.imgur.com/ZsZHYtN.png)
![](https://i.imgur.com/QY8tXqY.png)

## 功能：

- [x] **关键字搜索，字母不区分大小写。**
- [x] **添加：URL网址，本地软件路径，本地文档路径**
- [x] **双击/敲回车键快捷打开**
- [x] **选中删除**
- [ ] **修改：可使用添加功能，支持同名覆盖**

## 原理：

- 导入库  
tkinter,webbrowser均为python标准库，不需要另外安装
	```python
	import tkinter as tk
	import json
	import webbrowser
	from tkinter import messagebox
	from tkinter import *
	```

- 使用python自带界面开发库tkinter开发基本界面
	```python
	if __name__ == '__main__':
	    root = Tk()  # 构造窗体
	    root.title('Open Everything') # 标题
	    root.iconbitmap('opentool.ico') # 加载图标
	
	    root.resizable(0,0) # 固定窗口大小
	    app = Application(master=root)	
	```

- 读取json文件，加载数据到Listbox
	```python
	self.urllist = self.readUrlList() # 获取列表
	if self.urllist:
	    self.createWidgets()
	    self.mainloop()
	else:
	    messagebox.showinfo('Error','读取地址列表失败！请查看openlist.json文件是否存在并且格式正确。')

	```
	```python
	# 加载地址列表
        for item in self.urllist:
            self.listbox.insert(END, item)  # 从尾部插入
	```

- 添加事件处理
	```python
	def doevent(self):
        self.keywdbox.bind("<Return>",self.showlist) # 按回车键，显示搜索结果
        self.keywdbox.bind("<BackSpace>",self.showlistAll)
        self.listbox.bind('<Double-Button-1>',self.openurl) # 双击打开地址
        self.listbox.bind('<Return>',self.openurl) # 按Enter键打开地址
	```
- 使用`webbrowser.open(url)`方法打开路径.  
这个方法比较强大，如果是http地址，会直接在浏览器中打开，如果是本地地址，会直接打开本地的软件/文件夹/文档等
	```python
    def openurl(self,event):
        urlname = self.listbox.get(self.listbox.curselection())
        url = self.urllist[urlname] # 根据key值获取对应url值

        if url is not None and url != '':
            webbrowser.open(url)
        else:
            messagebox.showinfo('Error !', '打开地址失败！地址为空。')
	```

- 搜索功能  
搜索功能实现比较简单，遍历字典key值，判断关键字是否存在key中
	```python
    def showlist(self, event):
        keywd = self.keywdbox.get().strip()
        if keywd:
            self.listbox.delete(0, END) # 先做清空列表动作

            for item in self.urllist:
                if keywd.lower() in item.lower():   # 判断关键字是否存在字典key中
                    self.listbox.insert(END, item)  # 加载搜索结果
	```

- 退出软件时重新保存json文件
	```python
    def savaUrllist(self):
        with open('openlist.json', 'w', encoding='utf-8') as f:
            json.dump(self.urllist,f, ensure_ascii=False, indent=2)

        print('文件保存成功。')
	```

- 打包软件  
win下使用pyinstaller  
Mac下使用py2app

![](https://i.imgur.com/XCDeKgY.png)

## 使用教程

- 获取软件和源码：
`GitHub地址:`[https://github.com/turbobin/Open-Manager](https://github.com/turbobin/Open-Manager)

- 下载`OpenTool.exe`，解压到本地路径即可使用。


## LICENSE

MIT

---------------------

## 更新 -- 20180916	 **Thinks for @CYDROM's pull requests**
**更新点：**

* 增加实时查询：输入就开始查询。之前输入关键字需要按Enter键筛选结果，现在只要输入就在同时筛选，优化了用户体验；
* 拼音查询：全拼或拼音首字母查询，比如之前要输入完整的关键字`'百度'`'，现在输入`'baidu'`就可以快速筛选出来；
	* 安装第三方包`pip install pypinyin` 
```python
from pypinyin import Style
import pypinyin
......
	def showlist(self, event):
        keywd = self.keywdbox.get().strip()
        if keywd:
            self.listbox.delete(0, END)
            # print(urllist)
            for item in self.urllist:
                if (keywd.lower() in item.lower()) or (keywd.lower() in pypinyin.slug(item.lower(), separator='') or
                    (keywd.lower() in pypinyin.slug(item.lower(),style=Style.FIRST_LETTER,separator=''))):
                    self.listbox.insert(END, item)  # 加载搜索结果
        else:
            self.listbox.delete(0, END)
            for item in self.urllist:
                self.listbox.insert(END, item)  # 空字符时，加载所有列表
```
* 方向键快捷键：输入框中按 Down键，进入条目区，条目区按下Left键返回搜索框；

**优化：**

* 打开软件时，使光标直接定位到搜索框
* 打开添加子窗口时，使光标定位到输入框，并使根窗口失效(不可点击)，上一版本可打开多个添加窗口，根窗口还可以聚焦，不太合理。

具体实现细节，可 `git clone https://github.com/turbobin/Open-Manager.git`查看。

--------------------
## 更新 --20181205
Chrome书签收藏有 200 个以上了，如何把这些书签导入我的收藏神器中呢？
1.在 Chrome 浏览器中右上角点击**书签** --> **书签管理器** --> **点击右上角** --> **导出书签**，会下载一个类似`bookmarks_2018_12_05.html`文件，双击打开，如图：

![](https://i.imgur.com/PquhQbc.png)

2.下面我们来用 BeautifulSoup 把书签名和对应 url 爬下来，保存 json 文件，程序如下：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on '2018/12/05'

from bs4 import BeautifulSoup
import requests
import json

def create_soup():
	f = open("bookmarks_2018_12_05.html", encoding="utf-8")
	soup = BeautifulSoup(f, 'html.parser')
	return soup


def dumps_json(soup):
	openlist = dict()
	tag_a = soup.find_all('a')
	for a in tag_a:
		openlist[a.string] = a.get('href')

	content = json.dumps(openlist, ensure_ascii=False, indent=2)
	with open("openlist.json", "w", encoding="utf-8") as f:
		f.write(content)


def main():
	soup = create_soup()
	dumps_json(soup)

if __name__ == '__main__':
	main()
```
3.把文件 openlist.json (固定命名) 放到 OpenTool.exe 文件同级目录下，可以和原来的 openlist.json 做一下合并，现在打开软件，可以看到书签已经加载进来了。
![](https://i.imgur.com/Fvxqm0t.png)

--------------------
欢迎 Star 和 Fork ~  


如有问题，请提出改进建议，谢谢！联系:**turbobin@foxmail.com**

---
**博客地址：**[https://turbobin.github.io/](https://turbobin.github.io/2018/12/05/python-Tkinter/)

