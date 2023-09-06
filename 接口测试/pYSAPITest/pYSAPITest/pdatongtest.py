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

    def writestr2file(self, fname, data):
        file = open(fname, 'w+', encoding="utf-8")
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
        file.write(msg.encode("utf-8").decode("utf-8") + '\n')
        file.close()

    def login(self, user, password):
        print("login user=" + user + "; password=" + password)
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        httpcode = ""
        code = ""
        body = {
            'username': user,
            'password': password
        }
        try:
            response = requests.post(
                psettings.url + "/api/user/login", headers=psettings.header, data=json.dumps(body))
            httpcode = str(response.status_code)
            data = json.loads(response.text.encode('utf-8'))
            print(data)
            code = data['code']
            if (response.status_code == 200 and data['code'] == 200):
                psettings.header["Authorization"] = "Token " + \
                    data['data']["AuthToken"]
                message = message + "login success! user=%s password=%s Token=%s" % (
                    user, password, psettings.header["Authorization"])
                print(message)
                result = "Success"
                # if (data.get("data").get("AuthToken") is not None):
                #    psettings.token = data['data']["AuthToken"]
                #    print( "AuthToken: " + psettings.token )
            else:
                message = "Code=%s Message=%s" % (
                    data['code'], data['message'])
                result = "Failed"
        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("login error, exception:" + message)
            result = "Failed"
        self.writereport(putil.get_datetimestring() + "; Login; " + result + "; " + httpcode +
                         "; " + str(code) + "; user=%s, password=%s" % (user, password) + "; " + message)
        return result

    def logout(self):
        print("logout...")
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        httpcode = ""
        code = ""

        #psettings.header["Authorization"] = "Token " + psettings.token
        print("Token=" + psettings.header["Authorization"])
        try:
            response = requests.post(
                psettings.url + "/api/user/logout", headers=psettings.header)
            httpcode = str(response.status_code)
            data = json.loads(response.text.encode('utf-8'))
            print(data)
            code = data['code']
            if (response.status_code == 200 and data['code'] == 200):
                message = message + \
                    "logout success! user=%s password=%s" % (
                        psettings.user, psettings.password)
                result = "Success"
            else:
                message = "Code=%s Message=%s" % (
                    data['code'], data['message'])
                result = "Failed"

        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("logout error, exception:" + message)
            result = "Failed"
        self.writereport(putil.get_datetimestring() + "; Logout; " +
                         result + "; " + httpcode + "; " + str(code) + ";  ; " + message)

    def deletefw(self, tasklist=[]):
        print("logout...")
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        code = ""
        httpcode = ""
        print(tasklist)
        if(len(tasklist) > 0):
            if(len(tasklist[0]) > 0):
                tasklist = tasklist[0]
        print("Token=" + psettings.header["Authorization"])
        payload = {
            'taskIdList': tasklist
        }
        print(json.dumps(payload))
        psettings.header['Content-type'] = 'application/json'
        try:
            response = requests.delete(
                psettings.url + "/api/task/delete", headers=psettings.header, data=json.dumps(payload))
            httpcode = str(response.status_code)
            data = json.loads(response.text.encode('utf-8'))
            code = data['code']
            print(data)
            if (response.status_code == 200 and data['code'] == 200):
                message = message + \
                    "delete task success! tasklist=%s" % (str(tasklist))
                print(message)
                result = "Success"
            else:
                message = "Code=%s Message=%s" % (
                    data['code'], data['message'])
                result = "Failed"

        except Exception as e:
            result = "Failed"
            message = repr(e)
            print("Exception:" + message)
            self.writelog("logout error, exception:" + message)
        self.writereport(putil.get_datetimestring() + "; Delete FW; " + result + "; " +
                         httpcode + "; " + str(code) + "; tasklist=%s; " % (str(tasklist)) + message)
        return result

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
        code = ""
        httpcode = ""
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
            httpcode = str(response.status_code)
            # print(response.text.encode('utf-8'))
            data = json.loads(response.text.encode('utf-8'))
            code = data['code']
            #print(data, sep = "\n")
            if (response.status_code == 200 and data['code'] == 200):
                result = "Success"
                datalist = data.get('data').get('dataList')
                message = message + \
                    "get task list success! task list size=%d" % (
                        len(datalist))
            else:
                message = "Code=%s Message=%s" % (
                    data['code'], data['message'])
                result = "Failed"

        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("get task list error, exception:" + message)

        self.writereport(putil.get_datetimestring() + "; Get Task List; " + result + "; " + httpcode + "; " + str(code) +
                         "; page=%d limit=%d keywords=%s sortby=%d taskstatus=%d; " % (page, limit, keywords, sortby, taskstatus) + message)
        return result, datalist

    def createtask(self, filename, taskname, startnow, plugin, firmware, devicename, devicepart, deviceclass, version, vendor):
        print("create task...")
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        code = ""
        httpcode = ""
        #psettings.header["Authorization"] = "Token " + psettings.token
        print("Token=" + psettings.header["Authorization"])
        multipart_encoder = MultipartEncoder(
            fields={
                "taskName": taskname,
                "startNow": str(startnow),
                "plugin": plugin,
                'firmware': (filename, firmware, 'application/octet-stream'),
                'device_name': devicename,
                'device_part': devicepart,
                'device_class': deviceclass,
                'version': version,
                'vendor': vendor
            },
            boundary='-----------------------------2385610611750'
        )

        psettings.header['Content-type'] = multipart_encoder.content_type

        #print (multipart_encoder)
        try:
            response = requests.post(
                psettings.url + "/api/task/create", headers=psettings.header, data=multipart_encoder)
            httpcode = str(response.status_code)
            # print(response.text.encode('utf-8'))
            data = json.loads(response.text.encode('utf-8'))
            code = data['code']
            print(data)
            if (response.status_code == 200 and data['code'] == 200):
                message = message + "create task success!"
                result = "Success"
            else:
                message = "Code=%s Message=%s" % (
                    data['code'], data['message'])
                result = "Failed"

        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("create task error, exception:" + message)
        self.writereport(putil.get_datetimestring() + "; Create Task; " + result + "; " + httpcode + "; " + str(code) +
                         "; filename=%s taskname=%s plugin=%s devicename=%s devicepart=%s deviceclass=%s version=%s vendor=%s; " % (filename, taskname, plugin, devicename, devicepart, deviceclass, version, vendor) + message)
        return result

    def findouttasks(self, page, limit, keywords, sortby, taskstatus, taskname):
        #taskidlist = list(range(0))
        taskidlist = []
        message = ""
        count = 0

        result, datalist = self.gettasklist(
            page, limit, keywords, sortby, taskstatus)
        print("FW list size=" + str(len(datalist)))
        if(result == "Failed"):
            message = "Failed to find out task"
            return "Failed", taskidlist
        for item in datalist:
            #print( "id=" + str(item['id']) + ", task_name=" + item["task_name"] + ", file_name=" + item["file_name"] + ", device_name = " + item["device_name"] + ", device_part=" + item["device_part"] )
            if(item["task_name"] == taskname or len(taskname) == 0):
                count = count + 1
                idlist = [1]
                idlist[0] = item['id']
                message = "found out task, taskid = %d" % item['id']
                print(message)
                taskidlist.extend(idlist)
                #taskidlist.insert(len(taskidlist), item['id'])

        message = "found %d taskid by taskname" % count + \
            "task id list = " + ", ".join(str(i) for i in taskidlist)
        self.writereport(putil.get_datetimestring() + "; Findout FW; " +
                         result + "; ; ; taskname=%s ; " % (taskname) + message)
        return result, taskidlist

    def getpdftaskresult(self, taskid, pdffilename):
        message = ""
        timer = putil.Timer()
        result = "Failed"
        reportmessage = ""
        code = ""
        httpcode = ""
        #psettings.header["Authorization"] = "Token " + psettings.token
        print("开始下载报告[taskID=%d]..." % taskid)
        print("Token=" + psettings.header["Authorization"])
        psettings.header['Content-type'] = 'application/json'
        data = {
            "taskId": taskid
        }
        try:
            response = requests.post(
                psettings.url + "/api/task/getPDF", headers=psettings.header, data=json.dumps(data))
            httpcode = str(response.status_code)
            if (httpcode == '200'):
                self.writebytesfile(
                    pdffilename, response.content)
                message = message + "Get report success!"
                print(message)
                result = "Success"
            else:
                message = "Error, Get report failed, Code=" + httpcode
                print(message)
                result = "Failed"

        except Exception as e:
            message = repr(e)
            print("Exception:" + message)
            self.writelog("Get report error, exception:" + message)
        self.writereport(putil.get_datetimestring(
        ) + "; Get report; " + result + "; " + httpcode + "; ;" + message)
        return 0

    def analyzing(self):
        taskidlist = []
        message = ""
        result, datalist = self.gettasklist(1, 1000, "", 0, 3)
        print("current FW list size=" + str(len(datalist)))
        if(result == "Failed" or len(datalist) < 1):
            message = "Failed to find out task"
            return False
        # for item in datalist:
        #    print( "id=" + str(item['id'])  + ", task_status=" + str(item['task_status']) + ", process="  + str(item['process']) + "uuid=" + str(item['uuid']) + ", task_name=" + item["task_name"] + ", file_name=" + item["file_name"] + ", device_name = " + item["device_name"] + ", device_part=" + item["device_part"] )
        for item in datalist:
            #print( "id=" + str(item['id']) + ", task_name=" + item["task_name"] + ", task_status=" + item['task_status'] + ", process="  + str(item['process']) + ", file_name=" + item["file_name"] + ", device_name = " + item["device_name"] + ", device_part=" + item["device_part"] )
            if(item["process"] < 1 and item['task_status'] != 0):
                idlist = [1]
                idlist[0] = item['id']
                message = "taskid = %d is on analyzing" % item['id']
                print(message)
                taskidlist.extend(idlist)
        if(len(taskidlist) > 0):
            message = "%d tasks is on analyzing" % (
                len(taskidlist)) + "task id list = " + ", ".join(str(i) for i in taskidlist)
            self.writereport(putil.get_datetimestring(
            ) + "; on analyzing; " + "Yes" + "; ; ; taskname=%s ; " + message)
            return True
        else:
            message = "all anaylsis are completed!"
            self.writereport(putil.get_datetimestring(
            ) + "; on analyzing; " + "No" + "; ; ; taskname=%s ; " + message)
            return False

    def checkalive(self, timeout):
        timer = putil.Timer()
        print("just check service is alive...")
        result = self.login(psettings.user, psettings.password)
        if(result == "Failed"):
            return
        while timer.is_timeupminutes(timeout) == False:
            time.sleep(30)
            result = self.gettasklist(1, 100, "", 0, 3)
            # if(result == "Failed"):
            #    return

        result = self.logout()
        # if(result == "Failed"):
        #    return

    def checkalive2(self, timeout):
        timer = putil.Timer()
        prefixname = "task#"
        vendor = "Tesla-model#"
        i = 0
        ifile = 0
        subfolders, files = putil.run_fast_scandir(
            r'D:\Share\FW Samples', [], [".txt", ".html", ".xlsx", ".pdf"])
        print("just check service is alive...")
        result = self.login(psettings.user, psettings.password)
        if(result == "Failed"):
            return
        while timer.is_timeupminutes(timeout) == False:

            if(self.analyzing() == False):
                print("no tasks are on anaylsis, let's send a new task")
                firmware = self.readbytesfile(files[ifile])
                plugin = '["binwalk", "crypto_hints", "cwe_checker", "file_type", "software_components", "users_and_passwords", "cpu_architecture", "cve_lookup", "elf_analysis", "ip_and_uri_finder", "file_hashes"]'
                self.createtask(files[ifile], prefixname + "%00d" % (i), 1, plugin,
                                firmware, "device name", "kernel", "cls", "1", vendor + str(i))
                i = i + 1
                ifile = ifile + 1
                if (ifile >= len(files)+1):
                    ifile = 0
            else:
                print("tasks are on anaylsis")
            time.sleep(10)
            # if(result == "Failed"):
            #    return

        result = self.logout()
        # if(result == "Failed"):
        #    return

    def run(self):
        print("start to run...")
        self.login(psettings.user, psettings.password)
        time.sleep(1)

        # self.analyzing()

        #firmware = self.readbytesfile(psettings.fwname)
        plugin = '["binwalk", "crypto_hints", "cwe_checker", "file_type", "software_components", "users_and_passwords", "cpu_architecture", "cve_lookup", "elf_analysis", "ip_and_uri_finder", "file_hashes" ]'
        #plugin = '["binwalk", "crypto_hints"]'
        #self.createtask(psettings.fwname, "大通检测任务", plugin, firmware, "ニッサン日产", "complete", "Cäsar(ÄäÖößÜü)", "1", "三星삼성")
        #self.createtask(psettings.fwname, " _13_ ", 1, plugin, firmware, "device name", "complete", "cls", "1", "BYS")

        # self.deletefw([66])

        #result, taskidlist = self.findouttaskid(1, 100, "", 0, 3, "task001")
        #print("return taskidlist=" + ", ".join(str(i) for i in taskidlist) )
        result = self.getpdftaskresult(
            11, r"D:\SourceCode\pcode\pYSAPITest\report.pdf")

        #result, taskidlist = self.findouttasks(1, 1000, "", 0, 3, "")
        # print("list string =" + taskidlist)ls

        # self.deletefw([taskidlist])

        #result, datalist = self.gettasklist(1, 1000, "task", 0, 3)

        self.logout()


test = TestAPI()


test.run()
