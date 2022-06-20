from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
from os import path
from regSys import regist_process, login_process, registUsernameCheck

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)

        client.send(bytes("Greetings from the cave!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    user = modeAccept(client)

    name = user['username']
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def modeAccept(client):
    client.send(bytes("Please type 'login' or 'reg' to join server", "utf8")) 
    mode = client.recv(BUFSIZ).decode("utf8").lower()
    if mode == 'reg':
        client.send(bytes("Regist new account!", "utf8"))
        regist_process(client)
        modeAccept(client)
    elif mode == 'login':
        return login_process(client)
    else:
        client.send(bytes("Invalid input", "utf8"))
        modeAccept(client)

clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 33000
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
