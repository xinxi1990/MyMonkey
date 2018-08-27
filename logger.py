# coding=utf-8


'''
日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
使用规则:
1.正常输出使用INFO
2.捕获异常使用ERROR
3.调试代码使用DEBUG
4.setLevel可以通过外部参数修改

@author:xinxi
'''

import logging
import sys
import time
from colorama import Back, Fore, Style, init
from colorlog import ColoredFormatter



init(autoreset=True)

log_colors_config = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red',
}


def setup_logger(log_level):
    """setup root logger with ColoredFormatter."""
    level = getattr(logging, log_level.upper(), None)
    if not level:
        color_print("Invalid log level: %s" % log_level, "RED")
        sys.exit(1)

    # hide traceback when log level is INFO/WARNING/ERROR/CRITICAL
    if level >= logging.INFO:
        sys.tracebacklimit = 0

    formatter = ColoredFormatter(
        u"%(log_color)s%(bg_white)s%(levelname)-8s%(reset)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors=log_colors_config
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(level)


def coloring(dt,text, color="WHITE"):
    fore_color = getattr(Fore, color.upper())

    if isinstance(text,tuple or list):
        text = str(text)

    return fore_color + ' - ' + dt + ' - ' + text

def color_print(msg, color="WHITE"):
    fore_color = getattr(Fore, color.upper())
    print(fore_color + msg)

def log_with_color(level):
    """ log with color by different level
    """
    def wrapper(text):
        dt = time.strftime("%Y-%m-%d %H:%M:%S")
        color = log_colors_config[level.upper()]
        getattr(logging, level.lower())(coloring(dt,text, color))

    return wrapper

log_debug = log_with_color("debug")
log_info = log_with_color("info")
log_warning = log_with_color("warning")
log_error = log_with_color("error")
log_critical = log_with_color("critical")
