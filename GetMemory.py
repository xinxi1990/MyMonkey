# coding=utf-8


'''
获取设备内存

Naitve Heap Size 代表最大总共分配空间
Native Heap Alloc 已使用的内存
Native Heap Free  剩余内存
Naitve Heap Size约等于Native Heap Alloc + Native Heap Free

@author:xinxi

'''


import time
import os
import sys
from DateBean import DateBean
import logger

reload(sys)
sys.setdefaultencoding('utf-8')

f = None


heapalloc = 0

class GetMemory():

    def __init__(self,dev):
        self.dev = dev
        self.db = DateBean()

    def getmeminfo(self,activity):
        '''
        获取内存信息并写入文件
        :return:
        '''
        global heapalloc
        try:
            cmd = "adb -s %s shell dumpsys meminfo %s" %(self.dev, self.db.packagename)
            logger.log_debug(cmd)
            for index in os.popen(cmd).readlines():
                if index.startswith('  Dalvik Heap'):
                    heapalloc = index.split()[7]

        except Exception, e:
            logger.log_error("获取内存失败" + str(e))
            heapalloc = 0

        finally:
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(self.db.mempath, 'ab+') as f:
                f.write(
                    str(times) + ',' +
                    str(heapalloc) + ',' +
                    str(activity) + ',' + '\n'
                )

