__author__ = 'Waldo'


'''
Simple socket server using threads
'''



import socket, json
from threading import *
import re


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8888
serversocket.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            # try:

            try:
                json_load = self.sock.recv(1024).decode()
                print(json_load)
                db_events = json.loads(json_load)
                from icarus_server import db, Event
                for db_event in db_events['data']:
                    event = Event(device_id=db_events['id'],v1=db_event['v1'],
                              v2=db_event['v2'],v3=db_event['v3'],
                              v4=db_event['v4'],v5=db_event['v5'],
                              v6=db_event['v6'],v7=db_event['v7'],
                              v8=db_event['v8'],v9=db_event['v9'],
                              device_time=db_event['t1'])
                    db.session.add(event)
                    db.session.commit()

                print('Client sent:',db_events )
                self.sock.send(b'Success')
            except Exception as e:
                self.sock.send(b'Failure')

                break


serversocket.listen(5)
host_port = str(host) + ":" + str(port)
print ('TCP Server Listening on', host_port)
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)



# import socket
# import sys
#
# HOST = '0.0.0.0'   # Symbolic name, meaning all available interfaces
# PORT = 8888 # Arbitrary non-privileged port
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('Socket created')
#
# #Bind socket to local host and port
# try:
#     s.bind((HOST, PORT))
# except socket.error as msg:
#     print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
#     sys.exit()
#
# print('Socket bind complete')
#
# #Start listening on socket
# s.listen(10)
# print('Socket now listening')
#
# #now keep talking with the client
# while 1:
#     #wait to accept a connection - blocking call
#     conn, addr = s.accept()
#     print('Connected with ' + addr[0] + ':' + str(addr[1]))
#
# s.close()