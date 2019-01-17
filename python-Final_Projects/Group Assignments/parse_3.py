import os
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
'''
越过山丘小组：李响、张以欣、梁紫君、梁彧彧
用于爬取中医著作、药材药方、中医大辞典
将中医著作存至'D:\\Parse\TCM\Books\著作名+章节名.txt'；
将药材药方、中医大辞典（著作下方内容）存至'D:\\Parse\TCM\Medicine\药材药方名（或辞典词条名）.txt'；
'''
if __name__ == "__main__":
    #获取首页链接标题
    url =  "http://www.guoxuedashi.com/zhongyi/"
    raw_url = "http://www.guoxuedashi.com"
    new_word = requests.get(url)
    soup = BeautifulSoup(new_word.content,"html.parser")
    result =soup.find_all("dd")
    if not os.path.exists("D:\\Parse\\TCM/"):
       os.mkdir("D:\\Parse\\TCM/")

    i=0
    #依次进入二级页面
    for elem in result:
        i=i+1
        if i>60:
            #进入各药材药方药材药方（或辞典词条）页面
            final_url=raw_url+elem.a['href']
            # print(final_url1)
            reps=requests.get(final_url)
            final_soup = BeautifulSoup(reps.content,"html.parser")
            med_name = final_soup.find("div",class_="info_tree").h1.get_text() #药材药方名（或辞典词条名）
            med_def= final_soup.find("div",class_="info_content zj clearfix").span.get_text() #药材药方（或辞典词条）内容
            #print(med_name)
            #存至文件
            with open('D:\\Parse\\TCM/Medicine/'+med_name+'.txt',"a",encoding='utf-8') as f:
                f.write(med_name+'\n')
                f.write(med_def+'\n')

        else:
            #进入中医著作页面
            final_url=raw_url+elem.a['href']
            print(final_url)
            reps=requests.get(final_url)
            new_soup = BeautifulSoup(reps.content,"html.parser")
            book_name = new_soup.find("div",class_="info_tree").h1.get_text()
            new_result=new_soup.find_all("li")

            #依次进入中医著作各章节
            for new_elem in new_result:
                next_url=raw_url+new_elem.a['href']
                #print(next_url)
                new_reps=requests.get(next_url)
                final_soup = BeautifulSoup(new_reps.content,"html.parser")
                chapter_name = final_soup.find("div",class_="info_tree").h1.get_text() #获取各章节名
                chapter_def= final_soup.find("div",class_="info_txt clearfix").get_text() #获取各章节内容
                #print(chapter_name)

                #写入文件
                with open('D:\\Parse\\TCM/Books/'+book_name+' '+chapter_name+'.txt',"a",encoding='utf-8') as f:
                    f.write(chapter_name+'\n')
                    f.write(chapter_def+'\n')
