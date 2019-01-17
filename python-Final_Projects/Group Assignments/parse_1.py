import os
import time
from pyquery import PyQuery as pq
from selenium import webdriver
'''
越过山丘小组：李响 张以欣 梁紫君 梁彧彧
用于爬取国学大师部件及每个部件对应的所有汉字的详情信息；
所有部件存至D:\\Parse\\bujian.txt；
每个部件对应的汉字存至D:\\Parse\部件名.txt；
每一部件中各个汉字的详情内容存至D:\\Parse\部件名_details.txt；
详情内容二级页面的图片url存至D:\\Parse\部件名_pics_url.txt；
相同偏旁汉字所有信息写在同一文件；
'''
if __name__ == "__main__":
    browser = webdriver.Chrome()
    browser.get('http://www.guoxuedashi.com/zidian/bujian/')
    html = browser.page_source
    # 获取并储存所有偏旁部首
    doc = pq(html, parser="html")
    doc1 = pq(doc('.table2').html())
    list_1 = []
    txt = doc1('tbody tr td a').text().replace(' ', '')   #取消字间空格
    for i in txt:
        list_1.append(i)
    # 将右侧偏旁部首放在bujian.txt中
    with open('D:\\Parse\\bujian.txt', 'w', encoding='utf-8') as f1:
        for i in list_1:
            f1.write(i)
            f1.write(" ")
    f1.close()

    # 依次搜索每个部件对应汉字
    bs: str
    for bs in list_1:
        input = browser.find_element_by_id('q')
        input.clear()
        input.send_keys(bs)
        button = browser.find_element_by_id('but1')
        button.click()    #模拟点击
        time.sleep(10)    #等待页面加载完成
        browser.switch_to.window(browser.window_handles[-1])    #加载新页面后需重新定位句柄
        letter=browser.find_element_by_css_selector('#show')
        list_2 = []
        for i in letter.text:
            list_2.append(i)
        #将每个部件对应汉字写入文档
        with open('D:\\Parse/' + bs + '.txt', 'a', encoding='utf-8') as f:
            for i in list_2:
                f.write(i)
                f.write(" ")
        f.close()
        #依次打开汉字页
        letter_childs=letter.find_elements_by_tag_name("a")
        for letter_child in letter_childs:
            #进入详情页一级页面，将各个字的详情信息（基本解释）写入文件
            letter_child.click()
            time.sleep(2)
            browser.switch_to.window(browser.window_handles[-1])
            html = browser.page_source
            doc = pq(html, parser="html")
            with open('D:\\Parse\\'+bs+ '_details.txt','a',encoding='utf-8') as f1:
                f1.write(doc('.tit03').eq(0).text())
                f1.write(doc('.zui').text())
                f1.write(doc('.tit03').eq(1).text())
                f1.write(doc('p').eq(2).text())
                f1.write(doc('.tit03').eq(2).text())
                #f1.write(doc('#shupage').text())
            f1.close()
            #获取各个文字在字典中的解释：转至详情页二级页面，抓取图片url
            elem=browser.find_element_by_css_selector("#shupage > tbody:nth-child(1)")
            links = elem.find_elements_by_tag_name("a")
            j=0
            for link in links:
                j=j+1
                if j>=10: break;
                #time.sleep(2)
                if "pic" in link.get_attribute("href") and "_blank" in link.get_attribute("target"):
                    link.click()
                    time.sleep(2)
                    browser.switch_to.window(browser.window_handles[-1])
                    #sreach_window3=browser.current_window_handle
                    url = browser.find_element_by_css_selector("body > div > center > img").get_attribute("src")
                    #详情页二级页面图片url写入文件
                    with open('D:\\Parse\\'+bs+'_pics_url.txt','a',encoding='utf-8') as f1:
                        f1.write(url+'\n')
                    f1.close()
                    browser.close()
                    browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

    #删除空文件
    results = []#所有的文件
    files=os.listdir("D:\\Parse")
    for file in files:
        if os.path.getsize(os.path.join("D:\\Parse", file)) == 0:  # 文件大小为0
            os.remove(os.path.join("D:\\Parse", file))  # 删除这个文件
    else:
        path = os.path.join("D:\\Parse", file)#合并成一个完整路径
        results.append(path)




