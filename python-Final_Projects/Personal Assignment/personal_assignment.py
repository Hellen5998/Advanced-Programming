# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import os
from os import listdir
import jieba
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
'''

所有者：李响
用于爬取百度百科词条“李响”搜索结果前30页内容并进行文本聚类;
结果以[label_0]：文件名1...n；
     [label_1]:文件名1...n；
     ...
     [label_9]:文件名1...n形式呈现;
爬取文本以txt格式存至D:\Parse\lixiang\+标题名+.txt;
停用词存至D:\Parse\stopword.txt;

'''

'''判断页面元素是否存在的函数'''
def is_element_exist(css):
    try:
        browser.find_element_by_tag_name(css)
        return True
    except:
        return False
def is_class_para(classname):
    elems_div=browser.find_elements_by_tag_name('div')
    for elem_div in elems_div:
        if elem_div.get_attribute('class')==classname: return True
    return False

'''程序入口'''
if __name__ == "__main__":
    if not os.path.exists("D:\\Parse\\lixiang"):
            os.mkdir("D:\\Parse\\lixiang")       #避免文件重复
    browser=webdriver.Chrome()
    browser.get('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E6%9D%8E%E5%93%8D&rsv_pq=e9eac30b000042d1&rsv_t=900evnw09NlwnP87hdCecRuUTGXjtpWCuFkyIAodAiLNPQLVEL%2BM2ZdPLPE&rqlang=cn&rsv_enter=1&rsv_sug3=6&rsv_sug1=5&rsv_sug7=100&rsv_sug2=0&inputT=3328&rsv_sug4=3329')
    i=0
    while(i<30):    #抓取搜索结果前30页文本
        i=i+1
        '''开始依次抓取'''
        elems=browser.find_elements_by_class_name('t')
        for elem in elems:
            print("正在抓取文章："+elem.text+"...")   #抓取进程可视化
            title=elem.text
            title=title.replace('?','').replace('/','').replace('<','').replace('>','').replace('|','').replace('*','').replace('"','')    #避免文件名禁用符
            elem.find_element_by_tag_name('a').click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[-1])
            if is_class_para('para'):
                elems_div=browser.find_elements_by_class_name('para')
                for elem_div in elems_div:
                    #print(elem_div.text)
                    with open('D:\\Parse\\lixiang/'+title+'.txt',"a",encoding='utf-8') as f:  #将正文内容写入文件，文件名为链接列表名
                        f.write(elem_div.text)
                        f.write('\n')
            elif is_element_exist('p'):
                elems_p=browser.find_elements_by_tag_name('p')
                for elem_p in elems_p:
                    #print(elem_p.text)
                    with open('D:\\Parse\\lixiang/'+title+'.txt',"a",encoding='utf-8') as f:  #将正文内容写入文件，文件名为链接列表名
                        f.write(elem_p.text)
                        f.write('\n')
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        browser.find_elements_by_class_name('n')[-1].click()
        time.sleep(3)
        browser.switch_to.window(browser.window_handles[0])
    '''分析抓取结果'''
    all_file=listdir('D:/Parse/lixiang')
    for file in all_file:
            if os.path.getsize(os.path.join("D:/Parse/lixiang", file)) == 0:  #删除空文件
                os.remove(os.path.join("D:/Parse/lixiang", file))
    labels=[] #搜索结果列表
    corpus=[] #空语料库
    '''过滤停用词'''
    typetxt=open('D:/Parse/stopwords.txt')
    texts=['\u3000','\n',' '] #爬取的文本中未处理的特殊字符
    '''建立停用词库'''
    for word in typetxt:
        word=word.strip()
        texts.append(word)
    '''建立语料库：分词+过滤停用词'''
    for i in range(0,len(all_file)):
        filename=all_file[i]
        filelabel=filename.split('.')[0]
        labels.append(filelabel)
        file_add='D:/Parse/lixiang/'+ filename
        print(file_add)
        doc=open(file_add,encoding='utf-8').read()
        data=jieba.cut(doc,cut_all=True) #文本分词
        data_adj=''
        delete_word=[]
        for item in data:
            if item not in texts: #过滤停用词
                data_adj+=item+' '
            else:
                delete_word.append(item)
        corpus.append(data_adj) #语料库建立完成
    '''文本聚类'''
    vectorizer=CountVectorizer()    #将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()  #统计每个词语的tf-idf权值
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))   #第一个fit_transform计算tf-idf，第二个fit_transform将文本转为词频矩阵
    weight=tfidf.toarray()      #将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    word=vectorizer.get_feature_names()     #获取词袋模型中的所有词
    mykms=KMeans(n_clusters=10)
    y=mykms.fit_predict(weight)
    for i in range(0,10):
        label_i=[]
        for j in range(0,len(y)):
            if y[j]==i:
                label_i.append(labels[j])
        print('label_'+str(i)+':'+str(label_i))
