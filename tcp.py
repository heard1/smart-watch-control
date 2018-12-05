#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:53:25 2018

@author: lisicong
"""
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Activation
import keras
import numpy as np
import socket
from socket import *

import link

from pynput.keyboard import Key, Controller
keyboard = Controller()

host = '0.0.0.0'
port = 2334
bufsiz = 1024
flag=0
res0=[]
U=[]
direct='empty'

count=0

def Screen(direct):
    if direct=='down':
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    if direct=='up':
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    if direct=='left':
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    if direct=='right':
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    if direct=='push':
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        

def Car(direct):
    res=''
    if direct=='down':
        res='2'
    if direct=='up':
        res='1'
    if direct=='left':
        res='3'
    if direct=='right':
        res='4'
    if direct=='push':
        res='5'

    address = ('192.168.43.97', 2333)  
    s = socket(AF_INET, SOCK_STREAM)  
    try:
        s.settimeout(10)
        s.connect(address)
        s.send(bytes(res,encoding='utf8'))
        #print('car success!',res)
    except:
        #print('Pi error!',res)
        return


def pi(direct):
    res=''
    res+='0'
    if direct=='down':
        res+=' 0'
    if direct=='up':
        res+=' 1'
    if direct=='push':
        res+=' 2'
    if direct=='left':
        res+=' 3'
    if direct=='right':
        res+=' 4'

    address = ('192.168.3.10', 667)  
    s = socket(AF_INET, SOCK_STREAM)  
    try:
        s.connect(address)
        s.send(bytes(res,encoding='utf8'))
        print('Pi success!',res)
    except:
        print('Pi error!',res)



#numm=0
#path='/Users/admin/Desktop/SRTP/up/0.txt'
#开启套接字
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#绑定服务端口
tcpSerSock.bind((host, port))
#开始监听
tcpSerSock.listen(5)
model = load_model('model.h5')
while True:
    #等待客户端连接
    print ('waiting for connection...')
    res0.clear()
    flag=0
    count=0
    tcpCliSock, addr = tcpSerSock.accept()
    print ('...connected from:', addr)
    while True:
        #接收客户端信息
        data = tcpCliSock.recv(bufsiz)
        data = data.decode()
        if not data:
            break
        #客户端信息
        #print(count,data)
        count+=1
        try:
            if flag==0:
                A=[float(i) for i in data.split()]
                if len(A)==6:
                    continue
                U=A[0]
                flag=1
                res0.clear()
                continue
            else:
                A=[float(i) for i in data.split()]
                if(len(A)==1):
                    U=A[0]
                    res0.clear()
                    continue
                res0+=A
        except:
            res0+=[0,0,0,0,0,0]
        if len(res0)>=300:
            res0=res0[:300]
            tem=[res0]
            tem=np.array(tem)
            ret=model.predict(tem)
            ret=ret[0].tolist()
            i=ret.index(max(ret))
            if i==0:
                direct='left'
            if i==1:
                direct='right'
            if i==2:
                direct='up'
            if i==3:
                direct='down'
            if i==4:
                direct='push'
            print(U,direct)
            if U==3:
                Screen(direct)
            if U==2:
                Car(direct)
            if U==1:
                link.bulb(direct)
            res0.clear()
            flag=0
            count=0
            #path='/Users/admin/Desktop/SRTP/up/'+str(numm)+'.txt'
            #numm+=1
        #'''
        #f=open(path,'a')
        #f.write(data)
        #f.close()
        tcpCliSock.send(bytes(direct,encoding='utf8'))
        direct='empty'
        if(len(res0)>300):
            res0.clear()
    tcpCliSock.close()
tcpSerSock.close()