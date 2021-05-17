import mysql.connector
import pandas as pd
import numpy as np
# mydb = mysql.connector.connect(
#     host="121.4.125.198",
#     user="6f",
#     passwd="6fengYYDS!",
#     database="kfk"
# )

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="kfk"
)
mycursor = mydb.cursor()

#meta-meta,side=1,2,4
def fb(s:str, n,times,side):
    mycursor.execute(s)
    data=pd.DataFrame(mycursor.fetchall(),dtype=np.float)
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

#meta 左右
def findRobot(s:str, n):
    return fb(s,n,2,4)
#meta2 右
def findRobot2(s:str, n):
    return fb(s,n,2,2)

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
    x=c>(mean+2*variance)
    y=c<(mean-2*variance)
    z=(x|y)&(z1)
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
    s='''select userId,date,count(*)
    from
        (select userId,DATE_FORMAT(date,'%Y-%m-%d %H:%i') as date
        from getdetail
        ) as x
    group by userId, date;'''
    n=2
    return findRobot2(s,n)

#J 偏好某类category，j在逻辑上存在问题，舍去
def getUser_preferSpecificCategory():
    return

#K getDetail过多

def getUser_getDetailTooMuch():
    s='''select userId,count(*) as num
    from getdetail
    group by userId;'''
    n=1
    return findRobot2(s,n)

# 通过IP获得UserId
def ip2userId(l):
    # l = getIP_ToomanyUsersLoginAndSuccess().tolist()
    l=['106.80.115.90']
    s='''select userId
    from login
    where ipAddr=%s ;'''
    ans=pd.DataFrame(dtype=np.float)
    for i in l:
        mycursor.execute(s,[i])
        ans=pd.DataFrame(mycursor.fetchall())
       # ans.append(mycursor.fetchall())
    print(ans)

ip2userId([])


#获取四类robot

#1

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
    r1=getUser_getDetailTooMuch()
    ip1=getIP_ToomanyUsersLoginAndSuccess()
    r2=getUser_getDetailTooFrequently()


