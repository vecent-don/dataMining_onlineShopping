import Util
path='E:\\tmpfile\\data3.txt'

dics=[]


def findUrl():
    x=set()
    for i in dics:
        x.add(i['uri'])
    for i in x:
        print(i)

def findBuy():
    x=list()
    for i in dics:
        if(i['uri']=='/item/favor'):
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
        dics.append(Util.getDic(line))

findBuy()



