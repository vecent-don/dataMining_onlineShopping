+ data链接https://box.nju.edu.cn/f/e4d0f922ed914d58a01b/?dl=1
+ 在properties.txt里面写自己电脑上数据文件夹的路径,数据放在一个干净的文件里面,把文件夹绝对路径写在txt第一行
+ schema.sql是mysql的init脚本,右键执行就行了,但可能要配data source(和软工二一样),我下的是mysql for 5.1
+ 爆红的import,自行下对应的库就可以了,但是注意,mysql的库比较坑,要下mysql,也要下mysql-connector(这个库的下载不给提示的)
+ pyMysql的最上面自己改一下自己的用户名和密码
+ influx是入口文件,第一个方法是从本地读数据(要从我给的链接里下txt,配置properties.txt),第二个方法是从kafka实时写数据到数据库
   测试下来第一个方法写10w条数据,大概8s

:warning: 有任何问题及时沟通,方法写的很乱,我也懒得调了

robot 文件里面是找机器人的文件
4个函数在最下面，都是以*robot()命名

+ 获得所有潜在的机器人
    + 撞库机器人
        +  pwdRobot()
        +  函数返回所有的可疑IP
    + 抢单机器人
        +   orderGrabingRobot()
        +   返回可疑的UserId
    +  刷单机器人、
        +   scaplingRobot()
        +   返回可疑的UserId
    +   爬虫机器人
        +   crawlerRobot()
        +   返回可疑的UserId，默认会回打tag
+ 附加选项
    + 将可疑IP传入ip2userId(l)函数，会获得该IP下访问过的所有用户
    + 将可疑Ip传入tagRobot,会在buy和getDetail表中标注的机器人
    + robot.py函数的最上, batch，epoch1，epoch为3个超参数，因为getDeta表过大了
      区间为（epoch1\*batch，epoch\*batch）
      也许你希望限制单次查询的范围,例如batch = 1000000，epoch1=0，epoch=1 的组合即意味着会查询 (0\*1000000,1\*1000000)区间内的数据