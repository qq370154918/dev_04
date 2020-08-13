# -*- coding: utf-8 -*-

import locale
import platform


def datetime_fmt():
    # 判断当前运行系统
    if platform. system().lower().count('windows')>0:
        locale.setlocale(locale.LC_CTYPE, "Chinese")
    return '%Y年%m月%d日 %H:%M:%S'
