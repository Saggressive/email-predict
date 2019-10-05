import re
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from functools import reduce
def BernoulliNB_x(df,y_train):
    df[df<=0.005]=0
    df[df>0.005]=1
    df[df.shape[1]]=y_train
    y_0=y_train[y_train==0].count()
    y_1=y_train[y_train==1].count()
    Py0=(y_0+1.0)/(y_0+y_1+2.0)#此处添加的是平滑因子，防止出现概率为0的情况
    Py1=1-Py0
    list=[]
    list.append(Py0)
    list.append(Py1)
    dict={}
    df.dropna(axis=0, how='any')
    print(df.head(10))
    for i in range(df.shape[1]-1):
        dfx0=df[df[i]==0]
        dfx0y1=dfx0[dfx0[df.shape[1]-1]==1]#为1就是垃圾邮件
        Px0y1=(dfx0y1.shape[0]+1)*1.0/(y_1+df.shape[1]-1)*1.0
        Px1y1=1-Px0y1
        dfx0y0=dfx0[dfx0[df.shape[1]-1]!=1]#不为垃圾邮件
        Px0y0=(dfx0y0.shape[0]+1)*1.0/(y_0+df.shape[1]-1)*1.0
        Px1y0=1-Px0y0
        dict["Px0y1"+str(i)]=Px0y1
        dict["Px1y1"+str(i)]=Px1y1
        dict["Px0y0"+str(i)]=Px0y0
        dict["Px1y0"+str(i)]=Px1y0
    return dict,list
def predict(dict,list1,data,j):
    list2=[]
    list3=[]
    data=data.copy()
    data[data <= 0.005] = 0
    data[data > 0.005] = 1
    for i in range(data.shape[1]):
        if data[i][j]==0:
            list2.append(dict["Px0y0"+str(i)])
            list3.append(dict["Px0y1"+str(i)])
        elif data[i][j]==1 :
            list2.append(dict["Px1y0" + str(i)])
            list3.append(dict["Px1y1" + str(i)])
    p0=reduce(lambda x, y: x * y, list2)#list2
    p1=reduce(lambda x, y: x * y, list3)
    p0=p0*list1[0]
    p1=p1*list1[1]
    if(p1>p0):
        return 1.
    else:
        return 0.
# data={0:[0,2,3,4,5,6],1:[2,3,4,5,6,7]}
# df=pd.DataFrame(data)
# print(df)
# df1=df[0:1]
# train=pd.Series(data[0])
# t1=train[:1]
# dict,list=BernoulliNB_x(df,train)
# predict(dict,list,df1,t1[0])