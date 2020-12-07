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
import socket
import threading

class sigServer(threading.Thread):
    def __init__(self,ip,port,flst):
        self.ip = ip
        self.port = port

        self.src = SigGen(125,20)
        self.ws = tWebSocket(ip,port)
        self.flst = flst

        self.connected = False
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def getdata(self):
        data = self.src.getdata_asstrlist(self.flst)
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
                    elif command[1] == 'RecordStop':
                        pass

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

if __name__ == '__main__':
    sr = sigServer('127.0.0.1',54123,[10,17,18,19,20,21,22,25])
    sr.mainloop()







