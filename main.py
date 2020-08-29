import tkinter as tk
from tkinter import *
from classes.board import Board

print(Board().check_card(1))
root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300)
canvas1.pack()


def hello():
    label1 = tk.Label(root, text=str(Board().check_card(1)), fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 200, window=label1)


button1 = tk.Button(text='Noice!', command=hello, bg='brown', fg='white')
canvas1.create_window(150, 150, window=button1)
canvas = Canvas(root, width = 300, height = 300)
canvas.pack()
img = PhotoImage(file=Board().check_card(1).image_file)
canvas.create_image(20,20, anchor=NW, image=img)

root.mainloop()