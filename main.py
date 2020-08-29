import tkinter as tk
from tkinter import *
from classes.board import Board

root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=450)

def startGame():
    startButton.forget()
    howToButton.forget()
    multiplayerButton.forget()
    label1 = tk.Label(root, text=str(Board().check_card(1)), fg='green', font=('helvetica', 12, 'bold'))
    canvas.create_window(1920, 1080, window=label1)


    for i in range(12):
        row = i % 4
        column = i // 4
        print(row, column)
        card = board.check_card(i + 1)
        img = PhotoImage(file=card.image_file)
        card.image = img
        button1 = tk.Button(command=clicked, image=img)
        canvas.create_window(row * 200 + 100, column * 150, window=button1, anchor=NW)

def clicked():
    print("hi")

def howToPlay():

    startButton.forget()
    howToButton.forget()
    multiplayerButton.forget()
    backButton.pack()

def multiplayer():
    startButton.forget()
    howToButton.forget()
    multiplayerButton.forget()
    backButton.pack()

def homePage():
    backButton.forget()
    startButton.pack()
    multiplayerButton.pack()
    howToButton.pack()


board = Board()
startButton = tk.Button(command=startGame, text='Start Game')
multiplayerButton = tk.Button(command=multiplayer, text='Multiplayer')
howToButton = tk.Button(command=howToPlay, text='How To Play')
backButton = tk.Button(command=homePage, text='<--Back')
startButton.pack()
multiplayerButton.pack()
howToButton.pack()

canvas.pack(side = LEFT)


root.mainloop()