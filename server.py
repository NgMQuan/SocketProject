from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
from os import path
from regSys import *
from search import *

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def refundMethod(user, htn, rt, arv, lea):
    userR = 0
    for i in data.account['account']:
        if i != {} and i['username'] == user['username']:
            for j in i['book']:
                if j != {} and htn == j['hotelName'] and rt == str(j['roomID']) and arv == j['arrivalDate'] and lea == j['leavingDate']:
                    userR = j
                    i['book'].remove(userR)
                    user['book'].remove(userR)
                    i['finish'] = ""
                    user['finish'] = ""
                    break
    if userR == 0:
        return -1
    for i in data.hotel['hotel']:
        if htn == i['name']:
            for j in i['room']:
                if rt == str(j['ID']):
                    for k in j['book']:
                        if k['arrivalDate'] == arv and k['leavingDate'] == lea:       
                                    j['book'].remove(k)
                                    fo = open('hotel.json', 'w')
                                    json.dump(data.hotel, fo)
                                    fo = open('account.json', 'w')
                                    json.dump(data.account, fo)
                                    return userR['roomPrice']
    return -1

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    user = modeAccept(client)

    while True:
        mode, htn, rt, ard, lvd, nt = [str(i) for i in client.recv(2048).decode('utf-8').split('\n')]
        if mode == "book":
            if book_room(client, user, htn, rt, ard, lvd, nt) is True:
                client.sendall(str.encode("sB"))
            else:
                client.sendall(str.encode("fB"))
        elif mode == "search":
            IDlist = search_room(client, htn, ard, lvd)
            if len(IDlist) == 0:
                client.sendall(str.encode("fS"))
            else:
                data = str(IDlist)
                data = data.encode()
                client.sendall(data)
        elif mode == "finish":
            totalMoney = getPayment(user)
            totalMoney = str(totalMoney)
            client.sendall(str.encode(totalMoney))
        else:
            refund = refundMethod(user, htn, rt, ard, lvd)
            client.sendall(str.encode(str(refund)))

    # msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"))
    # clients[client] = name

    # while True:
    #     msg = client.recv(BUFSIZ)
    #     if msg != bytes("{quit}", "utf8"):
    #         broadcast(msg, name+": ")
    #     else:
    #         client.send(bytes("{quit}", "utf8"))
    #         client.close()
    #         del clients[client]
    #         broadcast(bytes("%s has left the chat." % name, "utf8"))
    #         break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def modeAccept(client):
    mode, user, passw, pay = [str(i) for i in client.recv(2048).decode('utf-8').split('\n')]
    if mode == 'log':
        acc = login_process(client, user, passw)
        if acc == -1:
            client.sendall(str.encode("fL"))
            return modeAccept(client)
        else:
            client.sendall(str.encode("sL"))
            client.sendall(str.encode(acc['username']))
            return acc
    else:
        if regist_process(client, user, passw, pay) is True:
            client.send(str.encode("sR"))
        else:
            client.send(str.encode("fR"))
        return modeAccept(client)
    """
    mode = client.recv(BUFSIZ).decode("utf8").lower()
    print(mode)
    username = client.recv(BUFSIZ).decode("utf8").lower()
    print(username)
    password = client.recv(BUFSIZ).decode("utf8").lower()
    print(password)
    pay = client.recv(BUFSIZ).decode("utf8").lower()
    print(pay)
    client.send(bytes("accept", "utf8"))
    username = client.recv(BUFSIZ).decode("utf8").lower()
    print(mode)
    if mode == 'reg':
        regist_process(client)
        modeAccept(client)
    elif mode == 'login':
        return login_process(client) """
class Data:
    def __init__(self):
        self.fiA = open('account.json')
        self.fiH = open('hotel.json')
        self.account = json.load(self.fiA)
        self.hotel = json.load(self.fiH)

clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 60008
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

data = Data()

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    try:
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)

        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except KeyboardInterrupt:
        SERVER.close()
    finally:
        SERVER.close()
