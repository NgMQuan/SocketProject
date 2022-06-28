from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tki import *

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            #msg = client_socket.recv(BUFSIZ).decode("utf8")
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

receive_thread = Thread(target=receive)
receive_thread.start()

root = tk.Tk()
initRegScr(root)
root.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()