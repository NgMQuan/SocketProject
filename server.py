from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
from os import path
from regSys import *
from search import search_room

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected.2" % client_address)

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def searchRoom(client):
    htn, ard, lvd = [str(i) for i in client.recv(2048).decode('utf-8').split('\n')]

    IDlist = search_room(client, htn, ard, lvd)
    if len(IDlist) == 0:
        client.sendall(str.encode("fS"))
        return searchRoom(client, htn, ard, lvd)
    else:
        return IDlist


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    user = modeAccept(client)
    IDlist = searchRoom(client)
    data = str(IDlist)
    data = data.encode()
    client.sendall(data)
    


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


clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 60008
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

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
