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
from serial_ads import *
import scipy.signal as scipy_signal
from copy import copy


class adsSource(object):
    def __init__(self,com,notchfilter,bandpass): #目标是125hz
        self.ads = adsReader(com,115200)
        self.ads.start()
        
        srate = 250
        self.downsample = 2
        
        self.srate = srate
        self.notchfilter = notchfilter
        self.bandpass = bandpass
        fs = self.srate/2
        if self.bandpass is not None:
            self._bp = True
            Wp = np.array([bandpass[0] / fs, bandpass[1] / fs])
            Ws = np.array([(bandpass[0]*0.5) / fs, (bandpass[1]+10) / fs])
            N, Wn = scipy_signal.cheb1ord(Wp, Ws, 3, 40)
            self.bpB, self.bpA = scipy_signal.cheby1(N,0.5,Wn,'bandpass')
        else:
            self._bp = False
        
        # notch filter
        Fo = 50
        Q = 15
        w0 = Fo / (fs)
        self.notchB, self.notchA = scipy_signal.iirnotch(w0=w0, Q=Q)
        
        # 固定显示4秒的数据
        timerange = 4
        self._plength = int(self.srate * (0.5+timerange))
        self._slength = int(self.srate * timerange)
        self.signal = []

    def reset_clk(self):
        pass
    
    def getdata_asstrlist(self):
        data = self.ads.readarray()
        self.signal.append(data)
        eeg = np.hstack(self.signal)[:, -self._plength:]
        self.signal = [eeg]
        sig = copy(eeg)
        if eeg.shape[-1] >= self._plength:
            if self.notchfilter:
                sig = scipy_signal.filtfilt(self.notchB, self.notchA, sig)
            if self._bp:
                sig = scipy_signal.filtfilt(self.bpB, self.bpA, sig)
            
            sig1 = sig[:,-self._slength::self.downsample]                               #将采样到125hz
            return sig1,sig1.astype(np.int32).astype(np.str)
        else:
            return None
