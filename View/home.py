from tkinter import *
from tkinter import ttk


class Home:
    def __init__(self, window):
        self.wind = window
        self.wind.title('DataStructure')
        ##self.wind(height=10, columns=4)

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text='Options project')
        frame.grid(row=0, column=0, ipady=160, ipadx=160)

        # Name Input
        #Label(frame, text='Name: ').grid(row=0, column=0)
        self.json = Entry(frame)
        self.json.grid(row=0, column=1)

        # Button Add
        button1 = ttk.Button(frame, text='Play').grid(row=0, column=0)
        button2 = ttk.Button(frame, text='Next').grid(row=1, column=0)
        button3 = ttk.Button(frame, text='Reset').grid(row=2, column=0)


if __name__ == '__main__':
    window = Tk()
    #window.geometry('400x500')
    #window.resizable(width=0, height=0)
    application = Home(window)
    window.mainloop()
