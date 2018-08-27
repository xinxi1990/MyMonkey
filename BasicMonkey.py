# coding=utf-8

'''
monkey常用操作类
@author xinxi
'''


import os
import time
import re
import subprocess
from AdbCommon import AdbCommon
import random
import logger
import linecache
from DateBean import DateBean

#quotiety = int(10000000 / 60)

quotiety = int(62500 / 60)
# 事件和时间的系数

CRASH = 'CRASH'
ANR = 'ANR'
anr = 'anr'
Exception= 'Exception'
NoResponse = 'No Response'
Monkeyfinished = '// Monkey finished'
NullPointer="java.lang.NullPointerException"
IllegalState="java.lang.IllegalStateException"
IllegalArgument="java.lang.IllegalArgumentException"
ArrayIndexOutOfBounds="java.lang.ArrayIndexOutOfBoundsException"
RuntimeException="java.lang.RuntimeException"
SecurityException="java.lang.SecurityException"
# 过滤Monkey关键字

key = []

e = None
pid = None
activitylist = []

class BasicMonkey():

    def __init__(self, dev):
        self.dev = dev
        # 设备devicesid
        self.event = pow(10, 5)
        # 发送事件总数,100W
        self.adc = AdbCommon(self.dev)
        self.pck = 'com.luojilab.player'
        self.activity = 'com.luojilab.business.HomeTabActivity'
        self.db = DateBean()

    def runmonkey(self,seed, packagename, throttle, runtime,monkeylog, errorlog):
        '''
        执行Monkey
        :return:
        '''

        if not os.path.exists(self.db.monkeyfolder):
            os.mkdir(self.db.monkeyfolder)
        cmd = 'adb -s %s shell monkey ' \
              '-s %d ' \
              '-p %s ' \
              '--hprof ' \
              '--throttle %d ' \
              '--ignore-crashes ' \
              '--ignore-timeouts ' \
              '--ignore-security-exceptions ' \
              '--ignore-native-crashes ' \
              '--monitor-native-crashes ' \
              '--pct-syskeys 10 ' \
              '-v -v -v %d  2>%s 1>%s' % \
              (self.dev,int(seed), packagename, int(throttle),
               self.event, errorlog,monkeylog)

        logger.log_info("Monkey命令:%s" % cmd)
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        return cmd


    def stopmonkey(self):
        '''
        停止Monkey
        :return:
        '''
        # 利用管道打印内容
        try:

            grep_cmd = "adb -s %s shell ps | grep monkey" % self.dev
            pipe = os.popen(grep_cmd)
            result = pipe.read()
            if result == '':
                logger.log_info('monekey进程不存在')
            else:
                logger.log_info('monekey进程存在')
                pid = result.split()[1]
                # kill monkey进程
                stop_cmd = "adb -s %s shell kill %s" % (self.dev,pid)
                os.system(stop_cmd)
                self.stopmonkey()
        except Exception as e:
            logger.log_error('stopmonkey异常: ' + str(e))


    def getmonkey(self,monkeylog):
        '''
        通过monkeylog日志判断monkey是否结束
        :param monkeylog:
        :return: 0表示未结束,1表示结束
        '''
        with open(monkeylog) as f:
            if Monkeyfinished in f.read():
                return 1
            else:
                return 0


    def findmonkey(self):
        '''
        寻找Monkey的pid
        :return:
        '''
        global e
        global pid
        try:
            grep_cmd = "adb -s %s shell ps | grep monkey" % self.dev
            pipe = os.popen(grep_cmd)
            pids = pipe.read()
            if pids == '':
               logger.log_info("当前monkey进程不存在")
               return 1
            else:
               pid = pids.split()[1]
            logger.log_info("当前monkey进程pid:%s" % pid)
            return 0
        except Exception ,e:
            logger.log_error("当前monkey进程不存在:%s" % str(e))
            return 1

    def emptylogcat(self):
        '''
        在monkey运行前执行adb logcat -c清空所有log缓存日志
        :return: 0表示执行成功,1表示执行出现异常
        '''
        try:
            logger.log_info("使用adb logcat -c清空手机中的手机中的log")
            os.popen("adb -s %s logcat -c" % self.dev )
            return 0

        except Exception,e:
            logger.log_error("执行adb logcat -c出现异常%s" % str(e))
            return 1


    def getlogcat(self):
        '''
        获取logcat日志中所有日志
        :return:返回保存logcat的文件地址
        '''
        if not os.path.exists(self.db.logdir):
            os.mkdir(self.db.logdir)
        logcatname = self.db.logdir + "/" + time.strftime("%Y%m%d%H%M%S") + "_logcat.log"
        # 定义logcat文件保存地址
        cmd = "adb -s %s logcat -d  >%s" % (self.dev,logcatname)
        # 获取logcat日志
        os.popen(cmd)
        time.sleep(2)
        return logcatname


    def writeerror(self,logcatpath,wirteerrorpath):
        '''
        根据log文件地址,写入到error文件中
        :param logcatpath: log文件地址
        :param wirteerrorpath: 写入error的文件地址
        :return:0表示有错误日志,1表示没有错误日志
        '''
        f = open(logcatpath, "r")
        lines = f.readlines()
        if len(lines) == 0:
            logger.log_info("扫描%s路径的log日志为空,将删除" % logcatpath)
            os.system('rm -rf %s' % logcatpath)
        else:
            if not os.path.exists(self.db.logdir):
                os.mkdir(self.db.logdir)
            fr = open(wirteerrorpath, "a")
            for line in lines:
                if (re.findall(CRASH, line) or
                        re.findall(ANR, line) or
                        re.findall(NoResponse, line) ):
                    number = lines.index(line)  # 找到行数
                    fr.write("第%s行" % number + ' , ' +"错误原因:%s" % line)
                    fr.write("\n")
            f.close()
            fr.close()
            if os.path.getsize(wirteerrorpath)  == 0:
                logger.log_info("扫描%s路径的log日志中未发现错误日志" % logcatpath)
                os.system('rm -rf %s' % wirteerrorpath)
                return 1
            else:
                logger.log_info("扫描%s路径的log日志中发现错误日志,过滤后的文件路径%s" % (logcatpath,wirteerrorpath))
                return 0


    def returnmonkey(self,activity):
        '''
        如果不在monkey的运行activity中,重新返回monkey运行
        :param activity 当前运行的activity
        :return:
        '''

        if activity.startswith('com.luojilab'):
            logger.log_info('monke运行未溢出activity范围')
            return 0
        else:
            logger.log_info('monke运行溢出activity范围,跳转到%s' % self.activity)
            cmd = "adb -s %s shell am start -n %s/%s" % (self.dev, self.pck, self.activity)
            os.system(cmd)
            return 1


    def whitelistrun(self,activity,whitelist):
        '''
        白名单机制,只能执行定义的activity
        com.xxxxx.xxxxx.erechtheion.activity.ErechInfoActivity
        com.xxxxx.xxxxx.ddplayer.player.LuoJiLabPlayerActivity
        com.xxxxx.xxxxx.HomeTabActivity
        com.xxxxx.xxxxx.studyplan.ui.activity.SettingStudyPlanActivity
        :param activity 当前运行的activity
        :param whitelist白名单列表
        :return:
        '''
        global activitylist

        if whitelist != '' or len(whitelist) != 0:
            if isinstance(whitelist,str):
                activitylist = whitelist.split(',')
            elif isinstance(whitelist,dict or tuple):
                activitylist = whitelist
            if re.findall(activity,str(activitylist)):
                logger.log_info('monke运行未溢出白名单范围')
                return 0

            else:
                try:
                    randomactivity = (random.randint(0, len(activitylist) - 1))
                    logger.log_info('monke运行溢出activity范围,跳转到%s' % activitylist[randomactivity])
                    cmd = "adb -s %s shell am start -n %s/%s" % (self.dev, self.pck, activitylist[randomactivity])
                    logger.log_info('monkey跳转命令:%s' % cmd)
                    os.system(cmd)
                    return 1
                except Exception as e:
                    logger.log_error('monke运行跳转到白名单异常: ' + str(e))
        else:
            logger.log_info('monke运行白名单未配置')


    def grepmonkey(self,filename):
        '''
        从monkeylog日志从获取行数,判断是否结束
        如果本次和前一次的行数一样,则认为已经结束了monkey
        :return:
        '''
        return len(linecache.getlines(filename))


