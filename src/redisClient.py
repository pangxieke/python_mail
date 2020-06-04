# /usr/local/bin python3
# -*- coding: utf-8 -*-

'redis client'

__author__ = 'pangxieke@126.com'

import redis
import json
import conf


class RedisClient():
    def __init__(self, host, port=6379,
                 password=None, db=0, socket_timeout=None,
                 socket_connect_timeout=None):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout
        self.client = None

    def handle(self, func, *args, **kwargs):
        status, reason = self.check()
        if status != 200:
            return (status, reason, None)
        try:
            callback = getattr(self.client, func)
        except Exception as e:
            status = 500
            reason = "no func=%s, exception=%s" % (func, e)
            return (status, reason, None)

        result = None
        try:
            result = callback(*args, **kwargs)
        except Exception as e:
            self.client = None
            status = 500
            reason = "call func=%s, catch an exception=%s" % (func, e)
        return (status, reason, result)

    def check(self):
        status, reason = 200, "OK"
        if self.client:
            return (status, reason)

        try:
            client = redis.Redis(host=self.host,
                                 port=self.port, db=self.db,
                                 password=self.password,
                                 socket_timeout=self.socket_timeout,
                                 socket_connect_timeout=self.socket_connect_timeout)
            self.client = client
        except Exception as e:
            status = 500
            reason = "connect exception, %s" % (str(e))
        return (status, reason)


def test():
    client = RedisClient(conf.redisHost, conf.redisPort)
    status, reason = client.check()
    print("status:", status, "reason:", reason)

    obj = {
        "receivers": ["pangxieke@126.com", "pangxieke@126.com"],
        "subject": "online fitting v2 error",
        "body": "this is body",
        "subtype": "html"
    }
    value = json.dumps(obj)
    key = "mail_notify"

    client.handle("lpush", key, value)


if __name__ == '__main__':
    test()
