from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

def initRegScr(top):
    reg = tk.Frame(top)
    #Background
    Background = tkinter.Canvas(reg, bg="sky blue").place(height = 400,width = 355)
    #Labels
    inform = tkinter.Label (reg,bg ="white",text =  " Create Account",font=('Helvetica 30 bold'),fg = "sky blue").place(x = 430, y = 100)
    welcome = tkinter.Label (reg,bg ="sky blue",text =  " Welcome back! ",font=('Helvetica 30 bold'),fg = "white").place(x = 59, y = 100)
    welcom1 = tkinter.Label (reg,bg ="sky blue" ,text =" Already a customer, sign in to continue booking", font =('Helvetica 15'),  fg = "white")
    username = tkinter.Label (reg,bg ="light grey", text = " Username ", font=('Helvetica 15 bold'),fg = "sky blue")
    password = tkinter.Label (reg,bg = "light grey", text = " Password ",font=('Helvetica 15 bold'),fg = "sky blue")
    payId = tkinter.Label (reg,bg = "light grey", text = " Pay ID ",font=('Helvetica 15 bold'),fg = "sky blue")
    #string var
    usn = tkinter.StringVar()
    pas = tkinter.StringVar()
    pay = tkinter.StringVar()
    #entry
    entry_username = tkinter.Entry (reg)
    entry_password = tkinter.Entry (reg)
    entry_payId = tkinter.Entry (reg)
    #button
    create_button =tkinter.Button(reg, text="Create", command=create_user)
    signin_button = tkinter.Button (reg, text = " Sign in ", command = create_user)
    #display calls
    reg.pack()
    welcom1.place ( x = 29, y = 190)
    username.place (x = 400, y = 200 )
    password.place ( x= 400 , y = 240)
    payId.place ( x= 400 , y = 280)
    entry_username.place ( x = 490, y = 200)
    entry_password.place ( x = 490, y = 240 )
    entry_payId.place ( x = 490, y = 280 )
    signin_button.place (x = 130, y = 270 )
    create_button.place(x = 540, y = 320)