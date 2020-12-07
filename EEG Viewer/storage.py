#!/usr/bin/env python
#-*- coding:utf-8 -*-

#Copyright (C) 2018, Nudt, JingshengTang, All Rights Reserved
#Author: Jingsheng Tang
#Email: mrtang@nudt.edu.cn


import multiprocessing
from multiprocessing import Queue

import os
import re
import csv

def name_file(path,head,extention): #EEG_recording_0.csv/EEG_recording_1.csv/EEG_recording_2.csv
    if not os.path.isdir(path):
        os.makedirs(path)
        return head + '00' + extention

    pattern = re.compile(head + '\d+' + extention)
    npattern = re.compile('\d+')
    filelst = os.listdir(path)
    mn = -1
    for f in filelst:
        r = pattern.match(f)
        if r is not None:
            nums = npattern.findall(f)
            num = int(nums[0])
            if len(nums)>0 and num>=mn:
                mn = num
    return path + r'/' + head + '%02d'%(mn+1) + extention


def writefile1(filename,que,ev):
    f = open(filename,'w',encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['ch1','ch2','ch3','ch14','ch5','ch6','ch7','ch8'])
    while not ev.is_set():
        data = que.get()
        data = data.tanspose()
        for i in range(0,data.shape[0]):
            csv_writer.writerow(data[i,:])
    f.close()

def writefile(que):
    print('[storage] process started!')
    csv_writer = None
    while True:
        buf = que.get()
        cmd = buf[0]
        if cmd[:5] == 'start':
            headname = cmd[8:]
            filename = name_file('./data',headname,'.csv')
            print('[storage] create file: ',filename)
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(['ch1', 'ch2', 'ch3', 'ch14', 'ch5', 'ch6', 'ch7', 'ch8'])

            f = open(filename, 'a', encoding='utf-8', newline='')
            csv_writer = csv.writer(f)

        elif cmd[:4] == 'stop':
            csv_writer = None
            try:
                f.close()
            except:
                pass
            print('[storage] close file')

        elif cmd[:5] == 'write':
            if csv_writer is not None:
                data = buf[1].transpose()
                csv_writer.writerows(data)

        elif cmd[:4] == 'quit':
            try:
                f.close()
            except:
                pass
            break

    print('[storage] process kill')




class Storage():
    def __init__(self):
        self.que = Queue()
        p = multiprocessing.Process(target = writefile,args=(self.que,))
        p.start()

    def start(self,filename):
        self.que.put(['start:::%s'%(filename),])

    def stop(self):
        self.que.put(['stop',])

    def quit(self):
        self.que.put(['quit', ])

    def write(self,data):
        self.que.put(['write', data])




