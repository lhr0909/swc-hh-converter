from Tkinter import *
import tkFileDialog
import tkMessageBox



class View(object):

    def __init__(self, master):
        """Construct the interface"""
        self._master = master
        master.title('Seals with Clubs Hand History Converter')
        master.minsize(width=450, height=100)
        master.resizable(0, 0)

        self.label1 = Label(master, text='Input Folder')
        self.label1.grid(row=0)
        self.label2 = Label(master, text='Processed Folder')
        self.label2.grid(row=1)

        self.entry1 = Entry(master)
        self.entry1.grid(row=0, column=1, padx=20, ipadx=50)
        self.entry2 = Entry(master)
        self.entry2.grid(row=1, column=1, padx=20, ipadx=50)
        
        self.b = Button(master, text='Start/Stop', command=self.startpressed)
        self.b.grid(row=1, column=3, padx=20, ipadx=30, ipady=5)

        self.ib = Button(master, text='Browse', command=self.browse1)
        self.ib.grid(row=0, column=2, pady=5)
        self.pb = Button(master, text='Browse', command=self.browse2)
        self.pb.grid(row=1, column=2, pady=5, )

        self._filename = ''


    def startpressed(self):
        tkMessageBox.askyesno("Warning","Do you wish to Proceed? ")

    def browse1(self):
        self._filename = tkFileDialog.askdirectory()
        self.entry1.delete(0, END)
        self.entry1.insert(0, self._filename)

    def browse2(self):
        self._filename = tkFileDialog.askdirectory()
        self.entry2.delete(0, END)
        self.entry2.insert(0, self._filename)

root = Tk()
View(root)
root.mainloop()
