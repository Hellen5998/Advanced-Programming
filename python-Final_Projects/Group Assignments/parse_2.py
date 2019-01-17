# coding: utf-8

# In[1]:

import requests
import os
from bs4 import BeautifulSoup

'''
越过山丘小组：李响 张以欣 梁紫君 梁彧彧
用于爬取国学大师说文解字每个字的详情信息及其在扫描版《说文解字》中的图片url
所有详情信息以txt格式存至D:\Echo\Parse\shuowenjiezi\字名 说文解字.txt
所有图片url存储在每个字的详情信息txt中，存于详情信息后

'''
if __name__ =="__main__":
    r=requests.get('http://www.guoxuedashi.com/ShuoWenJieZi/')
    from pyquery import PyQuery as pq
    doc=pq(r.text)
    doc1 = pq(doc('#ff').html())
    doc2=doc1('dd')
    raw_url="http://www.guoxuedashi.com"

    if not os.path.exists("D:\\Parse\\shuowenjiezi"):
        os.mkdir("D:\\Parse\\shuowenjiezi/")

    for elem in doc2('a'):
        url=raw_url+elem.get('href') #进入每个字所在的页面
        reps=requests.get(url)
        soup=BeautifulSoup(reps.content,"html.parser")
        final_name=soup.find("div",class_="info_tree").h1.get_text()
        final_def = soup.find("div",class_="info_txt2 clearfix").get_text()
        doc3 = pq(reps.text)
        doc4 = pq(doc3('div.info_txt2.clearfix').html())
        final_url=raw_url+doc4('a').attr('href') #进入图片所在页面
        reps_1=requests.get(final_url)
        doc5=pq(reps_1.text)
        doc6 = pq(doc5.html())

        for new_elem in doc6('img'): #遍历所有img
            img=new_elem.get('src')

        with open('D:\\Parse\\shuowenjiezi/'+final_name+'.txt',"a",encoding='utf-8') as f:
                f.write(final_name+'\n')
                f.write(final_def+'\n')
                f.write(img)

