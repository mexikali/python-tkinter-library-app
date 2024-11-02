from tkinter import *
from messages import *

class LoginFrame(Frame):

    def __init__(self, client):
        Frame.__init__(self)

        self.client = client

        self.master.title("Login")
        self.master.geometry("250x125")

        self.master.resizable(False, False)

        # for the center the window on the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = (screen_width - 250) // 2
        y_coordinate = (screen_height - 125) // 2
        self.master.geometry(f"{250}x{125}+{x_coordinate}+{y_coordinate}")

        # Frame1 : userName
        self.frame1 = Frame()
        self.frame1.pack(padx=5, pady=5)

        self.userNameLabel = Label(self.frame1, text="User name")
        self.userNameLabel.pack(side=LEFT, padx=5, pady=5)

        self.userName = Entry(self.frame1, name="username")
        self.userName.pack(side=LEFT, padx=5, pady=5)

        # Frame2 : password
        self.frame2 = Frame()
        self.frame2.pack(padx=5, pady=5)

        self.passwordLabel = Label(self.frame2, text="Password")
        self.passwordLabel.pack(side=LEFT, padx=5, pady=5)

        self.password = Entry(self.frame2, name="password", show="*")
        self.password.pack(side=LEFT, padx=5, pady=5)

        # Frame2 : login button
        self.frame3 = Frame()
        self.frame3.pack(padx=5, pady=5)

        self.login = Button(self.frame3, text="Login", command=self.ButtonPressed)
        self.login.pack(side=LEFT, padx=5, pady=5)

        self.master.protocol("WM_DELETE_WINDOW", exitWindow)

    def ButtonPressed(self):
        username = self.userName.get()  # get username from the entry
        password = self.password.get()  # get password from the entry

        input_str = "login" + ";" + username + ";" + password
        self.client.send(input_str.encode())
        self.master.destroy()

    def logindestroy(self):
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()

    def getUserName(self, username):
        self.userName = username
        return username
