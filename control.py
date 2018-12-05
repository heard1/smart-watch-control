import socket
from socket import *
#import link

from pynput.keyboard import Key, Controller
keyboard = Controller()

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
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        
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

    address = ('192.168.6.224', 2333)  
    s = socket(AF_INET, SOCK_STREAM)  
    try:
        s.settimeout(10)
        print('try')
        s.connect(address)
        print('try2')
        s.send(bytes(res,encoding='utf8'))
        #print('car success!',res)
    except:
        #print('Pi error!',res)
        print('fail')
        return

flag=1
while True:
    x=input("light --0\ncar ↑ --1\ncar ↓ --2\ncar ← --3\ncar → --4\n")
    if x==0:
        if flag==1:
            link.bulb('up')
        if flag==-1:
            link.bulb('down')
        flag=-flag
    if x==1:
        Car('up')
    if x==2:
        Car('down')
    if x==3:
        Car('left')
    if x==4:
        Car('right')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

