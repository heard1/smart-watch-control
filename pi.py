from socket import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)


host = '0.0.0.0'
port = 666
bufsiz = 1024
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((host, port))
tcpSerSock.listen(5)


while True:
    print ('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('...connected from:', addr)
    while True:
        data = tcpCliSock.recv(bufsiz)
        data = data.decode()
        print(data)
        if not data:
            break
        #print(data)
        try:
        #[x,y] x=0,LED 
            res=[int(i) for i in data.split()]
        #LED 
            if res[0]==0 and res[1]==4:
                GPIO.output(3, GPIO.HIGH)
            if res[0]==0 and res[1]==3:
                GPIO.output(11, GPIO.HIGH)
            if res[0]==0 and res[1]==2:
                n=5
                while n!=0:
                    GPIO.output(3, GPIO.HIGH)
                    GPIO.output(11, GPIO.HIGH)
                    time.sleep(0.1)  
                    GPIO.output(3, GPIO.LOW)
                    GPIO.output(11, GPIO.LOW)
                    time.sleep(0.1)
                    n-=1 
            if res[0]==0 and res[1]==1:
                GPIO.output(3, GPIO.HIGH)
                GPIO.output(11, GPIO.HIGH)
            if res[0]==0 and res[1]==0:
                GPIO.output(3, GPIO.LOW)
                GPIO.output(11, GPIO.LOW)
        #FAN

        except:
            print('error!')
        
        tcpCliSock.send(bytes('sucess!',encoding='utf8'))
        
    tcpCliSock.close()
tcpSerSock.close()

'''
import RPi.GPIO as GPIO
import time
PIN_NO=3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
for x in range(500):
        GPIO.output(PIN_NO, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(PIN_NO, GPIO.LOW)
        time.sleep(2)
GPIO.cleanup()


10.189.176.151
srtpsrtp


import socket    
address = ('10.189.176.151', 666)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.connect(address)     
s.send(bytes('0 1',encoding='utf8'))
'''