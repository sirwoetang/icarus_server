__author__ = 'Waldo'

#!/usr/bin/env python

import socket, json


TCP_IP = '85.90.246.74'
TCP_PORT = 8888
BUFFER_SIZE = 1024
MESSAGE = '''{
    "id":"1",
    "data": [{
            "v1": 1,
            "v2": "1.111",
            "v3": "1",
            "v4": "1",
            "v5": "1",
            "v6": "1",
            "v7": "1",
            "v8": "1",
            "v9": "1",
      		"t1":"2011-12-19T15:28:46.493Z"
        },
        {
            "v1": 1.111,
            "v2": "1",
            "v3": "1",
            "v4": 2.9997,
            "v5": "1",
            "v6": "1",
            "v7": "1",
            "v8": "1",
            "v9": "1",
            "t1":"2011-12-19T15:28:46.493Z"
        }]
}'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
s.close()

print("Response data:", data)