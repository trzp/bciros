#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/5 15:41
# @Version : 1.0
# @File    : signalgenerator.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved

import time
import numpy as np


class SigGen(object):   #产生125hz正弦数据
    def __init__(self,fs,gain):
        self.fs = fs
        self.gain = gain
        self.tstp = 1./self.fs
        self.clk = time.perf_counter()

    def reset_clk(self):
        self.clk = time.perf_counter()

    def get_t_base(self):
        ct = time.perf_counter()
        if ct - self.clk < 0.05:
            return None

        t_base = np.arange(self.clk, ct, self.tstp)
        self.clk = ct
        return t_base

    def getdata(self,flst):
        t_base = self.get_t_base()
        if t_base is None:
            return None

        vals = []
        for f in flst:
            val = np.sin(2 * np.pi * f * t_base) * self.gain
            vals.append(val)

        return np.vstack(vals)

    def getdata_asstrlist(self,flst):
        t_base = self.get_t_base()
        if t_base is None:
            return None

        vals = []
        for f in flst:
            val = np.sin(2 * np.pi * f * t_base) * self.gain
            val = list(val.astype(np.int32).astype(np.str))
            vals.append(val)

        return vals

if __name__ == "__main__":
    src = SigGen(125,100)
    time.sleep(0.2)
    data = src.getdata_asstrlist([1,5])
    bufs = []
    for d in data:
        tem = ','.join(d)
        bufs.append(tem)
    buf = '<split>'.join(bufs)
    buf = '<head>' + buf + '<split>'
    pass

