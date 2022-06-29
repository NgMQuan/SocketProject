import json
from os import path

BUFSIZ = 1024


def regist_process(client, username, password, pay):
    username = client.recv(BUFSIZ).decode("utf8")
    #file hasnt created yet
    if path.isfile('account.json') is False:
        raise Exception("File not found", SERVER.close())
    #open data file to read
    fi = open('account.json')
    #load json data to dict account
    account = json.load(fi)
    #checkduplicate username
    if len(username) < 5 or registUsernameCheck(account, username) is False:
        #client.send(bytes("Username has been created or too short (<5 symbol)! Enter again", "utf8"))
        regist_process(client)
    else:
        #client.send(bytes("Username is valid!", "utf8"))
            #check and create new password
        password = registPassword(client)
        #check and accept the pay method
        pay = acceptPayMethod(client)
        nAcc = {
            "username": username,
            "password": password,
            "payID": pay
        }
        account['account'].append(nAcc)
        fo = open('account.json', 'w')
        json.dump(account, fo)


def registUsernameCheck(account, username):
    for i in account['account']:
        if username == i['username']:
            return False
    return True

def registPassword(client):
    password = client.recv(BUFSIZ).decode("utf8")
    if len(password) < 3:
        client.send(bytes("Password not valid! Try again", "utf8"))
        password = registPassword(client)
    return password

def acceptPayMethod(client):
    pay = client.recv(BUFSIZ).decode("utf8")
    if pay.isdigit() is False or len(pay) != 10:
        client.send(bytes("Card number not valid! Try again", "utf8"))
        pay = acceptPayMethod(client)
    return pay

def login_process(client, username, password):
    # file hasnt created yet
    if path.isfile('account.json') is False:
        raise Exception("File not found", SERVER.close())
    # open data file to read
    fi = open('account.json')
    # load json data to dict account
    account = json.load(fi)
    # get login info
    accountL = loginUsernameCheck(account, username, password)
    return accountL

def loginUsernameCheck(account, username, password):
    for i in account['account']:
        if username == i['username'] and password == i['password']:
            return i
    return -1
