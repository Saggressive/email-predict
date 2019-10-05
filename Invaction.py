import os
def read_index_file(file_path):#返回每个邮件得情况，是否为垃圾邮件
    _dict={"spam":"1","ham":"0"}#spam:1是垃圾邮件,ham：0不为垃圾邮件
    file=open(file_path)#打开标签文件，标签文件的内容为每个样本是否为垃圾邮件的判断
    my_dict={}
    for line in file:
        arr=line.split(" ")#01标签和其所在得文件夹地址之间有空格，使用split（）分割，产生一个队列。eg.['spam', '../data/215/082\n']
        if len(arr)==2:
            key,value=arr
            value=value.replace("../data","").replace("\n","")#替换
            my_dict[value]=_dict[key.lower()]#打上标签，spam:1是垃圾邮件,ham：0不为垃圾邮件
    file.close()
    return my_dict
#from to date
def read_file(file_path):
    file=open(file_path,"r",encoding="gb2312",errors="ignore")
    content_dic={}
    flag=False
    for line in file:
        line=line.strip()#用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
        if line.startswith("From:"):#获取发送人地址
            content_dic["from"]=line[5:]
        elif line.startswith("To:"):#获取接收地址
            content_dic["to"]=line[3:]
        elif line.startswith("Date:"):#获取日期
            content_dic["date"]=line[5:]
        elif not line:#读入空行，就说明开始准备处理邮件得内容
            flag=True
        if flag:
            if "content" in content_dic:
                content_dic["content"]+=line
            else:
                content_dic["content"]=line
    file.close()
    return content_dic
def process_file(filepath):
    content_dic=read_file(filepath)
    result=content_dic.get("from","unkonw").replace(",","").replace("，","").strip()+','#读取出每个from标签，将豆号和末尾的换行去掉，加上豆号
    result+=content_dic.get("to","unkonw").replace(",","").replace("，","").strip()+','
    result+=content_dic.get("date","unkonw").replace(",","").replace("，","").strip()+','
    result+=content_dic.get("content","unkonw").replace(",","").replace("，","").strip()
    return result
index_dict=read_index_file("D:/ALL_DATA/email/data/full/index")
line1=os.listdir("D:/ALL_DATA/email/data")#获取data文件夹下的文件目录，队列得形式返回
for list1 in line1:
    filepath_1="D:/ALL_DATA/email/data/"+list1
    print('开始处理文件夹:' + filepath_1)
    line2=os.listdir(filepath_1)
    write_file_path = 'D:/ALL_DATA/email/produce/' + list1#处理完后得存储路径，比如000文件夹地所有信息全部存储到000.txt
    with open(write_file_path,"w",encoding='utf-8') as writter:
        for list2 in line2:
            filepath_2=filepath_1+'/'+list2#具体一封邮件得地址
            index_key='/'+list1+'/'+list2
            if index_key in index_dict:
                content_str=process_file(filepath_2)#获取日期，收发人，邮件内容
                content_str=content_str+','+index_dict[index_key]+'\n'#是否为垃圾的标签，即为0和1.
                writter.writelines(content_str)
filepath="D:/ALL_DATA/email/result/result"
with open(filepath,"w",encoding="utf-8") as writter:#
    for list1 in line1:
        _filepath = "D:/ALL_DATA/email/produce/" +list1
        print("开始合并文件:" + _filepath)
        with open(_filepath,"r",encoding="utf-8") as file:
            for list2 in file:
                writter.writelines(list2)#将所有提取的信息整合到rusult这个文件夹里


