from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import plot_model
import keras
import numpy as np

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=300))
model.add(Dense(10, activation='relu'))
model.add(Dense(5, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 生成数据
data1 = np.random.random((500, 300))
#labels = np.random.randint(5, size=(500, 1))
#one_hot_labels = keras.utils.to_categorical(labels, num_classes=5)
#model.fit(data, one_hot_labels, epochs=20, batch_size=10)
data=[]
num=0
for i in range(100):
    path='/Users/admin/Desktop/srtp/left/'+str(num)+'.txt'
    f=open(path,'r')
    a=f.read()
    a=a.split()
    b=[float(i) for i in a]
    while len(b)<300:
        b.append(0)
    if len(b)>300:
        b=b[:300]
    data.append(b)
    num+=1


num=0
for i in range(100):
    path='/Users/admin/Desktop/srtp/right/'+str(num)+'.txt'
    f=open(path,'r')
    a=f.read()
    a=a.split()
    b=[float(i) for i in a]
    while len(b)<300:
        b.append(0)
    if len(b)>300:
        b=b[:300]
    data.append(b)
    num+=1   

    
num=0
for i in range(100):
    path='/Users/admin/Desktop/srtp/up/'+str(num)+'.txt'
    f=open(path,'r')
    a=f.read()
    a=a.split()
    b=[float(i) for i in a]
    while len(b)<300:
        b.append(0)
    if len(b)>300:
        b=b[:300]
    data.append(b)
    num+=1    

num=0
for i in range(100):
    path='/Users/admin/Desktop/srtp/down/'+str(num)+'.txt'
    f=open(path,'r')
    a=f.read()
    a=a.split()
    b=[float(i) for i in a]
    while len(b)<300:
        b.append(0)
    if len(b)>300:
        b=b[:300]
    data.append(b)
    num+=1   
    
num=0
for i in range(100):
    path='/Users/admin/Desktop/srtp/push/'+str(num)+'.txt'
    f=open(path,'r')
    a=f.read()
    a=a.split()
    b=[float(i) for i in a]
    while len(b)<300:
        b.append(0)
    if len(b)>300:
        b=b[:300]
    data.append(b)
    num+=1

data=np.array(data)
#data=[np.array(i) for i in data]
#data=np.array(data, dtype=np.float32)

a=np.full((100),0)
b=np.full((100),1)
label=np.append(a,b)
c=np.full((100),2)
label=np.append(label,c)
d=np.full((100),3)
label=np.append(label,d)
e=np.full((100),4)
label=np.append(label,e)
label = keras.utils.to_categorical(label, num_classes=5)

model.fit(data, label, epochs=20, batch_size=10)

res=[]
for layer in model.layers:
    res.append(layer.get_weights())
one=res[0][0]
two=res[1][0]
model.save('model.h5') 
plot_model(model, to_file='model.png')