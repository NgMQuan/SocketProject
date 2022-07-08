import json
from os import path

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
    if int(date1[0:2]) > int(date2[0:2]):
	    return False
    return True