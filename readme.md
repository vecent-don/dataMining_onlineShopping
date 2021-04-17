+ data链接https://box.nju.edu.cn/f/e4d0f922ed914d58a01b/?dl=1
+ 在properties.txt里面写自己电脑上数据文件夹的路径,数据放在一个干净的文件里面,把文件夹绝对路径写在txt第一行
+ schema.sql是mysql的init脚本,右键执行就行了,但可能要配data source(和软工二一样),我下的是mysql for 5.1
+ 爆红的import,自行下对应的库就可以了,但是注意,mysql的库比较坑,要下mysql,也要下mysql-connector(这个库的下载不给提示的)
+ pyMysql的最上面自己改一下自己的用户名和密码
+ influx是入口文件,第一个方法是从本地读数据(要从我给的链接里下txt,配置properties.txt),第二个方法是从kafka实时写数据到数据库
   测试下来第一个方法写10w条数据,大概8s

:warning: 有任何问题及时沟通,方法写的很乱,我也懒得调了