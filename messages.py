from tkinter import messagebox
import tkinter as tk
from tkinter.messagebox import askyesno

def errorMessages(title, message):
    root = tk.Tk()
    root.geometry("1x1")
    root.overrideredirect(True)
    messagebox.showerror(title, message)
    root.destroy()

def infoMessages(title, message):
    root = tk.Tk()
    root.geometry("1x1")
    root.overrideredirect(True)
    messagebox.showinfo(title, message)
    root.destroy()

def exitWindow():
    answer = askyesno(title='Exit', message='Do you want to exit ?')
    if answer:
        exit(1)
