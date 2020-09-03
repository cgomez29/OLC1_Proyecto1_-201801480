from tkinter import *
from tkinter import Tk, Entry, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar, RIGHT, Y, HORIZONTAL, VERTICAL, simpledialog
import os
from controller.AnalyzerJS import AnalyzerJS
from controller.AnalyzerCSS import AnalyzerCSS
from controller.AnalyzerHTML import AnalyzerHTML
from ui.TextWidget import ScrollText
from controller.GraphGenerator import GraphGenerator

class MainWindow():
    def __init__(self):

        title = 'Analizador Léxico'
        self.analyzerJS = AnalyzerJS()
        self.analyzerCSS = AnalyzerCSS()
        self.analyzerHTML = AnalyzerHTML()
        self.graphGenerator = GraphGenerator()
        self.fileName = ""
        self.fileType = ""
        self.root = Tk()
        self.root.configure(bg = "#000000")
        self.root.geometry('1400x600')
        #self.root.iconbitmap('icon.ico')
        self.root.title(title)

    
        #self.textEditor = Entry(self.root, width=10)
        self.textConsola = Entry(self.root, width=10)
        self.btnRun = Button(self.root, text="Validar", bg="#008080", command=self.btn_click_run)


        ##Menu bar
        menuBar = Menu(self.root)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New", command = self.new_file)
        fileMenu.add_command(label="Open File", command = self.open_file)
        fileMenu.add_command(label="Save", command = self.save_file)
        fileMenu.add_command(label="Save AS", command = self.saveAs_file)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command = self.salir)
        menuBar.add_cascade(label="File", menu = fileMenu)

        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="User manual", command = self.open_user_manual)
        helpMenu.add_command(label="Technical manual", command =  self.open_technical_manual)
        helpMenu.add_command(label="About", command = self.about)
        helpMenu.add_separator()
        menuBar.add_cascade(label="help", menu=helpMenu)
        self.root.config(menu=menuBar)

        self.txt = ScrollText(self.root)
        self.txt.insert(END, '\n')
        self.txt.place(x=30, y=40)

        #self.textEditor = scrolledtext.ScrolledText(self.root, width=80, height=32, bg="#cccccc", fg="#1a1a1a")
        #self.textEditor.place(x=30, y=40)

        self.textConsola = scrolledtext.ScrolledText(self.root, width=60, height=25, bg="#cccccc", fg="#1a1a1a")
        self.textConsola.place(x=750, y=40)
        self.btnRun.place(x=34, y=10)
        #print(self.textEditor.index(INSERT))

    def run(self):
        self.root.mainloop()
    
    def salir(self):
        value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
        if value :
            root.destroy()

    def about(self):
        value = messagebox.showinfo("About", "Organización de Lenguajes y Compiladores 1 "+ 
        " \n Creador: Cristian Alexander Gomez Guzman \n 201801480")

    def new_file(self):
        self.txt.delete(1.0, END)
        self.textConsola.delete(1.0, END)

    def open_file(self):
        self.fileName = filedialog.askopenfilename(title= "Seleccionar archivo",initialdir = "./", filetypes= (("js files","*.js"),
         ("html files","*.html"),("css files","*.css"),("All Files","*.*")))
        if self.fileName != "":
            file = open(self.fileName, "r", encoding="utf-8")
            content = file.read()
            file.close()
            #tipo de archivo leido
            self.fileType = self.fileName.split('.')[-1]
            self.txt.delete("1.0", END)
            self.txt.insert("1.0", content)
    
    def open_technical_manual(self):
        os.system("C:\6 semestre\COMPI1\Proyecto1\resource\ManualUser.pdf")
    def open_user_manual(self):
        os.system("C:\6 semestre\COMPI1\Proyecto1\resource\ManualUser.pdf")

    def saveAs_file(self):
        pass

    def save_file(self):
        guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/", filetypes= (("All Files","*.*"),("js files","*.js"),
         ("html files","*.html"),("css files","*.css"), ("rmt files", "*.rmt")))
        fguardar = open(guardar, "w+")
        fguardar.write(self.txt.get(1.0, END))
        fguardar.close()
        self.fileName = guardar

    def btn_click_run(self):
        content = ""
        content = self.txt.get("1.0", END)
        contentConsole = []
        contentText = []
        #self.fileType identifica el tipo de archivo leido
        if (self.fileType == "js"):
            #contentConsole = self.analyzerJS.analyzer_java(content)
            
            #contentText = self.analyzerJS.analyzer_java(content)
            contentText = self.analyzerJS.analizar(content)
            contentConsole = self.analyzerJS.getArrayErrors()

            #SINGNOS DE LA CLASE JAVA
            signos = {"PUNTOCOMA":';', "LLAVEAPERTURA":'{', "LLAVECIERRE":'}', "IGUAL":'=', "PARENTECISA": '(',
                        "PARENTESISC": ')', "COMILLAS": "\'", "COMILLAD": "\"", "ASTERISCO": "*", "SLASH": "/", "SUMA": '+',
                        "NEGATIVO": '-', "DIVICION2": '%', "MAYORQ": '>', "MENORQ": '<', "PUNTO": '.', "COMA": ',',
                        "CONJUNCION":'&', "DISYUNCION": '|', "NEGACION": '!', "CORCHETEA": '[', "CORCHETEC": ']', "GUIONBAJO": '_',
                        "DOSPUNTOS": ':'}
            
            for reserved in contentText:
                fila = reserved[0] 
                columna = reserved[1] - 1
                identificador = reserved[2]
                palabra = len(reserved[3])
                idWord = reserved[3]
                if (reserved[2] == 'reservada'):
                    #print(identificador, fila, columna,  str(int(columna) + palabra))
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'red')
                elif (reserved[2] == "int" or reserved[2] == "Boolean"):
                    self.txt.tag_add(idWord, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(idWord, 'blue')
                elif (reserved[2] == "String" or reserved[2] == "Char"):
                    self.txt.tag_add(idWord, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(idWord, 'yellow')
                elif (reserved[2] == 'Id'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'green')   
                elif (reserved[2] in signos):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'orange')
                elif (reserved[2] == 'ComentaryL'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'gray')
                elif (reserved[2] == 'COMILLA' or reserved[2] == 'COMILLAS' or reserved[2] == 'COMILLAD'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'yellow')   

            #Coloreando palabras no reconocidas
            for error in contentConsole:
                fila = error[0]
                columna = error[1] - 1
                palabra = len(error[2])
                self.txt.tag_add("No reconocido", str(fila), str(columna), str(int(columna) + palabra))
                self.txt.tag_config("No reconocido", 'black')

            #Insertando errores encontrados en consola
            self.textConsola.delete("1.0", END)
            self.textConsola.insert("1.0", contentConsole)  
            self.graphGenerator.graphJS(contentText)
            
            #print("------------ERRORES  JS------------------------")
            #for x in self.analyzerJS.getArrayErrors():
                #print(x)

        elif (self.fileType == "html"):
            contentText =  self.analyzerHTML.analizar(content)
            contentConsole = self.analyzerHTML.getArrayError()
            signos = {"MENORQUE": '<', "MAYORQ": '>', "SLASH": "/", "IGUAL": '=', "EXCLAMACION": '!',
                        "COMILLASD": '\"'}

            for key in contentText:
                fila = key[0] 
                columna = key[1] - 1
                identificador = key[2]
                palabra = len(key[3])
                idWord = key[3]
                
                if (key[2] == 'reservada'):
                    #print(identificador, fila, columna,  str(int(columna) + palabra))
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'red')
                elif (key[2] == 'Id'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'green')   
                elif (key[2] == 'ComentaryL'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'gray')
                elif (key[2] in signos):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'orange')
                elif (key[2] == "int" or key[2] == "Boolean"):
                    self.txt.tag_add(idWord, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(idWord, 'blue')
                elif (key[2] == 'COMILLA' or key[2] == 'COMILLAS' or key[2] == 'COMILLAD'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'yellow')   
            self.textConsola.delete("1.0", END)
            self.textConsola.insert("1.0", contentConsole)  

        elif (self.fileType == "css"):
            contentText =  self.analyzerCSS.analizar(content)
            contentConsole = self.analyzerCSS.getArrayError()
            signos = {"PUNTOYCOMA": ';', "LLAVEA": '{', "LLAVEC": '}', "DOSPUNTOS": ':', "SLASH" : '/', "ASTERISCO": '*',
                        "COMA": ',', "PORCENTAJE": '%', "NUMERAL": '#', "PARENTESISA": '(', "PARENTESISC": ')', "COMILLAS": "'",
                        "COMILLAD": "\"", "SLASHI": '\\'}

            for key in contentText:
                fila = key[0] 
                columna = key[1] - 1
                identificador = key[2]
                palabra = len(key[3])
                idWord = key[3]
                
                if (key[2] == 'reservada'):
                    #print(identificador, fila, columna,  str(int(columna) + palabra))
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'red')
                elif (key[2] == 'Id'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'green')   
                elif (key[2] == 'ComentaryL'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'gray')
                elif (key[2] in signos):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'orange')
                elif (key[2] == "int" or key[2] == "Boolean"):
                    self.txt.tag_add(idWord, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(idWord, 'blue')
                elif (key[2] == 'COMILLA' or key[2] == 'COMILLAS' or key[2] == 'COMILLAD'):
                    self.txt.tag_add(identificador, str(fila), str(columna), str(int(columna) + palabra))
                    self.txt.tag_config(identificador, 'yellow')   
            self.textConsola.delete("1.0", END)
            self.textConsola.insert("1.0", contentConsole)  
        elif (self.fileType == "rmt"):
            pass
        else:
            print("No se reconoce este tipo de archivo!")
       