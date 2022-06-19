import json
from os import path

BUFSIZ = 1024


def regist_process(client):
    client.send(bytes("Enter new username", "utf8"))
    username = client.recv(BUFSIZ).decode("utf8")
    # file hasnt created yet
    if path.isfile('account.json') is False:
        raise Exception("File not found", SERVER.close())
    # open data file to read
    fi = open('account.json')
    # load json data to dict account
    account = json.load(fi)
    # checkduplicate username
    if registUsernameCheck(account, username) is False:
        client.send(bytes("Username has been created! Enter again", "utf8"))
        regist_process(client)
    else:
        client.send(bytes("Username is valid! Now enter the password", "utf8"))


def login_process(client):
    client.send(bytes("Enter username", "utf8"))
    username = client.recv(BUFSIZ).decode("utf8")
    client.send(bytes("Enter password", "utf8"))
    password = client.recv(BUFSIZ).decode("utf8")
    # file hasnt created yet
    if path.isfile('account.json') is False:
        raise Exception("File not found", SERVER.close())
    # open data file to read
    fi = open('account.json')
    # load json data to dict account
    account = json.load(fi)
    # checkduplicate username
    if loginUsernameCheck(account, username, password) is False:
        client.send(bytes("Wrong username or password!", "utf8"))
        login_process(client)
    else:
        client.send(bytes("Access Granted", "utf8"))


def registUsernameCheck(account, username):
    for i in account['account']:
        if username == i['username']:
            return False
    return True


def loginUsernameCheck(account, username, password):
    for i in account['account']:
        if username == i['username'] and password == i['password']:
            return True
    return False