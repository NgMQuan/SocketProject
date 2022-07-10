from http import client
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import *
from tkinter import ttk
import json
#from tkProc import *

def initGUI(client_socket):
    a = Controller(client_socket)
    a.mainloop()
    
def getUser(uID):
    for i in data.account['account']:
        if i['username'] == uID:
            return i
    return -1
    
def create_user (client_socket, usn, pas, pay, mode, control, frame):
    """Handles sending username and password."""
    if (type(pay) == str):
        client_socket.sendall(str.encode("\n".join([mode, usn.get(), pas.get(), "0"])))
        usn.set("")
        pas.set ("")
    else:
        client_socket.sendall(str.encode("\n".join([mode, usn.get(), pas.get(), pay.get()])))
        usn.set("")
        pas.set ("")
        pay.set("")

    flag = client_socket.recv(2048).decode('utf-8')

    if flag == "sL":
        userID = client_socket.recv(2048).decode('utf-8')
        control.thisClient = getUser(userID)
        control.showframe(Home)
        arr1 = []
        arr2 = []
        for i in control.thisClient['book']:
            if i != {}:
                arr1.append(i['hotelName'])
                arr2.append(i['roomID'])
        control.frames[Refund].hl.set(arr1)
        control.frames[Refund].rl.set(arr2)
    elif flag == "fR":
        frame.announceS.grid_forget()
        frame.announceF.grid(row = 3, column = 5)
    elif flag == "sR":
        frame.announceF.grid_forget()
        frame.announceS.grid(row = 3, column = 5)
    else:
        frame.announceF.grid(row = 3, column = 5)

def sendSearch(client_socket, htn, ard, lvd, control, frame, root):
    global hotelSearchName
    global IDlist
    hotelSearchName = htn.get()
    client_socket.sendall(str.encode("\n".join(["search", hotelSearchName, "0", ard.get(), lvd.get(), "0"])))
    htn.set("")
    ard.set("")
    lvd.set("")

    flag = client_socket.recv(2048).decode('utf-8')

    if flag == 'fS':
        frame.announceF.grid(row = 8, column = 1)
    else:
        # data = client_socket.recv(2048)
        # data = data.decode('utf-8')
        frame.announceF.grid_forget()
        data = eval(flag)
        IDlist = data
        frameRoom = Room(root, client_socket, control)
        frameRoom.grid(row = 0, column = 0, sticky = "nsew")
        frameRoom.tkraise()

def sendBook(client_socket, htn, rt, ard, lvd, nt, control, frame, root):
    client_socket.sendall(str.encode("\n".join(["book", htn.get(), rt.get(), ard.get(), lvd.get(), nt.get()])))
    htn.set("")
    rt.set("")
    ard.set("")
    lvd.set("")
    nt.set("")
    flag = client_socket.recv(2048).decode('utf-8')
    if flag == 'sB':
        frame.payment.grid_forget()
        frame.announceF.grid_forget()
        frame.announceS.grid(row = 8, column = 1)
    else:
        frame.payment.grid_forget()
        frame.announceS.grid_forget()
        frame.announceF.grid(row = 8, column = 1)
        
    data.fi = open('account.json')
    data.account = json.load(data.fi)
    data.fi = open('hotel.json')
    data.hotels = json.load(data.fi)
    control.thisClient = getUser(control.thisClient['username'])
    arr1 = []
    arr2 = []
    for i in control.thisClient['book']:
        if i != {}:
            arr1.append(i['hotelName'])
            arr2.append(i['roomID'])
    control.frames[Refund].hl.set(arr1)
    control.frames[Refund].rl.set(arr2)
    control.frames[Refund].yourHotelList['listvariable'] = control.frames[Refund].hl
    control.frames[Refund].yourRoomList['listvariable'] = control.frames[Refund].rl

def finishBooking(client_socket, control, frame, root):
    client_socket.sendall(str.encode("\n".join(["finish", "0", "0", "0", "0", "0"])))
    totalMoney = client_socket.recv(2048).decode('utf-8')
    if totalMoney == "0":
        frame.announceF.grid_forget()
        frame.announceS.grid_forget()
        frame.payment.grid(row = 8, column = 1)
    else:
        frame.announceF.grid_forget()
        frame.announceS.grid_forget()
        frame.payment['text'] = "Total Money: %s" % totalMoney
        frame.payment.grid(row = 8, column = 1)

def refundBooking(client_socket, frame, control):
    client_socket.sendall(str.encode("\n".join(["refund", frame.htn.get(), frame.rt.get(), frame.ard.get(), frame.lvd.get(), "0"])))
    frame.htn.set("")
    frame.rt.set("")
    frame.ard.set("")
    frame.lvd.set("")
    refundMoney = client_socket.recv(2048).decode('utf-8')
    if refundMoney == "-1":
        frame.payment.grid(row = 8, column = 1)
    else:
        frame.payment['text'] = "Sucessful. Refund: to %s payID: %s" %(refundMoney, control.thisClient['payID'])
        frame.payment.grid(row = 8, column = 1)
    data.fi = open('account.json')
    data.account = json.load(data.fi)
    data.fi = open('hotel.json')
    data.hotels = json.load(data.fi)
    control.thisClient = getUser(control.thisClient['username'])
    arr1 = []
    arr2 = []
    for i in control.thisClient['book']:
        if i != {}:
            arr1.append(i['hotelName'])
            arr2.append(i['roomID'])
    control.frames[Refund].hl.set(arr1)
    control.frames[Refund].rl.set(arr2)

class Controller(tk.Tk):
    def __init__(self, client_socket, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.thisClient = {}
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for i in (Reg, Log, Home, Book, Refund):
            frame = i(container, client_socket, self)

            self.frames[i] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.showframe(Reg)

    def showframe(self, index):
        frame = self.frames[index]
        frame.tkraise()


class Reg(tk.Frame):
    def __init__(self, root, client_socket, contrl):
        tk.Frame.__init__(self, root)

        #Background
        self.Background = tk.Canvas(self, bg="sky blue").place(height = 400,width = 500)
        #Labels
        self.inform = tk.Label (self,bg ="white",text =  "Create An Account",font=('Helvetica 30 bold'),fg = "sky blue").grid(row = 0, column = 5, padx = 10, pady = 10)
        self.welcome = tk.Label (self,bg ="sky blue",text =  "Welcome back! ",font=('Helvetica 30 bold'),fg = "white").grid(row = 0, column = 0, padx = 10, pady = 10)
        self.welcom1 = tk.Label (self,bg ="sky blue" ,text ="Already a customer, sign in to continue booking", font =('Helvetica 15'),  fg = "white")
        self.username = tk.Label (self,bg ="light grey", text = "Username ", font=('Helvetica 15 bold'),fg = "sky blue")
        self.password = tk.Label (self, bg = "light grey", text = "Password ",font=('Helvetica 15 bold'),fg = "sky blue")
        self.payId = tk.Label (self,bg = "light grey", text = "Pay ID ",font=('Helvetica 15 bold'),fg = "sky blue")
        self.announceF = tk.Label(self, text = "Fail to register! Please check and try again!",font=('Helvetica 10 italic'),fg = "red")
        self.announceS = tk.Label(self, text = "Success! Press sign in button and log in to continue!",font=('Helvetica 10 italic'),fg = "green")
        #string var
        self.usn = tk.StringVar()
        self.pas = tk.StringVar()
        self.pay = tk.StringVar()
        #entry
        self.entry_username = ttk.Entry(self, textvariable = self.usn)
        self.entry_password = ttk.Entry(self,show = "*", textvariable = self.pas)
        self.entry_payId = ttk.Entry(self,textvariable = self.pay)
        #button
        self.create_button =ttk.Button(self, text="Register", command=lambda: create_user(client_socket, self.usn, self.pas, self.pay, "reg", contrl, self))
        self.signin_button = ttk.Button (self, text = "Sign In", command = lambda: contrl.showframe(Log))
        #display calls
        self.welcom1.grid(row = 3, column = 0, padx = 30, pady = 10)
        self.username.grid(row = 4, column = 4, padx = 40, pady = 10)
        self.password.grid(row = 5, column = 4, padx = 40, pady = 10)
        self.payId.grid(row = 6, column = 4, padx = 40, pady = 10)
        self.entry_username.grid(row = 4, column = 5, padx = 20, pady = 10, ipadx = 80, ipady = 3)
        self.entry_password.grid(row = 5, column = 5, padx = 20, pady = 10, ipadx = 80, ipady = 3)
        self.entry_payId.grid(row = 6, column = 5, padx = 20, pady = 10, ipadx = 80, ipady = 3)
        self.signin_button.grid(row = 6, column = 0, padx = 10, pady = 10)
        self.create_button.grid(row = 7, column = 5, padx = 10, pady = 10)

class Log(tk.Frame):
    def __init__(self, root, client_socket, contrl):
        tk.Frame.__init__(self, root)
        #Background
        self.Background = tk.Canvas(self, bg="sky blue").place(height = 400,width = 550)
        #Labels
        self.inform = tk.Label (self,bg ="white",text =  "Log In To Your Account",font=('Helvetica 30 bold'),fg = "sky blue").grid(row = 0, column = 5, padx = 10, pady = 10)
        self.welcome = tk.Label (self,bg ="sky blue",text =  "Welcome back! ",font=('Helvetica 30 bold'),fg = "white").grid(row = 0, column = 0, padx = 10, pady = 10)
        self.welcom1 = tk.Label (self,bg ="sky blue" ,text ="Not a customer, create an account to continue booking", font =('Helvetica 15'),  fg = "white")
        self.username = tk.Label (self,bg ="light grey", text = "Username ", font=('Helvetica 15 bold'),fg = "sky blue")
        self.password = tk.Label (self,bg = "light grey", text = "Password ",font=('Helvetica 15 bold'),fg = "sky blue")
        self.announceF = tk.Label(self, text = "Fail to log in! Please check and try again!",font=('Helvetica 10 italic'),fg = "red")
        #string var
        self.usn = tk.StringVar()
        self.pas = tk.StringVar()
        #entry
        self.entry_username = ttk.Entry(self, textvariable = self.usn)
        self.entry_password = ttk.Entry(self, show = "*", textvariable = self.pas)
        #button
        self.create_button =ttk.Button(self, text="Login", command=lambda: create_user(client_socket, self.usn, self.pas, "0", "log", contrl, self))
        self_button = ttk.Button (self, text = "Sign Up", command = lambda: contrl.showframe(Reg))
        #display calls
        self.welcom1.grid(row = 3, column = 0, padx = 30, pady = 10)
        self.username.grid(row = 4, column = 4, padx = 40, pady = 10)
        self.password.grid(row = 5, column = 4, padx = 40, pady = 10)
        self.entry_username.grid(row = 4, column = 5, padx = 20, pady = 10, ipadx = 80, ipady = 3)
        self.entry_password.grid(row = 5, column = 5, padx = 20, pady = 10, ipadx = 80, ipady = 3)
        self_button.grid(row = 5, column = 0, padx = 10, pady = 10)
        self.create_button.grid(row = 6, column = 5, padx = 10, pady = 10)

class Home(tk.Frame):
    def __init__(self, root, client_socket, contrl):
        tk.Frame.__init__(self, root)
        #Background
        self.Background = tk.Canvas(self, bg="sky blue").place(height = 750,width = 750)
        #Labels
        self.searchLabel = tk.Label (self, bg ="sky blue", text = "Search Room",font=('Helvetica 30 bold'),fg = "white").grid(row = 3, column = 1, pady = 10)
        self.note = tk.Label (self, bg ="sky blue" , text = "Fill up the form below to search", font =('Helvetica 15'),  fg = "white")
        self.hotelName = tk.Label (self, bg ="light grey", text = "Hotel name", font=('Helvetica 15 bold'),fg = "sky blue")
        self.arrivalDate = tk.Label (self, bg = "light grey", text = "Arrival Date",font=('Helvetica 15 bold'),fg = "sky blue")
        self.leavingDate = tk.Label (self, bg = "light grey", text = "Leaving Date",font=('Helvetica 15 bold'),fg = "sky blue")
        self.announceF = tk.Label(self, bg = "sky blue", text = "Fail to search or hotel is full! Please check and try again!",font=('Helvetica 10 italic'),fg = "red")
        
        #string var
        self.htn = tk.StringVar()
        self.ard = tk.StringVar()
        self.lvd = tk.StringVar()
        #entry
        self.entry_hotelName = ttk.Entry(self, textvariable = self.htn)
        self.entry_arrivalDate = ttk.Entry(self, textvariable = self.ard)
        self.entry_leavingDate = ttk.Entry(self, textvariable = self.lvd)
        #button
        self.searchButton =ttk.Button(self, text = "Search", command=lambda: sendSearch(client_socket, self.htn, self.ard, self.lvd, contrl, self, root))
        self.bookingButton = ttk.Button (self, text = "Book", command = lambda: contrl.showframe(Book))
        self.refundButton = ttk.Button(self, text = "Refund", command = lambda: contrl.showframe(Refund))
        #display calls
        self.note.grid(row = 4, column = 1, pady = 10)
        self.hotelName.grid(row = 5, column = 0, pady = 10)
        self.arrivalDate.grid(row = 6, column = 0, pady = 10)
        self.leavingDate.grid(row = 7, column = 0, pady = 10)
        self.entry_hotelName.grid(row = 5, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_arrivalDate.grid(row = 6, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_leavingDate.grid(row = 7, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.searchButton.grid(row = 9, column = 1, padx = 10, pady = 10)
        self.bookingButton.grid(row = 10, column = 1, padx = 10, pady = 10)
        self.refundButton.grid(row = 11, column = 1, padx = 10, pady = 10)
        # hotel list
        self.hotelBox = tk.LabelFrame(self, text='HOTEL LIST', bd=4, labelanchor='n', font='Helvetica 30 bold', fg='navy blue', width=600, height=100)
        hotel = []
        for i in data.hotels['hotel']:
            hotel.append(i['name'])
        self.hotelBox.grid(row = 0, column = 1)
        self.hotel_var = tk.StringVar(value = hotel)
        self.htlist = tk.Listbox(self.hotelBox, bg = "light green", height = 5, width = 31, font = ("Helvetica 20"), fg = "white", listvariable = self.hotel_var)
        scrollbar = tk.Scrollbar(self, orient = 'vertical', command = self.htlist.yview)
        self.htlist['yscrollcommand'] = scrollbar.set
        self.htlist.grid(row = 1, column = 1)

class Room(tk.Frame):
    def __init__(self, root, client_socket, contrl):
        tk.Frame.__init__(self, root)

        # Create frame
        mainframe = tk.Frame(self)
        mainframe.pack(fill=BOTH, expand=1)
        # Create canvas
        roomcanvas = tk.Canvas(mainframe, height = 600)
        roomcanvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Add scrollbar
        roomscrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=roomcanvas.yview)
        roomscrollbar.pack(side=RIGHT, fill=Y) 
        # Configure Canvas
        roomcanvas.configure(yscrollcommand=roomscrollbar.set)
        roomcanvas.bind('<Configure>', lambda e: roomcanvas.configure(scrollregion = roomcanvas.bbox("all")))
        # Create another frame in canvas
        roomframe = tk.Frame(roomcanvas, bg = "sky blue", height = 600, width = 500)
        # Add new roomframe to a window in canvas 
        roomcanvas.create_window((0,0), window = roomframe, anchor = "nw")

        self.hotelName = tk.Label (roomframe, bg ="light green", text = hotelSearchName,font=('Helvetica 30 bold'),fg = "navy blue").grid(row = 0, column = 0, pady = 10)
        count = 1
        for i in data.hotels['hotel']:
            if hotelSearchName == i['name']:
                for j in i['room']:
                    if int(j['ID']) in IDlist:
                        tk.Label(roomframe, bg ="sky blue", text = "ID: %s" %j['ID'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = "Type: %s" %j['type'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = "Description: %s" %j['description'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = "Price: %s" %j['price'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = j['image'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = "____________________________________________________________________",font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                break
        self.searchAgainButton = tk.Button(roomframe, text="Search Again", command = lambda: contrl.showframe(Home)).grid(row=count,column=0)
        count += 1
        self.bookingButton = tk.Button(roomframe, text="Book", command = lambda: contrl.showframe(Book)).grid(row=count,column=0)

class Book(tk.Frame):
    def __init__(self, root, client_socket, contrl):
        tk.Frame.__init__(self, root)
        #Background
        self.Background = tk.Canvas(self, bg="sky blue").place(height = 500,width = 550)
        #Labels
        self.searchLabel = tk.Label (self, bg ="sky blue", text = "Booking",font=('Helvetica 30 bold'),fg = "white").grid(row = 0, column = 1, pady = 10)
        self.note = tk.Label (self, bg ="sky blue" , text = "Fill up the form below to book", font =('Helvetica 15'),  fg = "white")
        self.hotelName = tk.Label (self, bg ="light grey", text = "Hotel name", font=('Helvetica 15 bold'),fg = "sky blue")
        self.roomType = tk.Label (self, bg ="light grey", text = "Room type", font=('Helvetica 15 bold'),fg = "sky blue")
        self.arrivalDate = tk.Label (self, bg = "light grey", text = "Arrival Date",font=('Helvetica 15 bold'),fg = "sky blue")
        self.leavingDate = tk.Label (self, bg = "light grey", text = "Leaving Date",font=('Helvetica 15 bold'),fg = "sky blue")
        self.noteUser = tk.Label (self, bg ="light grey", text = "Note", font=('Helvetica 15 bold'),fg = "sky blue")
        self.announceS = tk.Label(self, bg = "sky blue", text = "Success!",font=('Helvetica 10 italic'),fg = "green")
        self.announceF = tk.Label(self, bg = "sky blue", text = "Fail to book! Please check and try again!",font=('Helvetica 10 italic'),fg = "red")
        self.payment = tk.Label(self, bg = "sky blue", text = "You haven't booked anything!",font=('Helvetica 10 italic'),fg = "black")
        #string var
        self.htn = tk.StringVar()
        self.rt = tk.StringVar()
        self.ard = tk.StringVar()
        self.lvd = tk.StringVar()
        self.nt = tk.StringVar()
        #entry
        self.entry_hotelName = ttk.Entry(self, textvariable = self.htn)
        self.entry_roomType = ttk.Entry(self, textvariable = self.rt)
        self.entry_arrivalDate = ttk.Entry(self, textvariable = self.ard)
        self.entry_leavingDate = ttk.Entry(self, textvariable = self.lvd)
        self.entry_noteUser = ttk.Entry(self, textvariable = self.nt)
        #button
        self.searchButton =ttk.Button(self, text = "Search", command = lambda: contrl.showframe(Home))
        self.bookingButton = ttk.Button (self, text = "Submit", command=lambda: sendBook(client_socket, self.htn, self.rt, self.ard, self.lvd, self.nt, contrl, self, root))
        self.finishButton = ttk.Button (self, text = "Finish", command = lambda: finishBooking(client_socket, contrl, self, root))
        self.refundButton = ttk.Button (self, text = "Refund", command = lambda: contrl.showframe(Refund))
        #display calls
        self.note.grid(row = 2, column = 1, pady = 10)
        self.hotelName.grid(row = 3, column = 0, pady = 10)
        self.roomType.grid(row = 4, column = 0, pady = 10)
        self.arrivalDate.grid(row = 5, column = 0, pady = 10)
        self.leavingDate.grid(row = 6, column = 0, pady = 10)
        self.noteUser.grid(row = 7, column = 0, pady = 10)
        self.entry_hotelName.grid(row = 3, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_roomType.grid(row = 4, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_arrivalDate.grid(row = 5, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_leavingDate.grid(row = 6, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_noteUser.grid(row = 7, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.searchButton.grid(row = 9, column = 0, padx = 10, pady = 10)
        self.bookingButton.grid(row = 9, column = 1, padx = 10, pady = 10)
        self.finishButton.grid(row = 9, column = 2, padx = 10, pady = 10)
        self.refundButton.grid(row = 10, column = 1, padx = 10, pady = 10)

class Refund(tk.Frame):
    def __init__(self, root, client_socket, control):
        tk.Frame.__init__(self, root)
        self.child1 = tk.Frame(self)
        self.child2 = tk.LabelFrame(self, text='YOUR-BOOKED-LIST', labelanchor='n', font='Helvetica 30 bold', fg='pink', width=600, height=100)
        #Background
        self.Background = tk.Canvas(self.child1, bg="sky blue").place(height = 500,width = 550)
        #Labels
        self.searchLabel = tk.Label (self.child1, bg ="sky blue", text = "Refund",font=('Helvetica 30 bold'),fg = "white").grid(row = 0, column = 1, pady = 10)
        self.hotelName = tk.Label (self.child1, bg ="light grey", text = "Hotel name", font=('Helvetica 15 bold'),fg = "sky blue")
        self.roomType = tk.Label (self.child1, bg ="light grey", text = "Room ID", font=('Helvetica 15 bold'),fg = "sky blue")
        self.arrivalDate = tk.Label (self.child1, bg ="light grey", text = "Arrival Date", font=('Helvetica 15 bold'),fg = "sky blue")
        self.leavingDate = tk.Label (self.child1, bg ="light grey", text = "Leaving Date", font=('Helvetica 15 bold'),fg = "sky blue")
        self.payment = tk.Label(self.child1, text = "Fail to remove! Please check and try again!",font=('Helvetica 10 italic'),fg = "red")
        self.hotelNameCol = tk.Label(self.child2, text = "Hotel", bg = "black", font=('Helvetica 20 bold'),fg = "pink")
        self.roomTypeCol = tk.Label(self.child2, text = "Room", bg = "black", font=('Helvetica 20 bold'),fg = "pink")
        #string var
        self.htn = tk.StringVar()
        self.rt = tk.StringVar()
        self.hl = tk.StringVar()
        self.rl = tk.StringVar()
        self.ard = tk.StringVar()
        self.lvd = tk.StringVar()
        #entry
        self.entry_hotelName = ttk.Entry(self.child1, textvariable = self.htn)
        self.entry_roomType = ttk.Entry(self.child1, textvariable = self.rt)
        self.entry_arrivalDate = ttk.Entry(self.child1, textvariable = self.ard)
        self.entry_leavingDate = ttk.Entry(self.child1, textvariable = self.lvd)
        #button
        self.searchButton =ttk.Button(self.child1, text = "Search", command = lambda: control.showframe(Home))
        self.submitButton = ttk.Button (self.child1, text = "Submit", command = lambda: refundBooking(client_socket, self, control))
        self.bookButton = ttk.Button(self.child1, text = "Book", command=lambda: control.showframe(Book))
        #listbox
        self.yourHotelList = tk.Listbox(self.child2, height = 10, width = 20, font = ("Helvetica 20"), listvariable = self.hl)
        self.yourRoomList = tk.Listbox(self.child2, height = 10, width = 20, font = ("Helvetica 20"), listvariable = self.rl)
        
        #scrollbar
        self.scrollbarH = tk.Scrollbar(self, orient = 'vertical', command = self.yourHotelList.yview)
        self.scrollbarR = tk.Scrollbar(self, orient = 'vertical', command = self.yourRoomList.yview)
        self.yourHotelList['yscrollcommand'] = self.scrollbarH.set
        self.yourRoomList['yscrollcommand'] = self.scrollbarR.set
        #display calls
        self.hotelName.grid(row = 3, column = 0, pady = 10)
        self.roomType.grid(row = 4, column = 0, pady = 10)
        self.arrivalDate.grid(row = 5, column = 0, pady = 10)
        self.leavingDate.grid(row = 6, column = 0, pady = 10)
        self.entry_hotelName.grid(row = 3, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_roomType.grid(row = 4, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_arrivalDate.grid(row = 5, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.entry_leavingDate.grid(row = 6, column = 1, padx = 10, pady = 10, ipadx = 80, ipady = 3)
        self.searchButton.grid(row = 9, column = 0, padx = 10, pady = 10)
        self.submitButton.grid(row = 9, column = 1, padx = 10, pady = 10)
        self.bookButton.grid(row = 9, column = 2, padx = 10, pady = 10)
        self.child1.grid(row = 0, column = 0)
        self.hotelNameCol.grid(row = 1, column = 0)
        self.roomTypeCol.grid(row = 1, column = 1, padx = 50)
        self.yourHotelList.grid(row = 2, column = 0, pady = 10)
        self.yourRoomList.grid(row = 2, column = 1, pady = 10)
        self.child2.grid(row = 0, column = 1)

class Data:
    def __init__(self):
        self.fi = open('hotel.json')
        # load json data to dict account
        self.hotels = json.load(self.fi)
        self.fi = open('account.json')
        self.account = json.load(self.fi)
#only read
IDlist = []
hotelSearchName = ""
data = Data()


