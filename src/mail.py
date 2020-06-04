#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from redisClient import RedisClient
import time
import json
import logging
import logging.config
import conf

LOG_CONFIG = "./conf/log_config.ini"
logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger()


def run(client):
    while True:
        status, reason, result = client.handle("rpop", "mail_notify")
        if status != 200 or result is None:
            if status != 200:
                logger.error("redis error, status=%d, reason=%s", status, reason)
            time.sleep(10)
            continue

        logger.info("result=%s", result.decode("utf-8"))

        try:
            obj = json.loads(result.decode("utf-8"))
        except:
            logger.error("body is't json format, value=%s", result)

        print(obj)
        try:
            receivers = obj["receivers"]
            subject = obj["subject"]
            body = obj["body"]
            subtype = obj.get("subtype", "plain")
        except:
            logger.error("some filed of mail is not found, value=%s", result)

        send(receivers, subject, body, subtype)
        logger.info("send mail success, receivers=%s", receivers)


def send(receivers, subject, body, subtype):
    host = conf.host
    port = conf.port
    sender = conf.sender
    pwd = conf.pwd

    msg = MIMEText(body, subtype, "utf8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)

    try:
        s = smtplib.SMTP()
        # 调试信息
        # s.set_debuglevel(1)
        s.connect(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receivers, msg.as_string())
        s.quit()
    except smtplib.SMTPException:
        print("Error: send failed")


def main():
    client = RedisClient(conf.redisHost, conf.redisPort)
    run(client)

    print("send success")


if __name__ == '__main__':
    main()
