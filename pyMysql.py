import mysql

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    passwd="123456"
)
batchSize=1000
# def createTable():
#
#
#     mycursor = mydb.cursor()
#
#     mycursor.execute("CREATE DATABASE mydatabase")

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



def callInsert():
    i=0
    sql1='''INSERT INTO (sessionId ,date ,userId ,itemId, categoryId) VALUES (%s,%s,%s,%s,%s)'''
    sql2

    while True:
        i=0
        l=[]
        while i<batchSize:
            l.append()
        insertMany()