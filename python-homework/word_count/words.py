import functools
#定义文件读取函数，并且输出元素为词频的字典
def readFile(file_name):
    y = []
    with open(file_name, 'r',encoding="utf-8") as f:
        x=f.readlines()          #readlines（）函数以list形式返回所有行
    for line in x:
        y.extend(line.split())       #extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）;split()函数用于切分行
    word_list=[]
    
# 单词格式化：去掉分词之后部分英文前后附带的标点符号
    for word in y:
        word1 = word
        while True:
            lastchar = word1[-1:]
            if lastchar in [",", ".", "!", "?", ";", '"','-']:
                word1=word1.rstrip(lastchar)
            else:
                word1=word1
                break
 
        while True:
            firstchar = word1[0]
            if firstchar in [",", ".", "!", "?", ";", '"','-']:
                word1=word1.lstrip(firstchar)
            else:
                word1=word1
                break
        word_list.append(word1)
     #统计词频
    tf = {}
    for word in word_list:
        word = word.lower()
        word = ''.join(word.split())
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    return tf

#合并两个字典
def merge(dic1, dic2):
    for k, v in dic1.items():
        if k in dic2.keys():
            dic2[k] += v
        else:
            dic2[k] = v    
    return dic2

#获得前n个最热词和词频
def top_counts(word_list,n=10):
    value_key_pairs = sorted([(count, tz) for tz, count in word_list.items()],reverse=True)
    return value_key_pairs[:n]
    
#获得前n个非最热词和词频
def bottom_counts(word_list,n=10):
    value_key_pairs = sorted([(count, tz) for tz, count in word_list.items()],reverse=False)
    return value_key_pairs[:n]
 
#入口
if __name__ == '__main__':
    file_list = [r'C:\Users\dell\Desktop\本地化的响\高级编程\corpara\1.txt',
                 r'C:\Users\dell\Desktop\本地化的响\高级编程\corpara\2.txt',
                 r'C:\Users\dell\Desktop\本地化的响\高级编程\corpara\3.txt',
                 r'C:\Users\dell\Desktop\本地化的响\高级编程\corpara\4.txt',
                 r'C:\Users\dell\Desktop\本地化的响\高级编程\corpara\5.txt']
 
    cc=map(readFile,file_list) #map（）函数将第一个变量作用于每一个list元素
    word_list = functools.reduce(merge,cc) #reduce（）函数将字典依次合并
    
    top_counts=top_counts(word_list)
    print ("词频前十:")
    print('freq*     word')
    print('-----     -----')
    for word in top_counts[0:10]:
        print("{0:<10}{1}".format(word[0], word[1]))
        
    bottom_counts=bottom_counts(word_list)
    print ("词频倒数前十:")
    print('freq*     word')
    print('-----     -----')
    for word in bottom_counts[0:10]:
        print("{0:<10}{1}".format(word[0], word[1]))