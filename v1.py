# 安装：pip3 install kafka-python
from kafka import KafkaConsumer
import  signal

def keyboard_handler(signum,frame):
    global  stop
    stop=True

# 需要在校园网环境或nju vpn环境中使用
consumer = KafkaConsumer(
    'foobar',
    bootstrap_servers='172.29.4.17:9092',
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='PLAIN',
    sasl_plain_username='student',
    sasl_plain_password='nju2021',
)
path='E:\\tmpfile\\kafka\\data'

stop=False
signal.signal(signal.SIGINT,keyboard_handler)
i=0
index=90
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

