from tkinter import *
from tkinter import Tk, Entry, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar, RIGHT, Y, HORIZONTAL, VERTICAL, simpledialog
import os


class MainWindow():
    def __init__(self):
        title = 'Analizador Léxico'
        self.root = Tk()
        self.root.configure(bg = "#000000")
        self.root.geometry('1400x600')
        #self.root.iconbitmap('icon.ico')
        self.root.title(title)

    
        self.textEditor = Entry(self.root, width=10)
        self.textConsola = Entry(self.root, width=10)

        ##Menu bar
        menuBar = Menu(self.root)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open File", command = self.open_file)
        fileMenu.add_command(label="Save", command= self.save_file)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command= self.root.quit)
        menuBar.add_cascade(label="File", menu = fileMenu)

        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="User manual")
        helpMenu.add_command(label="About", command = self.about)
        helpMenu.add_separator()
        menuBar.add_cascade(label="help", menu=helpMenu)
        self.root.config(menu=menuBar)

        self.textEditor = scrolledtext.ScrolledText(self.root, width=80, height=32, bg="#cccccc", fg="#1a1a1a")
        self.textEditor.place(x=30, y=20)
        self.textConsola = scrolledtext.ScrolledText(self.root, width=60, height=25, bg="#cccccc", fg="#1a1a1a")
        self.textConsola.place(x=750, y=20)

    def run(self):
        self.root.mainloop()

    def about(self):
        value = messagebox.showinfo("About", "Organización de Lenguajes y Compiladores 1 "+ 
        " \n Creador: Cristian Alexander Gomez Guzman \n 201801480")

    def open_manual(self):
        pass

    def open_file(self):
        nameFile = filedialog.askopenfilename(title= "Seleccionar archivo",initialdir = "C:/", filetypes= (("js files","*.js"),
         ("html files","*.html"),("css files","*.css"),("All Files","*.*")))
        if nameFile != "":
            file = open(nameFile, "r", encoding="utf-8")
            content = file.read()
            file.close()
            self.textEditor.delete("1.0", END)
            self.textEditor.insert("1.0", content)
    def save_file():
        pass