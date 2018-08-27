# coding=utf-8

'''
@property方法取出值
@monkeyfolder.setter 重新设置属性的值
@author:xinxi
'''
import time

class DateBean(object):

    def __init__(self):
        self._monkeyfolder = 'MonkeyLog'
        self._monkeylog = self._monkeyfolder + '/MonkeyInfo_%s.log' % time.strftime("%Y%m%d%H%M%S")
        self._monkeyerrorlog =  self._monkeyfolder + '/MonkeyError_%s.log' % time.strftime("%Y%m%d%H%M%S")
        self._logdir = 'Log'
        self._writeerror = self._logdir + "/" + time.strftime("%Y%m%d%H%M%S") + "_writeerror.log"
        self._outfolder = 'out'
        self._mempath = self._outfolder + '/meminfo.txt'
        self._cpupath = self._outfolder + '/cpu.txt'
        self._networkpath = self._outfolder + '/network.txt'
        self._fpspath = self._outfolder + '/fpspath.txt'
        self._packagename= 'com.luojilab.player'

        self._dependlist = ['DependApp/simiasque-debug.apk',
                            'DependApp/app-wifi.apk',
                            'DependApp/app-wifi-androidTest.apk']

        self._dependname = ['org.thisisafactory.simiasque',
                            'com.example.xinxi.myapplication',
                            'com.example.xinxi.myapplication.test']

        self._simiasquename = 'org.thisisafactory.simiasque'
        self._simiasqueactivity = 'org.thisisafactory.simiasque.MyActivity_'
        self._simulator = True
        self._appdebug = False
        self._runtime = 3600
        self._monkeycmd = ''


    @property
    def monkeyfolder(self):
        return self._monkeyfolder

    @monkeyfolder.setter
    def monkeyfolder(self, value):
        self._monkeyfolder = value

    @property
    def monkeyerrorlog(self):
        return self._monkeyerrorlog

    @monkeyerrorlog.setter
    def monkeyerrorlog(self, value):
        self._monkeyerrorlog = value

    @property
    def monkeylog(self):
        return self._monkeylog

    @monkeylog.setter
    def monkeylog(self, value):
        self._monkeylog = value

    @property
    def logdir(self):
        return self._logdir

    @logdir.setter
    def logdir(self, value):
        self._logdir= value

    @property
    def writeerror(self):
        return self._writeerror

    @writeerror.setter
    def writeerror(self, value):
        self._writeerror = value

    @property
    def outfolder(self):
        return self._outfolder

    @outfolder.setter
    def outfolder(self, value):
        self._outfolder = value

    @property
    def mempath(self):
        return self._mempath

    @mempath.setter
    def mempath(self, value):
        self._mempath = value

    @property
    def cpupath(self):
        return self._cpupath

    @cpupath.setter
    def cpupath(self, value):
        self._cpupath = value

    @property
    def networkpath(self):
        return self._networkpath

    @networkpath.setter
    def networkpath(self, value):
        self._networkpath = value

    @property
    def fpspath(self):
        return self._fpspath

    @fpspath.setter
    def fpspath(self, value):
        self._fpspath= value

    @property
    def packagename(self):
        return self._packagename

    @packagename.setter
    def packagename(self, value):
        self._packagename = value

    @property
    def dependlist(self):
        return self._dependlist

    @dependlist.setter
    def dependlist(self, value):
        self._dependlist = value

    @property
    def dependname(self):
        return self._dependname

    @dependlist.setter
    def dependlist(self, value):
        self._dependname = value

    @property
    def simiasquename(self):
        return self._simiasquename

    @simiasquename.setter
    def simiasquename(self, value):
        self._simiasquename = value

    @property
    def simiasqueactivity(self):
        return self._simiasqueactivity

    @simiasqueactivity.setter
    def simiasqueactivity(self, value):
        self._simiasqueactivity = value

    @property
    def simulator(self):
        return self._simulator

    @simulator.setter
    def simulator(self, value):
        self._simulator = value

    @property
    def appdebug(self):
        return self._appdebug

    @appdebug.setter
    def appdebug(self, value):
        self._appdebug = value

    @property
    def runtime(self):
        return self._runtime

    @runtime.setter
    def runtime(self, value):
        self._runtime = value

    @property
    def monkeycmd(self):
        return self._monkeycmd

    @monkeycmd.setter
    def monkeycmd(self, value):
        self._monkeycmd = value

