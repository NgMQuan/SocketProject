from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

def create_user (client_socket, usn, pas, pay):
    """Handles sending username and password."""
    client_socket.send(bytes("reg", "utf8"))
    client_socket.send(bytes(usn.get(), "utf8"))
    client_socket.send(bytes(pas.get(), "utf8"))
    client_socket.send(bytes(pay.get(), "utf8"))
    usn.set("")
    pas.set ("")
    pay.set("")