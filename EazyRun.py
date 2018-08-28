# coding=utf-8


'''
配置config.yaml执行
@author xinxi
'''


from GetMemory import GetMemory
from GetCPU import GetCPU
from GetNetWork import GetNetWork
from GetFPS import GetFPS
from BasicMonkey import BasicMonkey
from ReportServer import Flask
from SendMail import *
from CrashSQL import *
from DateBean import DateBean
import logger


def run():

    configYaml =  readyaml("Config.yml")
    apkname = configYaml["apkname"]
    # apk包名
    runtime = configYaml["runtime"]
    # monkey运行时间
    seed = configYaml["seed"]
    # monkey命令的seed值
    apkpath = configYaml["apkpath"]
    # apk路径
    throttle = configYaml["throttle"]
    # 时间间隔
    simulator = configYaml["simulator"]
    # 设备是否模拟器参数
    appdebug = configYaml["appdebug"]
    # app是否是debug
    devices = configYaml["devces"]
    # 设备号
    whitelist = configYaml["whitelist"]
    # 白名单列表
    account = configYaml["account"]
    # 登录账号
    pwd = configYaml["pwd"]
    # 登录密码
    loglevel = configYaml["loglevel"]
    # 日志等级

    adc = AdbCommon(devices)
    # 初始化AdbCommon类
    db = DateBean()
    logger.setup_logger(loglevel)
    # 设置log级别
    

    try:
        if isinstance(int(runtime), int):
            if int(runtime) > 60:
                logger.log_info('输入的运行时间太大,最大运行时间是60分钟')
            else:
                flag1 = True

    except Exception, e:
        logger.log_error('输入的runtime参数,类型必须是整数' + '\n' + '异常信息:' + str(e))

    try:
        if isinstance(int(seed), int):
            flag2 = True
        else:
            logger.log_info('输入的seed参数,类型必须是整数')

    except Exception, e:
        logger.log_error('输入的seed参数,类型必须是整数'  + '\n' + '异常信息:' + str(e))

    try:
        if isinstance(int(throttle), int):
            flag3 = True
        else:
            logger.log_info('输入的throttle参数,类型必须是整数')

    except Exception, e:
        logger.log_error('输入的throttle参数,类型必须是整数' + '\n' + '异常信息:' + str(e))

    rootpath = str(sys.argv[0]).split('/')
    lists = list(rootpath)
    del lists[-1]
    newpath = '/'.join(lists)
    os.chdir(newpath)
    # 跳转到当前目录下
    logger.log_info('当前文件路径:'+os.getcwd())
    # 获得当前工作目录

    try:
         db.simulator = simulator
         flag4 = True

    except Exception, e:
        logger.log_error('修改simulator失败' + '\n' + '异常信息:' + str(e))

    try:
        db.appdebug = appdebug
        flag5 = True

    except Exception, e:
        logger.log_error('修改appdebug失败'  + '\n' + '异常信息:' + str(e))

    try:
        apkpath = adc.getfolderapk(apkpath)
        flag6 = True
    except Exception, e:
        logger.log_error('获取apk路径失败'  + '\n' + '异常信息:' + str(e))

    if flag1 and flag2 and flag3 and flag4 and flag5 and flag6 == True :

        info = 'apkname is:"{}'.format(apkname) + '\n' + 'runtime is:{}'.format(runtime) + '\n' + \
              'seed is:{}'.format(seed) + '\n' + 'apkpath is: {}'.format(apkpath) + '\n' + \
              'throttle is: {}'.format(throttle) + '\n' + 'simulator is: {}'.format(simulator)  + '\n' + \
              'appdebug is: {}'.format(appdebug) + '\n' + 'devices is: {}'.format(devices) + '\n' + 'whitelist is: {}'.format(str(whitelist))
        logger.log_info(info)

        if adc.getdevices() != 0:
            if adc.installdependapp() == 0:
                if adc.launch_app(db.simiasquename,db.simiasqueactivity) == 0:
                    adc.sendbroadcast(0)
                    # 开启隐藏导航栏
                    if adc.installapp(apkname, apkpath) == 0:

                       main(devices=devices,seed=seed, apkname=apkname,
                            throttle=throttle, runtime=runtime,whitelist=whitelist,
                            account=account,pwd=pwd,simulator=db.simulator,db=db)
                        # 调用运行主方法

                    else:
                        logger.log_info('安装%s失败,请检查apk文件路径%s' % (apkname, apkpath))

            else:
                logger.log_info('安装依赖app失败')

        else:
            logger.log_info('手机设备未链接')

    else:
        logger.log_info('请检查输入参数个数')



def main(**kwargs):
    '''
    Main主脚本执行Monkey和性能采集,并生成html报告
    '''
    devices = kwargs['devices']
    seed = kwargs['seed']
    apkname = kwargs['apkname']
    throttle = kwargs['throttle']
    runtime = kwargs['runtime']
    whitelist = kwargs['whitelist']
    account = kwargs['account']
    pwd = kwargs['pwd']
    simulator = kwargs['simulator']
    db = kwargs['db']

    adc = AdbCommon(devices)
    bsm = BasicMonkey(devices)
    net = GetNetWork(devices)
    fps = GetFPS(devices)
    mem = GetMemory(devices)
    cpu = GetCPU(devices)
    # 初始化类

    starttime = int(abs(round(time.time(), 0)))
    starttimestamps = time.strftime('%Y-%m-%d %H:%M:%S')

    logger.log_info('Monkey脚本 - 开始' + '\n' \
                 + '开始时间:%s' % str(starttimestamps))

    logger.log_info('删除临时保存性能文件')

    if adc.delfiles(db.outfolder)  == 0 and bsm.emptylogcat() == 0:
        # 删除out文件夹下所有临时文件

        monkeylog = db.monkeylog
        monkeyerrorlog = db.monkeyerrorlog
        writeerror = db.writeerror

        monkeycmd = bsm.runmonkey(seed, apkname, throttle, runtime, monkeylog, monkeyerrorlog)
        # 执行Monkey

        flag = True
        time.sleep(3)

        while flag:

            if not os.path.exists(db.outfolder):
                os.mkdir(db.outfolder)
            # 创建性能报告临时文件夹

            adc.checkwifi()
            # 检查wifi状态并开启

            activity = adc.getactivity()
            # 获取当前运行的activity

            bsm.whitelistrun(activity,whitelist)
            # 检测monkey运行状态

            cpu.getcpu(activity)
            # 采集CPU
            mem.getmeminfo(activity)
            # 采集内存
            net.selectnetwork(simulator,activity)
            # 采集流量
            fps.getfps(activity)
            # 采集FPS

            currenttime = int(abs(round(time.time(), 0)))
            # 获取当前运行时间

            logger.log_info('已经运行时间: %d' % (currenttime - starttime))
            logger.log_info('预期运行时间: %d' % (int(runtime) * 60))

            if (currenttime - starttime) >= (int(runtime) * 60):
                bsm.stopmonkey()
                flag = False

            else:
                time.sleep(30)


        logger.log_info('采集性能数据结束')

        endtime = int(abs(round(time.time(), 0)))
        difftime = (endtime - starttime)

        endtimestamps = time.strftime('%Y-%m-%d %H:%M:%S')

        logger.log_info('Monkey脚本 - 结束' + '\n' + \
              ',结束时间:%s' % str(endtimestamps) + \
              ',耗时%s秒' % str(difftime))

        adc.sendbroadcast(1)
        # 关闭隐藏导航

        if bsm.writeerror(monkeylog, writeerror) == 0:
            # 获取monkeylog所有日志
            send_mail(devices,monkeylog, writeerror,str(difftime),monkeycmd)
            # 发送报警邮件
            dt= time.strftime("%Y-%m-%d %H:%M:%S")
            # 插入数据库时间
            CrashSQL().insert_table("""'%s','%s','%s','crash','%s'""" % (dt,devices,adc.getpackageinfo(apkname),monkeylog))
            # 设备号、apk版本号、monkeylog日志插入android_crash表中

        CrashSQL().insert_table(
            """'%s','%s','%s','run success','%s'""" % (time.strftime("%Y-%m-%d %H:%M:%S"), devices, adc.getpackageinfo(apkname), ''))
        # 设备号、apk版本号、monkeylog日志插入android_crash表中

        Flask.task(monkeycmd=monkeycmd)
        # 执行生成性能报告




if __name__ == '__main__':
    run()




