from statCollector import StatCollector
from battleMap import BattleMap
from tooltip import *
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

window = tk.Tk()
window.title("BattleTracker")
window.columnconfigure(0, minsize=200)
window.rowconfigure([0, 1, 2], minsize=50)
style = ThemedStyle(window)
style.theme_use("equilux")
bg = style.lookup('TLabel', 'background')
fg = style.lookup('TLabel', 'foreground')
window.configure(bg=style.lookup('TLabel', 'background'))

class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.lblGreeting = ttk.Label(master, text="Welcome to the BattleTracker")
        self.lblGreeting.grid(row=0, column=0)
        self.btnOpen = ttk.Button(master, command=self.inputWindow, text="Input Stats")
        self.btnOpen.grid(row=1, column=0)
        self.btnMap = ttk.Button(master, command=self.showMap, text="Show Map")
        self.btnMap.grid(row=2, column=0)
    
    def inputWindow(self):
        self.inWin = StatCollector(self.master)
        self.btnOpen["state"] = "disabled"
        self.btnOpen["state"] = "normal"

    def showMap(self):
        self.mapWin = BattleMap([32, 46], self.master)

battleWin = mainWindow(window)

window.mainloop()