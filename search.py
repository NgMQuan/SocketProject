import json
from os import path

BUFSIZ = 1024


def search_room(client):
    client.send(bytes("Enter hotel name: ", "utf8"))
    hotelname = client.recv(BUFSIZ).decode("utf8")
    client.send(bytes("Enter arrival date: (dd/mm/yyyy) ", "utf8"))
    arrivalDate = client.recv(BUFSIZ).decode("utf8")
    client.send(bytes("Enter leaving date: (dd/mm/yyyy) ", "utf8"))
    leavingDate = client.recv(BUFSIZ).decode("utf8")
    if (check_date_format(arrivalDate) and check_date_format(leavingDate)) is False:
        client.send(bytes("Wrong date format!", "utf8"))
        search_room(client)
    if is_sooner(arrivalDate, leavingDate) is False:
        client.send(bytes("Arrival date must be sooner than leaving date!", "utf8"))
        search_room(client)
    client.send(bytes("Searching...", "utf8"))

    if path.isfile('hotel.json') is False:
        raise Exception("File not found", SERVER.close())
    # open data file to read
    fi = open('hotel.json')
    # load json data to dict account
    hotel = json.load(fi)
    
    # Send room list
    for i in hotel['hotel']:
        if hotelname == i['name']:
            for j in i['room']:
                if j['arrivalDate'] == -1 or is_sooner(leavingDate, j['arrivalDate']) or is_sooner(j['leavingDate'], arrivalDate):
                    roomInfo = """Room ID: %s
                    Room Type: %s
                    Description: %s
                    Price: %s""" % (j['ID'], j['type'], j['description'], j['price'])
                    client.send(bytes(roomInfo, "utf8"))
            break


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