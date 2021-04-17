import Util
import pyMysql
path='E:\\tmpfile\\data3.txt'
dics=[]

import time
# start=time.clock()

def findUrl():
    x=set()
    for i in dics:
        x.add(i['uri'])
    for i in x:
        print(i)

def findBuy():
    x=list()
    for i in dics:
        if(i['uri']=='/item/buy'):
            x.append(i)
    for i in x:
        print(i)

def findDetail():
    x=list()
    for i in dics:
        if(i['uri']=='/item/getDetail'):
            x.append(i)
    for i in x:
        print(i)

with open(path,'r',encoding = 'utf-8') as f:
    i=0
    # 多个 consumer 可以重复消费相同的日志，每个 consumer 只会消费到它启动后产生的日志，不会拉到之前的余量
    while True:
        line=f.readline()
        i+=1
        if not line  :
            break
        dics.append(Util.getRealDic(Util.getDic(line)))


for i in dics:
    # if i['uri']=='/item/buy':
    #     a=0
    pyMysql.callInsert(i['uri'],i)

pyMysql.callInsert("",{},True)

end=time.clock()
# print("len: "+str(len(dics))+"time: "+str(end-start))
