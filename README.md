# 使用python发送邮件
python结合Redis队列发送邮件。其他服务写入发送数据到redis队列。
python服务轮询队列，发送邮件。

## Redis队列
配置项`conf/config.py`,配置redis服务地址

添加redis队列，`key`为`mail_notify`
```
lpush mail_notify "{\"receivers\": \"pagnxieke@126.com\", \"subject\": \"this is subject\", \"body\": \"this is body\", \"subtype\": \"html\"}"
```

## Python
python服务读取redis队列信息，发送邮件

配置项`conf/config.py`,
```
host = "smtp.126.com"
port = 25
sender = "***@126.com"
pwd = "password"

redisHost = "127.0.0.1"
redisPort = "6379"
```

## Docker
使用脚本，结合`docker build`命令创建image
`sh ./docker_build.sh`

docker 运行
```
docker run --name mail -d \
    -v /data/services/mail/conf:/usr/src/app/conf \
    -v /data/logs:/usr/src/app/logs \
    mail:v1.0
```
