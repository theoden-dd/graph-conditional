"""Internal module with tcl/tk tools."""
import tkinter as tk


def run_tkinter():
    window = tk.Tk()
    window.title('Условный граф')
    window.geometry('640x480')

    var1 = tk.IntVar()
    c1 = tk.Checkbutton(window, text='Python', variable=var1, onvalue=1, offvalue=0)
    c1.pack()

    window.mainloop()

