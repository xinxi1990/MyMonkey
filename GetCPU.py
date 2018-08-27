# coding=utf-8


'''

获取设备cpu
@author xinxi

User space（用户空间）和 Kernel space（内核空间）
Kernel space 是 Linux 内核的运行空间，User space 是用户程序的运行空间
'''


import time
import os
import re
from AdbCommon import AdbCommon
from DateBean import DateBean
import logger



total = 0

class GetCPU():

    def __init__(self, dev):
        self.dev = dev
        # 设备devicesid
        self.db = DateBean()

    def get_cpu_kel(self):
        ''''
        # 得到几核cpu
        '''
        cmd = "adb -s " + self.dev + " shell cat /proc/cpuinfo"
        process = (os.popen(cmd))
        output = process.read()
        res = output.split()
        num = re.findall("processor", str(res))
        return len(num)


    def getcpu(self, activity):
        '''
        统计com.xxxx.xxxxx,cpu的占用率
        :return:
        '''
        global total

        try:
            cmd = "adb -s %s shell dumpsys cpuinfo | grep %s" % (self.dev, self.db.packagename)
            logger.log_debug(cmd)
            result = os.popen(cmd)
            for line in result.readlines():
                if re.findall(self.db.packagename, line):
                    total = line.split()[0].replace('%', '')
        except Exception, e:
            logger.log_error("获取cpu失败:" + str(e))
            total = 0
        finally:
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(self.db.cpupath, 'ab+') as f:
                f.write(
                    str(times) + ',' +
                    str(total) + ',' +
                    str(activity) + ',' + '\n'
                )



