import tkinter as tk
from tkinter import *
from classes.board import Board
import tkinter as tk
from tkinter import *
from classes.board import Board
from random import choice
from functools import partial


root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=450)
root.configure(bg="blue")
canvas = tk.Canvas(root, width=1000, height=500, )
canvas.configure(bg="white")
card_buttons = []
board = Board()

def select_card(i):
    card_buttons[i].configure(bg="#fcff66")

def startGame():
    startButton.forget()
    howToButton.forget()
    multiplayerButton.forget()


    for i in range(12):
        row = i % 4
        column = i // 4
        card = board.check_card((row, column))
        img = PhotoImage(file=card.image_file)
        card.image = img
        card_button = tk.Button(image=img)
        card_button.configure(command=partial(select_card, i))
        card_buttons.append(card_button)

        canvas.create_window(row * 200 + 100, column * 150, window=card_button, anchor=NW)

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

