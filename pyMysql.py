from Util import getRealDic,getDic
import mysql.connector



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="kfk"
)
batchSize=1000

mycursor = mydb.cursor()
sqldetail = '''INSERT INTO getDetail(sessionId ,date ,userId ,itemId, categoryId) VALUES (%s,%s,%s,%s,%s)'''
sqlbuy = '''INSERT INTO buy(sessionId ,date ,userId ,itemId, categoryId,isSecondKill,success) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
sqllogin = '''INSERT INTO login(sessionId ,date ,userId ,success,ipAddr) VALUES (%s,%s,%s,%s,%s)'''
sqlcart = '''INSERT INTO cart(sessionId ,date ,userId ,itemId, categoryId) VALUES (%s,%s,%s,%s,%s)'''
sqlfavor = '''INSERT INTO favor(sessionId ,date ,userId ,itemId, categoryId) VALUES (%s,%s,%s,%s,%s)'''


#
# tdetail = (test['sessionId'], test['time'], test['userId'], test['itemId'], test['categoryId'])
# tbuy = (test['sessionId'], test['time'], test['userId'], test['itemId'], test['categoryId'],test['isSecondKill'], test.get('success', 0))
# tlogin = (test['sessionId'], test['time'], test['userId'],  test['success'], test['IPADDR'])
# tcart = (test['sessionId'], test['time'], test['userId'], test['itemId'], test['categoryId'])
#
# ldetail = []
# lbuy = []
# llogin = []
# lcart = []
sql = [sqldetail, sqlbuy, sqllogin, sqlcart,sqlfavor]
counts = [0, 0, 0, 0,0]
uris = ["/item/getDetail", "/item/buy", "/user/login", "/item/cart","/item/favor"]
t = ["(test['sessionId'], test['time'], test['userId'], test['itemId'], test['categoryId'])",
     "(test['sessionId'], test['time'], test['userId'], test['itemId'], test['categoryId'],test['isSecondKill'], test.get('success',0))",
     "(test['sessionId'], test['time'], test['userId'],  test['success'], test['IPADDR'])",
     "(test['sessionId'], test['time'], test['userId'], test['itemId'], test['categoryId'])",
        "(test['sessionId'], test['time'], test['userId'], test['itemId'], test['categoryId'])"
     ]
l = [[], [], [], [],[]]


def insertMany(val:list,sql:str):
    mycursor = mydb.cursor()
    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    # val = [
    #     ('Peter', 'Lowstreet 4'),
    #     ('Amy', 'Apple st 652'),
    #     ('Hannah', 'Mountain 21'),
    #     ('Michael', 'Valley 345'),
    #     ('Sandy', 'Ocean blvd 2'),
    #     ('Betty', 'Green Grass 1'),
    #     ('Richard', 'Sky st 331'),
    #     ('Susan', 'One way 98'),
    #     ('Vicky', 'Yellow Garden 2'),
    #     ('Ben', 'Park Lane 38'),
    #     ('William', 'Central st 954'),
    #     ('Chuck', 'Main Road 989'),
    #     ('Viola', 'Sideway 1633')
    # ]

    mycursor.executemany(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

def callInsert(s:str,test:dict,flag:bool=False):
    global counts,t,l
    #last time
    if flag:
        for i in range(len(uris)):
            # try:
            mycursor.executemany(sql[i], l[i])
            # except:
            #     x=0
            l[i] = []
            counts[i] = 0
            print(uris[i] + " inserts")
            mydb.commit()
        return

    for i in range(len(uris)):
        if s==uris[i]:
            counts[i]+=1
            l[i].append(eval(t[i]))
    for i in range(len(uris)):
        if counts[i]>=batchSize:
            # try:
            mycursor.executemany(sql[i],l[i])
            # except:
            #     x=0
            l[i]=[]
            counts[i]=0
            print(uris[i]+" inserts")
            mydb.commit()





#sql1='''INSERT INTO getDetail(sessionId  ,userId ,itemId, categoryId) VALUES (%s,%s,%s,%s)'''
# sql1='''INSERT INTO getDetail(sessionId ,date ,userId ,itemId, categoryId) VALUES (%s,%s,%s,%s,%s)'''
# s='got: [SESSIONID=9a183c12631dcde4cc5560a2599351ef] 2017-11-25 10:10:21 DEBUG [nio-8080-exec-1] com.some.taopao.aop.LogHandler : uri=/item/cart | requestBody={"userId" : "118675", "itemId" : "1668927", "categoryId" : "4444302"}';
# test=getRealDic(getDic(s))
# ldetail=(test['sessionId'],test['time'],test['userId'],test['itemId'],test['categoryId'])
# lbuy=(test['sessionId'],test['time'],test['userId'],test['itemId'],test['categoryId'],test.get('success',0))
# llogin=(test['sessionId'],test['time'],test['userId'],test['itemId'],test['success'],test['IPADDR'])
# lcart=(test['sessionId'],test['time'],test['userId'],test['itemId'],test['categoryId'])
#
# mycursor = mydb.cursor()
# mycursor.executemany(sql1, [(test['sessionId'],test['time'],test['userId'],test['itemId'],test['categoryId'])])
#
# mydb.commit()