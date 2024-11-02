import socket
from tkinter import *
from tkinter import messagebox
from messages import *
from datetime import datetime

class LibrarianFrame(Frame):
    def __init__(self, client, userName):
        Frame.__init__(self)

        self.userName = userName

        self.master.title("Librarian Panel")
        self.master.geometry("300x500")
        self.master.resizable(False, False)

        # for the center the window on the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = (screen_width - 300) // 2
        y_coordinate = (screen_height - 500) // 2
        self.master.geometry(f"{300}x{500}+{x_coordinate}+{y_coordinate}")

        self.frame1 = Frame()
        self.frame1.pack(padx=5, pady=5)

        self.client = client

        self.booksTitle = Label(self.frame1, text="Books")
        self.booksTitle.pack(padx=5, pady=5)

        self.frame2 = Frame()
        self.frame2.pack(padx=5, pady=5)

        self.books = ["A Tale of Two Cities",
                      "The Little Prince",
                      "Harry Potter",
                      "And Then The Were None",
                      "Dream of the Red Chamber",
                      "The Hobbit",
                      "She: A History of Adventure",
                      "Vardi Wala Gunda",
                      "The Da Vinci Code",
                      "The Alchemist"]

        self.chooseVar = [IntVar() for _ in range(len(self.books))]

        for i in range(len(self.books)):
            label = Label(self.frame2, text=self.books[i])
            label.grid(row=i, column=0, sticky="w")

            button_ = Checkbutton(self.frame2,
                                  variable=self.chooseVar[i],
                                  onvalue=i + 1,
                                  offvalue=0,  # You can set this to another value if needed
                                  )
            button_.grid(row=i, column=1, sticky="e")

        self.frame3 = Frame()
        self.frame3.pack(padx=5, pady=5)

        self.dateLabel = Label(self.frame3, text="Date (dd.mm.yyyy):")
        self.dateLabel.pack(side=LEFT, padx=5, pady=5)

        self.dateEntry = Entry(self.frame3)
        self.dateEntry.pack(side=LEFT, padx=5, pady=5)

        self.frame4 = Frame()
        self.frame4.pack(padx=5, pady=5)

        self.nameLabel = Label(self.frame4, text="Client's name: ")
        self.nameLabel.pack(side=LEFT, padx=5, pady=5)

        self.nameEntry = Entry(self.frame4)
        self.nameEntry.pack(side=LEFT, padx=5, pady=5)

        self.frame5 = Frame()
        self.frame5.pack(padx=10, pady=30)

        self.rentButton = Button(self.frame5, text="Rent", command=self.RentButtonPressed)
        self.rentButton.pack(side=LEFT, padx=5, pady=5)

        self.returnButton = Button(self.frame5, text="Return", command=self.ReturnButtonPressed)
        self.returnButton.pack(side=LEFT, padx=5, pady=5)

        self.CloseButton = Button(self.frame5, text="Close", command=self.CloseButtonPressed)
        self.CloseButton.pack(side=RIGHT, padx=5, pady=5)

        # when 'X' is pressed, it gives a confirmation window(exitWindow function will be run)
        self.master.protocol("WM_DELETE_WINDOW", exitWindow)

    def RentButtonPressed(self):

        rented = [var.get() for var in self.chooseVar if var.get() != 0]
        inputDate = self.dateEntry.get()
        clientName = self.nameEntry.get()

        if checkInputs(rented, inputDate, clientName):
            rented = ";".join(map(str, rented))
            msg = "rent" + ";" + self.userName + ";" + clientName + ";" + inputDate + ";" + rented
            self.client.send(msg.encode())

            data = self.client.recv(1024).decode()
            data = data.split(";")
            if data[0] == 'availabilityerror':
                msg = "The following books are out of stock to rent: \n"
                for i in data[1:]:
                    i = i.split("|")
                    msg = msg + "\n" + i[0] + "  --  " + i[1]
                errorMessages("Availability Error", msg)

            elif data[0] == 'renterror':
                msg = f"Client '{data[1]}' cannot rent new books without returning the following books that s/he rents: \n"
                for i in data[2:]:
                    i = i.split("|")
                    msg = msg + "\n" + i[0] + "  --  " + i[1]
                errorMessages("Rent Error", msg)

            elif data[0] == 'fileError':
                errorMessages("File Error", "An error occurred while saving the file. Please try again.")

            else:
                infoMessages("Success", "The operation was completed successfully.")
        else:
            errorMessages("Input Error", "You entered missing or incorrect entries. ")


    def ReturnButtonPressed(self):
        returned = [var.get() for var in self.chooseVar if var.get() != 0]
        inputDate = self.dateEntry.get()
        clientName = self.nameEntry.get()

        if checkInputs(returned, inputDate, clientName):
            returned = ";".join(map(str, returned))
            msg = "return" + ";" + self.userName + ";" + clientName + ";" + inputDate + ";" + returned
            self.client.send(msg.encode())
            data = self.client.recv(1024).decode()
            data = data.split(";")
            if data[0] == 'returnerror':
                msg = f"Client '{data[1]}' can not return this or these book(s): \n"
                for i in data[2:]:
                    i = i.split("|")
                    msg = msg + "\n" + i[0] + "  --  " + i[1]
                errorMessages("Return Error", msg)

            elif data[0] == 'fileError':
                errorMessages("File Error", "An error occurred while saving the file. Please try again.")
            elif data[0] == 'daterror':
                errorMessages("Date Error", "The book cannot be returned before the rental date.")
            else:
                infoMessages("Success", data[1])
        else:
            errorMessages("Input Error", "You entered missing or incorrect entries. ")


    def CloseButtonPressed(self):
        self.client.close()
        self.master.destroy()
        exit(1)


def checkInputs(checkButtons, inputDate, clientName):

    if len(checkButtons) == 0:
        return False

    if clientName == "":
        return False

    try:
        datetime.strptime(inputDate, '%d.%m.%Y')
    except ValueError:
        return False

    return True

if __name__ == "__main__":
    SERVER = "127.0.0.1"
    PORT = 9000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    window = LibrarianFrame(client, "deneme123")
    data = client.recv(1024).decode()
    print(data)
    window.mainloop()
