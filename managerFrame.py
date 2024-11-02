import socket
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from messages import *


class ManagerFrame(Frame):
    def __init__(self, client):
        Frame.__init__(self)
        self.pack()
        self.client = client
        self.master.title("Manager Panel")
        self.master.resizable(False, False)

        # for the center the window on the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = (screen_width - 450) // 2
        y_coordinate = (screen_height - 210) // 2
        self.master.geometry(f"{450}x{210}+{x_coordinate}+{y_coordinate}")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.title = Label(self.frame1, text="REPORTS")
        self.title.pack(padx=5, pady=5)

        # Frame 2:
        self.frame2 = Frame()
        self.frame2.pack()

        reportSelections = ["(1)What is the most rented book overall?",
                            "(2) Which librarian has the highest number of operations?",
                            "(3) What is the total generated revenue by the library?",
                            "(4) What is the average rental period for the 'Harry Potter' book?"]

        self.chosenReport = StringVar()
        self.chosenReport.set(reportSelections[0])

        for i in range(len(reportSelections)):
            button_ = Radiobutton(self.frame2,
                                  text=reportSelections[i],
                                  variable=self.chosenReport,
                                  value=i,
                                  )
            button_.pack(anchor='w')

        self.frame3 = Frame()
        self.frame3.pack(padx=25, pady=5)

        self.CreateButton = Button(self.frame3, text="Create", command=self.CreateButtonPressed, height=1, width=40)
        self.CreateButton.pack(side=LEFT, padx=5, pady=5)

        self.CloseButton = Button(self.frame3, text="Close", command=self.CloseButtonPressed, height=1, width=15)
        self.CloseButton.pack(side=RIGHT, padx=5, pady=5)
        self.master.protocol("WM_DELETE_WINDOW", exitWindow)

    def CreateButtonPressed(self):

        input_ = int(self.chosenReport.get())
        msg = ""
        msg1 = ""

        if input_ == 0:
            msg = "report1"
            msg1 = "The Most Rented book(s):\n"
        elif input_ == 1:
            msg = "report2"
            msg1 = "Librarian(s) has the highest number of operations:\n"
        elif input_ == 2:
            msg = "report3"
            msg1 = "Total generated revenue by the library:\n"
        elif input_ == 3:
            msg = "report4"
            msg1 = "The average rental period for the 'Harry Potter' book:\n"
        else:
            msg = "error"

        self.client.send(msg.encode())

        data = self.client.recv(1024).decode()
        data = data.split(";")
        for i in data[1:]:
            msg1 = msg1 + "\n" + i
        infoMessages(data[0], msg1)

    def CloseButtonPressed(self):
        self.client.close()
        self.master.destroy()
        exit(1)


if __name__ == "__main__":
    SERVER = "127.0.0.1"
    PORT = 9000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    window = ManagerFrame(client)
    data = client.recv(1024).decode()
    print(data)
    window.mainloop()
