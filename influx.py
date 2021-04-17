import Util
import pyMysql
import os
import glob
import kafkaConsuming

def getDataFromLocal():
    dirPath='./properties.txt'
    with open(dirPath,'r',encoding='utf-8') as f:
        line=f.readline()
        print(line)
    # f=os.walk(line)
    # paths=[]
    # for dirpath, dirnames, filenames in f:
    #     # print(dirpath)
    #     # print(dirnames)
    #     paths=filenames
    paths=glob.glob(line+"\\"+"*.txt")
    for path in paths:
        dics=[]
        with open(path, 'r', encoding='utf-8') as f:
            i = 0
            while True:
                line = f.readline()
                i += 1
                if not line:
                    break
                dics.append(Util.getRealDic(Util.getDic(line)))
        for i in dics:
            pyMysql.callInsert(i['uri'], i)

    pyMysql.callInsert("", {}, True)

def getDataInRealTime():
    kafkaConsuming.writeInRealTime()

getDataInRealTime()