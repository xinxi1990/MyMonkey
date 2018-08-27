# coding=utf-8
import os
import sys
import time
import logger
from flask import Flask, request
from flask import render_template
import requests
from threading import Thread
from DateBean import DateBean

rootpath = str(sys.argv[0]).split('/')
lists = list(rootpath)
del lists[-1]
newpath = '/'.join(lists)
os.chdir(newpath)
print '当前文件路径:'+os.getcwd()


mempath = os.getcwd() + '/' + DateBean().mempath
cpupath = os.getcwd() + '/' + DateBean().cpupath
networkpath = os.getcwd() + '/' + DateBean().networkpath
fpspath = os.getcwd() + '/' + DateBean().fpspath
# memer/cpu/network/fps文件路径

htmlpath = os.getcwd() + '/ReportServer/performanceReport/performance_%s.html' % time.strftime("%Y%m%d%H%M%S")
# html报告地址

host = '0.0.0.0'
port = 8888

def create_app():
    '''
    创建app
    :return:app
    '''
    app = Flask(__name__)
    return app


app = create_app()


def runflask():
    '''
    启动Flask
    :return:
    '''
    app.run(host=host, port=port, debug=False, threaded=False)


def stopflask():
    '''
    停止Flask
    :return:
    '''
    result = os.popen('lsof -i:%d' % port)

    for index in result.readlines():

        if index.startswith('Python'):
            pid = index.split()[1]
            os.system('kill %s' % pid)


def gethtml(monkeycmd):
    '''
    获取HTML报告
    :return:0表示获取html正常,1表示获取html失败
    '''
    logger.log_info("start gethtml")

    try:
        error = False
        data = {'monkeycmd': monkeycmd}
        r = requests.post('http://%s:%d/' % (host, port),data=data)
        with open(htmlpath, 'wb+') as f:
            f.write(r.content)

        logger.log_info('performance.html write complete' + '\n' \
              + 'path is: %s' % htmlpath)

    except Exception as e:
        logger.log_error('performance.html write fail' + '\n' + str(e))
        error = True


    r.close()
    stopflask()
    if error:
        return 1
    else:
        return 0


def readmeminfo():
    '''
    读取内存txt文件的数据
    :return:
    '''
    time = []
    info = []
    activity = []

    with open(mempath, 'r') as f:
        for index in f.readlines():
            time.append(index.split(',')[0])
            info.append(index.split(',')[1])
            activity.append(index.split(',')[2])

    return time, info, activity


def readcpu():
    '''
    读取CPUtxt文件的数据
    :return:
    '''
    time = []
    info = []
    activity = []

    with open(cpupath, 'r') as f:
        for index in f.readlines():
            time.append(index.split(',')[0])
            info.append(index.split(',')[1])
            activity.append(index.split(',')[2])

    return time, info, activity


def readnetwork():
    '''
    读取NetWork.txt文件的数据
    :return:
    '''
    time = []
    info = []
    activity = []

    with open(networkpath, 'r') as f:
        for index in f.readlines():
            time.append(index.split(',')[0])
            info.append(index.split(',')[1])
            activity.append(index.split(',')[2])

    return time, info, activity

def readfps():
    '''
    读取fps.txt文件的数据
    :return:
    '''
    time = []
    info = []
    activity = []

    with open(fpspath, 'r') as f:
        for index in f.readlines():
            time.append(index.split(',')[0])
            info.append(index.split(',')[1])
            activity.append(index.split(',')[2])

    return time, info, activity



def task(**kwargs):
    '''
    定义两个线程,用来做异步操作
    :return:
    '''
    def async(f):
        def wrapper(*args, **kwargs):
            thr = Thread(target=f, args=args, kwargs=kwargs)
            thr.start()
        return wrapper

    # 定义异步执行
    @async
    def asyncgethtml():
        time.sleep(2)
        gethtml(kwargs['monkeycmd'])
        logger.log_info("GetHtml complete")

    def asyncrunflask():
        runflask()
        logger.log_info("RunFlask complete")

    asyncgethtml()
    asyncrunflask()


@app.route('/',methods=['POST'])
def html():
    '''
    拼接html报告
    :return:template.html
    '''
    tuples = ()
    # 空元祖

    data = readmeminfo()
    # 内存数据

    i = []  # 小列表
    j = []  # 大列表
    for index in range(len(data[0])):
        i.append(data[0][index])
        i.append(int(data[1][index]))
        j.append(i)
        i = []
    tuples = tuples + tuple(j)
    # 返回拼接的元祖

    tuples1 = ()
    # 空元祖
    data1 = readcpu()
    # cpu数据

    k = []  # 小列表
    H = []  # 大列表
    for index in range(len(data1[0])):
        k.append(data1[0][index])
        k.append(float(data1[1][index]))
        H.append(k)
        k = []
    tuples1 = tuples1 + tuple(H)
    # 返回拼接的元祖


    tuples2 = ()
    # 空元祖
    data2 = readnetwork()
    # 读取流量

    m = []  # 小列表
    n = []  # 大列表
    for index in range(len(data2[0])):
        m.append(data2[0][index])
        m.append(float(data2[1][index]))
        n.append(m)
        m = []
    tuples2 = tuples2 + tuple(n)
    # 返回拼接的元祖

    tuples3 = ()
    # 空元祖
    data3 = readfps()
    # 读取FPS

    w = []  # 小列表
    q = []  # 大列表
    for index in range(len(data3[0])):
        w.append(data3[0][index])
        w.append(float(data3[1][index]))
        q.append(w)
        w = []
    tuples3 = tuples3 + tuple(q)
    # 返回拼接的元祖

    return render_template("template.html",title=request.form['monkeycmd'],
                           data=tuples, memtime=data[0], meminfo=data[1], memactivity=data[2],
                           data1=tuples1, cputime=data1[0], cpuinfo=data1[1], cpuactivity=data1[2],
                           data2=tuples2, nettime=data2[0], netinfo=data2[1], netactivity=data2[2],
                           data3=tuples3, fpstime=data3[0], fpsinfo=data3[1], fpsactivity=data3[2]
                           )


