# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:10:34 2020

@author: SCPC
"""

import socket
import threading
import json
import time

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
cal = 0
callll = 0
def message_recv(stop_event, client_executor, addr):
    global msg
    global cal
    time.sleep(1)
    stop_event.clear()
    time.sleep(1)
    while not stop_event.is_set():
        cal += 1
        print("call ",cal)
        msg = client_executor.recv(1024).decode('utf-8')
        if msg == "exit":
          stop_event.set()
        else:
          print(msg)
          
    print("end the thread")



def on_new_connection(client_executor, addr):
    print('Accept new connection from %s:%s...' % addr)
    client_executor.send(bytes(repr(json.dumps(sendData)).encode('utf-8'))) 

    pill2kill = threading.Event()
    recv_thread = threading.Thread(target = message_recv, args= (pill2kill, client_executor, addr))
    recv_thread.start()
    
    while msg != "exit":
        continue
    
    recv_thread.join()
    client_executor.close()
    print('Connection from %s:%s closed.' % addr)
        
    return

    

# 构建Socket实例、设置端口号  和监听队列大小
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('140.113.214.173', 10087))
listener.listen(5)
print('Waiting for connect...')

# 进入死循环，等待新的客户端连入。一旦有客户端连入，就分配一个线程去做专门处理。然后自己继续等待。
while True:
    client_executor, addr = listener.accept()
    t = threading.Thread(target=on_new_connection, args=(client_executor, addr))
    t.start()