import tkinter as tk

master = tk.Tk()


def return_strings():
    return e1, e2


canvas1 = tk.Canvas(master, width=400, height=120)
canvas1.pack()

label1 = tk.Label(master, text="Location: (ex: Cluj Iulius Mall)", font='Calibri 12 bold')
canvas1.create_window(120, 20, window=label1)
label2 = tk.Label(master, text="Date: (ex: 22/12/2020)", font='Calibri 12 bold')
canvas1.create_window(120, 50, window=label2)

e1 = tk.Entry(master)
canvas1.create_window(300, 20, window=e1)
e2 = tk.Entry(master)
canvas1.create_window(300, 50, window=e2)

file = tk.Button(master,
                 text='SELECT SCHEDULE',
                 command=lambda: [return_strings, master.quit()],
                 font='Calibri 12 bold')

canvas1.create_window(200, 100, window=file)
tk.mainloop()
