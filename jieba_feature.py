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
                 names=["from", "to", "date", "content", "label"])#dataframe框架结构
# 4、特征工程之三 => jieba分词操作

# 将文本类型全部转换为str类型，然后进行分词操作
df["content"] = df["content"].astype("str")

'''
#1、jieba分词的重点在于：自定义词典
#2、jieba添加分词字典，jieba.load_userdict("userdict.txt"),字典格式为：单词 词频(可选的) 词性(可选的)
#   词典构建方式：一般都是基于jieba分词之后的效果进行人工干预
#3、添加新词、删除词   jieba.add_word("")   jieba.del_word("")    
#4、jieba.cut: def cut(self, sentence, cut_all=False, HMM=True)
#   sentence:需要分割的文本，cut_all:分割模式，分为精准模式False、全分割True，HMM：新词可进行推测
#5、长文本采用精准分割，短文本采用全分割模式
#   一般在短文本处理过程中还需要考虑词性，并且还可能将分割好的单词进行组合
#   词性需要导入的包：import jieba.posseg
'''
df["jieba_cut_content"] = list(map(lambda st:" ".join(jieba.cut(st)),df["content"])) # 分开的词用空格隔开
print(df.head(2))
