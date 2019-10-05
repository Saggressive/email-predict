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
print(type(df))
# 5、特征工程之四 =>邮件长度对是否是垃圾邮件的影响
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
for i in range(64620):
    if(type(df["content"].values[i])!=float):#邮件的内容为空，即为nan时
        long = len(df["content"].values[i])
    else:
        print(df["content"].values[i])
        long=0
    list1.append(long)
df["content_length"] = pd.Series(list1)
#print(map(lambda st: print(str(len(st))+'\n'),str(df["content"])))
df["content_length_type"] = pd.Series(map(lambda st: process_content_length(st), df["content_length"]))
# 按照邮件长度类别和标签进行分组groupby，抽取这两列数据相同的放到一起，
# 用agg和内置函数count聚合不同长度邮件分贝是否为垃圾邮件的数量,
# reset_insex:将对象重新进行索引的构建
df2 = df.groupby(["content_length_type", "label"])["label"].agg(["count"]).reset_index()#df.groupby(["content_length_type", "label"])后
#"content_length_type", "label"变为行索引名称，.reset_index()让其重新变为列索引
print("************************\n")
print(df2)
# label == 1：是垃圾邮件，对长度和数量进行重命名，count命名为c1
df3 = df2[df2.label == 1][["content_length_type", "count"]].rename(columns={"count": "c1"})
df4 = df2[df2.label == 0][["content_length_type", "count"]].rename(columns={"count": "c2"})
print(df3)
df5 = pd.merge(df3, df4)  # 数据集的合并，pandas.merge可依据一个或多个键将不同DataFrame中的行连接起来

df5["c1_rage"] = df5.apply(lambda r: r["c1"] / (r["c1"] + r["c2"]), axis=1)  # 按行进行统计
df5["c2_rage"] = df5.apply(lambda r: r["c2"] / (r["c1"] + r["c2"]), axis=1)
print(df5.head(5))

# 画图
plt.plot(df5["content_length_type"], df5["c1_rage"], label=u"垃圾邮件比例")
plt.plot(df5["content_length_type"], df5["c2_rage"], label=u"正常邮件比例")
plt.xlabel(u"邮件长度标记")
plt.ylabel(u"邮件比例")
plt.grid(True)
plt.legend(loc=0)
plt.savefig("垃圾和正常邮件比例.png")
plt.show()





