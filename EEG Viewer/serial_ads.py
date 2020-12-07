#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/22 21:24
# @Version : 1.0
# @File    : serial_ads.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved


import threading
import socket
import time
import serial
import multiprocessing
from multiprocessing import Event
from multiprocessing import Queue
import struct
import numpy as np

def ads_ser(port,baud,que,ev):
    # 独立进程高速读取数据
    # ev初始为空
    # 主控调用ev.set()启动
    # 主控调用ev.clear()终止
    ser = serial.Serial(port,baudrate = baud)
    print('[serial] serial opended!')
    while not ev.is_set():  #等待启动
        time.sleep(0.01)
    
    print('[serial] start acquisition!')
    
    while ev.is_set():
        b = ser.read(135)
        que.put(b)
    print('[serial] serial closed!')
    ser.close()

class adsReader():
    def __init__(self,port='COM7',baud=115200):
        self.stev = Event()
        self.stev.clear()
        self.que = Queue()
        self.uads = unpackAds1299Data()
        p = multiprocessing.Process(target = ads_ser,args=(port,baud,self.que,self.stev))
        p.start()
        
    def start(self):
        self.stev.set()
    
    def stop(self):
        self.stev.clear()
    
    def readraw(self):
        buffer = b''
        while not self.que.empty():
            buffer += self.que.get()
        return buffer
    
    def readarray(self):
        buffer = self.readraw()
        data = self.uads.unpack(buffer)
        return data

#下位机发送的数据包长度为27字节，前3字节为0xAA,0xBB,0xCC作为包头

class unpackAds1299Data():
    def __init__(self,ads_gain = 24,scaling_output = True):
        ADS1299_Vref = 4.5         # reference voltage for ADC in ADS1299.  set by its hardware
        ADS1299_gain = ads_gain    #由主控芯片进行寄存器配置，默认设置为24
        self.scale_fac_uVolts_per_count = ADS1299_Vref /float((pow(2, 23) - 1)) / ADS1299_gain * 1000000.
        self.scaling_output = scaling_output
        self.max = 0
        self.buffer = b''
        
    def unpack(self,buffer):
        self.buffer += buffer
        self.dlen = len(self.buffer)
        payload = b''
        indx = 0
        tail = 0
        while indx < self.dlen-26: # <= 27
            head = struct.unpack('3B',self.buffer[indx:indx+3])
            if head[0] == 0xAA and head[1]==0xBB and head[2]==0xCC: #搜索到包头
                tem = self.buffer[indx+3:indx+27]
                payload += tem
                indx += 27
                tail = indx     #tail记录的是最后一个有效数据包后面的搜索起点
            else:
                indx += 1
        
        self.buffer = self.buffer[tail:]

        if len(payload)==0: return None

        data = []
        for i in range(0, len(payload), 3):  # 每三个字节为一个数据S
            literal_bytes = payload[i:i + 3]
            myInt = self.__unpack(literal_bytes)
            data.append(myInt)

        pnum = int(len(data) / 8)
        data = np.array(data, dtype=np.float64)
        data = data.reshape(pnum, 8).transpose()
        return data

    
    def __unpack(self,literal_bytes):    # 接受三个字节,对应一个数据
        unpacked = struct.unpack('3B', literal_bytes)

        # 3byte int in 2s compliment    对补码的处理
        if (unpacked[0] > 127):
            pre_fix = bytes(bytearray.fromhex('FF'))
        else:
            pre_fix = bytes(bytearray.fromhex('00'))

        literal_bytes = pre_fix + literal_bytes   #补齐为四字节

        #高位先行，即big-endian
        myInt = struct.unpack('>i', literal_bytes)[0]
        
        return myInt * self.scale_fac_uVolts_per_count

        
def main():
    ar = adsReader()
    ar.start()
    for i in range(1000):
        print(ar.readarray().shape)
        # ar.readarray()
        time.sleep(0.2)
    ar.stop()
 
 
if __name__ == '__main__':
    main()