import mysql.connector
import pandas as pd
import numpy as np

mydb = mysql.connector.connect(
    host="121.4.125.198",
    user="6f",
    passwd="6fengYYDS!",
    database="kfk"
)
batch = 1000000
epoch1=0
epoch=1   #8

# batch = 10000
# epoch1=0
# epoch = 4
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="123456",
#     database="kfk"
# )

mycursor = mydb.cursor()

#statistics analysis
def getSuspects(data, n,times,side):
    c=data.iloc[:,n]
    mean=c.mean()
    variance=c.std()
    x=set()
    if side==1:
        x = c < (mean + times * variance)
    if side==2:
        x = c > (mean + times * variance)
    if side==4:
        x = (c < (mean + times * variance)) | (c > (mean + times * variance))
    robots=data.loc[x]
    print(mean,variance)
    print(robots)

    return robots.iloc[:,0]

#meta-meta,side=1,2,4
def fb(s:str, n,times,side):
    mycursor.execute(s)
    data=pd.DataFrame(mycursor.fetchall(),dtype=np.float)
    robots=getSuspects(data, n,times,side)
    return robots

#meta 左右
def findRobot(s:str, n):
    return fb(s,n,2,4)
#meta2 右
def findRobot2(s:str, n):
    return fb(s,n,2,2)

#A 行为分析
#A.废弃 由于5表连接统计用户行为并不现实，本特征分析转由用户行为分析同学在该部分实现


#B登录正确率过低，且尝试次数过多(超过10次)
def getIP_LoginSuccessRateTooLow():
    s='''select ipAddr,sum(if(success=1,1,0))/count(success) as rate, count(success) as attempt from login group by ipAddr;'''
    mycursor.execute(s)
    data=pd.DataFrame(mycursor.fetchall(),dtype=np.float)
    c=data.iloc[:,1]
    d=data.iloc[:,2]
    z1=d>10
    mean=c.mean()
    variance=c.std()
    # x=c>(mean+2*variance)
    y=c<(mean-2*variance)
    # z=(x|y)&(z1)
    z=y
    robots=data.loc[z]
    print(robots)
    return robots.iloc[:,0]

#almost zero, in this case, this rate relates more to the customer behavior rather than robot behavior ->not useful,
#c 直接购买的比例过高 统计每一个用户直接购买的数目和有购物车行为的数目
def getUser_directPerchase():
    s='''select buy.userId, count(cart.userId)  c1, count(buy.userId)  c2, count(cart.userId)/count(buy.userId)  as rate
    from buy left join cart on buy.userId=cart.userId and buy.itemId=cart.itemId and buy.date>cart.date
    group by buy.userId;'''
    n=3
    return findRobot(s,n)


#D 购买的时间分布
def getUser_puchaseTimeDistribute():
    s='''select userId, sum(if(DATE_FORMAT(date,'%i')=59 or DATE_FORMAT(date,'%i')=60,1,0)) / count(*) as rate
    from buy
    GROUP BY userId;'''
    n=1
    return findRobot2(s,n)

#E isSecondKill 准确率评估
def getUser_isSecondKillSuccess():
    s='''select userId, sum(success)/count(*) as  rate
    from buy
    where isSecondKill=1
    group by userId;'''
    n=1
    return findRobot2(s,n)


#F 刷单行为-太过于偏好够买某类东西（多次复购该类商品）
def getUser_purchaseTooMuch():
    s='''select userId,count(*) as totalType,max(num)
    from (select userId,itemId,count(*) as num
        from buy
        group by userId,itemId
        ) as x
    group by userId;'''
    n=2
    return findRobot2(s,n)

#G 刷单行为-单位时间（1min） 内buy请求过高
def getUser_buyTooFrequently():
    s="""select
        userId, date, count(*)
        from
            (select userId, DATE_FORMAT(date, '%Y-%m-%d %H:%i') as date
            from buy
            ) as x   
        group by userId, date;"""
    n=2
    return findRobot2(s,n)

#H 单位为IP，某个IP下用户数目过多
def getIP_ToomanyUsersLoginAndSuccess():
    s='''select ipAddr,count(*)
    from login
    where success=1
    group by ipAddr;'''
    n=1
    return findRobot2(s,n)

#I 1min 内用户请求数（简化为getDetail的数目）
def getUser_getDetailTooFrequently():
#     s='''select userId,date,count(*)
#     from
#         (select userId,DATE_FORMAT(date,'%Y-%m-%d %H:%i') as date
#         from getDetail
#         ) as x
#     group by userId, date;'''
#
#     s2='''select userId,DATE_FORMAT(date,'%Y-%m-%d %H:%i') date,count(*)
#         from getDetail
#         group by userId, DATE_FORMAT(date,'%Y-%m-%d %H:%i');'''


    s='''select userId,date,count(*)
    from
        (select userId,DATE_FORMAT(date,'%Y-%m-%d %H:%i') as date
        from getDetail
        where id<={} and id>={} 
        ) as x
    group by userId ,date;'''
    n=2
    tmpFrame=pd.DataFrame(dtype=np.float)
    for i in range(epoch1,epoch):
        low=i*batch
        high=(i+1)*batch
        sql=s. format(high,low)

        mycursor.execute(sql)
        tmpFrame=tmpFrame.append(mycursor.fetchall())
        print("getDetailTooFrequently ",i," is finished")

    tmpFrame.columns=['userId','date','count']
    tmpFrame.groupby(['userId','date'])['count'].sum()
    #print(tmpFrame)
    tmpFrame.columns=[0,1,2]
    ans=getSuspects(tmpFrame,n,2,2).astype(np.float)
    # print(ans)
    return ans

#getUser_getDetailTooFrequently()

#J 偏好某类category，j在逻辑上存在问题，舍去
def getUser_preferSpecificCategory():
    return

#K getDetail过多

def getUser_getDetailTooMuch():
    s='''select userId,count(*) as num
    from getDetail
    where id>={} and id<={} 
    group by userId;'''
    tmpFrame = pd.DataFrame(dtype=np.float)
    for i in range(epoch1,epoch):
        low=i*batch
        high=(i+1)*batch
        sql=s.format(low,high)
        mycursor.execute(sql)
        tmpFrame = tmpFrame.append(mycursor.fetchall())
        print("getDetailTooMuch", i, " is finished")

    n=1
    ans = getSuspects(tmpFrame, n, 2, 2).astype(np.float)
    return ans


# 通过IP获得UserId
def ip2userId(l):
    l = getIP_ToomanyUsersLoginAndSuccess().tolist()
    #l=['106.80.115.90']
    s='''select userId
    from login
    where ipAddr=(%s) ;'''
    ans=pd.DataFrame(dtype=np.float)

    for i in l:
        mycursor.execute(s,[i])
        tmp=pd.DataFrame(mycursor.fetchall())
        ans=ans.append(tmp)

    ans=ans.drop_duplicates().iloc[:,0].astype(np.float)
    return ans

def tagRobot(robots):
    sql='''
    update getDetail set getDetail.isRebot=1 where userId=%s;
    '''
    sql2='''update buy set buy.isRebot=1 where userId=%s;
    '''
    # sql3='''update buy set buy.isRebot=0 where userId=736721.0;'''
    #
    # mycursor.execute(sql3)
    # mydb.commit()
    for i in robots.iterrows():
        t=i[1][0]
        mycursor.execute(sql,[t])
        mycursor.execute(sql2, [t])
    mydb.commit()




#获取四类robot

#1撞库机器人 B
#没有道理封杀用户，所以只返回IP
def pwdRobot():

    r1=getIP_LoginSuccessRateTooLow()

    return r1
#pwdRobot()

#C无效，因此只使用D，E
#2  抢单机器人 D&E
def orderGrabingRobot():
    r1=getUser_puchaseTimeDistribute()
    r2=getUser_isSecondKillSuccess()
    r3=pd.merge(r1,r2)
    print(r3)
    return r3

#3 刷单机器人 F&G：多次复购+短时间高频buy请求
def scaplingRobot():
    r1=getUser_purchaseTooMuch()
    r2=getUser_buyTooFrequently()
    r3=pd.merge(r1,r2)
    print(r3)
    return r3

#4 爬虫机器人 K&H&I (&J)
def crawlerRobot():
    print("---------------crawler------------------")
    r2 = getUser_getDetailTooFrequently()
    r1=getUser_getDetailTooMuch()
    ip1=getIP_ToomanyUsersLoginAndSuccess()
    # r1=[]
    # ip1=[]
    print("----------------IPing-------------------")
    r3=ip2userId(ip1)
    print("----------------tagging-----------------")
    r4=pd.merge(r1,r2)
    r4=pd.merge(r4,r3)
    tagRobot(r4)
    print(r4)
    return r4
# pwdRobot()
#
# orderGrabingRobot()
#
# scaplingRobot()
#
# crawlerRobot()

