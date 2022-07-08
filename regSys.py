import json
from os import path

BUFSIZ = 1024


def regist_process(client, username, password, pay):
    #file hasnt created yet
    if path.isfile('account.json') is False:
        raise Exception("File not found", SERVER.close())
    #open data file to read
    fi = open('account.json')
    #load json data to dict account
    account = json.load(fi)
    #checkduplicate username
    if len(username) < 5 or registCheck(account, username, password, pay) is False:
        #client.send(bytes("Username has been created or too short (<5 symbol)! Enter again", "utf8"))
        return False

    #client.send(bytes("Username is valid!", "utf8"))
    nAcc = {
        "username": username,
        "password": password,
        "payID": pay,
        "book": [],
        "finish": ""
    }
    account['account'].append(nAcc)
    fo = open('account.json', 'w')
    json.dump(account, fo)

    return True


def registCheck(account, username, password, pay):
    for i in account['account']:
        if username == i['username']:
            return False

    if len(password) < 3:
        return False

    if pay.isdigit() is False or len(pay) != 10:
        return False

    return True

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
