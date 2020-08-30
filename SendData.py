# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:10:34 2020

@author: SCPC
"""

import socket
import threading
import json

sendData = {
  "infolist":
  [
    {
      "name": "fefa",
      "age": "34"
    },
    {
      "name": "hrg",
      "age": "21"
    }
  ],
    "rangelist":
  [
    {
      "tone": "1",
      "range": ["11","21"]
    },
    {
      "tone": "4",
      "range": ["44","64"]
    },
    {
      "tone": "3",
      "range": ["53","73"]
    }
  ]
}

sendData2 = {
  "rangelist":
  [
    {
      "tone": "1",
      "range": ["11","21"]
    },
    {
      "tone": "4",
      "range": ["44","64"]
    },
    {
      "tone": "3",
      "range": ["53","73"]
    }
  ]
}

msg = ""

def message_recv(client_executor, addr):

    while True:
        global msg
        msg = client_executor.recv(1024).encoding('utf-8')
        if msg == 'exit':
            break
    

# 当新的客户端连入时会调用这个方法
def on_new_connection(client_executor, addr):
    print('Accept new connection from %s:%s...' % addr)
    client_executor.send(bytes(repr(json.dumps(sendData)).encode('utf-8')))   #发送json信息
    recv_thread = threading.Thread(target = message_recv, args= (client_executor, addr))
    recv_thread.start()
    
    while msg != "exit":
        print(msg)
    
    client_executor.send(bytes("Good Bye".encode('utf-8')))
    
    #client_executor.send(bytes(repr(json.dumps(sendData2)).encode('utf-8')))   #发送json信息
    client_executor.close()
    print('Connection from %s:%s closed.' % addr)

# 构建Socket实例、设置端口号  和监听队列大小
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('127.0.0.1', 10087))
listener.listen(5)
print('Waiting for connect...')

# 进入死循环，等待新的客户端连入。一旦有客户端连入，就分配一个线程去做专门处理。然后自己继续等待。
while True:
    client_executor, addr = listener.accept()
    t = threading.Thread(target=on_new_connection, args=(client_executor, addr))
    t.start()