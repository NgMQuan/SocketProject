from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

BUFSIZ = 1024

def create_user (client_socket, usn, pas, pay, mode, control):
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

    if flag == "success":
        control.showframe(Home)