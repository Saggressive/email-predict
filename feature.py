import re
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

## 设置字符集，防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

# 1、文件数据读取
df = pd.read_csv("D:/ALL_DATA/email/result/result", sep=",", header=None,
                 names=["from", "to", "date", "content", "label"])
# print(df.head())
def extract_email_server_address(str1):
    it=re.findall(r"@([a-zA-Z0-9]*\.[a-zA-Z0-9\.]+)",str(str1))
    result=""
    print(it)
    if len(it)>0:
        result+=it[0]
    if not result:
        result="unkown"
    return result
df["to_address"]=pd.Series(map(lambda str:extract_email_server_address(str),df["to"]))
df["from_address"]=pd.Series(map(lambda str:extract_email_server_address(str),df["from"]))
print("=================to address================")
print(df.to_address.value_counts().head(5))
print("邮件接收服务器接收类别数量:"+str(df.to_address.unique().shape))
print(("===============from address================"))
print((df.from_address.value_counts().head(5)))
print("邮件发送服务器发送类别数量:"+str(df.from_address.unique().shape))
from_address_df=df.from_address.value_counts().to_frame()
less_ten=from_address_df[from_address_df.from_address<=10].shape
print("发送邮件数量小于10封的服务器数量为:"+str(less_ten))


