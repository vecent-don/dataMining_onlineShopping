
import  re
import datetime


def usefulKey(s:str):
    li=['IPADDR']

def getDic(s:str):
    infoList=str.split(" ")
    #去掉‘【’
    for i in range(2):
        infoList[i]=preClean(infoList[i])




def preClean(s:str):
    s.strip()
    if(len(s)<=0) or s[0]!='[':
        return s
    return s[0:len(s)-1].strip()




def inUseList(s:str):
    #处理IPADDR
    dictionary={"IPADDR":["=","str"],}

#getTime
def regrex(s:str):
    searchObj=re.search(r"[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+",s)
    if searchObj:
        ans=searchObj.group()
        t=datetime.datetime.strptime(ans,'%Y-%m-%d %H:%M:%S')
        print(t.timestamp())
        print(ans)
        return t

#getUrl
def getUrl(s:str):
    searchObj=re.search(r"uri.?=.?[a-zA-Z//]+",s)
    if(searchObj):
        ans=searchObj.group()
        print(ans)
        return ans

def getRequestBody(s:str):
    searchObj=re.search(r"requestBody.?=.?\{.*\}",s)
    candidate=preClean(re.search(r"\{.*\}",searchObj.group()).group()).split(",")
    ans={}
    for i in candidate:
        key,value=getPair(i)
        ans[key]=value
        print(key+" "+value)


def getPair(s:str):
    index=s.find(":")
    if index==-1:
        print("getPair: "+s+" is wronf\n")
        return s,""
    key=preClean(s[0:index])
    value=preClean(s[index+1:len(s)])
    return key,value

s='got: [SESSIONID=9a183c12631dcde4cc5560a2599351ef] 2017-11-25 10:10:21 DEBUG [nio-8080-exec-1] com.some.taopao.aop.LogHandler : uri=/item/cart | requestBody={"userId" : "118675", "itemId" : "1668927", "categoryId" : "4444302"}';
getRequestBody(s)

