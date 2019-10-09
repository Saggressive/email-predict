import re
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import jieba
## 设置字符集，防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False
# 1、文件数据读取
df = pd.read_csv("D:/ALL_DATA/email/result/result", sep=",", header=None,
                 names=["from", "to", "date", "content", "label"])#返回一个dataframe类型数据。该文件的列索引为"from", "to", "date", "content", "label"
# print(df.head())
def extract_email_server_address(str1):
    it=re.findall(r"@([a-zA-Z0-9]*\.[a-zA-Z0-9\.]+)",str(str1))#用正则表达提取网址每次返回一个网址的列表，虽然列表只有一个元素。
    result=""
    if len(it)>0:
        result+=it[0]
    if not result:
        result="unkown"
    return result
df["to_address"]=pd.Series(map(lambda str:extract_email_server_address(str),df["to"]))#map返回一个列表
df["from_address"]=pd.Series(map(lambda str:extract_email_server_address(str),df["from"]))
def extract_email_date(str1):#提取邮件的时间
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
        # 2005-9-2 上午10:55，在此为了匹配特殊格式的时间
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
        # Sep 23 2005 1:04 AM，在此为了匹配特殊格式的时间
        week = "S"
        hour = "01"
        time_quantum = "3"
        pass
    elif str_len == 21:
        # August 24 2005 5:00pm，在此为了匹配特殊格式的时间
        week = "W"
        hour = "17"
        time_quantum = "1"
        pass
    else:
        # 匹配一个字符开头，+表示至少一次  \d 表示数字   ？表示可有可无  *? 非贪婪模式
        rex = r"([A-Za-z]+\d?[A-Za-z]*) .*?(\d{2}):\d{2}:\d{2}.*"
        it = re.findall(rex, str1)#返回一个一元素的列表，列表的值为二元组，eg[('Sun', '07')]
        if len(it) == 1 and len(it[0]) == 2:#判断返回的列表是否为一个元素，且为一元组
            week = it[0][0][-3]#it是一个列表，而it[0]在这是一个元组，it[0][0]元组的一个值为星期，[-3]表示星期的首之母
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
df["has_date"] = df.apply(lambda c: 0 if c["date_week"] == "unknown" else 1,axis=1)
df["content"] = df["content"].astype("str")
#***********************************************************************************
df["jieba_cut_content"] = list(map(lambda st:" ".join(jieba.cut(st)),df["content"])) # 分开的词用空格隔开
print("_______________________________________________________________________")
print(df["jieba_cut_content"].head(5))
print(df.head(2))
def process_content_length(lg):
    if lg < 10:
        return 0
    elif lg <= 100:
        return 1
    elif lg <= 500:
        return 2
    elif lg <= 1000:
        return 3
    elif lg <= 1500:
        return 4
    elif lg <= 2000:
        return 5
    elif lg <= 2500:
        return 6
    elif lg <= 3000:
        return 7
    elif lg <= 4000:
        return 8
    elif lg <= 5000:
        return 9
    elif lg <= 10000:
        return 10
    elif lg <= 20000:
        return 11
    elif lg <= 30000:
        return 12
    elif lg <= 50000:
        return 13
    else:
        return 14

list1 =[]
for i in range(len(df["content"])):
    if(type(df["content"].values[i])!=float):#邮件的内容为空，即为nan时,nan是一个float类型
        long = len(df["content"].values[i])
    else:
        print(df["content"].values[i])
        long=0
    list1.append(long)
df["content_length"] = pd.Series(list1)#得到长度的dataframe
#print(map(lambda st: print(str(len(st))+'\n'),str(df["content"])))
df["content_length_type"] = pd.Series(map(lambda st: process_content_length(st), df["content_length"]))
# 按照邮件长度类别和标签进行分组groupby，抽取这两列数据相同的放到一起，
# 用agg和内置函数count聚合不同长度邮件分贝是否为垃圾邮件的数量,
# reset_insex:将对象重新进行索引的构建
df2 = df.groupby(["content_length_type", "label"])["label"].agg(["count"]).reset_index()#df.groupby(["content_length_type", "label"])后
#"content_length_type", "label"变为行索引名称，.reset_index()让其重新变为列索引
# label == 1：是垃圾邮件，对长度和数量进行重命名，count命名为c1
df3 = df2[df2.label == 1][["content_length_type", "count"]].rename(columns={"count": "c1"})
df4 = df2[df2.label == 0][["content_length_type", "count"]].rename(columns={"count": "c2"})
df5 = pd.merge(df3, df4)  # 数据集的合并，pandas.merge可依据一个或多个键将不同DataFrame中的行连接起来
print("*****************************************************************")
print(df5.head(5))
df5["c1_rage"] = df5.apply(lambda r: r["c1"] / (r["c1"] + r["c2"]), axis=1)  # 按行进行统计,每个长度类型，垃圾邮件和普通邮件的比例
df5["c2_rage"] = df5.apply(lambda r: r["c2"] / (r["c1"] + r["c2"]), axis=1)
plt.plot(df5["content_length_type"],df5["c1_rage"],label=u"垃圾邮件比例")
plt.plot(df5["content_length_type"],df5["c2_rage"],label=u"正常邮件比例")
plt.xlabel(u"邮件长度标记")
plt.ylabel(u"邮件比例")
plt.grid(True)
plt.legend(loc=0)
plt.savefig("垃圾和正常邮件比例.png")
plt.show()
def precess_content_sema(x):
    if x > 10000:
        return 0.5 / np.exp(np.log10(x) - np.log10(500)) + np.log(abs(x - 500) + 1) - np.log(abs(x - 10000)) + 1
    else:
        return 0.5 / np.exp(np.log10(x) - np.log10(500)) + np.log(abs(x - 500) + 1) + 1


a = np.arange(1, 20000)
plt.plot(a, list(map(lambda t: precess_content_sema(t), a)), label=u"信息量")
plt.grid(True)
plt.legend(loc=0)
plt.savefig("信息量.png")
plt.show()
#根据长度添加信号量
df["content_sema"] = list(map(lambda st: precess_content_sema(st), df["content_length"]))
print(df.head(2))
# 查看列名称和列的数据类型
print(df.dtypes)

# 获取需要的列,drop删除不需要的列
df.drop(["from", "to", "date", "content", "to_address", "from_address",
         "date_week", "date_hour", "date_time_quantum", "content_length",
         "content_length_type"], 1, inplace=True)
print(df.info())#返回df的信息包括名称，数目，类型
print(df.head())
##此时的df就只有label,has_date,jieba_cut_content,content_sema，label是否是垃圾邮件，has_date是否有星期这个属性，如果没有就是垃圾邮件，
#jieba_cut就是对邮件内容进行分词后的结果，content_sema信号量（为邮件长度添加的）
#结果输出到CSV文件中
df.to_csv("D:/ALL_DATA/email/result_process02", encoding="utf-8", index=False)
