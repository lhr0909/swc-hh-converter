from Tkinter import *
import tkFileDialog
import tkMessageBox

from threading import Thread
from Queue import Queue
from SealsConverter import monitor_hand
import time, os

class View(object):

    def __init__(self, master):
        # GUI creation
        self._master = master
        master.title('Seals with Clubs Hand History Converter built for lhr0909')
        master.minsize(width=450, height=80)
        master.resizable(0, 0)

        self.inputFolderLabel = Label(master, text='Input Folder')
        self.inputFolderLabel.grid(row=0)
        self.processedFolderLabel = Label(master, text='Processed Folder')
        self.processedFolderLabel.grid(row=1)

        self.inputFolderEntry = Entry(master)
        self.inputFolderEntry.grid(row=0, column=1, padx=20, ipadx=50)
        self.processedFolderEntry = Entry(master)
        self.processedFolderEntry.grid(row=1, column=1, padx=20, ipadx=50)
        
        self.startButton = Button(master, text='Start', command=self.start_pressed)
        self.startButton.grid(row=1, column=3, padx=20, ipadx=30, ipady=5)

        self.inputFolderBrowseButton = Button(master, text='Browse', command=self.browse_input_folder)
        self.inputFolderBrowseButton.grid(row=0, column=2, pady=5)
        self.processedFolderBrowseButton = Button(master, text='Browse', command=self.browse_processed_folder)
        self.processedFolderBrowseButton.grid(row=1, column=2, pady=5, )

        # Initialization of various variables
        self.inputFolderPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/handhistories"
        self.processedFolderPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/converted_handhistories"
        self.inputFolderEntry.delete(0, END)
        self.inputFolderEntry.insert(0, self.inputFolderPath)
        self.processedFolderEntry.delete(0, END)
        self.processedFolderEntry.insert(0, self.processedFolderPath)

        self.started = Queue(1)
        self.monitor_thread = None

    def start_pressed(self):
        if self.started.empty():
            self.startButton["text"] = "Stop"
            self.started.put(True)
            self.monitor_thread = Thread(
                target=monitor_hand, 
                args=(
                    self.started, 
                    self.inputFolderPath, 
                    self.processedFolderPath, 
                    time.time(), 
                    5)
                )
            self.monitor_thread.start()
        else:
            self.startButton["text"] = "Start"
            self.started.get()
            self.monitor_thread.join()

    def browse_input_folder(self):
        self.inputFolderPath = tkFileDialog.askdirectory()
        self.inputFolderEntry.delete(0, END)
        self.inputFolderEntry.insert(0, self.inputFolderPath)

    def browse_processed_folder(self):
        self.processedFolderPath = tkFileDialog.askdirectory()
        self.processedFolderEntry.delete(0, END)
        self.processedFolderEntry.insert(0, self.processedFolderPath)

def main():
    root = Tk()
    View(root)
    root.mainloop()

if __name__ == "__main__":
    main()