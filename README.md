# 如何管理杂乱的电脑桌面和一大堆的浏览器收藏网址？我用python写了一个工具，迅速提高工作效率。

工作了一段时间发现，电脑桌面上已经满屏的常用软件、常用项目文件夹的快捷方式，一大堆的常用文档，浏览器上收藏的工作网址更是有100+，通常想打开一个文档、网址要寻找半天，有没有方法可以集中管理这些地址呢？
我用**python tkinter + webbrowser**写了一个地址收藏工具

![](https://i.imgur.com/vn7WO9d.png)
![](https://i.imgur.com/ZsZHYtN.png)

## 功能：

- [x] **关键字搜索，字母不区分大小写**
- [x] **添加：url网址，本地软件路径，本地文档路径**
- [x] **选中删除**
- [x] **双击/敲回车直接打开**
- [ ] **修改，可使用添加功能修改打开路径，起相同的名称，会覆盖原来的路径**

## 原理：

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
	# 加载网址列表
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
- 使用**webbrowser.open()**打开路径
这个方法比较强大，如果是http地址，会直接在浏览器中打开，如果是本地地址，会直接打开软件/文件夹/文档...
	```python
    def openurl(self,event):
        urlname = self.listbox.get(self.listbox.curselection())
        url = self.urllist[urlname] # 根据key值获取对应url值

        if url is not None and url != '':
            webbrowser.open(url)
        else:
            messagebox.showinfo('Error !', '打开网址失败！地址为空。')
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

- 打包软件
win下使用pyinstaller
Mac下使用py2app

![](https://i.imgur.com/XCDeKgY.png)

## 使用教程

- 获取软件和源码：
`GitHub地址：`[https://github.com/turbobin/Open-Manager](https://github.com/turbobin/Open-Manager)

- 下载`OpenTool.exe`，解压到本地路径即可使用。


## LICENSE

MIT

欢迎 Star 和 Fork ~