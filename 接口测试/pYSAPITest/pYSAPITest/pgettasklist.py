from selenium import webdriver
import json
import urllib
import requests
import base64
import threading
import time
import putil
import psettings
from requests_toolbelt import MultipartEncoder
from selenium import webdriver
import json
import urllib
import requests
import base64
import threading
import time
import putil
import psettings
from requests_toolbelt import MultipartEncoder


class TestAPI(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def readbytesfile(self, filename):
        file = open(filename, 'rb')
        fwdata = file.read()
        file.close()
        return fwdata

    def writebytesfile(self, fname, data):
        file = open(fname, 'wb+')
        file.write(data)
        file.close()

    def writelog(self, log):
        file = open(psettings.logfilename, 'a+')
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S     ", timeArray)
        # print(otherStyleTime)
        file.write(otherStyleTime + log + '\n')
        file.close()

    def writereport(self, msg):
        file = open(psettings.reportfilename, 'a+')
        file.write(msg + '\n')
        file.close()

    def login(self, user, password):
        print("login user=" + user + "; password=" + password)
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        statuscode = ""
        body = {
            'username': user,
            'password': password
        }
        try:
            response = requests.post(
                psettings.url + "/api/user/login", headers=psettings.header, data=json.dumps(body))
            print(response.text.encode('utf-8'))
            data = json.loads(response.text.encode('utf-8'))
            if (response.status_code == 200 and data['code'] == 200):
                psettings.header["Authorization"] = "Token " + \
                    data['data']["AuthToken"]
                message = message + "login success! uer=%s, password=%s, Token=%s" % (
                    user, password, psettings.header["Authorization"])
                print(message)
                result = "Success"
                # if (data.get("data").get("AuthToken") is not None):
                #    psettings.token = data['data']["AuthToken"]
                #    print( "AuthToken: " + psettings.token )
            else:
                message = response.text
                result = "Failed"
        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("login error, exception:" + message)

    def logout(self):
        print("logout...")
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        statuscode = ""

        #psettings.header["Authorization"] = "Token " + psettings.token
        print("Token=" + psettings.header["Authorization"])
        try:
            response = requests.post(
                psettings.url + "/api/user/logout", headers=psettings.header)
            print(response.text.encode('utf-8'))
            data = json.loads(response.text.encode('utf-8'))
            if (response.status_code == 200 and data['code'] == 200):
                message = message + \
                    "logout success! uer=%s; password=%s" % (
                        psettings.user, psettings.password)
                result = "Success"
            else:
                message = response.text
                result = "Failed"

        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("logout error, exception:" + message)

    # page:int 页面索引 默认1
    # limit:int 单页个数 默认10
    # keywords:string 搜索字符串
    # sortBy:int 排序方式 0-降序、1-升序 默认0
    # taskStatus:int # 扫描任务状态：0-空挡、1-进行、2-完成、 3-表示不筛选
    def gettasklist(self, page, limit, keywords, sortby, taskstatus):
        print("get task list...")
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        statuscode = ""
        datalist = []

        #psettings.header["Authorization"] = "Token " + psettings.token
        print("Token=" + psettings.header["Authorization"])
        para = {
            'page': str(page),
            'limit': str(limit),
            'keywords': keywords,
            'sortBy': str(sortby),
            'taskStatus': str(taskstatus)
        }
        try:
            response = requests.get(
                psettings.url + "/api/task/list", headers=psettings.header, params=para)
            # print(response.text.encode('utf-8'))
            data = json.loads(response.text.encode('utf-8'))
            #print(data, sep = "\n")
            if (response.status_code == 200 and data['code'] == 200):
                message = message + \
                    "get task list success! uer=%s; password=%s" % (
                        psettings.user, psettings.password)
                result = "Success"
                datalist = data.get('data').get('dataList')
            else:
                message = response.text
                result = "Failed"
            return result, datalist

        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("get task list error, exception:" + message)
            return "Failed", datalist

    def run(self):
        print("start to run...")
        self.login(psettings.user, psettings.password)
        time.sleep(3)

        result = self.gettasklist(1, 100, "", 0, 3)

        # self.logout()

        #uid = self.putonefwandcheck(r'D:\Share\test\app.bin')
        # return
test = TestAPI()

test.run()
