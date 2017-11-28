import sys
from scanner import Scanner
from tkinter import *
from tkinter import filedialog

class pyScanUI(Frame): 
    """
    A class to run the  GUI
    """
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.__initUI()
        
    def __initUI(self):
        self.parent.title("Python ExamScan")
        button_browse = Button(self.parent, text="Choose pdf of scans or jpg of key", command = self.button_browse_callback)
        button_browse.pack()

        self.fileEntry = Entry(self.parent, width = 50)
        self.fileEntry.pack()
        
        self.numQlabel = Label(self.parent, text = 'enter number of questions to grade:')
        self.numQlabel.pack()
        
        self.numQEntry = Entry(self.parent, width = 10)
        self.numQEntry.pack()
        
        self.ignorelabel = Label(self.parent, text = 'enter question numbers to ignore separated by commas:')
        self.ignorelabel.pack()
        
        self.ignoreEntry = Entry(self.parent, width = 50)
        self.ignoreEntry.pack()
        
        self.setavar=IntVar()
        self.setacheck = Checkbutton(self.parent, text = 'Any select-all-that-apply-questions?', variable= self.setavar)
        self.setacheck.pack()
        
        self.openQvar = IntVar()
        self.openQcheck = Checkbutton(self.parent, text = 'Any open ended questions to grade on the fly?', variable = self.openQvar)
        self.openQcheck.pack()
              
        button_go = Button(self.parent, text = "Run Scan", command = self.button_go_callback)
        button_go.pack()
        
        separator = Frame(self.parent, height =2, bd = 1, relief = SUNKEN)
        separator.pack(fill=X, padx = 5, pady = 5)
        
        button_gradebrowse = Button(self.parent, text='choose results .csv file to re-grade', command=self.button_gradebrowse_callback)
        button_gradebrowse.pack()
        
        self.csvEntry = Entry(self.parent, width = 50)
        self.csvEntry.pack()
        
        button_grade = Button(self.parent, text='Grade file', command=self.button_grade_callback)
        button_grade.pack()
        
        separator = Frame(self.parent, height =2, bd = 1, relief = SUNKEN)
        separator.pack(fill=X, padx = 5, pady = 5)
        
        button_exit = Button(self.parent, text = 'Exit', command=sys.exit)
        button_exit.pack()
        
        
    def button_browse_callback(self):
        filename = filedialog.askopenfilename()
        self.fileEntry.delete(0,END)
        self.fileEntry.insert(0,filename)

    def button_gradebrowse_callback(self):
        filename = filedialog.askopenfilename()
        self.csvEntry.delete(0,END)
        self.csvEntry.insert(0,filename)

    def button_go_callback(self):
        input_file = self.fileEntry.get()
        quests = int(self.numQEntry.get())
        markmissing=bool(self.setavar.get())
        openQ=bool(self.openQvar.get())
        ignores = self.ignoreEntry.get()
        
        Scanner(input_file, quests, markmissing, openQ, ignores)

    def button_grade_callback(self):
        input_file = self.csvEntry.get()
        #pyScan.gradeData(self,input_file)
