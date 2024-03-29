import time
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import BernoulliNB_me as BB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD  # 降维
from sklearn.naive_bayes import BernoulliNB  # 伯努利分布的贝叶斯公式
from sklearn.metrics import f1_score, precision_score, recall_score
import joblib
from try2 import allWell
from try1 import allRight
## 设置字符集，防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

def let_go(test_alpha=0.2,ber_alpha=1.0,ber_binarize=0.005):
    # 1、文件数据读取
    df = pd.read_csv("D:/ALL_DATA/email/result_process02", encoding="utf-8", sep=",")
    df.dropna(axis=0, how="any", inplace=True)  # inplace直接在df上更改，any参数就是只要一个列的莫一个参数是nan就把他给删掉。all意识
    # 是该行的全部列都为nan时才给他删除。
    # 对样本进行分割
    # X_train,X_test, y_train, y_test =cross_validation.train_test_split(train_data,train_target,test_size=0.4, random_state=0)
    #
    # cross_validatio为交叉验证
    #
    # 参数解释：
    # train_data：所要划分的样本特征集
    # train_target：所要划分的样本结果
    # test_size：样本占比，如果是整数的话就是样本的数量
    # random_state：是随机数的种子。
    x_train, x_test, y_train, y_test = train_test_split(df[["has_date", "jieba_cut_content", "content_sema"]],
                                                        df["label"], test_size=test_alpha, random_state=0)
    print("训练集的个数:" + str(x_train.shape[0]))
    print("测试集的个数:" + str(x_test.shape[0]))

    transformer = TfidfVectorizer()  # norm=l2,表示l2归一化use_idf=True,TfidfVectorizer的作用是获得单个分词的权重
    svd = TruncatedSVD(n_components=25)  # 奇异值分解，降维
    jieba_cut_content = list(x_train["jieba_cut_content"].astype("str"))

    transformer_model = transformer.fit(jieba_cut_content)
    df1 = transformer_model.transform(jieba_cut_content)
    svd_model = svd.fit(df1)
    df2 = svd_model.transform(df1)  # 此处返回一个数组
    data = pd.DataFrame(df2)

    # 3.2、数据合并
    # data["has_date"] = list(x_train["has_date"])
    # data["content_sema"] = list(x_train["content_sema"])
    t1 = time.time()
    nb = BernoulliNB(alpha=ber_alpha, binarize=ber_binarize)  # 贝叶斯分类模型构建
    model = nb.fit(data, y_train)
    # dict,_list=BB.BernoulliNB_x(data,y_train)#!!!!!!!!!!!!!!!此处使用的是自己构建的贝叶斯算法，进行构建
    t = time.time() - t1
    print("贝叶斯模型构建时间为:%.5f ms" % (t * 1000))
    # 4.1 对测试数据进行转换
    jieba_cut_content_test = list(x_test["jieba_cut_content"].astype("str"))
    data_test = pd.DataFrame(svd_model.transform(transformer_model.transform(jieba_cut_content_test)))
    # data_test["has_date"] = list(x_test["has_date"])
    # data_test["content_sema"] = list(x_test["content_sema"])
    predict = []
    # 4.2 对测试数据进行测试

    # for i in range(data_test.shape[0]):
    #     xtest=data_test[i:i+1]
    #     one_predict = BB.predict(dict, _list, xtest,i)
    #     predict.append(one_predict)
    # y_predict=np.array(predict)
    y_predict = model.predict(data_test)
    # 5、效果评估
    _precision_score = precision_score(y_test, y_predict)
    _recall_score = recall_score(y_test, y_predict)
    _f1_score = f1_score(y_test, y_predict)
    print("准确率为:%.5f" % _precision_score)
    print("召回率为:%.5f" % _recall_score)
    print("F1值为:%.5f" % _f1_score)
    printlist = []
    printlist.append(_precision_score)
    printlist.append(_recall_score)
    printlist.append(_f1_score)
    writelist = ['precision', 'recall', 'f1']
    fig2,ax2=plt.subplots(1, 1)
    ax2.bar(writelist,printlist)
    for x, y in enumerate(printlist):
        plt.text(x, y + 0.02, '%.4f '%y, ha='center', fontsize=16)
    plt.show()
    # data = pd.Series(printlist, index=writelist)
    # data.plot(kind='barh', color='k')
    plt.show()
    correct = np.equal(y_predict, y_test)
    p1 = 0
    p2 = 0
    prdeictlist = []
    j = 0
    for i in correct:
        j += 1
        if i == True:
            p1 += 1
        elif i == False:
            p2 += 0
        corr = (p1 * 1.0) / j
        if j % 100 == 0:
            prdeictlist.append(corr)
    prdeictlist.append(corr)
    predictarray = np.array(prdeictlist)
    fig1, ax1 = plt.subplots(1, 1)
    s = pd.Series(predictarray, index=np.arange(0, j, 100))
    s.plot(ax=ax1)
    ax1.set_title("测试样本数为"+str(y_predict.shape[0]))
    plt.show()
    joblib.dump(model,"model.pkl")

if __name__ == '__main__':
    print("是否对数据重新进行特征提取,请输入1/0:")
    yon=int(input())
    if yon==1:
        print("请稍等，该过程时间较长，大约五分钟。")
        allWell()
        allRight()
    elif yon==0:
        print("将使用过去提取的特征构建贝叶斯模型")
    print("**********邮件模型准备开始构建**********")
    print("请输入测试集和训练集的比例:")
    test_alpha = float(input())
    print("请输入构建贝叶斯的平滑因子alpha:")
    ber_aplha = float(input())
    print("请输入构建贝叶斯的阈值:")
    ber_binarize = float(input())
    print("**********邮件模型开始构建**********")
    let_go(test_alpha, ber_aplha, ber_binarize)
