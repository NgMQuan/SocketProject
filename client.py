from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys
sys.path.insert(0, 'GUI')
from tki import *

def receive():
    """Handles receiving of messages."""
    while True:
         try:
             msg = client_socket.recv(BUFSIZ).decode("utf8")
             #msg_list.insert(tkinter.END, msg)
    #         a = 0
         except OSError:  # Possibly client has left the chat.
             break


# def send(event=None):  # event is passed by binders.
#     """Handles sending of messages."""
#     msg = my_msg.get()
#     my_msg.set("")  # Clears input field.
#     client_socket.send(bytes(msg, "utf8"))
#     if msg == "{quit}":
#         client_socket.close()
#         root.quit()

# def on_closing(event=None):
#     """This function is to be called when the window is closed."""
#     my_msg.set("{quit}")
#     send()

HOST = "127.0.0.1"
PORT = 60008

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread()
receive_thread.start()

#root.protocol("WM_DELETE_WINDOW", on_closing)
if __name__ == "__main__":
    initGUI(client_socket)
