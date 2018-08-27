# coding=utf-8

import os, re
import subprocess
import logger
from DateBean import DateBean
import time
# model = 'ro.product.model'
# brand = 'ro.product.brand'
# version = 'ro.product.first_api_level'
# 真机获取

model = 'ro.product.model.geny'
brand = 'ro.product.brand.geny-def'
version = 'ro.build.version.sdk'

apkpath = 'undefined'
# 模拟器获取
appversion = 'undefined'



class AdbCommon():

    def __init__(self, dev):
        self.dev = dev
        self.db = DateBean()

    def getproductinfo(self):
        '''
        获取当前的设备的信息
        :return:当前设备的信息
        '''
        try:
            global model
            global board
            global osv
            result = os.popen('adb -s %s shell cat /system/build.prop' % self.dev)
            for line in result.readlines():
                if re.findall(model, line):
                    model = line.split('=')[1].replace('\n', '').replace('\r', '')
                if re.findall(brand, line):
                    board = line.split('=')[1].replace('\n', '').replace('\r', '')
                if re.findall(version, line):
                    osv = line.split('=')[1].replace('\n', '').replace('\r', '')

            return model, board, osv
        except Exception, e:
            logger.log_error("getproductinfo error! " + str(e))
            return 'undefined', 'undefined', 'undefined'

    def getactivity(self):
        '''
        获取当前的Activity
        :return:当前的Activity
        获取当前Activity有出现异常的时候,此时返回'undefined'
        '''
        try:
            cmd = 'adb -s %s shell dumpsys activity | grep "mFocusedActivity"' % self.dev
            result = os.popen(cmd)
            logger.log_debug(cmd)
            act =str(result.readlines()).split('/')[1].split()[0]
            return act

        except Exception, e:
            logger.log_error("GetActivity error! " + str(e))
            return 'undefined'


    def getdevices(self):
        '''
        获取设备id
        :return: 0表示未获取到,id是设备的真实id
        '''

        try:
            cmd = "adb devices"
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            id = pipe.read().split()[-2]
            if id != 'devices':
                return id
            else:
                logger.log_info("List of devices attached")
                return 0

        except Exception, e:
            logger.log_error("the process doesn't exist." + str(e))
            return 0

    def get_app_pid(self, pkg_name):
        '''
        根据包名得到进程id
        :return: 0表示未获取到,pid是设备的真实pid
        '''

        try:
            cmd = "adb -s %s shell ps | grep %s" % (self.dev, pkg_name)
            logger.log_debug(cmd)

            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            pid = pipe.read().split()[1]
            return str(pid)
        except Exception, e:
            logger.log_error("the process doesn't exist." + str(e))
            return 0

    def get_app_uid(self, pkg_name):
        '''
        根据包名得到进程id
        :return: 0表示未获取到,uid是设备的真实uid
        '''

        try:
            cmd = "adb -s %s shell cat /proc/%s/status" % (self.dev, self.get_app_pid(pkg_name))
            logger.log_debug(cmd)

            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            for index in pipe.readlines():
                if index.startswith('Uid'):
                    return index.split()[1]
        except Exception, e:
            logger.log_error("the process doesn't exist." + str(e))
            return 0

    def installdependapp(self):
        '''
        安装所有依赖的app
        :return: 0表示所有app安装成功1,表示app安装失败
        '''
        checklist = []

        for index in range(len(self.db.dependname)):

            if self.inspectapp(self.db.dependname[index]) != 0:
                cmd = 'adb -s %s install %s' % ((self.dev),self.db.dependlist[index])
                os.system(cmd)
                logger.log_debug(cmd)

                if self.inspectapp(self.db.dependname[index]) == 0:
                    logger.log_info(self.db.dependname[index] + '安装成功')
                else:
                    logger.log_info(self.db.dependname[index] + '安装失败')
                    checklist.append(False)
            else:
                logger.log_info(self.db.dependname[index] + '已安装')

        if False in checklist:
            return 1
        else:
            return 0

    def inspectapp(self, apkname):
        '''
        检查app是否存在
        :param apkname:0表示存在,1表示不存
        :return:
        '''
        try:
            cmd = 'adb -s %s shell pm list packages' % self.dev
            logger.log_debug(cmd)
            result = os.popen(cmd)

            if apkname in result.read():
                return 0
            else:
                return 1
        except Exception, e:
            logger.log_error('检查%s失败' % apkname + '\n' + '异常原因:%s' % e)
            return 1

    def installapp(self, apkname, apkpath):
        '''
        安装app
        :param path: apk路径
        :return: 0表示成功,1表示失败
        '''
        try:
            # if self.inspectapp(apkname) == 0:
            #     cmd = 'adb -s %s uninstall %s' % (self.dev,apkname)
            #     logger.log_debug(cmd)
            #     os.system(cmd)
            #
            # cmd = 'adb -s %s install %s' % (self.dev,apkpath)
            # logger.log_debug(cmd)
            # os.system(cmd)
            #
            # if self.inspectapp(apkname) == 0:
            #     return 0
            # else:
            #     return 1
            return 0

        except Exception, e:
            logger.log_error('安装%s失败' % apkname + '\n' + '异常原因:%s' % e)
            return 1

    def launch_app(self, packagename, activity):
        '''
        打开指定app
        packagename包名
        activity是指定的activity
        dev是设备号
        :return:
        '''
        if self.dev != 0:
            cmd = "adb -s %s shell am start -n %s/%s" % (self.dev, packagename, activity)
            logger.log_info(cmd)
            os.popen(cmd).read()
            time.sleep(3)
            return 0


    def sendbroadcast(self,enable):
        '''
        发送广播打开simiasque隐藏按钮
        :param enable: 0表示隐藏,1表示不隐藏
        :return:
        '''
        if enable == 0:
            switch = 'true'
            logger.log_info('开启隐藏导航栏')

        else:
            switch = 'false'
            logger.log_info('关闭隐藏导航栏')

        try:
            cmd = 'adb -s %s shell am broadcast -a org.thisisafactory.simiasque.SET_OVERLAY --ez enable %s' % (self.dev,switch)
            logger.log_debug(cmd)
            os.system(cmd)

        except Exception as e:
            logger.log_error('隐藏导航栏发送广播异常:' + str(e))

    def delfiles(self,folder):
        ''''
        删除文件夹下的所有文件
        :return 0 　表示删除成功,1表示删除失败
        '''
        folder = os.getcwd() + '/' + folder
        if os.path.exists(folder):
            cmd = 'rm -rf %s' % folder
            logger.log_debug(cmd)
            os.system(cmd)

        if os.path.exists(folder) == False:
            return 0
        else:
            return 1

    def replaceword(self,path, oldstart, new):
        '''
        替换文件中的某一行数据
        :param path: 文件路径
        :param old: 替换前的词语
        :param new: 替换后的词语
        :return:替换的后的文件
        '''
        try:
            with open(path, "r") as f:
                lines = f.readlines()

            with open(path, "w") as f_w:
                for line in lines:
                    if line.startswith(oldstart):
                        line = new + '\n'
                    f_w.writelines(line)

            with open(path, "r") as f:
                lines = f.read()

            if new in lines:
                return 0
            else:
                logger.log_info("修改%s中%s行失败" % (path, oldstart))
                return 1
        except Exception, e:
            logger.log_error("修改%s中%s行失败:%s" % (path, oldstart, str(e)))
            return 1

    def joinstr(self):
        '''
        统计monkey的命令和运行时间log日志等
        :return:
        '''
        title = '本次执行monkey命令:%s' % ''
        return title


    def getfolderapk(self,folderpath):
        '''
        获取目录下的apk,仿真包和正式包是带时间戳的,无法赋值
        :return:如果路径是.apk结尾,返回路径
        如果路径是文件夹,取文件夹中第一个文件名字拼接文件路径
        '''
        global apkpath
        logger.log_info('输入的apk路径:' + folderpath)

        if folderpath.endswith('.apk'):
            return folderpath

        else:
            for line in os.listdir(folderpath):
                if line.endswith('.apk'):
                   apkpath = os.path.join(folderpath, line)
                   break

                else:
                    apkpath = 'undefined'
            logger.log_info('返回的apk路径:' + apkpath)
            return apkpath

    def getpackageinfo(self,pkg):
        '''
        获取apk版本号
        :return:
        '''
        global appversion
        try:
            cmd = 'adb -s %s shell dumpsys package %s' % (self.dev,pkg)
            for line in os.popen(cmd).readlines():
                if re.findall(' versionName',line):
                    appversion = line.split('=')[1]
                    break
                else:
                    appversion = 'undefined'
        except Exception as e:
            appversion = 'undefined'
            logger.log_error('获取apk版本号异常:' + str(e))
        finally:
            return appversion


    def getnetstatus(self):
        '''
        获取当前网络状态
        :return:0表示连接状态,return表示未连接状态
        '''
        try:
            cmd = 'adb -s %s shell dumpsys wifi | grep ^Wi-Fi' % self.dev
            logger.log_info('获取wifi状态命令: ' + cmd)

            if 'enabled' in os.popen(cmd).read().strip():
                return 0
            else:
                return 1
        except Exception as e:
            logger.log_error('获取wifi状态异常: ' + str(e))
            return 1


    def openwifi(self):
        '''
        打开wifi
        :return:
        '''
        try:
            cmd = 'adb -s %s shell svc wifi enable' % self.dev
            logger.log_debug('打开wifi命令:' + cmd)
            os.system(cmd)
        except Exception as e:
            logger.log_error('打开wifi异常:' + str(e))


    def closewifi(self):
        '''
        关闭wifi
        :return:
        '''
        try:
            cmd = 'adb -s %s shell svc wifi disable' % self.dev
            logger.log_debug('关闭wifi命令:' + cmd)
            os.system(cmd)
        except Exception as e:
            logger.log_error('关闭wifi异常:' + str(e))


    def checkwifi(self):
        '''
        检查wifi状态,开始
        :return:
        '''
        if self.getnetstatus() == 1:
           self.openwifi()
           if self.getnetstatus() == 0:
               logger.log_info('wifi开启成功')
           else:
               logger.log_info('wifi未开启成功')
        else:
            logger.log_info('wifi已经是开启状态')



    

