

import pandas as pd
from socket import *
import os
import json

def string_to_list(str):
    list1=str.split("#")
    list=[]
    for li in list1:
        if li!="end":

            list.append(li.split('@'))
        else:
            list.append(li)
    return list

client_type = 'linxinfa'


def send_data(s, cmd, **kv):
    global client_type
    jd = {}
    jd['COMMAND'] = cmd
    jd['client_type'] = client_type
    jd['data'] = kv
    jsonstr = json.dumps(jd)
    #print('send: ' + jsonstr)
    s.sendall(jsonstr.encode('utf8'))

def get_message(s,cmd):
    send_data(s, 'SEND_DATA', data=cmd)
    li = []
    while True:
        try:
            string = s.recv(1024000).decode('utf-8')
        except:
            continue
        print(string)
        if string!= 'end':
            li += string_to_list(string)
        else:
            if string=="end":
                li.append(['end'])
            else:
                li += string_to_list(string[:-3])
                li.append(['end'])
            break
    return li


class User:
    def __init__(self, cookie) -> None:
        self.cookie = cookie

    '''
    input: 省市、院校、专业、方向
    output: 编码后的查询请求
    function: 将用户输入的查询条件转换为查询请求
    '''
    def ClientRequestSearch(self,city_,college_,major_,search_):
        if city_=='--请选择--':
            city_ = ''
        if college_=='' or college_=='--请输入--':
            college_ = ''
        if major_=='--请选择--':
            major_ = ''
        if search_=='--请选择--' or search_ == '':
            search_ = ''
        return self.cookie+'_search_'+city_[1:3]+'_'+college_+'_'+major_[1:5]+'_'+search_
    
    '''
    input: socket，查询请求语句，如果是正式运行修改iftest为False
    output: 已解码的查询结果(search result list)
    function: 发送查询请求并解码查询结果
    '''
    def sendSearchRequest(self, s, search_request, iftest, test_search_result = ["AAA-BBB-DDD-数一-英一-政治-专业课一_AAA-CCC-EEE-数一-英一-政治-专业课二"]):
        if not iftest:
            '''s.send(search_request.encode('utf-8'))
            datalist = []
            while True:
                data = s.recv(1024)     # get data
                if data.decode('utf-8') == 'end':
                    break
                else:
                    datalist.append(data.decode('utf-8'))'''
            print(search_request)
            datalist=get_message(s,search_request)
        else:
            datalist = test_search_result
        '''decode_datalist = self.decodedata(datalist)
        final_datalist = []
        for data in decode_datalist:
            # print(data)
            data_piece = data.split('-')
            # print(data_piece)
            final_datalist.append(data_piece)'''
        return datalist[:-2]

    '''
    input: 接收到的未解码的查询结果["AAA-BBB-数一-英一-政治-专业课一_AAA-CCC-数一-英一-政治-专业课二"]
    output: 解码后的查询结果(list)['AAA-BBB-数一-英一-政治-专业课一', 'AAA-CCC-数一-英一-政治-专业课二']
    function: 对从服务器发来的查询结果进行解码（拆分_）
    '''
    def decodedata(self, datalist):
        templist = []
        for item in datalist:
            templist += item.split('_')
        return templist
    
    '''
    input: socket，反馈内容
    output: 反馈结果(True/False)
    function: 提交反馈内容
    '''
    def admitFeedback(self, s, feedback_text, iftest=True):
        feedback_request = self.cookie+'_feedback_'+feedback_text
        print('Request: '+feedback_request)
        result = True
        if not iftest:
            datalist = get_message(s, feedback_request)
            
        return result
    
    '''
    input: socket
    output: [[1, '11111', '已接收', 'NULL'], [2, '22222', '已处理', '333']]
    function: 发送查询请求，返回反馈信息列表，解码并编号
    '''
    def enquiryFeedback(self, s, iftest=True, test_search_result=["11111111111111111111111111111111111-已接收-NULL_22222-已处理-333"]):
        enquiry_request = self.cookie+'_fsearch'
        print("Request: "+enquiry_request)
        if not iftest:
            '''s.send(enquiry_request.encode('utf-8'))
            datalist = []
            while True:
                data = s.recv(1024)     # get data
                if data.decode('utf-8') == 'end':
                    break
                else:
                    datalist.append(data.decode('utf-8'))'''
            datalist = get_message(s, enquiry_request)
        else:
            datalist = test_search_result
        '''decode_datalist = self.decodedata(datalist)
        print(decode_datalist)
        final_datalist = []
        for data in decode_datalist:
            # print(data)
            data_piece = data.split('-')
            # print(data_piece)
            data_piece.insert(0,len(final_datalist)+1)
            if data_piece[3] == "NULL":
                data_piece[3] = "还没有回复QAQ"
            final_datalist.append(data_piece)'''
        return datalist[:-1]


class Admin:
    def __init__(self) -> None:
        pass

    '''
    input: socke，name，passw
    output: 是否登录成功(True/False)
    function: 管理员登录
    '''
    def login(self, s, name, password, iftest=True):
        if name == '':
            name = "NULL"
        if password == '':
            password = "NULL"
        login_request = "admin_login_"+name+"_"+password
        print("Request: "+login_request)
        issucess = True
        if not iftest:
            #s.send(login_request.encode('utf-8'))
            res = get_message(s, login_request)
            if res[0][0] == '211':
                issucess = False
        return issucess
    
    def decode(self, data):
        datalist = data.split('_')
        return datalist

    '''
    input: socket
    output: 数据库信息['123456', '2000', '2023.04.15 20:38']
    function: 获得数据库信息
    '''
    def monitor(self, s, iftest=True, testdata='123456_2000_2023.04.15 20:38'):
        monitor_request = 'admin_monitor'
        print("Request: "+monitor_request)
        if not iftest:
            s.send(monitor_request.encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
        else:
            data = testdata
        data_final = self.decode(data)
        return data_final
    
    '''
    input: socket
    output: 反馈列表[['1', '1', '反馈内容', '已处理', '回复内容'], ['2', '2反馈内容', '已接收', '']]
    function: 获取全部反馈信息
    '''
    def getFeedbackList(self, s, iftest=True, testdata=['1-1-反馈内容-已处理-回复内容_2-2反馈内容-已接收-']):
        feedbacklist_request = 'admin_feedbacklist'
        print("Request: "+feedbacklist_request)
        if not iftest:
            #s.send(feedbacklist_request.encode('utf-8'))
            datalist = get_message(s, feedbacklist_request)
            '''while True:
                data = s.recv(1024)     # get data
                if data.decode('utf-8') == 'end':
                    break
                else:
                    datalist.append(data.decode('utf-8'))'''
        else:
            datalist = testdata
        '''data_final = []
        for data in datalist:
            datapiecelist = data.split('_')
            for datapiece in datapiecelist:
                data_final.append(datapiece.split('-'))'''
        return datalist[:-1]
    
    '''
    input: socke，反馈信息ID，回复内容
    output: 回复是否成功(True/False)
    function: 提交回复
    '''
    def commitRespond(self, s, feedback_id, respond, iftest=True):
        commit_request = "admin_reply_"+feedback_id+"_"+respond
        print("Request: "+commit_request)
        result = True
        if not iftest:
            data = get_message(s, commit_request)
            if data[0][0] == '311':
                result = False
        return result

if __name__ == "__main__":
    cookie = '1'
    user = User(cookie)
    admin = Admin()
    datalist = ["AAA-BBB-数一-英一-政治-专业课一_AAA-CCC-数一-英一-政治-专业课二"]
    # dl = user.sendSearchRequest(socket(),'test')
    # dl = user.enquiryFeedback(socket())
    # dl = admin.monitor(s=socket())
    dl = admin.getFeedbackList(socket())
    print(dl)