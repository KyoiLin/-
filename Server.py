# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
#import pymysql
import pandas as pd
import csv
import socket  # 导入 socket 模块
from threading import Thread
import time
import json
import pymysql
# 创建数据库连接
def Connect():
    conn = pymysql.connect(
    host = '127.0.0.1', # 连接主机, 默认127.0.0.1
    user = 'root',      # 用户名
    passwd = 'zhao011119liang',# 密码
    port = 3306,        # 端口，默认为3306
    db = 'data',        # 数据库名称
    charset = 'utf8'    # 字符编码
    )
    return conn


#cursor = conn.cursor()
#  创建数据表的sql 语句  并设置name_id 为主键自增长不为空
# sql_createTb = """CREATE TABLE MONEY (name_id INT NOT NULL AUTO_INCREMENT,LAST_NAME  CHAR(20),AGE INT,SEX CHAR(1),PRIMARY KEY(name_id))"""
# # 插入一条数据到moneytb 里面。
# sql_insert = "insert into money(LAST_NAME,AGE,SEX) values('de2',18,'0')"
# cursor.execute(sql_createTb)
# cursor.execute(sql_insert)
# sql="SELECT * FROM MONEY"
# cursor.execute(sql)
# results = cursor.fetchall()
# print(cursor.rowcount)
# conn.commit()



# cursor = conn.cursor()
# Data=pd.read_csv("output.csv",engine='python',encoding='gbk')
# Data=Data.astype(str)
# Data=Data.apply(lambda x: tuple(x), axis=1).values.tolist()
# # t=type(Data[2])
# # print(t)
# # sql_createTb = """CREATE TABLE AllData (key_id INT NOT NULL AUTO_INCREMENT,城市 VARCHAR(500),学校 VARCHAR(500),研究生院 VARCHAR(500),自主划线 VARCHAR(500),博士点 VARCHAR(500),考试方式 VARCHAR(500),院系所 VARCHAR(500),专业 VARCHAR(500),研究方向 VARCHAR(500),拟招人数 VARCHAR(500),政治 VARCHAR(500),英语 VARCHAR(500),业务课一 VARCHAR(500),业务课二 VARCHAR(500),PRIMARY KEY(key_id))"""
# # cursor.execute(sql_createTb)
# # print(cursor.rowcount)
# sql_insert = "INSERT INTO `AllData`(`城市`,`学校`,`研究生院`,`自主划线`,`博士点`,`考试方式`,`院系所`,`专业`,`研究方向`,`拟招人数`,`政治`,`英语`,`业务课一`,`业务课二`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# cursor.executemany(sql_insert, Data)
# conn.commit()
# conn.close()

def Feedback_Insert(Cookie_id,Feedback_id,Feedback_Text="''",Status='0',Reply="''"):
    conn=Connect()
    cursor = conn.cursor()
    sql_insert = "INSERT INTO `Feedback`(`cookie_id`,`反馈信息ID`,`反馈内容`,`状态`,`回复`) VALUES({},{},{},{},{})".format(Cookie_id,Feedback_id,Feedback_Text,Status,Reply)
    cursor.execute(sql_insert)
    conn.commit()
    conn.close()

def Feedback_Search(Cookie_id):
    conn = Connect()
    cursor = conn.cursor()
    sql_search = "SELECT * FROM `Feedback` WHERE 1=1"
    if Cookie_id:
        sql_search += " AND `Cookie_id` = {}".format(Cookie_id)
    cursor.execute(sql_search)
    result = cursor.fetchall()
    return result

def Feedback_Change(Feedback_id,Status='1',Reply=None):
    conn = Connect()
    cursor = conn.cursor()
    sql_updata="UPDATE `Feedback` SET `状态`='{}',`回复`='{}' WHERE `反馈信息ID`={}".format(Status,Reply,Feedback_id)
    cursor.execute(sql_updata)
    conn.commit()
    return ['1']
def Feedback_View():
    conn = Connect()
    cursor = conn.cursor()
    sql_search = "SELECT * FROM `Feedback`"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    return result
def Feedback_Backup():
    conn = Connect()
    cursor = conn.cursor()
    sql_search = "SELECT * FROM `Feedback`"
    cursor.execute(sql_search)
    results = cursor.fetchall()
    with open('backup_Feedback.csv', 'w', newline='') as csvfile:
        # 创建CSV写入器
        writer = csv.writer(csvfile)

        # 写入表头
        writer.writerow([i[0] for i in cursor.description])

        # 写入数据
        for row in results:
            writer.writerow(row)
def Feedback_ViewLine():
    conn = Connect()
    cursor = conn.cursor()
    sql_search = "SELECT COUNT(*) FROM `Feedback`"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    return result[0][0]

def Search(Pos=None,Name=None,Category=None,Profession=None):
    conn = Connect()
    cursor = conn.cursor()
    sql_search="SELECT * FROM `AllData` WHERE 1=1"
    if Pos:
        sql_search +=" AND SUBSTRING(`城市`, 2, 2) = {}".format(Pos)

    if Name:
        sql_search +=" AND SUBSTRING(`学校`, 8) = {}".format(Name)

    if Category:
        sql_search +=" AND SUBSTRING(`专业`, 2, 4) = {}".format(Category)

    if Profession:
        sql_search += " AND `专业` LIKE '%{}%'".format(Profession)

    cursor.execute(sql_search)
    result=cursor.fetchall()
    return result

def ViewAllData():
    conn = Connect()
    cursor = conn.cursor()
    sql_search = "SELECT COUNT(*) FROM `AllData`"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    return result
def BackupAllData():
    conn = Connect()
    cursor = conn.cursor()
    sql_search = "SELECT * FROM `AllData`"
    cursor.execute(sql_search)
    results = cursor.fetchall()
    with open('backup_AllData.csv', 'w', newline='') as csvfile:
        # 创建CSV写入器
        writer = csv.writer(csvfile)

        # 写入表头
        writer.writerow([i[0] for i in cursor.description])

        # 写入数据
        for row in results:
            writer.writerow(row)


admin_account={"admin":"admin"}

ADDRESS = ('', 8712)  # 绑定地址

g_socket_server = None  # 负责监听的socket

g_conn_pool = {}  # 连接池

all_cookid=[]
cookID_NUM=10000
FeedBack_id=Feedback_ViewLine()+1

test=[['a','a','4','5'],["a","a",'5','5','5'],['5','5','5']]

def turpe_turpe_to_list(turpe):
    List=[]
    for tur in turpe:
        List.append(list(tur))
    return List

def process_campus(str):
    for i in range(len(str)):
        swap = []
        swap.append(str[i][2][7:])
        swap.append(str[i][8][8:])
        swap.append(str[i][9][4:])
        for j in range(11, 15):
            str[i][j]=str[i][j].replace(' ', '')
            str[i][j]=str[i][j].replace('\n', '')
            str[i][j]=str[i][j].replace('\r', '')
            swap.append(str[i][j][5:])
        str[i]=swap
    return str

def to(string):
    return "'"+string+"'"

def process_cookid(input):
    input=input['data']
    input=input.split("_")
    print(input)
    str=[]
    #print(str)
    if input[0]!='admin':
        if input[1]=="feedback":
            global FeedBack_id
            print("instrt")
            print(to(input[0]))
            feedbackid="{}".format(FeedBack_id)
            print(feedbackid)
            print(to(input[0]),to(feedbackid),to(input[2]))
            Feedback_Insert(to(input[0]),Feedback_id=to(feedbackid),Feedback_Text=to(input[2]))
            print("success")
            FeedBack_id+=1
            str=[["100"]]
        elif input[1]=='search':
            str=Search(Pos=input[2],Name=to(input[3]),Category=input[4],Profession=input[5])
            str=turpe_turpe_to_list(str)
            t=process_campus(str.copy())
            return t
        elif input[1]=='fsearch':
            str=Feedback_Search(input[0])
            print(str)
            str=turpe_turpe_to_list(str)
    else:
        if input[1]=='monitor':
            print("monitor")
            str=ViewAllData()
            #print(str)
            str=turpe_turpe_to_list(str)
            t = process_campus(str.copy())
            return t
        elif input[1]=='feedbacklist':
            str=Feedback_View()
            str=turpe_turpe_to_list(str)
        elif input[1]=='reply':
            Feedback_Change(Feedback_id=input[2],Reply=input[3])
            str=[["300"]]
        elif input[1]=='backup':
            if input[2]=='1':
                BackupAllData()
            elif input[2]=='2':
                Feedback_Backup()
            else:
                Feedback_Backup()
                BackupAllData()
            str=[['400']]
        elif input[1]=='login':
            if input[2] in admin_account.keys() and admin_account[input[2]]==input[3]:
                str=[['200']]
            else:
                str=[['211']]

    return str
   

def list_to_string(List):
    List1=[]
    for li in List:
        List1.append('@'.join(li))
    List1.append("end")
    return "#".join(List1)

def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(50)
    print("server start，wait for client connecting...")


def accept_client():
    """
    接收新连接
    """
    while True:
        client, info = g_socket_server.accept()  # 阻塞，等待客户端连接
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client, info))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()


def message_handle(client, info):
    """
    消息处理
    """
    #stri="success connect!!"
    #client.sendall(stri.encode('utf-8'))
    while True:
        try:
            bytes = client.recv(1024)
            msg = bytes.decode(encoding='utf8')
            jd = json.loads(msg)
            cmd = jd['COMMAND']
            client_type = jd['client_type']
            if 'CONNECT' == cmd:
                g_conn_pool[client_type] = client
                print('on client connect: ' + client_type, info)
                cookid=jd['data']['data']
                if len(cookid)==0:
                    global cookID_NUM
                    from builtins import str
                    cookid=str(cookID_NUM)
                    cookID_NUM+=1
                    all_cookid.append(cookid)
                    client.sendall(cookid.encode('utf-8'))
            elif 'SEND_DATA' == cmd:
                print('recv client msg: ' + client_type+" "+jd['data']['data'])
                str = process_cookid(jd['data'])
                print(2)
                message = ""
                print(len(str))
                for i in str:
                    print(i)
                    i = "@".join(i)
                    if len(message.encode('utf-8')) + len(i.encode('utf-8')) > 1024000:
                        client.sendall(message.encode('utf-8'))
                        time.sleep(0.01)
                        message = i
                    else:
                        if len(message) == 0:
                            message = i
                        else:
                            message += "#" + i
                client.sendall(message.encode('utf-8'))
                time.sleep(0.01)
                client.sendall("end".encode('utf-8'))


        except Exception as e:
            print(e)
            remove_client(client_type)
            break

def remove_client(client_type):
    client = g_conn_pool[client_type]
    if None != client:
        client.close()
        g_conn_pool.pop(client_type)
        print("client offline: " + client_type)


if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    thread.join()



#result=Search("'11'",Category="'0101'",Profession="伦理")
#BackupAllData()