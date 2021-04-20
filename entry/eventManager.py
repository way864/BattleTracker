import math
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from bigHelper2D import correctPlacement

class EventManager():
    def __init__(self, root):
        self.root = root
        self.font = ('Papyrus', '14')
        
    def rightClickMenu(self, event):
        self.event = event
        self.tokenMenu = tk.Menu(self.root, tearoff=0)
        #self.trigMenu = tk.Menu(self.tokenMenu, tearoff=0)
        #self.aoeMenu = tk.Menu(self.tokenMenu, tearoff=0)
        #self.tokenMenu.add_command(label="Target Creature")
        #self.tokenMenu.add_command(label="Damage")
        #self.tokenMenu.add_command(label="Heal")
        self.tokenMenu.add_command(label="Conditions Info")
        self.tokenMenu.add_separator()
        #self.tokenMenu.add_cascade(label="Trig Functions", menu=self.trigMenu)
        #self.trigMenu.add_command(label="Distance", command=findDistance)
        #self.trigMenu.add_command(label="Find All in Range")
        #self.trigMenu.add_command(label="Spread Width")
        self.tokenMenu.add_cascade(label="AOE", menu=self.aoeMenu)
        self.aoeMenu.add_command(label="Circle")
        self.aoeMenu.add_command(label="Square")
        self.aoeMenu.add_command(label="Cone")
        self.aoeMenu.add_command(label="Line")
        self.aoeMenu.add_command(label="Ring Wall")
        self.aoeMenu.add_command(label="Line Wall")
        try:
            self.tokenMenu.tk_popup(self.event.x_root, self.event.y_root)
        finally:
            self.tokenMenu.grab_release()

    def moveToken(self, arg):
        self.tokenList = arg[0]
        self.mapSize = arg[1]
        self.moveWin = tk.Toplevel(master=self.root)
        self.moveWin.title("Move Token")
        style = ThemedStyle(self.moveWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.moveWin.configure(bg=style.lookup('TLabel', 'background'))
        self.moveWin.rowconfigure(0, minsize=100)
        self.moveWin.columnconfigure([0,1], minsize=100)
        self.selectionFrame = ttk.Frame(master=self.moveWin)
        self.selectionFrame.grid(row=0, column=0, rowspan=2, sticky='nw')
        self.moveToFrame = ttk.Frame(master=self.moveWin)
        self.moveToFrame.grid(row=0, column=1, sticky='nw')
        self.moveFinishFrame = ttk.Frame(master=self.moveWin)
        self.moveFinishFrame.grid(row=1, column=1)
        lblSelected = ttk.Label(master=self.selectionFrame, text="Selected Token", font=self.font)
        lblSelected.grid(row=0, column=0, sticky='w')
        names = []
        coordinates = []
        for being in self.tokenList:
            names.append(being["name"])
            coordinates.append(being["coordinate"])
        self.dropSelection = ttk.Combobox(self.selectionFrame, width=27, values=names)
        self.dropSelection.grid(row=0, column=1, sticky='w')
        self.dropSelection.current()
        self.btnCurrCoord = ttk.Button(master=self.selectionFrame, text="Show Current Coordinate", command=lambda arg=[names, coordinates]: self.showCoord(arg))
        self.btnCurrCoord.grid(row=1, column=0, sticky='w')
        self.lblActCoord = ttk.Label(master=self.selectionFrame, text=" ", font=self.font)
        self.lblActCoord.grid(row=1, column=1, sticky='w')
        lblSetNewCoord = ttk.Label(master=self.moveToFrame, text="Set New Coordinate", font=self.font)
        lblSetNewCoord.grid(row=0, column=0, sticky='w')
        self.entRowCoord = ttk.Entry(master=self.moveToFrame, width=5)
        self.entColCoord = ttk.Entry(master=self.moveToFrame, width=5)
        self.entZCoord = ttk.Entry(master=self.moveToFrame, width=5)
        self.entRowCoord.grid(row=0, column=1, sticky='w')
        self.entColCoord.grid(row=0, column=2, sticky='w')
        self.entZCoord.grid(row=0, column=3, sticky='w')

        self.lblOrThis = ttk.Label(master=self.moveToFrame, text="or move a number of spaces", font=self.font)
        #self.lblOrThis.grid(row=1, column=0, columnspan=4)

        self.lblFwdBack = ttk.Label(master=self.moveToFrame, text="Forward/Back", font=self.font)
        #self.lblFwdBack.grid(row=2, column=0, sticky='w')
        self.entRowDelta = ttk.Entry(master=self.moveToFrame, width=5)
        #self.entRowDelta.grid(row=2, column=1, sticky='w')
        self.fwdOrBack = tk.StringVar()
        self.rbnMoveFwd = ttk.Radiobutton(master=self.moveToFrame, text="Forward", variable=self.fwdOrBack, value='forward')
        #self.rbnMoveFwd.grid(row=2, column=2)
        self.rbnMoveBack = ttk.Radiobutton(master=self.moveToFrame, text="Back", variable=self.fwdOrBack, value='back')
        #self.rbnMoveBack.grid(row=2, column=3)
        self.lblLeftRight = ttk.Label(master=self.moveToFrame, text="Left/Right", font=self.font)
        #self.lblLeftRight.grid(row=3, column=0, sticky='w')
        self.entColDelta = ttk.Entry(master=self.moveToFrame, width=5)
        #self.entColDelta.grid(row=3, column=1, sticky='w')
        self.leftOrRight = tk.StringVar()
        self.rbnMoveLeft = ttk.Radiobutton(master=self.moveToFrame, text="Left", variable=self.leftOrRight, value='left')
        #self.rbnMoveLeft.grid(row=3, column=2)
        self.rbnMoveRight = ttk.Radiobutton(master=self.moveToFrame, text="Right", variable=self.leftOrRight, value='right')
        #self.rbnMoveRight.grid(row=3, column=3)
        self.lblUpDown = ttk.Label(master=self.moveToFrame, text="Up/Down", font=self.font)
        #self.lblUpDown.grid(row=4, column=0, sticky='w')
        self.entZDelta = ttk.Entry(master=self.moveToFrame, width=5)
        #self.entZDelta.grid(row=4, column=1, sticky='w')
        self.upOrDown = tk.StringVar()
        self.rbnMoveUp = ttk.Radiobutton(master=self.moveToFrame, text="Up", variable=self.upOrDown, value='up')
        #self.rbnMoveUp.grid(row=4, column=2)
        self.rbnMoveDown = ttk.Radiobutton(master=self.moveToFrame, text="Down", variable=self.upOrDown, value='down')
        #self.rbnMoveDown.grid(row=4, column=3)

        self.btnSet = ttk.Button(master=self.moveFinishFrame, text="Set Position", command=lambda arg=[False]: self.setNewCoord(arg))
        self.btnSet.grid(row=0, column=0, sticky='w')
        self.btnRemove = ttk.Button(master=self.moveFinishFrame, text="Remove Token", command=lambda arg=[True]: self.setNewCoord(arg))
        self.btnRemove.grid(row=0, column=1, sticky='w')
        self.lblSetFinished = ttk.Label(master=self.moveFinishFrame, text=" ", font=self.font)
        self.lblSetFinished.grid(row=0, column=2, sticky='w')

    def showCoord(self, arg):
        selOption = self.dropSelection.get()
        names = arg[0]
        coordinates = arg[1]
        index = names.index(selOption)
        if coordinates[index][0] != "" and coordinates[index][1] != "" and coordinates[index][2] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1

            self.lblOrThis.grid(row=1, column=0, columnspan=4)
            self.lblFwdBack.grid(row=2, column=0, sticky='w')
            self.entRowDelta.grid(row=2, column=1, sticky='w')
            self.rbnMoveFwd.grid(row=2, column=2, sticky='w')
            self.rbnMoveBack.grid(row=2, column=3, sticky='w')
            self.lblLeftRight.grid(row=3, column=0, sticky='w')
            self.entColDelta.grid(row=3, column=1, sticky='w')
            self.rbnMoveLeft.grid(row=3, column=2, sticky='w')
            self.rbnMoveRight.grid(row=3, column=3, sticky='w')
            self.lblUpDown.grid(row=4, column=0, sticky='w')
            self.entZDelta.grid(row=4, column=1, sticky='w')
            self.rbnMoveUp.grid(row=4, column=2, sticky='w')
            self.rbnMoveDown.grid(row=4, column=3, sticky='w')

        else:
            row = coordinates[index][0]
            col = coordinates[index][1]
            if len(self.moveToFrame.grid_slaves()) > 4:
                self.lblOrThis.grid_forget()
                self.lblFwdBack.grid_forget()
                self.entRowDelta.grid_forget()
                self.rbnMoveFwd.grid_forget()
                self.rbnMoveBack.grid_forget()
                self.lblLeftRight.grid_forget()
                self.entColDelta.grid_forget()
                self.rbnMoveLeft.grid_forget()
                self.rbnMoveRight.grid_forget()
                self.lblUpDown.grid_forget()
                self.entZDelta.grid_forget()
                self.rbnMoveUp.grid_forget()
                self.rbnMoveDown.grid_forget()

        z = coordinates[index][2]
        self.lblActCoord.config(text="{0}: {1}: {2}".format(row, col, z))

    def setNewCoord(self, arg):
        removingToken = arg[0]
        selOption = self.dropSelection.get()
        if selOption == "":
            messagebox.showinfo("Info", "Must select a creature.")
            return

        nameList = []
        for being in self.tokenList:
            nameList.append(being['name'])
        index = nameList.index(selOption)
        size = self.tokenList[index]['size']
        oneSpace = False
        if size == 'tiny' or size == 'small' or size == 'medium':
            oneSpace = True
        anyMoveAllowed = False
        goForwardBack = self.fwdOrBack.get()
        goLeftRight = self.leftOrRight.get()
        goUpDown = self.upOrDown.get()
        deltaFBStr = self.entRowDelta.get()
        deltaLRStr = self.entColDelta.get()
        deltaUDStr = self.entZDelta.get()

        if goForwardBack != "" or goLeftRight != "" or goUpDown != "":
            coordinate = self.tokenList[index]['coordinate']
            if coordinate[0] != "" and coordinate[1] != "" and coordinate[2] != "":
                anyMoveAllowed = True

        if removingToken == False and anyMoveAllowed == False and (self.entRowCoord.get() == "" or self.entColCoord.get() == "" or self.entZCoord.get() == ""):
            messagebox.showwarning("Warning", "Coordinate Fields Can't Be Empty!")
            return

        if removingToken == False:
            if anyMoveAllowed:
                for i in range(3):
                    coordinate[i] = int(coordinate[i])
                '''
                try:
                    deltaFB = int(deltaFBStr)
                    deltaLR = int(deltaLRStr)
                    deltaUD = int(deltaUDStr)
                except ValueError:
                    messagebox.showwarning("Warning", "Move fields must be integers!")
                    return
                '''
                try:
                    deltaFB = int(deltaFBStr)
                except ValueError:
                    deltaFB = 0
                try:
                    deltaLR = int(deltaLRStr)
                except ValueError:
                    deltaLR = 0
                try:
                    deltaUD = int(deltaUDStr)
                except ValueError:
                    deltaUD = 0

                if deltaFB < 0 or deltaLR < 0 or deltaUD < 0:
                    messagebox.showwarning("Warning", "Move fields cannot be negative!")
                    return
                if goForwardBack == 'forward':
                    coordinate[0] -= deltaFB
                    if oneSpace:
                        if coordinate[0] < 0:
                            coordinate[0] = 0
                    else:
                        coordinate = correctPlacement(coordinate, size, self.mapSize)
                if goForwardBack == 'back':
                    coordinate[0] += deltaFB
                    if oneSpace:
                        if coordinate[0] < self.mapSize[0] - 1:
                            coordinate[0] = self.mapSize[0] - 1
                    else:
                        coordinate = correctPlacement(coordinate, size, self.mapSize)
                if goLeftRight == 'left':
                    coordinate[1] -= deltaLR
                    if oneSpace:
                        if coordinate[1] < 0:
                            coordinate[1] = 0
                    else:
                        coordinate = correctPlacement(coordinate, size, self.mapSize)
                if goLeftRight == 'right':
                    coordinate[1] += deltaLR
                    if oneSpace:
                        if coordinate[1] < self.mapSize[1] - 1:
                            coordinate[1] = self.mapSize[1] - 1
                    else:
                        coordinate = correctPlacement(coordinate, size, self.mapSize)
                if goUpDown == 'down':
                    coordinate[2] -= deltaUD
                if goUpDown == 'up':
                    coordinate[2] += deltaUD

                newCoord = coordinate
                    
            else:
                try:
                    newRow = int(self.entRowCoord.get()) - 1
                    newCol = int(self.entColCoord.get()) - 1
                    newZ = int(self.entZCoord.get())
                    newCoord = [newRow, newCol, newZ]
                except ValueError:
                    messagebox.showwarning("Warning", "Set Coordinate fields must be integers!")
                    return
                if newCoord[0] > self.mapSize[0] - 1 or newCoord[0] < 0:
                    messagebox.showerror("Error", "Row Coordinate Out of Range of Map!")
                    return
                if newCoord[1] > self.mapSize[1] - 1 or newCoord[1] < 0:
                    messagebox.showerror("Error", "Column Coordinate Out of Range of Map!")
                    return
        else:
            newCoord = ["", "", ""]
        for being in self.tokenList:
            '''
            if being["coordinate"][0] == str(newCoord[0]) and being["coordinate"][1] == str(newCoord[1]):
                    messagebox.showerror("Error", "Space already taken!")
                    return
            '''
            if being["name"] == selOption:
                being["coordinate"] = [str(newCoord[0]), str(newCoord[1]), str(newCoord[2])]
        self.lblSetFinished.config(text="Position set! Please close window.")