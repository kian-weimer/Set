import tkinter as tk
from tkinter import *
from classes.board import Board
from functools import partial


root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=500)
canvas.configure(bg= '#ff4733')
card_buttons = []
board = Board()

def select_card(position):
    row = position % 4
    column = position // 4

    if card_buttons[position].cget('bg') == "#fcff66":
        card_buttons[position].configure(bg='white')
        board.remove_card((row,column))

    else:
        if(board.select_card((row,column))):
            card_buttons[position].configure(bg="#fcff66")

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
        card_button = tk.Button(image=img, bg="white")
        card_button.configure(command=partial(select_card, i))
        card_buttons.append(card_button)

        canvas.create_window(row * 200 + 100, column * 150, window=card_button, anchor=NW)

def howToPlay():
    canvas.itemconfigure(start_button_window, state='hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state='normal')

def multiplayer():
    canvas.itemconfigure(start_button_window, state = 'hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state = 'normal')

def homePage():
    canvas.itemconfigure(back_button_window, state = 'hidden')
    canvas.itemconfigure(start_button_window, state='normal')
    canvas.itemconfigure(multiplayer_button_window, state='normal')
    canvas.itemconfigure(how_to_button_window, state='normal')


board = Board()
startButton = tk.Button(command=startGame, text='Start Game', width = 20, height = 2, bg = '#ffef5e')
multiplayerButton = tk.Button(command=multiplayer, text='Multiplayer', width = 20, height = 2, bg = '#ffef5e')
howToButton = tk.Button(command=howToPlay, text='How To Play', width = 20, height = 2, bg = '#ffef5e')
backButton = tk.Button(command=homePage, text='<--Back')

start_button_window = canvas.create_window(505,150, window = startButton)
multiplayer_button_window = canvas.create_window(505,250, window = multiplayerButton)
how_to_button_window = canvas.create_window(505,350, window = howToButton)
back_button_window = canvas.create_window(505,250, window = backButton, state = 'hidden')
canvas.pack(side = LEFT)


root.mainloop()

