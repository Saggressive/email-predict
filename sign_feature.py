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


# 6、特征工程之五 ==> 添加信号量
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

df["content_sema"] = list(map(lambda st: precess_content_sema(st), df["content_length"]))
print(df.head(2))
