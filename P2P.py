# if the server disconnects, one of the clients becomes the server
# and every client that doesnot become the server will try to
# connect to the new server

import socket
import threading
import sys
import time
from random import randint

class Constants:
    port = 10000

class Server:

    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('0.0.0.0', Constants.port))
        sock.listen(1)
        print('Server is running')

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target = self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)

            #a[0] has the ip address of the connection
            self.peers.append(a[0])
            print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()



    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")

                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    #sends the updated list of peers to every connected peer (client)
    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ','

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))




class Client:

    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input("enter message to be sent to the serer\n"), "utf-8"))

    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, Constants.port))

        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)

            #break when server disconnects
            if not data:
                break

            # if the data is updated list of connected peers in p2p
            if data[0:1] == b'\x11':
                print('updated peers')
                self.updatePeers(data[1:])

            print(str(data, 'utf-8'))

    def updatePeers(self, peerData):
        #remove last item since the string ended in a ","
        P2P.peers = str(peerData, "utf-8").split(",")[:-1]

class P2P:
    peers = ['127.0.0.1']

'''
if len(sys.argv) > 1:
    client = Client(sys.argv[1])
else:
    server = Server()
'''

#when server disconnects
while True:
    try:
        print("Trying to connect ...")
        time.sleep(randint(1,5))

        #assuming that one of the peers has already become the server
        for peer in P2P.peers:
            try:
                client = Client(peer)

            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass

        # if none of the peers became the server we want to become the server
            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("could not start the server ...")

    except KeyboardInterrupt:
        sys.exit(0)

#this is a small addition