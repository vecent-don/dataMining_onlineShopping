
import  re
import datetime



def preClean(s:str):
    s=s.strip()
    if(len(s)<=0) or (s[0]!='[' and s[0]!='{'):
        return s
    return s[1:len(s)-1].strip()


#getTime
def getTime(s:str):
    searchObj=re.search(r"[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+",s)
    if searchObj:
        ans=searchObj.group()
        t=datetime.datetime.strptime(ans,'%Y-%m-%d %H:%M:%S')
        # print(t.timestamp())
        # print(ans)
        return "time",t

#getUrl
def getUrl(s:str):
    searchObj=re.search(r"uri.?=.?[a-zA-Z//]+",s)
    if(searchObj):
        ans=searchObj.group()
        # print(ans)
        return splitEqual(ans)

def getIPADDR(s:str):

    searchObj = re.search(r"IPADDR ?= ?([0-1]+\.){3}[0-1]+", s)
    if(searchObj==None):
        return None,None;
    return splitEqual(searchObj.group())

def getRequestBody(s:str):

    pattern=r"requestBody.?=.?\{.*\}"
    # pattern2="requestBody.?=.?\{.*\}"
    searchObj=re.search(pattern,s)
    candidate=preClean(re.search(r"\{.*\}",searchObj.group()).group())
    candidate=candidate.split(",")
    ans={}
    for i in candidate:
        key,value=getPair(i)
        ans[key]=value
        #print(key+" "+value)
    return "requestBody",ans

def splitEqual(s:str):
    s=s.split("=")
    return preClean(s[0]),preClean(s[1])

# def test(s:str):
#     print(s)
#     pattern=r"\\na"
#     print(pattern)
#     searchObject=re.search(pattern,s)
#     print(searchObject.group())
# test("\\na")

def getPair(s:str):
    index=s.find(":")
    if index==-1:
        print("getPair: "+s+" is wronf\n")
        return s,""
    key=preClean(s[0:index])
    key=key[1:len(key)-1]
    value=preClean(s[index+1:len(s)])
    value=value[1:len(value)-1]
    return key,value

def getDic(s:str):
    ans={}
    for i in [getUrl,getIPADDR,getTime,getRequestBody]:
        key,value=i(s)
        if(key!=None):
            ans[key]=value
    return ans


s='got: [SESSIONID=9a183c12631dcde4cc5560a2599351ef] 2017-11-25 10:10:21 DEBUG [nio-8080-exec-1] com.some.taopao.aop.LogHandler : uri=/item/cart | requestBody={"userId" : "118675", "itemId" : "1668927", "categoryId" : "4444302"}';
test=getDic(s)
a=0
