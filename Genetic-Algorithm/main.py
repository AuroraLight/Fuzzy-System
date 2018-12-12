import tkinter as tk
import GUI as mygui

if __name__ == '__main__':
    root = tk.Tk()
    application = mygui.GUI(root)
    application.master.mainloop()
    #root.mainloop()