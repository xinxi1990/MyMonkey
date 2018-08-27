# coding=utf-8

"""
常用文件操作类

@author:xinxi
"""

import os
import yaml
import logger


def readyaml(filepath):
    '''
    读取yaml文件
    :return:
    '''
    with open(filepath, "r") as f_r:
        content = yaml.load(f_r.read())
    return content


def writeyaml(filepath, key, value):
    '''
    写入yaml文件
    :param filepath:
    :return:
    '''
    content = readyaml(filepath)
    content[key] = value
    with open(filepath, "w") as f_r:
        yaml.dump(content, f_r, default_flow_style=False)


def stringwrap(string):
    '''
    字符串换行
    :return:
    '''
    try:
        targ = True
        flag = 90
        #最大15个字符
        stringlist = []
        while targ:
            if len(string) > flag:
                stringlist.append(string[0:flag])
                string = string[flag:]
            else:
                stringlist.append(string)
                targ = False
        return '\n'.join(stringlist)

    except Exception as e:
        logger.log_error('换行字符串失败' + str(e))
        return string


def ClearLog():
    '''
    清除所有本地所有缓存的log数据
    :return:
    '''
    pathlist = ['MonkeyLog','Log']

    for path in  pathlist:
        os.system('rm -rf %s' % path)


if __name__ == '__main__':
    print readyaml("Config.yml")