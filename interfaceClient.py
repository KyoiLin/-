
'''
Description: 测试时需要对网络连接设置进行调整，checkCookie中部分代码解除注释
Version: 1.0
Author: KyoiLin
Date: 2023-04-16 16:57:38
LastEditors: KyoiLin
LastEditTime: 2023-04-22 17:30:10
FilePath: \code\interfaceClient.py
Copyright (C) 2023 KyoiLin. All rights reserved.
'''
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from PIL import Image, ImageTk
import pandas as pd
import include.user as u
from socket import *
import os
import cv2 as cv

'''
网络连接设置
'''
ADDR = '192.168.56.1'   #服务器的ip地址
port=9000       # 统一的端口设置
buffsize=1024
'''
正式运行时修改以下五行代码让正常的socket运行即可
'''
if 0:
    s=socket(AF_INET, SOCK_STREAM)
    s.connect((ADDR,port))
else:
    s = socket()

filepath = "./asset/id-zy.csv"
logpath = "./logs/cookie.txt"
'''
正式运行时把logpath和test_cookie_path内容互换，并把iftest设置为False
'''
test_cookie_path = "./logs/cookie_temp.txt"
test_search_result = "AAA-BBB-数一-英一-政治-专业课一_AAA-CCC-数一-英一-政治-专业课二"
iftest = True

'''
检查cookie文件，若不存在则需要向服务器申请
读取到的cookieID直接作为string保存
'''
def checkCookie():
    global cookie
    if(os.path.exists(test_cookie_path)):
        with open(test_cookie_path, "r" , encoding="utf-8") as f:  # 打开文件
            cookie_ = f.read()  # 读取文件
        cookie = cookie_
    '''
    正式运行时取消以下注释
    '''
    # else:
    #     s.send('cookie'.encode('utf-8'))
    #     cookie_ = s.recv().decode('utf-8')
    #     print('Get Cookie: '+cookie_)
    #     cookie = cookie_

images = []
img = None
img2 = None
WIDTH = 1100
HEIGHT = 600
SIZE = '1100x600'
BGCOLOR = "#DDDDDD"
BTCOLOR = '#F5F5F5'
cookie = '0'

def create_rectangle(c1, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            images.append(ImageTk.PhotoImage(image))
            c1.create_image(x1, y1, image=images[-1], anchor='nw')
        c1.create_rectangle(x1, y1, x2, y2, **kwargs)

def round_rectangle(c1, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius,
            x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius,
            x1, y1]
    return c1.create_polygon(points, outline='#696969', width=1, **kwargs, smooth=True)

class main:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title('Base page')
        self.root.geometry(SIZE)
        self.root.resizable(False, False)
        firstpage(self.root)

class firstpage:
    def __init__(self, root) -> None:
        global img
        global images
        self.root = root
        self.firstpage = tk.Frame(self.root,width=WIDTH,height=HEIGHT)
        self.firstpage.place(x=0,y=0)
        
        self.c1 = tk.Canvas(self.firstpage, width=WIDTH, height=HEIGHT)
        img = tk.PhotoImage(file='./asset/cat.gif')   
        # tk.Label(self.firstpage, image=img).place(x=100,y=100)  #Label to image
        self.c1.create_image(940,400,image=img)
        rect1 = create_rectangle(self.c1, 80,220,880,550,width=0,fill='black',alpha=0.08)
        self.c1.place(x=0,y=0)
        title = tk.Label(self.firstpage, text='2023考研信息查询', font=("黑体",30,"bold"))
        title.place(x=325,y=70)
        mark = tk.Label(self.firstpage, text="*本平台信息仅供参考，一切信息请以院校官网及研招网为准！", fg='red', font=("黑体",15))
        mark.place(x=225,y=155)
        warning_btn = ttk.Button(self.firstpage, text="click here", width=15, command=self.warningbox)
        warning_btn.place(x=50,y=100)
        login_btn = tk.Button(self.firstpage, text='管理员入口>>>', width=15, command=self.login, relief='flat', bg=BGCOLOR, font=("等线",11,"underline","italic"))
        login_btn.place(x=730,y=510)
        tk.Label(self.firstpage, text='|', bg=BGCOLOR, font=("等线",13)).place(x=722,y=510)
        feedback_btn = tk.Button(self.firstpage, text='联系我们>>>', width=15, command=self.doFeedback, relief='flat', bg=BGCOLOR, font=("等线",11,"underline","italic"))
        feedback_btn.place(x=597,y=510)
        tk.Label(self.firstpage, text="所在省市", bg=BGCOLOR, font=("幼圆",17)).place(x=130,y=273)
        '''
        box_city读取用户输入城市信息box_city.get()
        '''
        self.box_city = ttk.Combobox(self.firstpage, width=25, height=20, state='readonly')
        self.box_city.place(x=245,y=278)
        self.box_city['value'] = self.getCityMenu()
        self.box_city.current(0)
        tk.Label(self.firstpage, text="院校名称", bg=BGCOLOR, font=("幼圆",17)).place(x=500,y=273)
        '''
        box_college读取用户输入院校名称box_college.get()
        '''
        self.box_college = ttk.Entry(self.firstpage, width=27)
        self.box_college.place(x=615,y=278)
        self.box_college.insert(0,'--请输入--')
        self.box_college.bind("<Button-1>",self.clearEntry)
        tk.Label(self.firstpage, text='学科类别', bg=BGCOLOR, font=("幼圆",17)).place(x=130,y=353)
        '''
        box_major读取用户输入专业名称box_major.get()
        '''
        self.box_major = ttk.Combobox(self.firstpage, width=25, height=20, state='readonly')
        self.box_major.place(x=245,y=358)
        self.box_major['value'] = self.getMajor()
        self.box_major.current(0)
        self.box_major.bind("<<ComboboxSelected>>", self.getSearch)
        tk.Label(self.firstpage, text="研究方向", bg=BGCOLOR, font=("幼圆",17)).place(x=500,y=353)
        '''
        box_search读取用户输入研究方向box_search.get()
        '''
        self.box_search = ttk.Combobox(self.firstpage, width=25, height=20, state='readonly')
        self.box_search.place(x=615,y=358)
        self.box_search['value'] = ('--请选择--')
        self.box_search.current(0)
        '''
        重置信息按钮
        '''
        bx1 = 285
        bx2 = 500
        by1 = 440
        round_rectangle(self.c1, bx1,by1,bx1+155,by1+40,radius=20,fill=BTCOLOR)
        reset_btn = tk.Button(self.firstpage, text="重   置", width=15, font=("幼圆",13),  relief='flat', bg=BTCOLOR, command=self.reset)
        reset_btn.place(x=bx1+5,y=by1+5)
        # self.roundRectButton(self.root, self.c1, bx1, by1, 155, 40, "查  询", 15, ("幼圆",13), self.doSearch, 5, 5)
        round_rectangle(self.c1, bx2,by1,bx2+155,by1+40,radius=20,fill=BTCOLOR)
        seasrch_btn = tk.Button(self.firstpage, text="查   询", width=15, font=("幼圆",13),  relief='flat', bg=BTCOLOR, command=self.doSearch)
        seasrch_btn.place(x=bx2+5,y=by1+5)

    '''
    重置四个输入框
    '''
    def reset(self,):
        self.box_city.set('--请选择--')
        self.box_college.delete(0,tk.END)
        self.box_college.insert(0,'--请输入--')
        self.box_major.set('--请选择--')
        self.box_search.set('--请选择--')

    def clearEntry(self, event):
        self.box_college.delete(0, tk.END)

    '''
    查询，获取查询结果并跳转至查询结果页面
    '''
    def doSearch(self,):
        global cookie
        user = u.User(cookie)
        city = self.box_city.get()
        college = self.box_college.get()
        major = self.box_major.get()
        search = self.box_search.get()
        # print(city, college, major, search)
        search_request = user.ClientRequestSearch(city,college,major,search)
        print('Request: '+search_request)
        testdatalist = user.sendSearchRequest(s, search_request, iftest)
        self.firstpage.destroy()
        SearchResultPage(self.root, testdatalist)

    '''
    跳转至反馈界面
    '''
    def doFeedback(self,):
        self.firstpage.destroy()
        FeedbackPage(self.root)

    def warningbox(self,):
        wb1 = showwarning(title="Warning", message="you click the button~")

    '''
    管理员登录，切换管理员界面
    '''
    def login(self,):
        global img2
        login = Toplevel(self.firstpage)
        login.geometry("350x400")
        login.resizable(False,False)
        login.title('Admin Login')
        c2 = tk.Canvas(login, width=350, height=400)
        c2.place(x=0,y=0)
        create_rectangle(c2, 50,70,300,350,width=0,fill='black',alpha=0.08)
        img2 = tk.PhotoImage(file='./asset/login1.gif') 
        c2.create_image(175,75,image=img2)
        form = tk.Frame(login, bg=BGCOLOR, width=200, height=200)
        form.place(x=75,y=110)
        tk.Label(form, text="Name:", bg=BGCOLOR, font=('Candara',15)).pack(anchor='w',pady=7)
        self.admin_name = tk.Entry(form, width=25)
        self.admin_name.pack(anchor='w',pady=7)
        tk.Label(form, text="Password:", bg=BGCOLOR, font=('Candara',15)).pack(anchor='w',pady=7)
        self.admin_password = tk.Entry(form, width=25, show='*')
        self.admin_password.pack(anchor='w',pady=7)
        def adminReset():
            self.admin_name.delete(0, tk.END)
            self.admin_password.delete(0, tk.END)
        def adminLogin():
            admin = u.Admin()
            name = self.admin_name.get()
            password = self.admin_password.get()
            result = admin.login(s, name, password, iftest)
            if result:
                self.firstpage.destroy()
                AdminPage(self.root)
            else:
               tk.messagebox.showwarning('Warning','用户名或密码错误！') 
        bx1 = 70; bx2 = 180; by1 = 295
        round_rectangle(c2, bx1,by1,bx1+80,by1+30,radius=20,fill=BTCOLOR)
        reset_btn = tk.Button(login, text="重  置", width=7, font=("幼圆",11),  relief='flat', bg=BTCOLOR, command=adminReset)
        reset_btn.place(x=bx1+10,y=by1+3)
        round_rectangle(c2, bx2,by1,bx2+80,by1+30,radius=20,fill=BTCOLOR)
        seasrch_btn = tk.Button(login, text="登  录", width=7, font=("幼圆",11),  relief='flat', bg=BTCOLOR, command=adminLogin)
        seasrch_btn.place(x=bx2+10,y=by1+3)

    '''
    input: none
    output: City List(tuple)
    function: 读取id文件获得城市列表，传入combobox作为菜单
    '''
    def getCityMenu(self,):
        menu = pd.read_csv(filepath)
        y = menu[['城市']][:31]
        l = y.values.tolist()
        menelist = []
        for item in l:
            menelist.append(item[0])
        menelist.insert(0,'--请选择--')
        return tuple(menelist)
    
    '''
    input: none
    output: Major List(tuple)
    function: 读取id文件获得专业列表，传入combobox作为菜单
    '''
    def getMajor(self,):
        menu = pd.read_csv(filepath)
        y = menu['专业'][:200]
        l = y.values.tolist()
        l.insert(0,'--请选择--')
        return tuple(l)
    
    '''
    input: none
    outpur: search directions(tuple)
    function: 根据输入的专业搜索对应的研究方向，返回研究方向tuple作为combobox菜单
    '''
    def getSearch(self, event):
        self.box_search.set('')
        major = self.box_major.get()
        if major == None:
            return
        else:
            menu = pd.read_csv(filepath)
            finddata = menu[menu['专业']==major]
            finddata.dropna(axis=1,how='all')
            fl = finddata.values.tolist()[0]
            fl = fl[1:]
            fll = []
            for item in fl:
                if item == item:
                    fll.append(item)
            fll = fll[1:]
            fll.insert(0,'--请选择--')
            self.box_search['value'] = tuple(fll[1:])
            if len(fll) > 1:
                self.box_search.current(0)
            return 
    
    def getDefaultSearch(self, ):
        fll = ['--请选择--']
        return tuple(fll[1:])

class SearchResultPage:
    def __init__(self, root, datalist) -> None:
        self.root = root
        self.secondpage = tk.Frame(self.root,width=WIDTH,height=HEIGHT)
        self.secondpage.place(x=0,y=0)

        global img
        self.c1 = tk.Canvas(self.secondpage, width=WIDTH, height=HEIGHT)
        img = tk.PhotoImage(file='./asset/cat.gif')   
        # tk.Label(self.secondpage, image=img).place(x=100,y=100)  #Label to image
        self.c1.create_image(940,400,image=img)
        rect1 = create_rectangle(self.c1, 80,220,880,550,width=0,fill='black',alpha=0.08)
        self.c1.place(x=0,y=0)
        title = tk.Label(self.secondpage, text='2023考研信息查询', font=("黑体",30,"bold"))
        title.place(x=325,y=70)
        mark = tk.Label(self.secondpage, text="*本平台信息仅供参考，一切信息请以院校官网及研招网为准！", fg='red', font=("黑体",15))
        mark.place(x=225,y=155)

        self.form = tk.Frame(self.secondpage,width=700, height=300, bg='blue')
        self.form.place(x=125,y=250)
        ybar = Scrollbar(self.form, orient='vertical')
        headlist = ('院校', '专业', '专业方向', '数学', '英语', '专业一', '专业二')
        tree = ttk.Treeview(self.form,column=headlist, show='headings',displaycolumns='#all',selectmode='none', height=11, yscrollcommand=ybar.set)
        ybar['command'] = tree.yview
        tree.heading('院校', text='院  校', anchor='center')
        tree.heading('专业', text='专  业', anchor='center')
        tree.heading('专业方向', text='专业方向', anchor='center')
        tree.heading('数学', text='数  学', anchor='center')
        tree.heading('英语', text='英  语', anchor='center')
        tree.heading('专业一', text='专业课一', anchor='center')
        tree.heading('专业二', text='专业课二', anchor='center')
        tree.column('院校', width=130, anchor='center')
        tree.column('专业', width=110, anchor='center')
        tree.column('专业方向', width=120, anchor='center')
        tree.column('数学', width=85, anchor='center')
        tree.column('英语', width=85, anchor='center')
        tree.column('专业一', width=85, anchor='center')
        tree.column('专业二', width=85, anchor='center')
        tree.grid(row=1, column=0, columnspan=4)
        ybar.grid(row=1, column=4,sticky='ns')

        bx1 = 713
        by1 = 505
        rect2 = round_rectangle(self.c1, bx1, by1, bx1+130, by1+27, radius=20, fill=BTCOLOR)
        reset_btn = tk.Button(self.secondpage, text="返 回 上 一 页", width=15, font=('幼圆',9,'bold'),  relief='flat', bg=BTCOLOR, command=self.toFirstpage)
        reset_btn.place(x=bx1+11,y=by1+5)
        for data in datalist:
            tree.insert('', 'end', values=data)
        
    def toFirstpage(self,):
        self.secondpage.destroy()
        firstpage(self.root)

class FeedbackPage:
    def __init__(self, root) -> None:
        self.root = root
        self.num=0
        global img
        global images
        self.feedbackpage = tk.Frame(self.root,width=WIDTH,height=HEIGHT)
        self.feedbackpage.place(x=0,y=0)
        self.c1 = tk.Canvas(self.feedbackpage, width=WIDTH, height=HEIGHT)
        img = tk.PhotoImage(file='./asset/cat.gif')   
        # tk.Label(self.firstpage, image=img).place(x=100,y=100)  #Label to image
        self.c1.create_image(940,400,image=img)
        rect1 = create_rectangle(self.c1, 80,220,880,550,width=0,fill='black',alpha=0.08)
        self.c1.place(x=0,y=0)
        title = tk.Label(self.feedbackpage, text='2023考研信息查询', font=("黑体",30,"bold"))
        title.place(x=325,y=70)
        mark = tk.Label(self.feedbackpage, text="*本平台信息仅供参考，一切信息请以院校官网及研招网为准！", fg='red', font=("黑体",15))
        mark.place(x=225,y=155)
        

        bx1 = 750; by1 = 430
        round_rectangle(self.c1, bx1,by1,bx1+108,by1+30,radius=20,fill=BTCOLOR)
        enquiry_btn = tk.Button(self.feedbackpage, text="查询反馈进度", width=13, font=("幼圆",9,'bold'),  relief='flat', bg=BTCOLOR, command=self.enquiry)
        enquiry_btn.place(x=bx1+5,y=by1+5)
        
        bx2 = 750; by2 = 470
        round_rectangle(self.c1, bx2,by2,bx2+108,by2+30,radius=20,fill=BTCOLOR)
        admit_btn = tk.Button(self.feedbackpage, text="提交反馈", width=13, font=("幼圆",9,'bold'),  relief='flat', bg=BTCOLOR, command=self.admit)
        admit_btn.place(x=bx2+5,y=by2+5)
        
        bx3 = 750; by3 = 510
        round_rectangle(self.c1, bx3,by3,bx3+108,by3+30,radius=20,fill=BTCOLOR)
        back_btn = tk.Button(self.feedbackpage, text="返回上一页", width=13, font=("幼圆",9,'bold'),  relief='flat', bg=BTCOLOR, command=self.back)
        back_btn.place(x=bx3+5,y=by3+5)
        
        self.form = tk.Frame(self.feedbackpage)
        self.form.place(x=125,y=250)
        self.tree1 = ttk.Treeview(
                                self.form,   
                                height=11,
                                columns=['编 号', '反馈内容','反馈状态','回      复'],  
                                show='headings'
                            )
        style_heading = ttk.Style()
        style_heading.configure("Treeview.Heading", font=('幼圆',11,'bold'), rowheigt=20)
        for x in ['编 号', '反馈内容','反馈状态','回      复']:
            self.tree1.heading(x, text = x, anchor='center')
        self.tree1.column('编 号', width=70, anchor='center')
        self.tree1.column('反馈内容', width=220, anchor='center')
        self.tree1.column('反馈状态', width=80, anchor='center')
        self.tree1.column('回      复', width=220, anchor='center')
        ybar = Scrollbar(self.form, orient='vertical')
        self.tree1.grid(row=1, column=0, columnspan=4)
        ybar.grid(row=1, column=4,sticky='ns')
        self.tree1.bind("<<TreeviewSelect>>", self.getDetails)
        tk.Label(self.feedbackpage, text='*单击条目可打开详情', bg=BGCOLOR).place(x=125,y=505)

    def enquiry(self,):
        global cookie
        user = u.User(cookie)
        datalist = user.enquiryFeedback(s,iftest)
        self.tree1.delete(*(self.tree1).get_children())
        for data in datalist:
            self.tree1.insert('', 'end', values=data)
    
    def getDetails(self, event):
        item = self.tree1.set(self.tree1.focus())
        if item:
            print(item)
            detail_win = tk.Toplevel(self.root)
            detail_win.geometry('275x250')
            # detail_win.resizable(False, False)
            detail_win.title("反馈"+item['编 号'])
            form = tk.Frame(detail_win, width=200, height=200)
            form.pack(anchor='center')
            tk.Label(form, text="反馈内容",font=('幼圆',13,'bold')).grid(row=0,column=0,pady=10,padx=10)
            tk.Message(form, text=item['反馈内容'],bg=BGCOLOR,width=100).grid(row=0,column=1,columnspan=3,pady=10,padx=10)
            tk.Label(form, text="反馈状态",font=('幼圆',13,'bold')).grid(row=1,column=0,pady=10,padx=10)
            tk.Label(form, text=item['反馈状态'],bg=BGCOLOR).grid(row=1,column=1,pady=10,padx=10)
            tk.Label(form, text='回复',font=('幼圆',13,'bold')).grid(row=2,column=0,pady=10,padx=10)
            tk.Message(form, text=item['回      复'],bg=BGCOLOR,width=100).grid(row=2,column=1,columnspan=3,pady=10,padx=10)

    def admit(self,):
        global cookie
        def adm():
            self.num+=1
            contant = self.feedtext.get('1.0','end-1c')
            if len(contant) == 0:
                tk.messagebox.showwarning('Warning','请输入内容！')
            else:
                user = u.User(cookie)
                admit_result = user.admitFeedback(s,contant,iftest)
                if admit_result:
                    tk.messagebox.showinfo('Info','提交成功！')
                else:
                    showwarning(title='Warning', message='提交失败！')

        win_admit=tk.Toplevel(self.root)
        win_admit.geometry('560x300')
        win_admit.resizable(False, False)
        window_form = tk.Frame(win_admit, width=400, height=200)
        window_form.pack()
        tk.Label(window_form,text='请在此处输入反馈内容',font=('幼圆',11,'bold')).grid(row=0,column=0,columnspan=2,pady=10)
        self.feedtext = Text(window_form,height=15,width=70)
        self.feedtext.grid(row=1,column=0,columnspan=70)
        admit_btn = ttk.Button(window_form, text="提交反馈", command=adm)
        admit_btn.grid(row=2,column=69,pady=10,padx=0)

    def back(self,):
        self.feedbackpage.destroy()
        firstpage(self.root)

class AdminPage:
    def __init__(self, root) -> None:
        self.root = root

if __name__ == "__main__":
    checkCookie()
    print("Now Cookie: "+cookie)
    root = tk.Tk()
    main(root)
    root.mainloop()
