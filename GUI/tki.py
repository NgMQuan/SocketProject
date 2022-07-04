from http import client
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import BOTH, ttk
from tkProc import *

def initGUI(client_socket):
    a = Controller(client_socket)
    a.mainloop()

class Controller(tk.Tk):
    def __init__(self, client_socket, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for i in (Reg, Log):
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
        self.Background = tk.Canvas(self, bg="sky blue").place(height = 400,width = 355)
        #Labels
        self.inform = tk.Label (self,bg ="white",text =  " Create Account",font=('Helvetica 30 bold'),fg = "sky blue").grid(row = 0, column = 4, padx = 10, pady = 10)
        self.welcome = tk.Label (self,bg ="sky blue",text =  " Welcome back! ",font=('Helvetica 30 bold'),fg = "white").grid(row = 0, column = 0, padx = 10, pady = 10)
        self.welcom1 = tk.Label (self,bg ="sky blue" ,text =" Already a customer, sign in to continue booking", font =('Helvetica 15'),  fg = "white")
        self.username = tk.Label (self,bg ="light grey", text = " Username ", font=('Helvetica 15 bold'),fg = "sky blue")
        self.password = tk.Label (self,bg = "light grey", text = " Password ",font=('Helvetica 15 bold'),fg = "sky blue")
        self.payId = tk.Label (self,bg = "light grey", text = " Pay ID ",font=('Helvetica 15 bold'),fg = "sky blue")
        #string var
        self.usn = tk.StringVar()
        self.pas = tk.StringVar()
        self.pay = tk.StringVar()
        #entry
        self.entry_username = ttk.Entry(self, textvariable = self.usn)
        self.entry_password = ttk.Entry(self, textvariable = self.pas)
        self.entry_payId = ttk.Entry(self,textvariable = self.pay)
        #button
        self.create_button =ttk.Button(self, text="Create", command=lambda: create_user(client_socket, self.usn, self.pas, self.pay, "reg"))
        self.signin_button = ttk.Button (self, text = " Sign in ", command = lambda: contrl.showframe(Log))
        #display calls
        self.welcom1.grid(row = 1, column = 0, padx = 30, pady = 10)
        self.username.grid(row = 3, column = 4, padx = 10, pady = 10)
        self.password.grid(row = 4, column = 4, padx = 10, pady = 10)
        self.payId.grid(row = 5, column = 4, padx = 10, pady = 10)
        self.entry_username.grid(row = 3, column = 5, padx = 20, pady = 10)
        self.entry_password.grid(row = 4, column = 5, padx = 20, pady = 10)
        self.entry_payId.grid(row = 5, column = 5, padx = 20, pady = 10)
        self.signin_button.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.create_button.grid(row = 6, column = 5, padx = 10, pady = 10)

class Log(tk.Frame):
    def __init__(self, root, client_socket, contrl):
        tk.Frame.__init__(self, root)
        #Background
        self.Background = tk.Canvas(self, bg="sky blue").place(height = 400,width = 355)
        #Labels
        self.inform = tk.Label (self,bg ="white",text =  " Login",font=('Helvetica 30 bold'),fg = "sky blue").grid(row = 0, column = 4, padx = 10, pady = 10)
        self.welcome = tk.Label (self,bg ="sky blue",text =  " Welcome back! ",font=('Helvetica 30 bold'),fg = "white").grid(row = 0, column = 0, padx = 10, pady = 10)
        self.welcom1 = tk.Label (self,bg ="sky blue" ,text =" Not a customer, create an account to continue booking", font =('Helvetica 15'),  fg = "white")
        self.username = tk.Label (self,bg ="light grey", text = " Username ", font=('Helvetica 15 bold'),fg = "sky blue")
        self.password = tk.Label (self,bg = "light grey", text = " Password ",font=('Helvetica 15 bold'),fg = "sky blue")
        #string var
        self.usn = tk.StringVar()
        self.pas = tk.StringVar()
        #entry
        self.entry_username = ttk.Entry(self, textvariable = self.usn)
        self.entry_password = ttk.Entry(self, textvariable = self.pas)
        #button
        self.create_button =ttk.Button(self, text="Login", command=lambda: create_user(client_socket, self.usn, self.pas, "0", "log"))
        self_button = ttk.Button (self, text = " Regist ", command = lambda: contrl.showframe(Reg))
        #display calls
        self.welcom1.grid(row = 1, column = 0, padx = 30, pady = 10)
        self.username.grid(row = 3, column = 4, padx = 10, pady = 10)
        self.password.grid(row = 4, column = 4, padx = 10, pady = 10)
        self.entry_username.grid(row = 3, column = 5, padx = 20, pady = 10)
        self.entry_password.grid(row = 4, column = 5, padx = 20, pady = 10)
        self_button.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.create_button.grid(row = 6, column = 5, padx = 10, pady = 10)