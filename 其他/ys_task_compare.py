""""
易识报告差异比较脚本

用于比较不同版本同一固件的cwe/cve等结果差异

相关依赖安装:
  pip install pymongo -i https://mirrors.aliyun.com/pypi/simple

"""
import pymongo

if __name__ == '__main__':
    # 服务器1相关配置
    username1 = 'admin'
    pwd1 = '123456'
    host1 = '103.79.25.186'
    port1 = '37018'
    task_id1 = '1591997845006340096'
    # 服务器2相关配置
    username2 = 'admin'
    pwd2 = '123456'
    host2 = '192.168.1.108'
    port2 = '27018'
    task_id2 = '1592860738589446144'
    client1 = pymongo.MongoClient(
        "mongodb://{}:{}@{}:{}/".format(username1, pwd1, host1, port1),
        maxPoolSize=1024)
    fuzz_db = client1['ys']['finished']  # 连接指定数据库
    data1 = fuzz_db.find_one({'_id': task_id1})['cwe_file']  # cwe_file / cve_file

    client2 = pymongo.MongoClient(
        "mongodb://{}:{}@{}:{}/".format(username2, pwd2, host2, port2),
        maxPoolSize=1024)
    db = client2['ys']['finished']  # 连接指定数据库
    data2 = db.find_one({'_id': task_id2})['cwe_file']  # # cwe_file / cve_file
    print('开始比较服务器1中存在，服务器2中不存在的情况')
    for path1 in data1:
        path2 = path1.replace(task_id1, task_id2)
        if path2 not in data2:
            print(path1)
    print('===========================================================')
    print('')
    print('开始比较服务器2中存在，服务器1中不存在的情况')
    for path2 in data2:
        path1 = path2.replace(task_id2, task_id1)
        if path1 not in data1:
            print(path2)