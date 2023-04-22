

import pandas as pd
from socket import *
import os

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
            city_ = 'NULL'
        if college_=='' or college_=='--请输入--':
            college_ = 'NULL'
        if major_=='--请选择--':
            major_ = 'NULL'
        if search_=='--请选择--' or search_ == '':
            search_ = 'NULL'
        return self.cookie+'_search_'+city_+'_'+college_+'_'+major_+'_'+search_
    
    '''
    input: socket，查询请求语句，如果是正式运行修改iftest为False
    output: 已解码的查询结果(search result list)
    function: 发送查询请求并解码查询结果
    '''
    def sendSearchRequest(self, s, search_request, iftest, test_search_result = ["AAA-BBB-DDD-数一-英一-政治-专业课一_AAA-CCC-EEE-数一-英一-政治-专业课二"]):
        if not iftest:
            s.send(search_request.encode('utf-8'))
            datalist = []
            while True:
                data = s.recv(1024)     # get data
                if data.decode('utf-8') == 'end':
                    break
                else:
                    datalist.append(data.decode('utf-8'))
        else:
            datalist = test_search_result
        decode_datalist = self.decodedata(datalist)
        print(decode_datalist)
        final_datalist = []
        for data in decode_datalist:
            # print(data)
            data_piece = data.split('-')
            # print(data_piece)
            final_datalist.append(data_piece)
        return final_datalist

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
            s.send(feedback_request.encode('utf-8'))
            getresult = s.recv(1024)
            if getresult.decode('utf-8') == '000':
                result = False
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
            s.send(enquiry_request.encode('utf-8'))
            datalist = []
            while True:
                data = s.recv(1024)     # get data
                if data.decode('utf-8') == 'end':
                    break
                else:
                    datalist.append(data.decode('utf-8'))
        else:
            datalist = test_search_result
        decode_datalist = self.decodedata(datalist)
        print(decode_datalist)
        final_datalist = []
        for data in decode_datalist:
            # print(data)
            data_piece = data.split('-')
            # print(data_piece)
            data_piece.insert(0,len(final_datalist)+1)
            if data_piece[3] == "NULL":
                data_piece[3] = "还没有回复QAQ"
            final_datalist.append(data_piece)
        return final_datalist


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
            s.send(login_request.encode('utf-8'))
            res = s.recv(1024).decode('utf-8')
            if res == '211':
                issucess = False
        return issucess

if __name__ == "__main__":
    cookie = '1'
    user = User(cookie)
    datalist = ["AAA-BBB-数一-英一-政治-专业课一_AAA-CCC-数一-英一-政治-专业课二"]
    # dl = user.sendSearchRequest(socket(),'test')
    dl = user.enquiryFeedback(socket())
    print(dl)