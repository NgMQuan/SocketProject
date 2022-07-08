import json
from os import path
from datetime import date, datetime

BUFSIZ = 1024


def search_room(client, htn, ard, lvd):
    IDlist = []
    if (check_date_format(ard) and check_date_format(lvd)) is False:
        return IDlist
    if is_sooner(ard, lvd) is False:
        return IDlist

    if path.isfile('hotel.json') is False:
        raise Exception("File not found", SERVER.close())
    # open data file to read
    fi = open('hotel.json')
    # load json data to dict account
    hotel = json.load(fi)
    
    # Send room list
    for i in hotel['hotel']:
        if htn == i['name']:
            for j in i['room']:
                if len(j['book']) == 0:
                    IDlist.append(j['ID'])
                else:
                    check = True
                    for k in j['book']:
                        if not(is_sooner(lvd, k['arrivalDate']) or is_sooner(k['leavingDate'], ard)):
                            check = False
                            break
                    if check is True:
                        IDlist.append(j['ID'])
            break
    return IDlist

def book_room(client, user, htn, rt, ard, lvd, nt):
    if (check_date_format(ard) and check_date_format(lvd)) is False:
        return False
    if is_sooner(ard, lvd) is False:
        return False
    if path.isfile('hotel.json') is False:
        raise Exception("File not found", SERVER.close())
    fhi = open('hotel.json')
    hotel = json.load(fhi)
    fai = open('account.json')
    account = json.load(fai)

    for i in account['account']:
        if user['username'] == i['username']:
            if i['finish'] != "":
                return False

    ID = ''
    roomBooked = {}

    for i in hotel['hotel']:
        if htn == i['name']:
            for j in i['room']:
                if j['type'] == rt:
                    if len(j['book']) == 0:
                        ID = j['ID']
                        roomBooked = {
                            "hotelName": htn,
                            "roomID": j['ID'],
                            "roomType": j['type'],
                            "roomDes": j['description'],
                            "roomPrice": j['price'],
                            "roomImage": j['image'],
                            "arrivalDate": ard,
                            "leavingDate": lvd
                        }
                        bookedDate = {
                            "arrivalDate": ard,
                            "leavingDate": lvd
                        }
                        j['book'].append(bookedDate)
                    else:
                        check = True
                        for k in j['book']:
                            if not(is_sooner(lvd, k['arrivalDate']) or is_sooner(k['leavingDate'], ard)):
                                check = False
                                break
                        if check is True:
                            ID = j['ID']
                            roomBooked = {
                                "hotelName": htn,
                                "roomID": j['ID'],
                                "roomType": j['type'],
                                "roomDes": j['description'],
                                "roomPrice": j['price'],
                                "roomImage": j['image'],
                                "arrivalDate": ard,
                                "leavingDate": lvd
                            }
                            bookedDate = {
                                "arrivalDate": ard,
                                "leavingDate": lvd
                            }
                            j['book'].append(bookedDate)
                if ID != '':
                    break
            break
    fho = open('hotel.json', 'w')
    json.dump(hotel, fho)
    
    for i in account['account']:
        if user['username'] == i['username']:
            i['book'].append(roomBooked)
    fao = open('account.json', 'w')
    json.dump(account, fao)

    if ID != '':
        return True
    else:
        return False

def getPayment(user):
    fai = open('account.json')
    account = json.load(fai)
    total = 0
    for i in account['account']:
        if user['username'] == i['username']:
            if len(i['book']) == 0:
                return total
            for j in i['book']:
                ard = j['arrivalDate']
                lvd = j['leavingDate']
                datearr = date(int(ard[6:]), int(ard[3:5]), int(ard[0:2]))
                dateleave = date(int(lvd[6:]), int(lvd[3:5]), int(lvd[0:2]))
                delta = dateleave - datearr
                datestay = delta.days
                total = total + datestay * int(j['roomPrice'])
            curtime = datetime.now()
            now = curtime.strftime("%d/%m/%Y %H:%M:%S")
            i['finish'] = now
            break
    fao = open('account.json', 'w')
    json.dump(account, fao)
    return total


# check format
def check_date_format(date):
    if len(date) != 10:
        return False
    if date[0].isdigit() and date[1].isdigit() and date[3].isdigit() and date[4].isdigit() and date[6].isdigit() and date[7].isdigit() and date[8].isdigit() and date[9].isdigit():
        return True
    return False


# check sooner
def is_sooner(date1, date2):
    if int(date1[6:10]) < int(date2[6:10]):
	    return True
    elif int(date1[6:10]) > int(date2[6:10]):
	    return False
    if int(date1[3:5]) < int(date2[3:5]):
	    return True
    elif int(date1[3:5]) > int(date2[3:5]):
	    return False
    if int(date1[0:2]) >= int(date2[0:2]):
	    return False
    return True