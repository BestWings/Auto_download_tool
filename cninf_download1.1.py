# -*- coding:utf-8 -*-

import Tkinter as tk
import tkMessageBox as mb
from ScrolledText import ScrolledText
import sys
import time
import json
import requests
import os
import re
import bs4 as bs
import urllib



#获取当前时间
def getNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

#返回当前目录下存在的pdf文件组
def getDirName(dir):
    DirName=[]
    f_list = os.listdir(dir)
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.pdf'.decode("utf-8"):
            DirName.append(os.path.splitext(i)[0])
    return DirName

#设置检查更新
'''
参数说明:
stock:代表股票的编码,category:代表类型

'''
class Check_update:
    def __init__(self,stock,category):
        self.stock=stock
        self.category=category
        self.url='http://www.cninfo.com.cn/cninfo-new/announcement/query'
        self.headers={"User-Agent":"Mozilla/5.0 (Macintosh;Intel Mac OS X 10_9_5) AppleWebKit 537.36(KHTML,like Gecko) Chrome",
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"} #设置头文件
        self.data = {
        'stock':stock,
        'category':category+';',
        'pageNum':"1",
        # 'pageSize':'15',
        'column':'sse',
        'tabName':'fulltext'
        }
    #adjunctSize
    def check(self):
        for item in pdf_rest_count:
            if self.category == item[u'category']:
                pdf_rest_count.remove(item)
        self.count =0
        self.r1 = re.compile(r'/(.*?)/')
        self.path_temp=r'D:/pdf/%s/%s'%(self.stock,path[self.category])
        if not os.path.isdir(self.path_temp):
            os.makedirs(self.path_temp)
        self.file_current =getDirName(self.path_temp)
        self.max_page=100000000   #假定无限大的页面
        for i in xrange(self.max_page):
            self.page = i + 1
            self.data['pageNum'] = str(self.page)
            self.HomePage = requests.post(self.url, data=self.data, headers=self.headers)
            self.soup1 = bs.BeautifulSoup(self.HomePage.text, "lxml")
            self.pdf_json = json.loads(self.soup1.get_text())["announcements"]
            if not len(self.pdf_json):
                break
            for item in self.pdf_json:
                self.pdf_date = self.r1.findall(item['adjunctUrl'])
                self.name=self.pdf_date[0]+"_"+item["announcementTitle"]
                if self.name in self.file_current:
                    pass
                else:
                    pdf_rest.append({u'category':self.category,u'title': item["announcementTitle"], u'date': self.pdf_date[0], u'id': item["announcementId"]})
                    self.count += 1
        pdf_rest_count.append({u'category': self.category, u'count': self.count})

#调整窗口位置居中
#返回屏幕的大小
def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()
#返回窗口的大小
def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()
#调整窗口在中心的为之一
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)
#隐藏
class Hide():
    def __init__(self,Master):
        Master.withdraw()
#终止一切
def quit_all():
    sys.exit(0)
#显示
class Show():
    def __init__(self,Master):
        Master.update()
        Master.deiconify()
#创建主窗口
class Create_main_window:
    def __init__(self,Master):
        center_window(Master, 550, 170)  # 设置窗口居中，设置宽度和高度
        Master.title("Download") #标题名
        Master.resizable(False, False) #设置无法改变大小
        Master.protocol("WM_DELETE_WINDOW", quit_all) #控制退出键
        # Master.iconbitmap('C:\Users\zwcpc\PycharmProjects\HaiGe_Spider\cong.ico') #添加图标


        self.frame1=tk.Frame(Master)
        # 设置提示
        self.label1 = tk.Label(self.frame1, text="选择你要下载的任务：")
        self.label1.grid(row=0, column=0, sticky=tk.W, padx=1, pady=2)

        # 设置股票代码
        self.label2 = tk.Label(self.frame1, text="股票代码")
        self.label2.grid(row=0, column=1, sticky=tk.E)
        self.stockCode_var = tk.StringVar()
        self.stockCode = tk.Entry(self.frame1, textvariable=self.stockCode_var)
        self.stockCode.insert(0, "600000")
        self.stockCode.grid(row=0, column=2, sticky=tk.W)

        # 复选框区域变量
        self.all_var = tk.BooleanVar()  # 全选
        self.ndbg_var = tk.BooleanVar()  # 年度报告
        self.bndbg_var = tk.BooleanVar()  # 半年度报告
        self.yjdbg_var = tk.BooleanVar()  # 一季度报告
        self.sjdbg_var = tk.BooleanVar()  # 三季度报告
        self.pg_var = tk.BooleanVar()  # 配股
        self.scgkfx_var = tk.BooleanVar()  # 首次公开发行及上市
        self.zf_var = tk.BooleanVar()  # 增发
        self.kzhz_var = tk.BooleanVar()  # 可转换债券
        self.qtrz_var = tk.BooleanVar()  # 其他融资

        # 复选框区域
        def all_select():
            if self.all_var.get() == 1:
                self.ndbg_var.set(1)
                self.bndbg_var.set(1)
                self.yjdbg_var.set(1)
                self.sjdbg_var.set(1)
                self.pg_var.set(1)
                self.scgkfx_var.set(1)
                self.zf_var.set(1)
                self.kzhz_var.set(1)
                self.qtrz_var.set(1)
            if self.all_var.get() == 0:
                self.ndbg_var.set(0)
                self.bndbg_var.set(0)
                self.yjdbg_var.set(0)
                self.sjdbg_var.set(0)
                self.pg_var.set(0)
                self.scgkfx_var.set(0)
                self.zf_var.set(0)
                self.kzhz_var.set(0)
                self.qtrz_var.set(0)

        self.all = tk.Checkbutton(self.frame1, text="全选", variable=self.all_var, command=all_select)
        self.all.grid(row=1, column=0, sticky=tk.W)

        self.ndbg = tk.Checkbutton(self.frame1, text="年度报告", variable=self.ndbg_var)
        self.ndbg.grid(row=2, column=0, sticky=tk.W)

        self.bndbg = tk.Checkbutton(self.frame1, text="半年度报告", variable=self.bndbg_var)
        self.bndbg.grid(row=2, column=1, sticky=tk.W)

        self.yjdbg = tk.Checkbutton(self.frame1, text="一季度报告", variable=self.yjdbg_var)
        self.yjdbg.grid(row=2, column=2, sticky=tk.W)

        self.sjdbg = tk.Checkbutton(self.frame1, text="三季度报告", variable=self.sjdbg_var)
        self.sjdbg.grid(row=2, column=3, sticky=tk.W)

        self.pg = tk.Checkbutton(self.frame1, text="配股", variable=self.pg_var)
        self.pg.grid(row=3, column=0, sticky=tk.W)

        self.scgkfx = tk.Checkbutton(self.frame1, text="首次公开发行及上市", variable=self.scgkfx_var)
        self.scgkfx.grid(row=3, column=1, sticky=tk.W)

        self.zf = tk.Checkbutton(self.frame1, text="增发", variable=self.zf_var)
        self.zf.grid(row=3, column=2, sticky=tk.W)

        self.kzhzq = tk.Checkbutton(self.frame1, text="可转换债券", variable=self.kzhz_var)
        self.kzhzq.grid(row=3, column=3, sticky=tk.W)

        self.qtrz = tk.Checkbutton(self.frame1, text="其他融资", variable=self.qtrz_var)
        self.qtrz.grid(row=4, column=0, sticky=tk.W)

        # 设置下一步按钮的功能在show_root2
        self.nextone = tk.Button(self.frame1, text="下一步", width=10,command=self.show_root2)
        self.nextone.grid(row=5, column=2)
        #设置退出按钮的功能为系统的退出
        self.quit = tk.Button(self.frame1, text="退出", width=10, command=quit_all)
        self.quit.grid(row=5, column=3)

        self.frame1.pack()

    def show_root2(self):
        info['stock'] = self.stockCode_var.get()
        info['category_ndbg_szsh'] = self.ndbg_var.get()
        info['category_bndbg_szsh'] = self.bndbg_var.get()
        info['category_yjdbg_szsh'] = self.yjdbg_var.get()
        info['category_sjdbg_szsh'] = self.sjdbg_var.get()
        info['category_scgkfx_szsh'] = self.scgkfx_var.get()
        info['category_pg_szsh'] = self.pg_var.get()
        info['category_zf_szsh'] = self.zf_var.get()
        info['category_kzhz_szsh'] = self.kzhz_var.get()
        info['category_qtrz_szsh'] = self.qtrz_var.get()
        if len(info['stock']) != 6:
            mb.showerror('输入错误', '请输入正确的股票代码！')
            return
        if not (info['category_ndbg_szsh'] or info['category_bndbg_szsh'] or info['category_yjdbg_szsh'] or info[
            'category_sjdbg_szsh'] or
                    info['category_scgkfx_szsh'] or info['category_pg_szsh'] or info['category_zf_szsh'] or info[
            'category_kzhz_szsh'] or info['category_qtrz_szsh']):
            mb.showerror('输入错误', '请至少选中一个内容')
            return
        self.frame1.quit()
        # if count == 0:
        #     Hide(root1)
        #     pass
        # else:
        Hide(root1)

# 设置跳转窗口
class Create_skip_window():
    def __init__(self, Master):
        center_window(Master, 550, 250)  # 设置窗口居中，设置宽度和高度
        Master.title("Download")  # 设置窗口标题
        Master.resizable(False, False)
        # Master.iconbitmap('C:\Users\zwcpc\PycharmProjects\HaiGe_Spider\cong.ico')  --添加图标
        Master.protocol("WM_DELETE_WINDOW", quit_all)
        self.frame2 = tk.Frame(Master)
        # 设置提示
        self.label1 = tk.Label(self.frame2, text="请注意网络通畅:")  # 设置提示项
        self.label1.grid(row=0, column=0, sticky=tk.W)

        self.blank = tk.Label(self.frame2, text="")  # 设置空行
        self.blank.grid(row=1, column=0, sticky=tk.W)

        self.blank = tk.Label(self.frame2, text="")  # 设置空白
        self.blank.grid(row=2, column=0, sticky=tk.W)

        self.check = tk.Button(self.frame2, text="检查更新", width=15, height=2,command=self.check_newItem)
        self.check.grid(row=2, column=1)

        self.blank = tk.Label(self.frame2, text="")  # 设置空白
        self.blank.grid(row=2, column=2, sticky=tk.W, padx=45, pady=1)

        self.download = tk.Button(self.frame2, text="开始下载", width=15, height=2,command=self.download_cninfo)
        self.download.grid(row=2, column=3)

        self.blank = tk.Label(self.frame2, text="")  # 设置空白
        self.blank.grid(row=2, column=4, sticky=tk.W, padx=45, pady=1)

        self.blank = tk.Label(self.frame2, text="")  # 设置空行
        self.blank.grid(row=3, column=0, sticky=tk.W)

        self.label2 = tk.Label(self.frame2, text="提示:")  # 设置提示项
        self.label2.grid(row=4, column=0, sticky=tk.E)

        self.txt = ScrolledText(self.frame2, width=40, height=5)
        self.txt.grid(row=4, column=1, columnspan=3)

        self.blank = tk.Label(self.frame2, text="")  # 设置空行
        self.blank.grid(row=5, column=0, sticky=tk.W)

        self.back = tk.Button(self.frame2, text="上一步", width=12, height=1,command=self.show_root1)
        self.back.grid(row=6, column=3)

        self.quit = tk.Button(self.frame2, text="退出", width=12, height=1, command=quit_all)
        self.quit.grid(row=6, column=4)

        self.frame2.pack()
    def show_root1(self):
        Hide(root2)
        Show(root1)
    def check_newItem(self):
        hint=0
        for key in info:
            if key == 'stock':
                pass
            if info[key] == False:
                for item in pdf_rest_count:
                    if item[u"category"]==key:
                        pdf_rest_count.remove(item)
                for item in pdf_rest:
                    if item[u"category"]==key:
                        pdf_rest.remove(item)
            if info[key] == True:
                check = Check_update(stock= info['stock'], category=key)  # 年度报告
                check.check()
        message = ""
        for item in pdf_rest_count:
            hint += 1
            message += str(hint) + u'、' + path[item[u'category']] + u'有' + str(item[u'count']) + u'个更新项\n'
        self.txt.delete(0.0, tk.END)
        self.txt.insert(tk.END, message)

    def download_cninfo(self):
        f = open('D:/pdf/log.txt', 'a')
        log = ''
        for item in pdf_rest:
            path_temp = r'D:/pdf/%s/%s' % (info['stock'], path[item[u'category']])
            localPDF = path_temp + '/' + item[u'date'] + '_' + item[u'title'] + '.pdf'
            url2 = "http://www.cninfo.com.cn/cninfo-new/disclosure/sse/download/" + item[u'id'] + '?announceTime=' + \
                   item[u'date']
            log1 = getNowTime() + ":" + path[item[u'category']].encode('utf-8') + "the pdf(" + item[u'date'].encode(
                'utf-8') + '_' + item[u'title'].encode('utf-8') + '.pdf' + ")starts downloading:\n"
            log += log1
            f.write(log1)
            self.txt.delete(0.0, tk.END)
            self.txt.insert(0.0, log)
            urllib.urlretrieve(url2, localPDF)
            log2 = getNowTime() + ":" + path[item[u'category']].encode('utf-8') + "pdf(" + item[u'date'].encode(
                'utf-8') + '_' + item[u'title'].encode('utf-8') + '.pdf' + ")downloads successfully!\n"
            f.write(log2)
            log += log2
            self.txt.delete(0.0, tk.END)
            self.txt.insert(0.0, log)
        mb.showinfo('恭喜', '所有任务下载成功！')
        f.close()

if __name__ == "__main__":
    info = dict()
    path = {'category_ndbg_szsh': u'年度报告', 'category_bndbg_szsh': u'半年度报告', 'category_yjdbg_szsh': u'一季度报告',
            'category_sjdbg_szsh': u'三季度报告', 'category_scgkfx_szsh': u'首次公开发行及上市', 'category_pg_szsh': u'配股',
            'category_zf_szsh': u'增发', 'category_kzhz_szsh': u'可转换债券', 'category_qtrz_szsh': u'其他融资'}  # 路径信息
    pdf_rest = list()
    pdf_rest_count = list()
    count = 0
    root1 = tk.Tk()
    main_window = Create_main_window(root1)
    root1.mainloop()
    for count in xrange(100000000):
        root2 = tk.Tk()
        skip_window = Create_skip_window(root2)
        root2.mainloop()