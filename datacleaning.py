import random

import pandas as pd
import numpy as np
import jieba
import os
word_month = []
word_school = []
import matplotlib.pylab as plt
def datacleaning(filename):
    file = open(filename)
    index_file = filename.find("数据")
    data = pd.read_csv(file).astype(str)
    data = data.dropna(how='all')
    time_list = list(data['times'].drop_duplicates())
    data_group = data.groupby(data['times'])
    for time_tag in time_list:
        data_content = data_group.apply(lambda df:df.to_dict(orient='records'))[time_tag]
        for contents in data_content:
            text = contents['content']
            count_word(text,"month")
            # dict1 = {time_tag: la}
    count_word(''.join([x[0] for x in word_month]),"school")
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 图中文字体设置为黑体
    plt.rcParams['axes.unicode_minus'] = False  # 负值显示
    fig = plt.figure(figsize=(8, 6))  # 新建画布
    ax = plt.subplot(1, 1, 1)  # 子图初始化
    ax.set_title("热词频率散点图")
    ax.set_xlabel("关键词")
    ax.set_ylabel("频率")
    for i in range(6):
        word_x = word_school[i][0]
        count_y = word_school[i][1]
        ax.scatter(word_x, count_y)  # 绘制散点图
    plt.savefig(filename[:index_file]+".png")
    plt.show()

def count_word(text,tag):
    words = jieba.lcut(text)
    count = {}
    for word in words:  # 使用 for 循环遍历每个词语并统计个数
        if len(word) < 2:  # 排除单个字的干扰，使得输出结果为词语
            continue
        else:
            count[word] = count.get(word, 0) + 1
    exclude = ["学院", "学生", "下午", '...']
    for key in list(count.keys()):  # 遍历字典的所有键，即所有word
        if key in exclude:
            del count[key]  # 删除字典中键为无关词语的键值对
    lista = list(count.items())
    lista.sort(key=lambda x:x[1], reverse=True)
    if(len(lista)>6):
        for i in range(6):  # 此处统计排名前五的单词，所以range(5)
            if (tag == "school"):
                word_school.append(lista[i])
            else:
                word_month.append(lista[i])
if __name__ == "__main__":
    path = 'E:\PycharmProjects\sdwu_branch'
    filedir = os.listdir(path)
    for filename in filedir:
        if (filename.find('数据') > 0):
            word_month.clear()
            word_school.clear()
            datacleaning(filename)
    exit()

