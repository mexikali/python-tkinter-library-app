import socket
from loginFrame import *
from managerFrame import *
from librarianFrame import *
from messages import *

SERVER = "127.0.0.1"
PORT = 9000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

data = client.recv(1024).decode()
if data != "connectionsuccess":
    errorMessages("Connection Failed", "Please try again...\n")
    exit(1)

result = 0

while result == 0:

    window = LoginFrame(client)
    window.mainloop()

    data = client.recv(1024).decode()
    if data == "loginfailure":
        errorMessages("Login Failed", "Incorrect username or password\n")
    else:
        result = 1

data = data.split(";")
if data[2] == "librarian":
    window = LibrarianFrame(client, data[1])
    window.mainloop()
elif data[2] == "manager":
    window = ManagerFrame(client)
    window.mainloop()

client.close()
