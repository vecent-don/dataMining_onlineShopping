# 安装：pip3 install kafka-python
from kafka import KafkaConsumer
import  signal
import pyMysql
import Util

def keyboard_handler(signum,frame):
    global  stop
    stop=True
stop = False
signal.signal(signal.SIGINT, keyboard_handler)



# 需要在校园网环境或nju vpn环境中使用
consumer = KafkaConsumer(
    'foobar',
    bootstrap_servers='172.29.4.17:9092',
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='PLAIN',
    sasl_plain_username='student',
    sasl_plain_password='nju2021',
)
'''
@param path: 你要存data的文件夹的路径,e.g."E:tmpfile\\kafka"
'''
def writeToLocal(path:str):
    path=path+'\\data'
    i=0
    index=100
    while True:
        i=0
        with open(path+str(index)+'.txt','a+',encoding = 'utf-8') as f:

            # 多个 consumer 可以重复消费相同的日志，每个 consumer 只会消费到它启动后产生的日志，不会拉到之前的余量
            for msg in consumer:
                line = msg.value.decode("utf-8")
                #print('got:', line)
                f.write(line+'\n')
                i+=1
                #f.flush()
                if not stop and i<10000:
                    continue;
                break;
        index+=1
        print(str(index)+ "is done")
        if(index>100):
            break

def writeInRealTime():
    # 多个 consumer 可以重复消费相同的日志，每个 consumer 只会消费到它启动后产生的日志，不会拉到之前的余量
    for msg in consumer:
        line = msg.value.decode("utf-8")
        print('got:', line)
        dic=Util.getRealDic(Util.getDic(line))
        pyMysql.callInsert(dic['uri'],dic)
        if not stop:
            continue;
        pyMysql.callInsert('',{},True)
        break;

