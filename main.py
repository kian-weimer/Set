import tkinter as tk
from tkinter import *
from classes.board import Board

print(Board().check_card(1))
root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=450)



def hello():
    label1 = tk.Label(root, text=str(Board().check_card(1)), fg='green', font=('helvetica', 12, 'bold'))
    canvas.create_window(1920, 1080, window=label1)



board = Board()

for i in range(12):
    row = i%4
    column = i//4
    print(row, column)
    card = board.check_card(i+1)
    img = PhotoImage(file=card.image_file)
    card.image = img
    button1 = tk.Button(command=hello, image=img)
    canvas.create_window(row*200 + 100,column*150, window=button1, anchor=NW)
canvas.pack(side = LEFT)


root.mainloop()