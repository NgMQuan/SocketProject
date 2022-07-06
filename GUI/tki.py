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
        control.showframe(Home)
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
    client_socket.sendall(str.encode("\n".join([hotelSearchName, ard.get(), lvd.get()])))
    htn.set("")
    ard.set("")
    lvd.set("")

    flag = client_socket.recv(2048).decode('utf-8')

    if flag == 'fS':
        frame.announceF.grid(row = 8, column = 1)
    else:
        # data = client_socket.recv(2048)
        # data = data.decode('utf-8')
        data = eval(flag)
        IDlist = data
        frameRoom = Room(root, client_socket, control)
        frameRoom.grid(row = 0, column = 0, sticky = "nsew")
        frameRoom.tkraise()

class Controller(tk.Tk):
    def __init__(self, client_socket, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for i in (Reg, Log, Home):
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
        self.password = tk.Label (self,bg = "light grey", text = "Password ",font=('Helvetica 15 bold'),fg = "sky blue")
        self.payId = tk.Label (self,bg = "light grey", text = "Pay ID ",font=('Helvetica 15 bold'),fg = "sky blue")
        self.announceF = tk.Label(self, text = "Fail to register! Please check and try again!",font=('Helvetica 10 italic'),fg = "red")
        self.announceS = tk.Label(self, text = "Succeed! Press sign in button and log in to continue!",font=('Helvetica 10 italic'),fg = "green")
        #string var
        self.usn = tk.StringVar()
        self.pas = tk.StringVar()
        self.pay = tk.StringVar()
        #entry
        self.entry_username = ttk.Entry(self, textvariable = self.usn)
        self.entry_password = ttk.Entry(self, textvariable = self.pas)
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
        self.entry_password = ttk.Entry(self, textvariable = self.pas)
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
        self.Background = tk.Canvas(self, bg="sky blue").place(height = 600,width = 750)
        #Labels
        self.searchLabel = tk.Label (self, bg ="sky blue", text = "Search Room",font=('Helvetica 30 bold'),fg = "white").grid(row = 3, column = 1, pady = 10)
        self.note = tk.Label (self, bg ="sky blue" , text = "Fill up the form below to search", font =('Helvetica 15'),  fg = "white")
        self.hotelName = tk.Label (self, bg ="light grey", text = "Hotel name", font=('Helvetica 15 bold'),fg = "sky blue")
        self.arrivalDate = tk.Label (self, bg = "light grey", text = "Arrival Date",font=('Helvetica 15 bold'),fg = "sky blue")
        self.leavingDate = tk.Label (self, bg = "light grey", text = "Leaving Date",font=('Helvetica 15 bold'),fg = "sky blue")
        self.announceF = tk.Label(self, bg = "sky blue", text = "Fail to search! Please check and try again!",font=('Helvetica 10 italic'),fg = "red")
        
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
        self.bookingButton = ttk.Button (self, text = "Book")
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
        
        # hotel list
        self.hotelBox = tk.LabelFrame(self, text='HOTEL LIST', bd=4, labelanchor='n', font='Helvetica 30 bold', fg='navy blue', width=600, height=100)
        hotel = []
        for i in hotels['hotel']:
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
        for i in hotels['hotel']:
            if hotelSearchName == i['name']:
                for j in i['room']:
                    if int(j['ID']) in IDlist:
                        tk.Label(roomframe, bg ="sky blue", text = j['ID'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = j['type'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = j['description'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = j['price'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = j['image'],font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                        tk.Label(roomframe, bg ="sky blue", text = "__________________________________",font=('Helvetica 15'),fg = "black").grid(row = count, column = 0, pady = 10)
                        count += 1
                break

IDlist = []
hotelSearchName = ""
fi = open('hotel.json')
# load json data to dict account
hotels = json.load(fi)