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
                 names=["from", "to", "date", "content", "label"])#dataframe框架结构
# def extract_email_date(str1):
#     if not isinstance(str1,str):
#         str1=str(str1)
#     len_str=len(str1)
#     week=""
#     hour=""
#     time_quantum=""
#     if len_str<10:
#         week="unknow"
#         hour="unknow"
#         time_quantum="unknown"
#     elif len_str==16:
#         rex=r"(\d{2}):\d{2}"
#         it=re.findall(rex,str1)
#         if len(it)==1:
#             hour = it[0]
#         else:
#             hour = "unknown"
#         week = "Fri"
#         time_quantum = "0"
#     elif len_str==19:
#         week="Sep"
#         hour="01"
#         time_quantum="3"
#     elif len_str==21:
#         week="Wed"
#         hour="17"
#         time_quantum="1"
#     else:
#         #r"([A-Za-z]+\d?[A-Za-z]*) .*?(\d{2}):\d{2}:\d{2}.*"
#         #r"([A-Za-z]+\d+?[A-Za-z]*).*?(\d{2}):\d{2}:\d{2}.*"
#         rex=r"([A-Za-z]+\d*?[A-Za-z]*).*?(\d{2}):\d{2}:\d{2}.*"
#         it=re.findall(rex,str1)
#         if len(it)==1 and len(it[0])==2:
#             week=it[0][0][-3]
#             hour=it[0][1]
#             int_hour=int(hour)
#             if int_hour<8:
#                 time_quantum="3"
#             elif int_hour<13:
#                 time_quantum="0"
#             elif int_hour<19:
#                 time_quantum="1"
#             else:
#                 time_quantum="2"
#         else:
#             week="unknown"
#             hour="unknown"
#             time_quantum="unknown"
#     week=week.lower()
#     hour=hour.lower()
#     time_quantum=time_quantum.lower()
#     return (week,hour,time_quantum)
# data_time_extract_result=list(map(lambda  st:extract_email_date(st),df["date"]))
# df["date_week"]=pd.Series(map(lambda t:t[0],data_time_extract_result))
# df["date_hour"]=pd.Series(map(lambda t:t[1],data_time_extract_result))
# df["date_time_quantum"] = pd.Series(map(lambda t:t[2],data_time_extract_result))
# print(df.head(2))
# print("=======星期属性字段描述======")
# print(df.date_week.value_counts().head(3))
# print(df[["date_week", "label"]].groupby(["date_week", "label"])["label"].count())
#
# print("=======小时属性字段描述======")
# print(df.date_hour.value_counts().head(3))
# print(df[['date_hour', 'label']].groupby(['date_hour', 'label'])['label'].count())
#
# print("=======时间段属性字段描述======")
# print(df.date_hour.value_counts().head(3))
# print(df[["date_time_quantum", "label"]].groupby(["date_time_quantum", "label"])["label"].count())
#
# # 添加是否有时间
# df["has_date"] = df.apply(lambda c: 0 if c["date_week"] == "unknown" else 1, axis=1)
# print(df.head(2))
#
def extract_email_date(str1):
    if not isinstance(str1, str):  # 判断变量是否是str类型
        str1 = str(str1)  # str类型的强转
    str_len = len(str1)

    week = ""
    hour = ""
    # 0表示：上午[8,12]；1表示：下午[13,18]；2表示：晚上[19,23]；3表示：凌晨[0,7]
    time_quantum = ""

    if str_len < 10:
        # unknown
        week = "unknown"
        hour = "unknown"
        time_quantum = "unknown"
        pass
    elif str_len == 16:
        # 2005-9-2 上午10:55
        rex = r"(\d{2}):\d{2}"  # \d  匹配任意数字,这里匹配10:55
        it = re.findall(rex, str1)
        if len(it) == 1:
            hour = it[0]
        else:
            hour = "unknown"
        week = "F"
        time_quantum = "0"
        pass
    elif str_len == 19:
        # Sep 23 2005 1:04 AM
        week = "S"
        hour = "01"
        time_quantum = "3"
        pass
    elif str_len == 21:
        # August 24 2005 5:00pm
        week = "W"
        hour = "17"
        time_quantum = "1"
        pass
    else:
        # 匹配一个字符开头，+表示至少一次  \d 表示数字   ？表示可有可无  *? 非贪婪模式
        rex = r"([A-Za-z]+\d?[A-Za-z]*) .*?(\d{2}):\d{2}:\d{2}.*"
        it = re.findall(rex, str1)
        if len(it) == 1 and len(it[0]) == 2:
            print(it[0])
            week = it[0][0][-3]#it是一个列表，而it[0]在这是一个元组，it[0][0]元组的一个值为星期
            hour = it[0][1]
            int_hour = int(hour)
            if int_hour < 8:
                time_quantum = "3"
            elif int_hour < 13:
                time_quantum = "0"
            elif int_hour < 19:
                time_quantum = "1"
            else:
                time_quantum = "2"
            pass
        else:
            week = "unknown"
            hour = "unknown"
            time_quantum = "unknown"
    week = week.lower()
    hour = hour.lower()
    time_quantum = time_quantum.lower()
    return (week, hour, time_quantum)


# 数据转换
data_time_extract_result = list(map(lambda st: extract_email_date(st), df["date"]))
df["date_week"] = pd.Series(map(lambda t: t[0], data_time_extract_result))
df["date_hour"] = pd.Series(map(lambda t: t[1], data_time_extract_result))
df["date_time_quantum"] = pd.Series(map(lambda t: t[2], data_time_extract_result))
print(df.head(2))
print(df["date_week"])
print("=======星期属性字段描述======")
print(df.date_week.value_counts().head(3))
print(df[["date_week", "label"]].groupby(["date_week", "label"])["label"].count())
print("********************************")
print("=======小时属性字段描述======")
print(df.date_hour.value_counts().head(3))
print(df[['date_hour', 'label']].groupby(['date_hour', 'label'])['label'].count())

print("=======时间段属性字段描述======")
print(df.date_time_quantum.value_counts().head(3))
print(df[["date_time_quantum", "label"]].groupby(["date_time_quantum", "label"])["label"].count())
print("**************************************************************")
print(df.groupby(["date_time_quantum", "label"])["label"].count())
# 添加是否有时间
df["has_date"] = df.apply(lambda c: 0 if c["date_week"] == "unknown" else 1, axis=1)
print(df.head(2))
