#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/3 10:57
# @Version : 1.0
# @File    : websocket.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved


import socket
import base64
import hashlib
import struct
import time
import threading

response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
               "Upgrade:websocket\r\n" \
               "Connection: Upgrade\r\n" \
               "Sec-WebSocket-Accept: %s\r\n" \
               "WebSocket-Location: ws://%s%s\r\n\r\n"
magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

class tWebSocket():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.con = None

    def accept(self,blocking = False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

        if not blocking:
            self.sock.setblocking(0)
            while True:
                try:
                    self.con,self.addr = self.sock.accept()
                    break
                except BlockingIOError:
                    time.sleep(0.2)

            while True:
                try:
                    data = self.con.recv(1024)
                    break
                except BlockingIOError:
                    time.sleep(0.1)
        else:
            self.sock.setblocking(1)
            self.con, self.addr = self.sock.accept()
            data = self.con.recv(1024)

        headers = self.get_headers(data)
        value = headers['Sec-WebSocket-Key'] + magic_string
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
        #handshake
        self.con.send(bytes(response_str, encoding='utf-8'))
        print('[websocket] connected!')

    def send(self,msg):
        self.con.send(msg)

    def recv(self,len):
        return self.con.recv(len)

    def get_headers(self,data):
        header_dict = {}
        data = str(data, encoding='utf-8')

        # for i in data.split('\r\n'):
        #     print(i)

        header, body = data.split('\r\n\r\n', 1)
        header_list = header.split('\r\n')
        for i in range(0, len(header_list)):
            if i == 0:
                if len(header_list[i].split(' ')) == 3:
                    header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(' ')
            else:
                k, v = header_list[i].split(':', 1)
                header_dict[k] = v.strip()
        return header_dict

    def pack_msg(self, msg_bytes):
        token = b"\x81"
        length = len(msg_bytes)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)

        msg = token + msg_bytes
        return msg

    def unpack_msg(self,info):
        payload_len = info[1] & 127
        if payload_len == 126:
            mask = info[4:8]
            decoded = info[8:]
        elif payload_len == 127:
            mask = info[10:14]
            decoded = info[14:]
        else:
            mask = info[2:6]
            decoded = info[6:]

        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)

        body = str(bytes_list, encoding='utf-8')
        return body

if __name__ == '__main__':
    pass

        








