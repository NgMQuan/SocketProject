from http import client
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import BOTH, ttk
from tkProc import *

def initGUI(client_socket):
    root = tk.Tk()
    root.title("Spy x Family Booking")
    root.geometry('1120x960')
    root.resizable(0, 0)
    scr = Reg(root, client_socket)
    root.mainloop()

class Reg:
    def __init__(self, root, client_socket):
        self.reg = tk.Frame(root).pack()
        #Background
        self.Background = tk.Canvas(self.reg, bg="sky blue").place(height = 400,width = 355)
        #Labels
        self.inform = tk.Label (self.reg,bg ="white",text =  " Create Account",font=('Helvetica 30 bold'),fg = "sky blue").place(x = 430, y = 100)
        self.welcome = tk.Label (self.reg,bg ="sky blue",text =  " Welcome back! ",font=('Helvetica 30 bold'),fg = "white").place(x = 59, y = 100)
        self.welcom1 = tk.Label (self.reg,bg ="sky blue" ,text =" Already a customer, sign in to continue booking", font =('Helvetica 15'),  fg = "white")
        self.username = tk.Label (self.reg,bg ="light grey", text = " Username ", font=('Helvetica 15 bold'),fg = "sky blue")
        self.password = tk.Label (self.reg,bg = "light grey", text = " Password ",font=('Helvetica 15 bold'),fg = "sky blue")
        self.payId = tk.Label (self.reg,bg = "light grey", text = " Pay ID ",font=('Helvetica 15 bold'),fg = "sky blue")
        #string var
        self.usn = tk.StringVar()
        self.pas = tk.StringVar()
        self.pay = tk.StringVar()
        #entry
        self.entry_username = ttk.Entry(self.reg, textvariable = self.usn)
        self.entry_password = ttk.Entry(self.reg, textvariable = self.pas)
        self.entry_payId = ttk.Entry(self.reg,textvariable = self.pay)
        #button
        self.create_button =ttk.Button(self.reg, text="Create", command=lambda: create_user(client_socket, self.usn, self.pas, self.pay))
        self.signin_button = ttk.Button (self.reg, text = " Sign in ", command = lambda: create_user(client_socket, self.usn, self.pas, self.pay))
        #display calls
        self.welcom1.place (x = 29, y = 190)
        self.username.place (x = 400, y = 200)
        self.password.place (x= 400 , y = 240)
        self.payId.place (x= 400 , y = 280)
        self.entry_username.place (x = 490, y = 200)
        self.entry_password.place (x = 490, y = 240)
        self.entry_payId.place (x = 490, y = 280)
        self.signin_button.place (x = 130, y = 270)
        self.create_button.place(x = 540, y = 320)
