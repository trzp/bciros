#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/5 17:20
# @Version : 1.0
# @File    : server.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved

from twebsocket import tWebSocket
from signalgenerator import *
from ads_reader import *
import socket
import threading
from storage import *
from multiprocessing import Queue
from multiprocessing import Event
from storage import *

MODEL = 'ads'
MODEL = 'generator'

class sigServer(threading.Thread):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

        if MODEL == 'generator':
            self.src = SigGen(125,20)
            self.flst = [10,17,18,19,20,21,22,25]
        elif MODEL == 'ads':
            self.src = adsSource("COM3",True,[1,90])
            
        self.ws = tWebSocket(ip,port)

        self.store = Storage()

        self.connected = False
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def getdata(self):
        vals,data = self.src.getdata_asstrlist(self.flst)
        self.store.write(vals)
        if data is None:    return None
        bufs = []
        for d in data:
            tem = ','.join(d)
            bufs.append(tem)
        tem = '<head>' + '<split>'.join(bufs)
        return bytes(tem,'utf-8')

    def run(self):
        while True:
            while not self.connected:
                time.sleep(0.2)

            while self.connected:
                msg = None

                try:
                    buf = self.ws.recv(1024)
                except:
                    self.connected = False
                    continue

                try:
                    msg = self.ws.unpack_msg(buf)
                except:
                    pass

                if msg is not None:
                    print('[server] command: ',msg)
                    command = msg.split(':::')
                    if command[1] == 'Disconnect':
                        self.connected = False
                    elif command[1] == 'RecordStart':
                        filename = command[2]
                        self.store.start(filename)
                    elif command[1] == 'RecordStop':
                        self.store.stop()

    def mainloop(self):
        self.start()
        while True:
            print('[server] connecting...')
            self.ws.accept(blocking=True)
            self.connected = True
            self.src.reset_clk()
            time.sleep(0.1)

            while self.connected:
                buf = self.getdata()
                if buf is None: continue
                msg = self.ws.pack_msg(buf)
                try:
                    self.ws.send(msg)
                except socket.error:
                    self.connected = False

                time.sleep(0.2)
        self.store.quit()

if __name__ == '__main__':
    sr = sigServer('127.0.0.1',54123)
    sr.mainloop()







