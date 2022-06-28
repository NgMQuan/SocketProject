#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
#https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import tkinter

HOST = "127.0.0.1"
PORT = 62000
if not PORT:
    PORT = 62000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def create_user (event = None):
    """Handles sending username and password."""

    client_socket.send(bytes("reg", "utf8"))
    client_socket.send(bytes(usn.get(), "utf8"))
    client_socket.send(bytes(pas.get(), "utf8"))
    client_socket.send(bytes(pay.get(), "utf8"))
    usn.set("")
    pas.set ("")
    pay.set("")


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Spy x Family Booking")
top.configure ( bg = "white")
Background = tkinter.Canvas(top, bg="sky blue").place(height = 400,width = 355)
inform = tkinter.Label ( top,bg ="white",text =  " Create Account",font=('Helvetica 30 bold'),fg = "sky blue").place(x = 430, y = 100)
welcome = tkinter.Label ( top,bg ="sky blue",text =  " Welcome back! ",font=('Helvetica 30 bold'),fg = "white").place(x = 59, y = 100)
welcom1 = tkinter.Label ( top,bg ="sky blue" ,text =" Already a customer, sign in to continue booking", font =('Helvetica 15'),  fg = "white")
welcom1.place ( x = 29, y = 190)
username = tkinter.Label ( top,bg ="light grey", text = " Username ", font=('Helvetica 15 bold'),fg = "sky blue")
username.place (x = 400, y = 200 )
usn = tkinter.StringVar()
password = tkinter.Label ( top,bg = "light grey", text = " Password ",font=('Helvetica 15 bold'),fg = "sky blue")
password.place ( x= 400 , y = 240)
pas = tkinter.StringVar()
payId = tkinter.Label ( top,bg = "light grey", text = " Pay ID ",font=('Helvetica 15 bold'),fg = "sky blue")
payId.place ( x= 400 , y = 280)
pay = tkinter.StringVar()
entry_username = tkinter.Entry (top)
entry_username.place ( x = 490, y = 200)
entry_password = tkinter.Entry (top)
entry_password.place ( x = 490, y = 240 )
entry_payId = tkinter.Entry (top)
entry_payId.place ( x = 490, y = 280 )
create_button =tkinter.Button(top, text="Create", command=create_user)
create_button.place(x = 540, y = 320)
signin_button = tkinter.Button (top, text = " Sign in ", command = create_user)
signin_button.place (x = 130, y = 270 )


#messages_frame =tkinter.Label(top, text = " Hello")

my_msg =tkinter.StringVar()  # For the messages to be sent.
#my_msg.set("Type your messages here.")
#scrollbar =tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
#msg_list =tkinter. Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
#scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
#msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
#msg_list.pack()
#messages_frame.pack()
# = tkinter.Entry(top, textvariable=my_msg)
#entry_field.bind("<Return>", send)
#entry_field.pack()
#send_button =tkinter.Button(top, text="Send", command=send)
#send_button.place(x = 130, y = 130)

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----


receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
