import tkinter as tk

master = tk.Tk()


def return_strings():
    return e1, e2


canvas1 = tk.Canvas(master, width=300, height=120)
canvas1.pack()

label1 = tk.Label(master, text="Location:", font='Calibri 12 bold')
canvas1.create_window(70, 20, window=label1)
label2 = tk.Label(master, text="Date:", font='Calibri 12 bold')
canvas1.create_window(70, 50, window=label2)

e1 = tk.Entry(master)
canvas1.create_window(180, 20, window=e1)
e2 = tk.Entry(master)
canvas1.create_window(180, 50, window=e2)


file = tk.Button(master,
          text='SELECT SCHEDULE',
          command=lambda:[return_strings,master.quit()],
                 font='Calibri 12 bold')

canvas1.create_window(150, 100, window=file)
tk.mainloop()

